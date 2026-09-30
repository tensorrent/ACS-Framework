"""Audit joint moment certificates with complex quadratic covers and rational monotonicity."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sp
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_shared_audit import terms_for
from dedekind_aggregate_noise_audit import complex_values
from dedekind_aggregate_integer_audit import integer_rows,objective_bound,endpoint,GRID,DUAL_GRID

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def rational_moment(q,order=0):
    d=9+4*q*q
    if order==0:return 12/d
    if order==1:return -96*q/(d*d)
    if order==2:return (1152*q*q-864)/(d*d*d)
    if order==3:return 4608*q*(9-4*q*q)/(d*d*d*d)
    raise ValueError(order)
def moment_interval(lo,hi,order=0):
    assert F(3,2)<lo<=hi
    # m decreases, m' increases, and m'' decreases above 3/2.
    left,right=(lo,hi) if order==1 else (hi,lo)
    return arb(str(rational_moment(left,order))).union(arb(str(rational_moment(right,order))))
def grid_value(q,upper):
    value=q*GRID
    return -((-value.numerator)//value.denominator) if upper else value.numerator//value.denominator
def number(x):
    q=F(x);return mp.mpf(q.numerator)/q.denominator

def run(certificate_path,measurements,proposals,previous_proposals,inputs,truth_path):
    ctx.prec=384;mp.mp.dps=85;a=arb(1)/25
    data=json.loads(certificate_path.read_text());m=json.loads(measurements.read_text());p=json.loads(proposals.read_text());old=json.loads(previous_proposals.read_text())
    source=[json.loads(x.read_text()) for x in inputs];truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    x=sp.symbols('x');function=12/(9+4*x*x)
    for order in [1,2,3]:assert sp.cancel(sp.diff(function,x,order)-rational_moment(x,order))==0
    altered=copy.deepcopy(m)
    for row in altered['rows']:
        for obs in [0,1]:row['observations'][obs]['R']=row['observations'][obs]['unwidened']
    integer_by_observation=[integer_rows(altered,obs) for obs in [0,1]]
    coefficient=[decode(row['scale'])*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh() for row in m['rows']]
    midpoint_checks=fresh_leaves=0;replays=[];displaced=[];improvements=[]
    for case in data['cases']:
        obs=case['observation_index'];delta=F(case['radius']);roots=source[obs]['positive_root_intervals'];alpha,sigma,terms=terms_for(m,case);active=any(sigma)
        expected=next(c for c in (p if case['multiplier_source']=='joint_adapted' else old)['cases'] if all(c[k]==case[k] for k in ['observation_index','radius','column','sign']))
        assert case['multipliers']==expected['multipliers'] and m['columns'][case['column']]['n']==case['n']
        assert [t['alpha'] for t in case['terms']]==list(map(str,alpha)) and [t['sigma'] for t in case['terms']]==list(map(str,sigma))
        assert len(case['root_bounds'])==len(roots)
        kappa=sum((arb(str(v))*k for v,k in zip(sigma,coefficient)),arb(0));assert kappa.overlaps(decode(case['kappa']))
        nominal,unit=objective_bound(integer_by_observation[obs],case['column'],case,len(m['columns']))
        assert unit==GRID*DUAL_GRID
        U0=endpoint(m['constant_moment_upper'],True)-sum(grid_value(rational_moment(F(r['hi'])),False) for r in roots)
        Uwide=endpoint(m['constant_moment_upper'],True)-sum(grid_value(rational_moment(F(r['hi'])+delta),False) for r in roots)
        assert Uwide>=U0>0
        finite_total=joint_total=arb(0);root_proofs=[];stream=hashlib.sha256()
        for index,(original,root) in enumerate(zip(roots,case['root_bounds'])):
            original_lo,original_hi=F(original['lo']),F(original['hi']);center=(original_lo+original_hi)/2
            lo,hi=original_lo-delta,original_hi+delta;assert F(3,2)<lo<=hi<20
            assert root['root_index']==index and F(root['lo'])==lo and F(root['hi'])==hi
            base_center,_,_=complex_values(arb(str(center)),a,terms);m_center=arb(str(rational_moment(center)))
            assert decode(root['base_H']).contains(base_center) and decode(root['base_moment']).contains(m_center)
            if delta and active:
                assert len(root['leaves'])==48;previous=lo
                for leaf in root['leaves']:
                    left,right=F(leaf['lo']),F(leaf['hi']);assert left==previous and left<right;middle=(left+right)/2
                    h,h1,_=complex_values(arb(str(middle)),a,terms)
                    finite=-2*(h-base_center);joint=finite-kappa*(arb(str(rational_moment(middle)))-m_center)
                    assert decode(leaf['finite_change']).contains(finite) and decode(leaf['joint_change']).contains(joint)
                    assert decode(leaf['finite_derivative']).contains(-2*h1)
                    assert decode(leaf['joint_derivative']).contains(-2*h1-kappa*arb(str(rational_moment(middle,1))))
                    previous=right;midpoint_checks+=1
                assert previous==hi
            else:assert root['leaves']==[]
            finite_upper=joint_upper=arb(0)
            if delta and active:
                base_H,_,_=complex_values(arb(str(original_lo)).union(arb(str(original_hi))),a,terms)
                base_m=moment_interval(original_lo,original_hi)
                for j in range(96):
                    left=lo+(hi-lo)*F(j,96);right=lo+(hi-lo)*F(j+1,96);middle=(left+right)/2
                    h,h1,_=complex_values(arb(str(middle)),a,terms)
                    _,_,h2=complex_values(arb(str(left)).union(arb(str(right))),a,terms)
                    half=arb(str((right-left)/2));v=arb(0,half);square=arb(0).union(half*half)
                    finite=-2*(h-base_H+h1*v+h2*square/2)
                    second_moment=moment_interval(left,right,2)
                    # Recombine the derivative coefficients before interval multiplication.
                    joint=(-2*(h-base_H)-kappa*(arb(str(rational_moment(middle)))-base_m)
                           +(-2*h1-kappa*arb(str(rational_moment(middle,1))))*v
                           +(-2*h2-kappa*second_moment)*square/2)
                    finite_upper=max(finite_upper,finite.upper());joint_upper=max(joint_upper,joint.upper());fresh_leaves+=1
                    stream.update(canonical({'lo':str(left),'hi':str(right),'finite':encode(finite),'joint':encode(joint),'moment_second_derivative':encode(second_moment)})+b'\n')
            finite_total+=finite_upper;joint_total+=joint_upper
            root_proofs.append({'root_index':index,'finite_increment_upper':encode(finite_upper),'joint_increment_upper':encode(joint_upper)})
        kappa_upper=endpoint(encode(kappa),True)
        separated=kappa_upper*Uwide+endpoint(encode(finite_total),True)*GRID
        uncapped=kappa_upper*U0+endpoint(encode(joint_total),True)*GRID
        budgets={'separate':separated,'coupled':min(separated,uncapped)};methods={}
        for name,budget in budgets.items():
            numerator=nominal*GRID+budget*DUAL_GRID;denominator=GRID*GRID*DUAL_GRID
            candidates=[v for v in range(5) if case['sign']*v*denominator<=numerator]
            assert set(candidates)<=set(case['methods'][name]['candidates']),('independent replay not yet as strong',obs,case['radius'],case['n'],case['sign'],name,candidates,case['methods'][name]['candidates'])
            assert truth[['A','B'][obs]][case['column']] in candidates
            if candidates!=case['methods'][name]['candidates']:
                improvements.append({**{k:case[k] for k in ['observation_index','radius','n','sign','multiplier_source']},'method':name,'producer':case['methods'][name]['candidates'],'independent':candidates})
            methods[name]={'objective_upper':str(F(numerator,denominator)),'budget_upper':str(F(budget,GRID*GRID)),'candidates':candidates}
        replays.append({**{k:case[k] for k in ['observation_index','radius','column','n','sign','multiplier_source']},
            'nominal_objective_upper':str(F(nominal,unit)),'baseline_unknown_moment_upper':str(F(U0,GRID)),
            'widened_unknown_moment_upper':str(F(Uwide,GRID)),'kappa_upper':str(F(kappa_upper,GRID)),
            'uncapped_joint_budget_upper':str(F(uncapped,GRID*GRID)),'root_bounds':root_proofs,'fresh_interval_stream_sha256':stream.hexdigest(),'methods':methods})
        if active:
            centers=[(number(r['lo'])+number(r['hi']))/2 for r in roots];dd=number(case['radius']);aa=mp.mpf(1)/25;mt=[];mk=mp.mpf(0)
            for av,sv,row in zip(alpha,sigma,m['rows']):
                prime=next(c['prime'] for c in m['columns'] if c['n']==row['center']);scale=2*mp.sqrt(mp.pi*aa)*mp.sqrt(row['center'])/mp.log(prime);u=mp.log(row['center'])
                if av:mt.append((number(str(av))*scale,u))
                if sv:mk+=number(str(sv))*scale*404*mp.exp(-16+aa/4)*mp.cosh(u/2)
            def h(t):return mp.exp(-aa*t*t)*mp.fsum(w*mp.cos(u*t) for w,u in mt)
            def mm(t):return 3/(mp.mpf('2.25')+t*t)
            def jj(t):return -2*h(t)-mk*mm(t)
            directions=[1 if mp.diff(jj,t)>=0 else -1 for t in centers]
            old_h=mp.fsum(h(t) for t in centers);old_m=mp.fsum(mm(t) for t in centers)
            for pattern in ['uniform_positive','uniform_negative','joint_gradient_positive','joint_gradient_negative']:
                direction=1 if pattern.endswith('positive') else -1
                values=[t+direction*dd*(s if pattern.startswith('joint_gradient') else 1) for t,s in zip(centers,directions)]
                finite=-2*(mp.fsum(h(t) for t in values)-old_h);joint=finite-mk*(mp.fsum(mm(t) for t in values)-old_m)
                assert arb(mp.nstr(finite,80))<=finite_total.upper()+arb('1e-70')
                assert arb(mp.nstr(joint,80))<=joint_total.upper()+arb('1e-70')
                displaced.append({**{k:case[k] for k in ['observation_index','radius','n','sign','multiplier_source']},'pattern':pattern,
                    'finite_change':mp.nstr(finite,80),'joint_increment':mp.nstr(joint,80),'within_separate_and_joint_increment_budgets':True})
        if case['sign']==1 and (case['n']==31 or case['multiplier_source']=='previous_noise_adapted'):
            print(json.dumps({'event':'independent_moment_replay','observation':obs,'radius':case['radius'],'source':case['multiplier_source']}),flush=True)
    assert midpoint_checks==sum(len(r['leaves']) for c in data['cases'] for r in c['root_bounds']) and fresh_leaves==2*midpoint_checks
    assert len(replays)==288
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [certificate_path,measurements,proposals,previous_proposals,truth_path]+inputs},
            'fresh_precision_bits':384,'fresh_partitions_per_active_root':96,'symbolic_moment_derivative_checks':3,'stored_midpoints_checked':midpoint_checks,
            'fresh_quadratic_interval_leaves':fresh_leaves,'exact_objective_bounds':2*len(replays),'objective_replays':replays,
            'independent_candidate_improvements':improvements,'independent_displaced_controls':displaced,
            'scope':'Complex quadratic interval covers independently check both finite and joint increments. Rational moment derivatives are symbolically checked; exact endpoint monotonicity above 3/2 gives moment enclosures and integer tail budgets. All producer exclusions and held-out coefficients are validated. FLINT remains shared for transcendental intervals; mpmath controls are independent samples, not completeness proofs.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['certificate','measurements','proposals','previous-proposals','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.certificate,a.measurements,a.proposals,a.previous_proposals,a.inputs,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'midpoints':r['stored_midpoints_checked'],'fresh_leaves':r['fresh_quadratic_interval_leaves'],'exact_bounds':r['exact_objective_bounds'],'improvements':len(r['independent_candidate_improvements'])}))
