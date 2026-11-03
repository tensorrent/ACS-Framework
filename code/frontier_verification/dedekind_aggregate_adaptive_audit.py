"""Check adaptive duals by complex quadratic covers and exact premise-by-premise replay."""
import argparse, copy, hashlib, json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_shared_audit import terms_for
from dedekind_aggregate_noise_audit import complex_values
from dedekind_aggregate_moment_audit import rational_moment,moment_interval,grid_value,number
from dedekind_aggregate_integer_audit import integer_rows,endpoint,GRID
from dedekind_aggregate_moment_local_audit import integer_dual,domain_bound,project,digest
from dedekind_aggregate_local_audit import catalog

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def audit_budget(m,source,case):
    ctx.prec=384; mp.mp.dps=85; a=arb(1)/25; delta=F(case['radius']); roots=source['positive_root_intervals']
    alpha,sigma,terms=terms_for(m,case); active=any(sigma)
    assert [t['alpha'] for t in case['terms']]==list(map(str,alpha)) and [t['sigma'] for t in case['terms']]==list(map(str,sigma))
    kappa=sum((arb(str(v))*decode(r['scale'])*404*(-16+a/4).exp()*(arb(r['center']).log()/2).cosh() for v,r in zip(sigma,m['rows'])),arb(0))
    assert kappa.overlaps(decode(case['kappa'])) and len(case['root_bounds'])==len(roots)
    U0=endpoint(m['constant_moment_upper'],True)-sum(grid_value(rational_moment(F(r['hi'])),False) for r in roots)
    Uwide=endpoint(m['constant_moment_upper'],True)-sum(grid_value(rational_moment(F(r['hi'])+delta),False) for r in roots)
    assert Uwide>=U0>0
    finite_total=joint_total=arb(0); midpoint_checks=fresh_leaves=0; stream=hashlib.sha256(); proofs=[]
    for index,(original,root) in enumerate(zip(roots,case['root_bounds'])):
        original_lo,original_hi=F(original['lo']),F(original['hi']); center=(original_lo+original_hi)/2; lo,hi=original_lo-delta,original_hi+delta
        assert F(3,2)<lo<=hi<20 and root['root_index']==index and F(root['lo'])==lo and F(root['hi'])==hi
        base_center,_,_=complex_values(arb(str(center)),a,terms); m_center=arb(str(rational_moment(center)))
        assert decode(root['base_H']).contains(base_center) and decode(root['base_moment']).contains(m_center)
        if delta and active:
            assert len(root['leaves'])==48; previous=lo
            for leaf in root['leaves']:
                left,right=F(leaf['lo']),F(leaf['hi']); assert left==previous and left<right; middle=(left+right)/2
                h,h1,_=complex_values(arb(str(middle)),a,terms); finite=-2*(h-base_center); joint=finite-kappa*(arb(str(rational_moment(middle)))-m_center)
                assert decode(leaf['finite_change']).contains(finite) and decode(leaf['joint_change']).contains(joint)
                assert decode(leaf['finite_derivative']).contains(-2*h1) and decode(leaf['joint_derivative']).contains(-2*h1-kappa*arb(str(rational_moment(middle,1))))
                previous=right; midpoint_checks+=1
            assert previous==hi
        else: assert root['leaves']==[]
        finite_upper=joint_upper=arb(0)
        if delta and active:
            base_H,_,_=complex_values(arb(str(original_lo)).union(arb(str(original_hi))),a,terms); base_m=moment_interval(original_lo,original_hi)
            for j in range(96):
                left=lo+(hi-lo)*F(j,96); right=lo+(hi-lo)*F(j+1,96); middle=(left+right)/2
                h,h1,_=complex_values(arb(str(middle)),a,terms); _,_,h2=complex_values(arb(str(left)).union(arb(str(right))),a,terms)
                half=arb(str((right-left)/2)); v=arb(0,half); square=arb(0).union(half*half)
                finite=-2*(h-base_H+h1*v+h2*square/2); second_moment=moment_interval(left,right,2)
                joint=(-2*(h-base_H)-kappa*(arb(str(rational_moment(middle)))-base_m)
                       +(-2*h1-kappa*arb(str(rational_moment(middle,1))))*v+(-2*h2-kappa*second_moment)*square/2)
                finite_upper=max(finite_upper,finite.upper()); joint_upper=max(joint_upper,joint.upper()); fresh_leaves+=1
                stream.update(canonical({'lo':str(left),'hi':str(right),'finite':encode(finite),'joint':encode(joint),'moment_second_derivative':encode(second_moment)})+b'\n')
        finite_total+=finite_upper; joint_total+=joint_upper
        proofs.append({'root_index':index,'finite_increment_upper':encode(finite_upper),'joint_increment_upper':encode(joint_upper)})
    kupper=endpoint(encode(kappa),True); separate=kupper*Uwide+endpoint(encode(finite_total),True)*GRID; joint=kupper*U0+endpoint(encode(joint_total),True)*GRID
    displaced=[]
    if active:
        centers=[(number(r['lo'])+number(r['hi']))/2 for r in roots]; dd=number(case['radius']); aa=mp.mpf(1)/25; mt=[]; mk=mp.mpf(0)
        for av,sv,row in zip(alpha,sigma,m['rows']):
            prime=next(c['prime'] for c in m['columns'] if c['n']==row['center']); scale=2*mp.sqrt(mp.pi*aa)*mp.sqrt(row['center'])/mp.log(prime); u=mp.log(row['center'])
            if av: mt.append((number(str(av))*scale,u))
            if sv: mk+=number(str(sv))*scale*404*mp.exp(-16+aa/4)*mp.cosh(u/2)
        def h(t): return mp.exp(-aa*t*t)*mp.fsum(w*mp.cos(u*t) for w,u in mt)
        def mm(t): return 3/(mp.mpf('2.25')+t*t)
        def jj(t): return -2*h(t)-mk*mm(t)
        directions=[1 if mp.diff(jj,t)>=0 else -1 for t in centers]; old_h=mp.fsum(h(t) for t in centers); old_m=mp.fsum(mm(t) for t in centers)
        for pattern in ['uniform_positive','uniform_negative','joint_gradient_positive','joint_gradient_negative']:
            direction=1 if pattern.endswith('positive') else -1; values=[t+direction*dd*(s if pattern.startswith('joint_gradient') else 1) for t,s in zip(centers,directions)]
            finite=-2*(mp.fsum(h(t) for t in values)-old_h); increment=finite-mk*(mp.fsum(mm(t) for t in values)-old_m)
            assert arb(mp.nstr(finite,80))<=finite_total.upper()+arb('1e-70') and arb(mp.nstr(increment,80))<=joint_total.upper()+arb('1e-70')
            displaced.append({'pattern':pattern,'finite_change':mp.nstr(finite,80),'joint_increment':mp.nstr(increment,80)})
    return {'certificate_sha256':hashlib.sha256(canonical(case)).hexdigest(),'stored_midpoints_checked':midpoint_checks,'fresh_quadratic_interval_leaves':fresh_leaves,
            'fresh_interval_stream_sha256':stream.hexdigest(),'root_bounds':proofs,'kappa_upper':str(F(kupper,GRID)),'baseline_unknown_moment_upper':str(F(U0,GRID)),
            'widened_unknown_moment_upper':str(F(Uwide,GRID)),'separate_budget_upper':str(F(separate,GRID*GRID)),
            'uncapped_joint_budget_upper':str(F(joint,GRID*GRID)),'budget_upper':str(F(min(separate,joint),GRID*GRID)),'independent_displaced_controls':displaced}

def replay(data,m,prior,budgets,truth):
    assert canonical(data['catalog'])==canonical(catalog()) and data['columns']==m['columns']==prior['columns']
    columns=m['columns']; altered=copy.deepcopy(m)
    for r in altered['rows']:
        for obs in [0,1]: r['observations'][obs]['R']=r['observations'][obs]['unwidened']
    rows=[integer_rows(altered,obs) for obs in [0,1]]; replays=[]; used=[]
    assert len(data['cases'])==16 and len(budgets)==len(data['certificates'])
    keys=[(obs,radius,profile) for obs in [0,1] for radius in ['0','1/200','1/50','1/10'] for profile in ['degree_only','degree_discriminant']]
    assert [(c['observation_index'],c['radius'],c['profile']) for c in data['cases']]==keys
    for case_index,case in enumerate(data['cases']):
        obs=case['observation_index']; seed=prior['cases'][case['prior_case_index']]
        assert seed['method']=='coupled' and all(seed[k]==case[k] for k in ['observation_index','radius','profile'])
        domains=copy.deepcopy(seed['final_domains']); assert domains==case['input_domains']; exact_proofs=[]; local_count=0; dual_count=0; extra=[]
        for iteration,step in enumerate(case['rounds'],1):
            assert step['iteration']==iteration and step['before_domains_sha256']==digest(domains)
            after_local,retained,removed=project(columns,domains,case['profile']); local_count+=len(removed)
            assert retained==step['local_models'] and removed==step['local_removals'] and digest(after_local)==step['after_local_sha256']
            expected=[(i,sign) for i,c in enumerate(columns) if c['n']<=31 and len(after_local[i])>1 for sign in [-1,1]]
            assert [(p['column'],p['sign']) for p in step['proposals']]==expected
            by_index={}; eligible=set()
            for p in step['proposals']:
                index=p['certificate_index']; used.append(index); cert=data['certificates'][index]; budget=budgets[index]
                assert p['case_index']==case_index and p['iteration']==iteration and p['premise_domains_sha256']==digest(after_local)
                assert all(p[k]==case[k] for k in ['observation_index','radius','profile'])
                assert all(p[k]==cert[k] for k in ['observation_index','radius','column','n','sign','multipliers'])
                assert cert['n']==columns[cert['column']]['n'] and budget['certificate_sha256']==hashlib.sha256(canonical(cert)).hexdigest()
                upper=domain_bound(integer_dual(rows[obs],cert,len(columns)),after_local,budget['budget_upper'])
                allowed=[v for v in after_local[cert['column']] if cert['sign']*v<=upper]; assert allowed and truth[['A','B'][obs]][cert['column']] in allowed
                by_index[index]=(cert,upper)
                for value in after_local[cert['column']]:
                    if cert['sign']*value>upper: eligible.add((cert['column'],value))
            domains=copy.deepcopy(after_local); seen=set()
            for witness in step['dual_removals']:
                index=witness['certificate_index']; cert,upper=by_index[index]; i=witness['column']; value=witness['candidate']
                assert all(witness[k]==cert[k] for k in ['column','n','sign']) and value in after_local[i] and (i,value) not in seen; seen.add((i,value))
                gap=cert['sign']*value-upper; assert gap>0 and value!=truth[['A','B'][obs]][i]
                domains[i].remove(value); exact_proofs.append({'iteration':iteration,'certificate_index':index,'column':i,'candidate':value,'objective_upper':str(upper),'strict_gap':str(gap)})
            extra.extend({'iteration':iteration,'column':i,'candidate':v} for i,v in sorted(eligible-seen))
            assert all(domains) and digest(domains)==step['after_domains_sha256'] and all(v in d for v,d in zip(truth[['A','B'][obs]],domains)); dual_count+=len(seen)
        assert domains==case['final_domains'] and not case['rounds'][-1]['local_removals'] and not case['rounds'][-1]['dual_removals']
        unique=lambda ds:sum(len(d)==1 for c,d in zip(columns,ds) if c['n']<=31)
        assert unique(domains)==case['adaptive_unique_targets'] and unique(case['input_domains'])==case['initial_unique_targets'] and sum(len(d)==1 for d in domains)==case['adaptive_unique_support']
        replays.append({**{k:case[k] for k in ['observation_index','radius','profile','initial_unique_targets','adaptive_unique_targets','adaptive_unique_support']},
                        'iterations':len(case['rounds']),'local_removals':local_count,'dual_removals':dual_count,'exact_dual_proofs':exact_proofs,
                        'additional_audit_exclusions_not_propagated':extra,'all_604_true_coefficients_retained_each_round':True})
    assert used==list(range(len(data['certificates'])))
    return replays

def run(adaptive_path,measurements,inputs,prior_feedback,prior_audit,truth_path):
    data=json.loads(adaptive_path.read_text()); m=json.loads(measurements.read_text()); sources=[json.loads(p.read_text()) for p in inputs]; prior=json.loads(prior_feedback.read_text())
    prior_check=json.loads(prior_audit.read_text()); truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    assert data['status']==prior_check['status']=='passed' and data['inputs_sha256']=={p.name:sha(p) for p in [measurements,prior_feedback,prior_audit]+inputs}
    assert prior_check['inputs_sha256'][prior_feedback.name]==sha(prior_feedback)
    budgets=[]
    for index,c in enumerate(data['certificates']):
        budgets.append(audit_budget(m,sources[c['observation_index']],c))
        if (index+1)%20==0: print(json.dumps({'event':'adaptive_complex_audit','certificates':index+1}),flush=True)
    replays=replay(data,m,prior,budgets,truth)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [adaptive_path,measurements,prior_feedback,prior_audit,truth_path]+inputs},
            'fresh_precision_bits':384,'fresh_partitions_per_active_root':96,'budget_replays':budgets,'domain_replays':replays,
            'stored_midpoints_checked':sum(b['stored_midpoints_checked'] for b in budgets),'fresh_quadratic_interval_leaves':sum(b['fresh_quadratic_interval_leaves'] for b in budgets),
            'independent_displaced_control_count':sum(len(b['independent_displaced_controls']) for b in budgets),
            'exact_domain_objectives':len(budgets),'local_removals':sum(r['local_removals'] for r in replays),'dual_removals':sum(r['dual_removals'] for r in replays),
            'scope':'Fresh complex quadratic covers and rational monotone moment bounds audit every changed multiplier. Integer coefficients and Fraction support calculations independently replay every exclusion from its exact previous domains. The local catalogue is independently enumerated. Truth is checked only downstream. Transcendental interval routes share FLINT; mpmath checks are samples. No optimality or surviving-field claim.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['adaptive','measurements','prior-feedback','prior-audit','truth','output']: p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True); a=p.parse_args(); r=run(a.adaptive,a.measurements,a.inputs,a.prior_feedback,a.prior_audit,a.truth)
    a.output.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps({k:r[k] for k in ['status','stored_midpoints_checked','fresh_quadratic_interval_leaves','exact_domain_objectives','local_removals','dual_removals']}))
