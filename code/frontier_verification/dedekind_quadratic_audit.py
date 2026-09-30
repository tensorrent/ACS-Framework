"""Exact integer audit of quadratic support, with a second interval precision."""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
import dedekind_coupled_recovery as core
from dedekind_coupled_audit import scaled,GRID,DUAL_GRID
from dedekind_shared_audit import integer_basis as first_integer_basis
import dedekind_quadratic_ordinate as quad

UNIT=GRID*DUAL_GRID


def read(path):return json.loads(path.read_text())


def integer_basis(rows,basis):
    result=first_integer_basis(rows,basis)
    for r,b in zip(result,basis):
        r['klo']=[scaled(k.lower()) for k in b['K']];r['khi']=[scaled(k.upper(),True) for k in b['K']]
        r['qerror']=scaled(b['quadratic_error'].upper(),True)
    return result


def exact_combination(basis,multipliers):
    C=len(basis[0]['wlo']);N=len(basis[0]['jlo'])
    vlo=[0]*C;vhi=[0]*C;jlo=[0]*N;jhi=[0]*N;klo=[0]*N;khi=[0]*N
    center=0;linear_tail=0;quadratic_tail=0
    for index,value in multipliers:
        scalar=F(value)*DUAL_GRID;assert scalar.denominator==1;scalar=scalar.numerator;b=basis[index]
        center+=scalar*(b['chi'] if scalar>=0 else b['clo'])
        prime=max(0,-scalar)*b['prime'];linear_tail+=abs(scalar)*b['error']+prime;quadratic_tail+=abs(scalar)*b['qerror']+prime
        low,high=('lo','hi') if scalar>=0 else ('hi','lo')
        vlo=[v+scalar*x for v,x in zip(vlo,b['w'+low])];vhi=[v+scalar*x for v,x in zip(vhi,b['w'+high])]
        jlo=[v+scalar*x for v,x in zip(jlo,b['j'+low])];jhi=[v+scalar*x for v,x in zip(jhi,b['j'+high])]
        klo=[v+scalar*x for v,x in zip(klo,b['k'+low])];khi=[v+scalar*x for v,x in zip(khi,b['k'+high])]
    linear=0;independent=0;coupled=0;vertices=0
    for lo,hi,E in zip(jlo,jhi,klo):
        D=max(abs(lo),abs(hi));linear+=D;independent+=D+max(0,-E)
        if E>0 and D<2*E:
            # Outward ceiling returns to the common integer scale, avoiding
            # a sum of thousands of unrelated rational denominators.
            coupled+=(D*D+4*E-1)//(4*E);vertices+=1
        else:coupled+=D-E
    assert coupled<=independent+N
    return {'vlo':vlo,'vhi':vhi,'center':center,'linear_tail':linear_tail,'quadratic_tail':quadratic_tail,
        'allowances':{'linear':linear,'independent_quadratic':independent,'quadratic':coupled},
        'interior_vertices':vertices,'endpoints':N-vertices}


def exact_objective(combination,column,sign,domains,mode):
    residual=0
    for i,(lo,hi,d) in enumerate(zip(combination['vlo'],combination['vhi'],domains)):
        target=sign*UNIT if i==column else 0;rlo,rhi=target-hi,target-lo
        residual+=max(d[0]*rlo,d[0]*rhi,d[-1]*rlo,d[-1]*rhi)
    tail=combination['linear_tail'] if mode=='linear' else combination['quadratic_tail']
    allowance=combination['allowances'][mode];upper=combination['center']+tail+allowance+residual
    return upper,{'weighted_center_upper':str(F(combination['center'],UNIT)),'tail_upper':str(F(tail,UNIT)),
        'ordinate_support_upper':str(F(allowance,UNIT)),'residual_support_upper':str(F(residual,UNIT)),
        'objective_upper_bound':str(F(upper,UNIT))}


def run(directory,prior,names):
    start=time.monotonic();raws={n:(directory/n).read_bytes() for n in names};results={n:json.loads(raw) for n,raw in raws.items()}
    assert all(r['status']=='passed' for r in results.values())
    truth=read(prior.parent/'2026-09-13-coupled-delta'/'Exact_Audit.json')['relaxation_ambiguity']['baseline_coefficients']
    replays=[];certificate_total=0;seed_control=None
    for bits in [160,224]:
        data,powers,rows,seeds,previous,provenance=quad.load(prior,bits);ctx.prec=bits
        basis,metadata=quad.prepare(data,rows,bits);ib=integer_basis(rows,basis)
        intervals={};exact={};multipliers_by_key={}
        for name,result in results.items():
            assert result['provenance']==provenance
            if result['precision_bits']==bits:assert result['basis']==metadata
            if 'proposals' in result:proposals=result['proposals']
            elif 'checks' in result:proposals=[c for check in result['checks'] for c in check['certificates']]
            else:proposals=[c for step in result['rounds'] for check in step['checks'] for c in check['certificates']]
            for p in proposals:
                key=p['combination_sha256'];assert key==core.sha(core.canonical(p['multipliers']))
                if key in intervals:assert multipliers_by_key[key]==p['multipliers'];continue
                alpha=[F(0)]*len(rows)
                for index,value in p['multipliers']:alpha[index]=F(value)
                intervals[key]=quad.combine(rows,basis,alpha);exact[key]=exact_combination(ib,p['multipliers']);multipliers_by_key[key]=p['multipliers']
            if result['precision_bits']==bits:
                assert all(intervals[k]['metadata']==v for k,v in result['combinations'].items())
            def evaluate(certificate,column,old,mode):
                nonlocal certificate_total,seed_control
                key=certificate['combination_sha256'];sign=certificate['sign'];assert sign in [-1,1]
                proof=quad.objective(intervals[key],column,sign,old,mode)
                retained=certificate['bounds'][mode] if 'bounds' in certificate else certificate
                if result['precision_bits']==bits:assert all(proof[k]==retained[k] for k in proof)
                integer,parts=exact_objective(exact[key],column,sign,old,mode)
                assert sign*truth[column]*UNIT<=integer
                certificate_total+=1
                excluded=[v for v in old[column] if sign*v*UNIT>integer]
                if seed_control is None and excluded:
                    reset,_=exact_objective(exact[key],column,sign,[list(range(5)) for _ in old],mode)
                    if any(sign*v*UNIT<=reset for v in excluded):seed_control={'file':name,'mode':mode,'n':powers[column][0],
                        'excluded':excluded,'valid_upper':parts['objective_upper_bound'],'without_seed_bounds':str(F(reset,UNIT))}
                return integer,core.decode(proof['objective_upper_bound']).upper(),{'n':powers[column][0],'sign':sign,
                    'combination_sha256':key,'mode':mode,'precision_bits':bits,**parts}
            def flat_stage(label,mode,steps,expected):
                domains=[list(d) for d in seeds];records=[]
                for step in steps:
                    old=[list(d) for d in domains];assert step['prior_domains_sha256']==core.sha(core.canonical(old))
                    for c in step['checks']:
                        column=c['column'];assert c['before']==domains[column]
                        integer,interval,record=evaluate(c,column,old,mode)
                        after=[v for v in domains[column] if c['sign']*v*UNIT<=integer]
                        assert after==[v for v in domains[column] if not arb(c['sign']*v)>interval]==c['after']
                        domains[column]=after;records.append(record)
                    assert step['remaining_domains_sha256']==core.sha(core.canonical(domains))
                assert domains==[d['candidates'] for d in expected]
                assert all(t in d for t,d in zip(truth,domains))
                replays.append({'file':name,'stage':label,'precision_bits':bits,'certificates':records,
                    'domains_sha256':core.sha(core.canonical(domains)),'all_604_arithmetic_coefficients_retained':True})
            if 'cases' in result:
                for case in result['cases']:flat_stage(case['mode'],case['mode'],case['rounds'],case['domains'])
            elif 'rounds' in result:
                domains=[list(d) for d in seeds];records=[]
                for step in result['rounds']:
                    old=[list(d) for d in domains];assert step['prior_domains_sha256']==core.sha(core.canonical(old))
                    for check in step['checks']:
                        column=check['column'];assert check['before']==old[column];bounds=[];balls=[]
                        for c in check['certificates']:
                            integer,interval,record=evaluate(c,column,old,'quadratic');bounds.append(integer);balls.append(interval);records.append(record)
                        after=[v for v in old[column] if all(c['sign']*v*UNIT<=b for c,b in zip(check['certificates'],bounds))]
                        assert after==check['after']==[v for v in old[column] if all(not arb(c['sign']*v)>b for c,b in zip(check['certificates'],balls))]
                        domains[column]=after
                    assert step['remaining_domains_sha256']==core.sha(core.canonical(domains))
                assert domains==[d['candidates'] for d in result['domains']]
                replays.append({'file':name,'stage':'optimized_main','precision_bits':bits,'certificates':records,
                    'domains_sha256':core.sha(core.canonical(domains)),'all_604_arithmetic_coefficients_retained':all(t in d for t,d in zip(truth,domains))})
                for case in result['controls']:flat_stage('proposal_control_'+case['mode'],case['mode'],case['rounds'],case['domains'])
            else:
                for mode in ['linear','independent_quadratic','quadratic']:
                    domains=[list(d) for d in seeds];records=[]
                    for check in result['checks']:
                        column=check['column'];bounds=[];balls=[]
                        for c in check['certificates']:
                            integer,interval,record=evaluate(c,column,seeds,mode);bounds.append(integer);balls.append(interval);records.append(record)
                        after=[v for v in seeds[column] if all(c['sign']*v*UNIT<=b for c,b in zip(check['certificates'],bounds))]
                        assert after==check['control_candidates'][mode]==[v for v in seeds[column] if all(not arb(c['sign']*v)>b for c,b in zip(check['certificates'],balls))]
                        domains[column]=after
                    replays.append({'file':name,'stage':'conic_'+mode,'precision_bits':bits,'certificates':records,
                        'domains_sha256':core.sha(core.canonical(domains)),'all_604_arithmetic_coefficients_retained':all(t in d for t,d in zip(truth,domains))})
            print(json.dumps({'event':'quadratic_exact_replay','file':name,'bits':bits,'cumulative_certificates':certificate_total}),flush=True)
        del intervals,exact,ib,basis
    assert seed_control
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'basis_source_sha256':core.sha(Path(quad.__file__).read_bytes()),
        'results_sha256':{n:core.sha(raw) for n,raw in raws.items()},'fixed_point_scale_bits':192,'multiplier_denominator':10**9,
        'quadratic_vertex_rule':'If E>0 and D<2E, round D^2/(4E) upward to the shared integer grid; otherwise use D-E. Here D bounds absolute combined linear coefficients and E is a lower bound for combined curvature.',
        'certificate_evaluations_across_precisions':certificate_total,'replays':replays,'missing_seed_control':seed_control,
        'elapsed_seconds':time.monotonic()-start,
        'scope':'Every retained objective is recomputed at 160 and 224 bits and checked through exact integer support arithmetic, including outward-rounded scalar quadratic maxima. Analytic intervals share FLINT/Arb. Optimizer status and primal coordinates are not feasibility certificates.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--prior',type=Path,required=True);p.add_argument('--results',nargs='+',required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.directory,a.prior,a.results);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'certificate_evaluations':r['certificate_evaluations_across_precisions']}))
