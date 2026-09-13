"""Replay ordinate-range recovery with exact integers and independent mpmath extrema."""
import argparse,json,time,warnings
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from flint import arb,ctx
from sympy import Poly,cyclotomic_poly,symbols
import dedekind_coupled_recovery as core
from dedekind_coupled_audit import integers,gap


def read(path):return json.loads(path.read_text())
def mp_endpoint(x):
    m,e=map(int,x.man_exp());return mp.mpf(m)*mp.power(2,e)
def inside(value,box):return mp_endpoint(box.lower())<=value<=mp_endpoint(box.upper())
def case_key(c):return c['additional_radius'],c['settings']['top'],c['method'],c['policy']


def run(directory,prior):
    start=time.monotonic();raw=(directory/'Measurements.json').read_bytes();data=json.loads(raw)
    names=['Ranges_Probe160.json','Ranges_160.json','Ranges_224.json']
    datasets={n:read(directory/n) for n in names}
    assert all(d['status']=='passed' and d['input_sha256']==core.sha(raw) for d in datasets.values())
    producer=Path(__file__).with_name('dedekind_ordinate_ranges.py')
    assert all(d['source_sha256']==core.sha(producer.read_bytes()) for d in datasets.values())
    assert all(d['core_sha256']==core.sha(Path(core.__file__).read_bytes()) for d in datasets.values())
    # Oracle data are computed only after the producer result files are frozen.
    powers=core.support(4096);x=symbols('x');phi=cyclotomic_poly(5,x);degrees={}
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for p in sorted({p for n,p,k in powers}):
            unit,factors=Poly(phi,x,modulus=p).factor_list();product=Poly(unit,x,modulus=p)
            for factor,e in factors:product*=factor**e
            assert product==Poly(phi,x,modulus=p)
            degrees[p]=[(int(e),int(f.degree())) for f,e in factors]
    truth=[sum(f for e,f in degrees[p] if k%f==0) for n,p,k in powers]
    prior_data=read(prior/'Exact_Audit.json')
    assert truth==prior_data['relaxation_ambiguity']['baseline_coefficients']
    cache={};replays=[];total=0;point_checks=0;missing_control=None;true_control=None
    for name,dataset in datasets.items():
        rows_by_key={}
        for bound in dataset['bounds']:
            settings=bound['settings'];top,bits=settings['top'],settings['precision_bits'];delta=bound['additional_radius']
            key=top,bits,delta
            if key not in cache:
                pp,rows,s=core.prepare(data,top,bits,delta);assert pp==powers
                cache[key]=rows,s
            base,s=cache[key];assert s==settings
            ctx.prec=bits
            for method,metadata in bound['measurements_by_method'].items():
                rows=[]
                for old,m in zip(base,metadata):
                    assert {k:v for k,v in m.items() if k not in ['R','range_method']}=={k:v for k,v in old['metadata'].items() if k!='R'}
                    assert m['range_method']==method
                    if method=='global':assert m['R']==old['metadata']['R']
                    rows.append({'weights':old['weights'],'R':core.decode(m['R']),'B':old['B'],'metadata':m})
                assert len(rows)==91
                rows_by_key[delta,top,method]=rows
            # Strict phase brackets certify every reported turning point by a
            # route independent of the producer's fixed-point iteration.
            ctx.prec=256
            for diagnostic in bound['diagnostics']:
                a=arb(1)/diagnostic['denominator'];u=arb(diagnostic['target']).log()
                assert 2*a/(u*u)<1 and diagnostic['critical_edge_boxes']==0
                for certificate in diagnostic['critical_points']:
                    t=core.decode(certificate['point']);k=certificate['k'];lo,hi=t.lower(),t.upper()
                    left=u*lo+(2*a*lo/u).atan()-k*arb.pi()
                    right=u*hi+(2*a*hi/u).atan()-k*arb.pi()
                    assert left<0 and right>0
                    ratio=2*a*t/u
                    value=((-1)**k)*(-a*t*t).exp()/(1+ratio*ratio).sqrt()
                    assert value.overlaps(core.decode(certificate['value']))
                    point_checks+=1
        for case in dataset['cases']:
            delta,top,method,policy=case_key(case);ctx.prec=case['settings']['precision_bits']
            tops=[t for t in [220,600,1000,1500,2000] if t<=top] if policy=='retained_prefix' else [top]
            rows=[r for t in tops for r in rows_by_key[delta,t,method]]
            assert len(rows)==case['measurement_count']
            assert core.sha(core.canonical([r['metadata'] for r in rows]))==case['measurements_sha256']
            ir=integers(rows);domains=[list(range(5)) for _ in powers];count=0
            for step in case['rounds']:
                assert core.sha(core.canonical(domains))==step['prior_domains_sha256']
                old=[list(d) for d in domains]
                for w in step['removals']:
                    i,c,j=w['column'],w['candidate'],w['measurement_index']
                    assert powers[i][0]==w['n'] and rows[j]['metadata']['n']==w['measurement_target'] and c in old[i]
                    exact=gap(ir[j],old,i,c,w['side']);assert exact>0 and c!=truth[i]
                    if missing_control is None and step['round']>1:
                        reset=gap(ir[j],[list(range(5)) for _ in powers],i,c,w['side'])
                        if reset<=0:missing_control={'file':name,'case':list(case_key(case)),'round':step['round'],
                            'witness':w,'valid_gap_scaled_integer':str(exact),'missing_prerequisite_gap_scaled_integer':str(reset)}
                    if true_control is None:
                        wrong=gap(ir[j],old,i,truth[i],w['side']);assert wrong<=0
                        true_control={'file':name,'case':list(case_key(case)),'witness':w,'true_coefficient':truth[i],
                                      'false_exclusion_gap_scaled_integer':str(wrong)}
                    domains[i].remove(c);count+=1
                assert core.sha(core.canonical(domains))==step['remaining_domains_sha256']
            assert domains==[d['candidates'] for d in case['domains']]
            assert all(t in d for t,d in zip(truth,domains))
            assert sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361)==case['unique_target_coefficients']
            total+=count;replays.append({'file':name,'case':list(case_key(case)),'exclusions':count,
                 'domains_sha256':core.sha(core.canonical(domains)),'all_604_arithmetic_coefficients_retained':True})
        print(json.dumps({'event':'exact_replay','file':name,'cases':len(dataset['cases']),'cumulative_exclusions':total}),flush=True)
    assert missing_control and true_control
    low={case_key(c):c for c in datasets['Ranges_160.json']['cases']}
    high={case_key(c):c for c in datasets['Ranges_224.json']['cases']}
    assert set(low)==set(high) and all(low[k]['domains']==high[k]['domains'] for k in low)
    assert all(c==low[case_key(c)] for c in datasets['Ranges_Probe160.json']['cases'])
    comparisons=0
    for dataset in [datasets['Ranges_160.json'],datasets['Ranges_224.json']]:
        cases={case_key(c):c for c in dataset['cases']}
        def contained(left,right):
            nonlocal comparisons
            assert all(set(a['candidates'])<=set(b['candidates']) for a,b in zip(left['domains'],right['domains']));comparisons+=1
        for delta in ['5e-6','5e-5','5e-4','5e-3']:
            for method in dataset['methods']:
                for top in [220,600,1000,1500,2000]:
                    contained(cases[delta,top,method,'retained_prefix'],cases[delta,top,method,'single_cutoff'])
                for a,b in zip([220,600,1000,1500],[600,1000,1500,2000]):
                    contained(cases[delta,b,method,'retained_prefix'],cases[delta,a,method,'retained_prefix'])
        for a,b in zip(['5e-6','5e-5','5e-4'],['5e-5','5e-4','5e-3']):
            for top in [220,600,1000,1500,2000]:
                for method in dataset['methods']:
                    for policy in ['single_cutoff','retained_prefix']:contained(cases[a,top,method,policy],cases[b,top,method,policy])
    # Independently find scalar extrema at 80 decimal digits. This is a
    # numerical cross-check, while strict Arb phase brackets supply certificates.
    mp.mp.dps=80;mp_cases=[];omitted_critical=None
    for bound in datasets['Ranges_224.json']['bounds']:
        delta=bound['additional_radius'];top=bound['settings']['top']
        if delta not in ['5e-4','5e-3'] or top not in [220,2000]:continue
        ctx.prec=224;radius=arb(delta)
        boxes=[arb(r['lo']).union(arb(r['hi']))+arb(0,radius.upper()) for r in data['roots'] if F(r['hi'])<top]
        for diagnostic in bound['diagnostics']:
            target=diagnostic['target']
            if target not in [2,11,361]:continue
            a=mp.mpf(1)/diagnostic['denominator'];u=mp.log(target);lo_sum=mp.mpf(0);hi_sum=mp.mpf(0);criticals=0
            certificates={c['k']:c for c in diagnostic['critical_points']}
            def h(t):return mp.exp(-a*t*t)*mp.cos(u*t)
            def theta(t):return u*t+mp.atan(2*a*t/u)
            for box in boxes:
                l,r=mp_endpoint(box.lower()),mp_endpoint(box.upper());values=[h(l),h(r)]
                first,last=int(mp.ceil(theta(l)/mp.pi)),int(mp.floor(theta(r)/mp.pi))
                for k in range(max(1,first),last+1):
                    t=mp.findroot(lambda t:theta(t)-k*mp.pi,(l,r),solver='secant',verify=True)
                    assert l<=t<=r and k in certificates and inside(t,core.decode(certificates[k]['point']))
                    value=h(t);assert inside(value,core.decode(certificates[k]['value']))
                    values.append(value);criticals+=1
                    if omitted_critical is None:
                        aa=arb(1)/diagnostic['denominator'];uu=arb(target).log();point=core.decode(certificates[k]['point'])
                        endpoint_values=[(-aa*z*z).exp()*(uu*z).cos() for z in [box.lower(),box.upper()]]
                        critical_value=core.decode(certificates[k]['value'])
                        upper=max(v.upper() for v in endpoint_values);lower=min(v.lower() for v in endpoint_values)
                        separation=max((critical_value-upper).lower(),(lower-critical_value).lower())
                        if separation>0 and box.contains(point):
                            omitted_critical={'height':top,'delta':delta,'target':target,'box':core.encode(box),
                              'critical_point':certificates[k],'endpoints':[core.encode(v) for v in endpoint_values],
                              'strict_gap_beyond_endpoint_hull':core.encode(separation)}
                lo_sum+=2*min(values);hi_sum+=2*max(values)
            assert criticals==diagnostic['critical_boxes']
            lower_slack=lo_sum-mp_endpoint(core.decode(diagnostic['stationary_lower_sum']).lower())
            upper_slack=mp_endpoint(core.decode(diagnostic['stationary_upper_sum']).upper())-hi_sum
            assert 0<=lower_slack<mp.mpf('1e-25') and 0<=upper_slack<mp.mpf('1e-25')
            mp_cases.append({'height':top,'delta':delta,'target':target,'roots_checked':len(boxes),'critical_points_checked':criticals,
               'minimum_sum':mp.nstr(lo_sum,72),'maximum_sum':mp.nstr(hi_sum,72),'lower_bound_slack':mp.nstr(lower_slack,30),
               'upper_bound_slack':mp.nstr(upper_slack,30),'inside_certified_extrema_bounds':True})
            print(json.dumps({'event':'mpmath_extrema','height':top,'delta':delta,'target':target,'criticals':criticals}),flush=True)
    assert len(mp_cases)==12 and omitted_critical
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'input_sha256':core.sha(raw),
       'results_sha256':{n:core.sha((directory/n).read_bytes()) for n in names},'fixed_point_scale_bits':192,
       'interval_replays':replays,'exclusions_replayed':total,'critical_point_strict_phase_brackets':point_checks,
       'precision_domain_comparisons':len(low),'domain_inclusion_comparisons':comparisons,'probe_repeat_cases':40,
       'arithmetic_factor_degrees':degrees,'mpmath_digits':80,'mpmath_extrema_cases':mp_cases,
       'adversarial_controls':{'missing_prerequisites':missing_control,'true_coefficient_elimination':true_control,'omitted_critical_point':omitted_critical},
       'elapsed_seconds':time.monotonic()-start,
       'scope':'Exact integer exclusion replay shares certified analytic input intervals. All reported turning points receive independent strict phase brackets; 12 scalar finite-sum extrema receive 80-digit numerical checks on producer machine-enlarged boxes. This neither optimizes correlated measurements nor proves remaining candidate vectors jointly feasible.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--prior',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=run(a.directory,a.prior);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cases':len(result['interval_replays']),'exclusions':result['exclusions_replayed'],
                      'critical_brackets':result['critical_point_strict_phase_brackets'],'mpmath_cases':len(result['mpmath_extrema_cases'])}))
