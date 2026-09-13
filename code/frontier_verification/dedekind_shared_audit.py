"""Exact shared-error dual replay, higher-precision checks and independent derivatives."""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sp
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_coupled_dual as dual
from dedekind_coupled_audit import scaled,integers,dual_bound,GRID,DUAL_GRID
import dedekind_shared_ordinate as shared

UNIT=GRID*DUAL_GRID


def read(p):return json.loads(p.read_text())
def mp_exact(x):
    m,e=map(int,x.man_exp());return mp.mpf(m)*mp.power(2,e)
def inside(value,box):return mp_exact(box.lower())<=value<=mp_exact(box.upper())


def integer_basis(rows,basis):
    return [{'wlo':[scaled(w.lower()) for w in r['weights']],
       'whi':[scaled(w.upper(),True) for w in r['weights']],
       'jlo':[scaled(j.lower()) for j in b['J']],
       'jhi':[scaled(j.upper(),True) for j in b['J']],
       'clo':scaled(b['center'].lower()),'chi':scaled(b['center'].upper(),True),
       'error':scaled(b['error'].upper(),True),'prime':scaled(r['B'].upper(),True)} for r,b in zip(rows,basis)]


def exact_bound(basis,column,certificate,domains):
    assert certificate['sign'] in [-1,1]
    vlo=[0]*len(domains);vhi=[0]*len(domains)
    jlo=[0]*len(basis[0]['jlo']);jhi=[0]*len(jlo);center=0;tail=0
    for index,value in certificate['multipliers']:
        scalar=F(value)*DUAL_GRID;assert scalar.denominator==1;scalar=scalar.numerator
        b=basis[index]
        center+=scalar*(b['chi'] if scalar>=0 else b['clo'])
        tail+=abs(scalar)*b['error']+max(0,-scalar)*b['prime']
        low,high=('lo','hi') if scalar>=0 else ('hi','lo')
        vlo=[v+scalar*w for v,w in zip(vlo,b['w'+low])]
        vhi=[v+scalar*w for v,w in zip(vhi,b['w'+high])]
        jlo=[v+scalar*j for v,j in zip(jlo,b['j'+low])]
        jhi=[v+scalar*j for v,j in zip(jhi,b['j'+high])]
    noise=sum(max(abs(a),abs(b)) for a,b in zip(jlo,jhi))
    residual=0
    for i,(lo,hi,domain) in enumerate(zip(vlo,vhi,domains)):
        e=certificate['sign']*UNIT if i==column else 0
        rlo,rhi=e-hi,e-lo
        residual+=max(domain[0]*rlo,domain[0]*rhi,domain[-1]*rlo,domain[-1]*rhi)
    value=center+tail+noise+residual
    return value,{'weighted_center_upper':str(F(center,UNIT)),'zero_taylor_prime_upper':str(F(tail,UNIT)),
       'shared_ordinate_upper':str(F(noise,UNIT)),'residual_support_upper':str(F(residual,UNIT)),
       'objective_upper_bound':str(F(value,UNIT))}


def run(directory,prior):
    start=time.monotonic();names=['Marginal_224.json','Shared_Probe160.json','Shared_160.json']
    results={n:read(directory/n) for n in names};assert all(r['status']=='passed' for r in results.values())
    assert results['Marginal_224.json']['source_sha256']==results['Shared_Probe160.json']['source_sha256']==core.sha(Path(shared.__file__).read_bytes())
    assert results['Shared_160.json']['basis_source_sha256']==core.sha(Path(shared.__file__).read_bytes())
    assert results['Shared_160.json']['source_sha256']==core.sha(Path(__file__).with_name('dedekind_shared_recovery.py').read_bytes())
    truth=read(prior.parent/'2026-09-13-coupled-delta'/'Exact_Audit.json')['relaxation_ambiguity']['baseline_coefficients']
    ctx.prec=224;data,powers,rows,seeds,provenance=shared.load(prior,2000,224,'5e-3')
    assert len(truth)==604 and all(t in d for t,d in zip(truth,seeds))
    marginal=results['Marginal_224.json'];assert marginal['provenance']==provenance
    matrix,rhs=dual.inequalities(rows);ir=integers(rows);marginal_replays=[]
    for case in marginal['cases']:
        domains=[list(d) for d in seeds]
        for step in case['rounds']:
            old=[list(d) for d in domains];assert core.sha(core.canonical(old))==step['prior_domains_sha256']
            for check in step['checks']:
                bounds=[dual_bound(ir,check['column'],c,old) for c in check['certificates']]
                after=[v for v in old[check['column']] if all(c['sign']*v*den<=num for c,(num,den) in zip(check['certificates'],bounds))]
                assert after==check['after'] and truth[check['column']] in after
                domains[check['column']]=after
                marginal_replays.append({'n':check['n'],'bounds':[str(F(num,den)) for num,den in bounds],'candidates':after})
            assert core.sha(core.canonical(domains))==step['remaining_domains_sha256']
        assert domains==[d['candidates'] for d in case['domains']] and case['unique_targets']==73
    replay_reports=[];certificate_count=0;removed_count=0;dependency_control=None
    for bits in [160,224]:
        data,powers,rows,seeds,provenance=shared.load(prior,2000,bits,'5e-3')
        basis,metadata=shared.shared_basis(data,rows,2000,bits,'5e-3');ib=integer_basis(rows,basis)
        for name in ['Shared_Probe160.json','Shared_160.json']:
            result=results[name]
            if bits==160:assert metadata==result['shared_basis']
            assert result['provenance']==provenance
            case=result['cases'][0] if name=='Shared_Probe160.json' else result
            domains=[list(d) for d in seeds];replayed=[]
            for step in case['rounds']:
                old=[list(d) for d in domains];assert core.sha(core.canonical(old))==step['prior_domains_sha256']
                for check in step['checks']:
                    column=check['column'];assert old[column]==check['before']
                    bounds=[];precise=[]
                    for certificate in check['certificates']:
                        scalar=[F(0)]*len(rows)
                        for i,v in certificate['multipliers']:scalar[i]=F(v)
                        proof=shared.shared_bound(rows,basis,column,certificate['sign'],scalar,old)
                        if bits==160:assert all(proof[k]==certificate[k] for k in proof)
                        exact,parts=exact_bound(ib,column,certificate,old)
                        assert certificate['sign']*truth[column]*UNIT<=exact
                        bounds.append(exact);precise.append(core.decode(proof['objective_upper_bound']).upper());certificate_count+=1
                        if bits==160 and dependency_control is None:
                            excluded=[v for v in old[column] if certificate['sign']*v*UNIT>exact]
                            if excluded:
                                reset,_=exact_bound(ib,column,certificate,[list(range(5)) for _ in seeds])
                                if any(certificate['sign']*v*UNIT<=reset for v in excluded):
                                    dependency_control={'file':name,'n':check['n'],'sign':certificate['sign'],'excluded_candidates':excluded,
                                        'valid_objective_upper_bound':parts['objective_upper_bound'],'without_seed_bounds':str(F(reset,UNIT))}
                        replayed.append({'round':step['round'],'n':check['n'],'sign':certificate['sign'],
                            'multipliers_sha256':core.sha(core.canonical(certificate['multipliers'])),
                            'precision_bits':bits,'interval_objective_upper_bound':core.encode(precise[-1]),**parts})
                    after=[v for v in old[column] if all(c['sign']*v*UNIT<=bound for c,bound in zip(check['certificates'],bounds))]
                    arb_after=[v for v in old[column] if all(not arb(c['sign']*v)>bound for c,bound in zip(check['certificates'],precise))]
                    assert after==arb_after==check['after'] and truth[column] in after
                    if bits==160:removed_count+=len(old[column])-len(after)
                    domains[column]=after
                assert core.sha(core.canonical(domains))==step['remaining_domains_sha256']
            assert domains==[d['candidates'] for d in case['domains']]
            replay_reports.append({'file':name,'precision_bits':bits,'certificates':replayed,
                'domains_sha256':core.sha(core.canonical(domains)),'all_604_arithmetic_coefficients_retained':all(t in d for t,d in zip(truth,domains))})
            print(json.dumps({'event':'exact_shared_replay','file':name,'bits':bits,'certificates':len(replayed)}),flush=True)
        del ib
        if bits==160:del basis
    assert dependency_control
    # The derivative identity is derived independently before evaluating samples.
    t,a,u=sp.symbols('t a u',real=True);h=sp.exp(-a*t*t)*sp.cos(u*t)
    expected=sp.exp(-a*t*t)*((4*a*a*t*t-2*a-u*u)*sp.cos(u*t)+4*a*u*t*sp.sin(u*t))
    assert sp.simplify(sp.diff(h,t,2)-expected)==0
    selected=[r for r in data['roots'] if F(r['hi'])<2000];ctx.prec=224;radius=arb('5e-3')
    boxes=[arb(r['lo']).union(arb(r['hi']))+arb(0,radius.upper()) for r in selected]
    assert core.sha(core.canonical([core.encode(b) for b in boxes]))==metadata['root_boxes_sha256']
    mp.mp.dps=80;point_checks=[];center_checks=[];omitted_remainder=None;wrong_support=None
    for index,(row,b) in enumerate(zip(rows,basis)):
        m=row['metadata']
        if m['n'] not in [2,32,361]:continue
        active=[j for j,s in enumerate(selected) if F(s['hi'])<m['height']]
        indices=sorted({active[0],active[1],active[len(active)//3],active[len(active)//2],active[-1]})
        aa=mp.mpf(1)/m['denominator'];uu=mp.log(m['n']);AA=2*mp.sqrt(mp.pi*aa)*mp.sqrt(m['n'])/mp.log(m['prime'])
        af=arb(1)/m['denominator'];uf=arb(m['n']).log();Af=core.decode(m['scale'])
        def mh(z):return mp.exp(-aa*z*z)*mp.cos(uu*z)
        for j in indices:
            box=boxes[j];center=box.mid();rad=box.rad();tt=mp_exact(center);rr=mp_exact(rad)
            derivative=mp.diff(mh,tt);J=2*AA*rr*derivative
            assert inside(J,b['J'][j])
            maximum=shared.hpp(af,uf,box).abs_upper()
            second_values=[mp.diff(mh,z,2) for z in [mp_exact(box.lower()),tt,mp_exact(box.upper())]]
            assert all(abs(v)<=mp_exact(maximum.upper()) for v in second_values)
            point_checks.append({'measurement_index':index,'target':m['n'],'height':m['height'],'root_index':j,
                 'normalized_derivative':mp.nstr(J,72),'second_derivatives':[mp.nstr(v,60) for v in second_values],
                 'derivative_enclosed':True,'second_derivatives_bounded':True})
        if m['height']==2000 and m['n'] in [32,361]:
            finite=2*mp.fsum(mh(mp_exact(boxes[j].mid())) for j in active)
            bg=arb(m['pole'])+arb(m['discriminant_term'])+arb(m['gamma'])
            observation=AA*(mp_exact(bg.mid())-finite);assert inside(observation,b['center'])
            center_checks.append({'target':m['n'],'roots':len(active),'finite_center_sum':mp.nstr(finite,72),
                'observation_with_inherited_background_midpoint':mp.nstr(observation,72),'inside_certified_center':True})
        if omitted_remainder is None:
            for j in active[:40]:
                box=boxes[j];center=box.mid();rad=box.rad();derivative=shared.hp(af,uf,center)
                if not(derivative>0 or derivative<0):continue
                step=-rad if derivative>0 else rad
                value=lambda z:(-af*z*z).exp()*(uf*z).cos()
                actual=2*Af*(value(center)-value(center+step));linear=b['J'][j].abs_upper()
                excess=actual-linear
                if excess>0:
                    omitted_remainder={'measurement_index':index,'target':m['n'],'root_index':j,'box':core.encode(box),
                        'chosen_displacement':core.encode(step),'actual_finite_observation_change':core.encode(actual),
                        'linear_support':core.encode(linear),'strict_excess_without_remainder':core.encode(excess)};break
        if wrong_support is None:
            positive=next((j for j in active if b['J'][j]>0),None);negative=next((j for j in active if b['J'][j]<0),None)
            if positive is not None and negative is not None:
                x,y=b['J'][positive],b['J'][negative];valid=x-y;wrong=(x+y).abs_upper();difference=valid-wrong
                if difference>0:wrong_support={'measurement_index':index,'root_indices':[positive,negative],
                    'J':[core.encode(x),core.encode(y)],'attainable_linear_change':core.encode(valid),
                    'invalid_absolute_of_sum_bound':core.encode(wrong),'strict_underestimate':core.encode(difference)}
    assert len(point_checks)==75 and len(center_checks)==2 and omitted_remainder and wrong_support
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),
       'basis_source_sha256':core.sha(Path(shared.__file__).read_bytes()),'results_sha256':{n:core.sha((directory/n).read_bytes()) for n in names},
       'fixed_point_scale_bits':192,'multiplier_denominator':10**9,'marginal_certificates':sum(len(r['bounds']) for r in marginal_replays),
       'marginal_replays':marginal_replays,'shared_certificates_across_precisions':certificate_count,
       'shared_replays':replay_reports,'candidate_removals_including_probe':removed_count,
       'symbolic_second_derivative_identity':True,'mpmath_digits':80,'derivative_point_checks':point_checks,'finite_center_checks':center_checks,
       'adversarial_controls':{'missing_seed_bounds':dependency_control,'omitted_taylor_remainder':omitted_remainder,'absolute_of_sum_instead_of_sum_of_absolutes':wrong_support},
       'elapsed_seconds':time.monotonic()-start,
       'scope':'All published shared duals are recomputed at 160 and 224 bits and replayed by exact integer support arithmetic. Analytic intervals share FLINT/Arb. Independent 80-digit derivative and center checks use inherited background intervals; they do not recertify the explicit formula, zero counts or unknown-field identifiability.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--prior',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.directory,a.prior);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'shared_certificates':r['shared_certificates_across_precisions'],
        'marginal_certificates':r['marginal_certificates'],'derivative_checks':len(r['derivative_point_checks'])}))
