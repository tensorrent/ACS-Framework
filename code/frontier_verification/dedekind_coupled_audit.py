"""Exact integer replay of interval/dual witnesses, held-out arithmetic and ambiguity."""
import argparse,ast,json,time,warnings
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from sympy import Poly,cyclotomic_poly,symbols
import dedekind_coupled_recovery as core

BITS=192
GRID=1<<BITS
DUAL_GRID=10**9


def scaled(x,ceiling=False):
    m,e=map(int,x.man_exp());shift=e+BITS
    if shift>=0:return m<<shift
    return -((-m)>>(-shift)) if ceiling else m>>(-shift)


def integers(rows):
    return [{'lo':[scaled(w.lower()) for w in r['weights']],
             'hi':[scaled(w.upper(),True) for w in r['weights']],
             'rlo':scaled(r['R'].lower()),'rhi':scaled(r['R'].upper(),True),
             'tail':scaled(r['B'].upper(),True)} for r in rows]


def gap(row,domains,column,candidate,side):
    lower=sum(w*d[0] for w,d in zip(row['lo'],domains))
    upper=sum(w*d[-1] for w,d in zip(row['hi'],domains))+row['tail']
    lo=lower+row['lo'][column]*(candidate-domains[column][0])
    hi=upper+row['hi'][column]*(candidate-domains[column][-1])
    return lo-row['rhi'] if side=='candidate_minimum_above_observation' else row['rlo']-hi


def dual_bound(rows,column,certificate,domains):
    assert certificate['sign'] in [-1,1]
    vector=[0]*len(domains);beta=0
    for index,value in certificate['multipliers']:
        rational=F(value);assert rational>=0
        scalar=rational*DUAL_GRID;assert scalar.denominator==1;scalar=scalar.numerator
        row=rows[index//2]
        if index%2==0:coefs=row['lo'];rhs=row['rhi']
        else:coefs=[-v for v in row['hi']];rhs=-row['rlo']+row['tail']
        vector=[v+scalar*a for v,a in zip(vector,coefs)];beta+=scalar*rhs
    unit=GRID*DUAL_GRID
    residual=[(certificate['sign']*unit if j==column else 0)-v for j,v in enumerate(vector)]
    correction=sum(max(v*d[0],v*d[-1]) for v,d in zip(residual,domains))
    return beta+correction,unit


def run(directory):
    start=time.monotonic();raw=(directory/'Measurements.json').read_bytes();data=json.loads(raw)
    names=['Coupled_160.json','Coupled_224.json','Uncertainty_Grid.json','Dual_224.json','Dual_Refined.json']
    raws={n:(directory/n).read_bytes() for n in names};datasets={n:json.loads(r) for n,r in raws.items()}
    assert all(d['status']=='passed' and d['input_sha256']==core.sha(raw) for d in datasets.values())
    forbidden={'candidates','local_candidates','models','retained_models','expected','coefficient'}
    assert all(not forbidden.intersection(r) for r in data['measurements'])
    source=Path(core.__file__).read_text();tree=ast.parse(source)
    imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
    assert imports==['fractions','pathlib','flint']
    calls={ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)}
    assert not {'local_models','local_inference','factor_list'}.intersection(calls)
    powers=core.support(4096);x=symbols('x');phi=cyclotomic_poly(5,x);arithmetic={};factorizations={}
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for p in sorted({p for n,p,k in powers}):
            unit,factors=Poly(phi,x,modulus=p).factor_list();product=Poly(unit,x,modulus=p)
            degrees=[]
            for f,e in factors:product*=f**e;degrees.append((int(e),int(f.degree())))
            assert product==Poly(phi,x,modulus=p)
            factorizations[p]=degrees
        for n,p,k in powers:arithmetic[n]=sum(f for e,f in factorizations[p] if k%f==0)
    cache={}
    def prepare(top,bits,delta):
        key=(top,bits,delta)
        if key not in cache:
            pp,rows,settings=core.prepare(data,top,bits,delta);assert pp==powers
            cache[key]=(rows,integers(rows),settings)
        return cache[key]
    replays=[];dependency_controls=[];total_exclusions=0
    for filename in names[:3]:
        for case in datasets[filename]['cases']:
            settings=case['settings'];top,bits=settings['top'],settings['precision_bits'];delta=case['additional_radius']
            rows,ir,actual_settings=prepare(top,bits,delta)
            assert actual_settings==settings and case['measurements']==[r['metadata'] for r in rows]
            domains=[list(range(5)) for _ in powers];checked=0
            for r in case['rounds']:
                assert r['prior_domains_sha256']==core.sha(core.canonical(domains))
                old=[list(d) for d in domains]
                for witness in r['removals']:
                    i,c,j=witness['column'],witness['candidate'],witness['measurement_index']
                    assert powers[i][0]==witness['n'] and c in old[i]
                    exact_gap=gap(ir[j],old,i,c,witness['side']);assert exact_gap>0,(filename,top,delta,witness)
                    assert c!=arithmetic[powers[i][0]]
                    if r['round']>1 and not dependency_controls:
                        reset_gap=gap(ir[j],[list(range(5)) for _ in powers],i,c,witness['side'])
                        if reset_gap<=0:dependency_controls.append({'file':filename,'height':top,'round':r['round'],'n':powers[i][0],
                           'candidate':c,'valid_gap_scaled_integer':str(exact_gap),'reset_prerequisite_gap_scaled_integer':str(reset_gap),
                           'missing_prerequisites_rejected':True})
                    domains[i].remove(c);checked+=1
                assert r['remaining_domains_sha256']==core.sha(core.canonical(domains))
            assert domains==[r['candidates'] for r in case['domains']]
            assert all(arithmetic[n] in d for (n,p,k),d in zip(powers,domains))
            total_exclusions+=checked
            replays.append({'file':filename,'height':top,'delta':delta,'exclusions_replayed':checked,
                            'all_604_true_coefficients_retained':True,'domains_sha256':core.sha(core.canonical(domains))})
            print(json.dumps({'event':'integer_replay','file':filename,'height':top,'delta':delta,'exclusions':checked}),flush=True)
    # Precision and added-uncertainty comparisons concern identical measurements.
    lo=datasets['Coupled_160.json']['cases'];hi=datasets['Coupled_224.json']['cases']
    assert all(a['domains']==b['domains'] for a,b in zip(lo,hi))
    for top in [1000,2000]:
        cases=[next(c for c in hi if c['settings']['top']==top)]+[c for c in datasets['Uncertainty_Grid.json']['cases'] if c['settings']['top']==top]
        for a,b in zip(cases,cases[1:]):assert all(set(x['candidates'])<=set(y['candidates']) for x,y in zip(a['domains'],b['domains']))
    dual_results=[];dual_count=0
    initial=datasets['Dual_224.json'];refined=datasets['Dual_Refined.json']
    for original,final in zip(initial['cases'],refined['cases']):
        top=original['settings']['top'];rows,ir,settings=prepare(top,224,original['additional_radius'])
        domains=[list(range(5)) for _ in powers];initial_exact=[]
        for target in original['targets']:
            column=target['column'];bounds=[dual_bound(ir,column,c,[list(range(5)) for _ in powers]) for c in target['certificates']]
            candidates=[v for v in range(5) if all(c['sign']*v*den<=num for c,(num,den) in zip(target['certificates'],bounds))]
            assert candidates==target['candidates'] and arithmetic[target['n']] in candidates
            domains[column]=candidates;dual_count+=2
            initial_exact.append({'n':target['n'],'bounds':[str(F(num,den)) for num,den in bounds],'candidates':candidates})
        refinements=[]
        for r in final['rounds']:
            assert r['prior_domains_sha256']==core.sha(core.canonical(domains));old=[list(d) for d in domains]
            for change in r['changes']:
                column=change['column'];bounds=[dual_bound(ir,column,c,old) for c in change['certificates']]
                candidates=[v for v in old[column] if all(c['sign']*v*den<=num for c,(num,den) in zip(change['certificates'],bounds))]
                assert candidates==change['after'] and arithmetic[change['n']] in candidates
                domains[column]=candidates;dual_count+=2
                refinements.append({'round':r['round'],'n':change['n'],'bounds':[str(F(num,den)) for num,den in bounds],'candidates':candidates})
            assert r['remaining_domains_sha256']==core.sha(core.canonical(domains))
        assert domains==[r['candidates'] for r in final['domains']]
        dual_results.append({'height':top,'initial_bounds':initial_exact,'refinements':refinements,
                             'final_domains_sha256':core.sha(core.canonical(domains))})
    assert dependency_controls
    # Tamper with a recorded elimination by substituting the true coefficient.
    first=hi[0];rows,ir,_=prepare(220,224,'0');w=first['rounds'][0]['removals'][0]
    true=arithmetic[w['n']]
    false_gap=gap(ir[w['measurement_index']],[list(range(5)) for _ in powers],w['column'],true,w['side'])
    assert false_gap<=0
    zero_dual={'sign':1,'multipliers':[]};wrong_correction_n=next(n for n,p,k in powers if arithmetic[n]==4)
    column=next(i for i,(n,p,k) in enumerate(powers) if n==wrong_correction_n)
    valid,den=dual_bound(ir,column,zero_dual,[list(range(5)) for _ in powers]);assert valid==4*den
    negative_rejected=False
    try:dual_bound(ir,column,{'sign':1,'multipliers':[[0,'-1']]},[list(range(5)) for _ in powers])
    except AssertionError:negative_rejected=True
    assert negative_rejected
    # Construct actual alternative assignments for the interval relaxation.
    # Held-out arithmetic supplies only the unchanged nuisance coordinates.
    ctx.prec=256;rows,ir,_=prepare(220,224,'0');baseline=[arithmetic[n] for n,p,k in powers]
    pair_columns=[next(i for i,(n,p,k) in enumerate(powers) if n==target) for target in [359,361]]
    alternatives=[];failed_alternatives=[]
    for c359 in [0,1]:
        for c361 in [1,2,3,4]:
            values=list(baseline);values[pair_columns[0]]=c359;values[pair_columns[1]]=c361
            gaps=[]
            for j,row in enumerate(rows):
                total=sum((w*c for w,c in zip(row['weights'],values)),arb(0))
                # q_tail=0 is allowed by the relaxation. Strict inclusion
                # proves feasibility for all real weights in their balls.
                lower=total-row['R'].lower();upper=row['R'].upper()-total
                if not(lower>0 and upper>0):break
                gaps.append({'measurement_index':j,'lower_gap':core.encode(lower),'upper_gap':core.encode(upper)})
            if len(gaps)==len(rows):alternatives.append({'c359':c359,'c361':c361,'tail_assignment':'0 in every row','strict_inclusion_gaps':gaps})
            else:failed_alternatives.append({'c359':c359,'c361':c361,'first_noncertified_row':j})
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'input_sha256':core.sha(raw),
            'results_sha256':{n:core.sha(r) for n,r in raws.items()},'fixed_point_scale_bits':BITS,
            'interval_replays':replays,'exclusions_replayed':total_exclusions,'exact_dual_certificates':dual_count,'dual_replays':dual_results,
            'factorization_residue_degrees':factorizations,'all_coefficient_checks_per_case':604,
            'adversarial_controls':{'missing_prerequisites':dependency_controls,'true_coefficient_elimination_rejected':false_gap<=0,
                                   'negative_dual_multiplier_rejected':negative_rejected,
                                   'omitted_support_correction_rejected':{'n':wrong_correction_n,'invalid_upper_bound':0,'validated_upper_bound':4}},
            'relaxation_ambiguity':{'baseline_coefficients':baseline,'columns':powers,'alternatives':alternatives,'noncertified_trials':failed_alternatives,
                'scope':'Assignments satisfying this finite interval relaxation, not alternative number fields or zero spectra. All beyond-cutoff prime-tail variables are set to their permitted lower bound zero.'},
            'elapsed_seconds':time.monotonic()-start,
            'scope':'Weight and measurement enclosures share the analytic/FLINT input; all exclusions and dual objectives are replayed with exact integers after outward rounding to a fixed dyadic grid. Polynomial arithmetic is held out until producer results are frozen.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.directory)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'exclusions':r['exclusions_replayed'],
           'dual_certificates':r['exact_dual_certificates'],'relaxation_alternatives':[(x['c359'],x['c361']) for x in r['relaxation_ambiguity']['alternatives']]}))
