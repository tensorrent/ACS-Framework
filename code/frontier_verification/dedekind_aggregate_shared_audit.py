"""Complex-exponential derivative ranges and exact replay of combined duals."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from flint import arb,acb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_integer_audit import integer_rows,objective_bound,endpoint,GRID,DUAL_GRID

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def number(s):
    q=F(s);return mp.mpf(q.numerator)/q.denominator


def complex_derivative(t,a,terms):
    z=acb(t);total=acb(0);triangle=arb(0)
    for w,u in terms:
        value=(-2*a*z+acb(0,u))*(acb(0,u)*z).exp()
        total+=w*value;triangle+=w.abs_upper()*value.real.abs_upper()
    gaussian=(-a*t*t).exp()
    return gaussian*total.real,(gaussian.abs_upper()*triangle).upper()


def terms_for(data,case):
    lam=[F(0)]*(2*len(data['rows']))
    for j,v in case['multipliers']:lam[j]=F(v)
    alpha=[lam[2*j]-lam[2*j+1] for j in range(len(data['rows']))]
    sigma=[lam[2*j]+lam[2*j+1] for j in range(len(data['rows']))]
    terms=[(arb(str(v))*decode(r['scale']),arb(r['center']).log()) for v,r in zip(alpha,data['rows']) if v]
    return alpha,sigma,terms


def run(shared_paths,measurements,recovery,inputs,baseline_radius):
    ds=[json.loads(p.read_text()) for p in shared_paths];m=json.loads(measurements.read_text());r=json.loads(recovery.read_text())
    source=[json.loads(p.read_text()) for p in inputs];ctx.prec=384;mp.mp.dps=85;a=arb(1)/25;T=20
    assert ds[0]['results']==ds[1]['results'];midpoints=0
    for d in ds:
        for case in d['cases']:
            obs=case['observation_index'];delta=F(case['radius']);alpha,sigma,terms=terms_for(m,case)
            assert [x['alpha'] for x in case['terms']]==list(map(str,alpha))
            assert [x['sigma'] for x in case['terms']]==list(map(str,sigma))
            for original,root in zip(source[obs]['positive_root_intervals'],case['root_bounds']):
                lo,hi=F(original['lo'])-delta,F(original['hi'])+delta
                assert F(root['lo'])==lo and F(root['hi'])==hi
                if not terms or not delta:
                    assert root['leaves']==[];continue
                assert len(root['leaves'])==d['partitions_per_root'];previous=lo
                for leaf in root['leaves']:
                    left,right=F(leaf['lo']),F(leaf['hi']);assert left==previous and left<right
                    value,_=complex_derivative(arb(str((left+right)/2)),a,terms)
                    assert decode(leaf['combined_derivative']).contains(value)
                    previous=right;midpoints+=1
                assert previous==hi
    assert midpoints==39600
    replays=[];fresh_leaves=0;displaced=[];independence_controls=[]
    for case in ds[1]['cases']:
        obs=case['observation_index'];radius=case['radius'];delta=F(radius);alpha,sigma,terms=terms_for(m,case)
        altered=copy.deepcopy(m)
        for row in altered['rows']:row['observations'][obs]['R']=row['observations'][obs]['unwidened']
        ir=integer_rows(altered,obs);certificate={'sign':case['sign'],'multipliers':case['multipliers']}
        base,unit=objective_bound(ir,case['column'],certificate,len(m['columns']))
        roots=source[obs]['positive_root_intervals'];enlarged=[arb(str(F(x['lo'])-delta)).union(arb(str(F(x['hi'])+delta))) for x in roots]
        assert all(x>0 and x<T for x in enlarged)
        U=decode(m['constant_moment_upper'])-sum((3/(arb('9/4')+x*x) for x in enlarged),arb(0));assert U>0
        tail=sum((arb(str(v))*decode(row['scale'])*U*(4+T*T)*(-a*T*T+a/4).exp()*(arb(row['center']).log()/2).cosh() for v,row in zip(sigma,m['rows'])),arb(0))
        global_bound=sum((arb(str(v))*decode(row['scale'])*((2*a/arb(1).exp()).sqrt()+arb(row['center']).log()) for v,row in zip(sigma,m['rows'])),arb(0)).upper()
        local_sum=shared_sum=arb(0);root_values=[];stream=hashlib.sha256()
        if terms and delta:
            for index,x in enumerate(roots):
                lo,hi=F(x['lo'])-delta,F(x['hi'])+delta;local=combined=arb(0)
                for j in range(96):
                    left=lo+(hi-lo)*F(j,96);right=lo+(hi-lo)*F(j+1,96)
                    value,triangle=complex_derivative(arb(str(left)).union(arb(str(right))),a,terms)
                    local=max(local,triangle);combined=max(combined,value.abs_upper());fresh_leaves+=1
                    stream.update(canonical({'lo':str(left),'hi':str(right),'derivative':encode(value),'triangle':encode(triangle)})+b'\n')
                local=min(local,global_bound);combined=min(combined,local)
                local_sum+=local;shared_sum+=combined
                root_values.append({'root_index':index,'local_upper':encode(local),'combined_upper':encode(combined)})
        errors={'global_rows':2*arb(radius)*len(roots)*global_bound,'local_rows':2*arb(radius)*local_sum,'shared_roots':2*arb(radius)*shared_sum}
        proofs={}
        for name,error in errors.items():
            extra=endpoint(encode(tail+error),True)*DUAL_GRID
            numerator=base+extra;candidates=[v for v in range(5) if case['sign']*v*unit<=numerator]
            assert candidates==case['methods'][name]['c7_candidates'],(obs,case['sign'],radius,name,candidates,case['methods'][name]['c7_candidates'])
            proofs[name]={'objective_upper':str(F(numerator,unit)),'c7_candidates':candidates,'input_error':encode(error)}
        replays.append({'observation_index':obs,'sign':case['sign'],'radius':radius,'base_objective_upper':str(F(base,unit)),
                        'zero_tail':encode(tail),'root_bounds':root_values,'fresh_evaluations_sha256':stream.hexdigest(),'proofs':proofs})
        if terms:
            centers=[(number(x['lo'])+number(x['hi']))/2 for x in roots];dd=number(radius);aa=mp.mpf(1)/25
            mt=[]
            for value,row in zip(alpha,m['rows']):
                if not value:continue
                prime=next(c['prime'] for c in m['columns'] if c['n']==row['center'])
                scale=2*mp.sqrt(mp.pi*aa)*mp.sqrt(row['center'])/mp.log(prime)
                mt.append((number(str(value))*scale,mp.log(row['center'])))
            def H(t):return mp.exp(-aa*t*t)*mp.fsum(w*mp.cos(u*t) for w,u in mt)
            signs=[1 if mp.diff(H,t)>=0 else -1 for t in centers];original=mp.fsum(H(t) for t in centers)
            for pattern in ['uniform_positive','uniform_negative','gradient_positive','gradient_negative']:
                direction=1 if pattern.endswith('positive') else -1
                shift=[direction*dd*(s if pattern.startswith('gradient') else 1) for s in signs]
                changed=-2*(mp.fsum(H(t+v) for t,v in zip(centers,shift))-original)
                assert arb(mp.nstr(abs(changed),80))<=errors['shared_roots'].upper()+arb('1e-70')
                displaced.append({'observation_index':obs,'radius':radius,'pattern':pattern,'combined_change':mp.nstr(changed,80),'within_shared_budget':True})
            if delta and not any(x['observation_index']==obs for x in independence_controls):
                independent_change=mp.mpf(0)
                for w,u in mt:
                    def h(t):return mp.exp(-aa*t*t)*mp.cos(u*t)
                    for t in centers:
                        direction=-1 if w*mp.diff(h,t)>0 else 1
                        independent_change-=2*w*(h(t+direction*dd)-h(t))
                if arb(mp.nstr(abs(independent_change),80))>errors['shared_roots'].upper():
                    independence_controls.append({'observation_index':obs,'radius':radius,'independent_row_displacement_change':mp.nstr(independent_change,80),
                        'shared_error_bound':encode(errors['shared_roots']),'violates_shared_bound':True,
                        'scope':'Different errors assigned to the same root in different rows violate the required common-input model. This is a control on that premise, not an alternate physical spectrum.'})
    assert fresh_leaves==47520 and len(displaced)==96 and len(independence_controls)==2
    baseline=json.loads(baseline_radius.read_text());comparisons=0
    for row in baseline['results']:
        selected=[x for x in ds[1]['results'] if x['observation_index']==row['observation_index'] and x['radius']==row['radius']]
        if selected:assert selected[0]['methods']['global_rows']==row['c7_candidates'];comparisons+=1
    assert comparisons==8
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in shared_paths+[measurements,recovery,baseline_radius]+inputs},
            'fresh_precision_bits':384,'fresh_partitions_per_root':96,'stored_leaf_midpoints_checked':midpoints,'fresh_complex_interval_leaves':fresh_leaves,
            'exact_objective_bounds':len(replays)*3,'objective_replays':replays,'independent_displaced_controls':displaced,
            'common_error_premise_controls':independence_controls,'baseline_radius_comparisons':comparisons,
            'scope':'Complex-exponential derivative evaluation checks every stored nonempty leaf midpoint, then independently covers all enlarged root intervals with a different partition and precision. Exact integer nominal duals and outward-added budgets reproduce every candidate bound. Both interval routes share FLINT. Mpmath displaced sums and deliberately independent row errors challenge the common-displacement premise.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--shared',type=Path,nargs=2,required=True)
    for n in ['measurements','recovery','baseline-radius','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.shared,a.measurements,a.recovery,a.inputs,a.baseline_radius)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'midpoints':r['stored_leaf_midpoints_checked'],'fresh_leaves':r['fresh_complex_interval_leaves'],'exact_bounds':r['exact_objective_bounds'],'displaced_controls':len(r['independent_displaced_controls'])}))
