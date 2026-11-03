"""Complex quadratic interval covers, integer objectives and off-grid counterexamples."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import mpmath as mp
from flint import arb,acb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_shared_audit import terms_for
from dedekind_aggregate_integer_audit import integer_rows,objective_bound,endpoint,DUAL_GRID

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def number(x):
    q=F(x);return mp.mpf(q.numerator)/q.denominator
def complex_values(t,a,terms):
    z=acb(t);h=h1=h2=acb(0)
    for w,u in terms:
        e=(acb(0,u)*z).exp();q=-2*a*z+acb(0,u)
        h+=w*e;h1+=w*q*e;h2+=w*(q*q-2*a)*e
    g=(-a*t*t).exp()
    return g*h.real,g*h1.real,g*h2.real

def run(certificates,measurements,recovery,proposals,inputs,truth_path):
    ds=[json.loads(p.read_text()) for p in certificates];m=json.loads(measurements.read_text());recovered=json.loads(recovery.read_text());proposed=json.loads(proposals.read_text())
    source=[json.loads(p.read_text()) for p in inputs];truth=json.loads(truth_path.read_text())['arithmetic_vectors'];ctx.prec=384;mp.mp.dps=85;a=arb(1)/25
    precision_differences=[]
    for x,y in zip(ds[0]['results'],ds[1]['results']):
        assert x['observation_index']==y['observation_index'] and x['radius']==y['radius']
        for name in x['methods']:
            if name.endswith('direct_one_sided'):assert x['methods'][name]==y['methods'][name]
            if x['methods'][name]!=y['methods'][name]:precision_differences.append({'observation_index':x['observation_index'],'radius':x['radius'],'method':name,'coarse_candidates':x['methods'][name],'finer_candidates':y['methods'][name]})
    midpoint_checks=0
    for d in ds:
        for case in d['cases']:
            obs=case['observation_index'];delta=F(case['radius']);alpha,sigma,terms=terms_for(m,case);roots=source[obs]['positive_root_intervals']
            assert len(case['root_bounds'])==len(roots)
            expected=next(c for c in proposed['cases'] if all(c[k]==case[k] for k in ['observation_index','radius','sign'])) if case['multiplier_source']=='noise_adapted' else next(c for t in recovered['results'][obs]['dual_targets'] if t['n']==7 for c in t['certificates'] if c['sign']==case['sign'])
            assert case['multipliers']==expected['multipliers']
            assert [x['alpha'] for x in case['terms']]==list(map(str,alpha)) and [x['sigma'] for x in case['terms']]==list(map(str,sigma))
            for index,(original,root) in enumerate(zip(roots,case['root_bounds'])):
                lo,hi=F(original['lo'])-delta,F(original['hi'])+delta
                assert root['root_index']==index and F(root['lo'])==lo and F(root['hi'])==hi
                base,_,_=complex_values(arb(str((F(original['lo'])+F(original['hi']))/2)),a,terms)
                assert decode(root['base_H']).contains(base)
                if not delta or not terms:assert root['leaves']==[];continue
                assert len(root['leaves'])==d['partitions_per_active_root'];previous=lo
                for leaf in root['leaves']:
                    left,right=F(leaf['lo']),F(leaf['hi']);assert left==previous and left<right
                    h,h1,_=complex_values(arb(str((left+right)/2)),a,terms);change=-2*(h-base)
                    assert decode(leaf['midpoint_change']).contains(change) and decode(leaf['derivative']).contains(h1)
                    assert decode(leaf['change']).contains(change)
                    previous=right;midpoint_checks+=1
                assert previous==hi
    assert midpoint_checks==158400
    replays=[];fresh_leaves=0;displaced=[];grid_controls=[]
    for case in ds[1]['cases']:
        obs=case['observation_index'];radius=case['radius'];delta=F(radius);alpha,sigma,terms=terms_for(m,case);roots=source[obs]['positive_root_intervals']
        altered=copy.deepcopy(m)
        for row in altered['rows']:row['observations'][obs]['R']=row['observations'][obs]['unwidened']
        certificate={'sign':case['sign'],'multipliers':case['multipliers']}
        nominal,unit=objective_bound(integer_rows(altered,obs),case['column'],certificate,len(m['columns']))
        wide=[arb(str(F(x['lo'])-delta)).union(arb(str(F(x['hi'])+delta))) for x in roots];assert all(x>0 and x<20 for x in wide)
        U=decode(m['constant_moment_upper'])-sum((3/(arb('9/4')+x*x) for x in wide),arb(0));assert U>0
        tail=sum((arb(str(v))*decode(row['scale'])*U*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh() for row,v in zip(m['rows'],sigma)),arb(0))
        global_bound=sum((arb(str(v))*decode(row['scale'])*((2*a/arb(1).exp()).sqrt()+arb(row['center']).log()) for row,v in zip(m['rows'],sigma)),arb(0)).upper()
        direct=derivative=arb(0);root_replays=[];stream=hashlib.sha256()
        if delta and terms:
            for index,root in enumerate(roots):
                base,_,_=complex_values(arb(root['lo']).union(arb(root['hi'])),a,terms)
                lo,hi=F(root['lo'])-delta,F(root['hi'])+delta;upper=first=arb(0)
                for j in range(128):
                    left=lo+(hi-lo)*F(j,128);right=lo+(hi-lo)*F(j+1,128);middle=(left+right)/2;half=arb(str((right-left)/2))
                    h,h1,_=complex_values(arb(str(middle)),a,terms)
                    _,deriv,second=complex_values(arb(str(left)).union(arb(str(right))),a,terms)
                    offset=arb(0,half);square=arb(0).union(half*half)
                    change=-2*(h-base+h1*offset+second*square/2)
                    upper=max(upper,change.upper());first=max(first,deriv.abs_upper());fresh_leaves+=1
                    stream.update(canonical({'lo':str(left),'hi':str(right),'quadratic_change':encode(change),'first_derivative':encode(deriv),'second_derivative':encode(second)})+b'\n')
                first=min(first,global_bound);direct+=upper;derivative+=2*arb(radius)*first
                root_replays.append({'root_index':index,'direct_error_upper':encode(upper),'derivative_upper':encode(first)})
        methods={}
        for name,error in [('direct_one_sided',direct),('symmetric_derivative',derivative)]:
            numerator=nominal+endpoint(encode(tail+error),True)*DUAL_GRID
            candidates=[v for v in range(5) if case['sign']*v*unit<=numerator]
            assert set(candidates)<=set(case['methods'][name]['c7_candidates']),('independent cover did not confirm all recorded exclusions',obs,radius,case['multiplier_source'],name,candidates,case['methods'][name]['c7_candidates'])
            assert truth[['A','B'][obs]][case['column']] in candidates
            methods[name]={'objective_upper':str(F(numerator,unit)),'input_error_upper':encode(error),'c7_candidates':candidates}
        replays.append({'observation_index':obs,'radius':radius,'sign':case['sign'],'multiplier_source':case['multiplier_source'],
                        'nominal_objective_upper':str(F(nominal,unit)),'zero_tail':encode(tail),'root_bounds':root_replays,'fresh_interval_stream_sha256':stream.hexdigest(),'methods':methods})
        if terms:
            centers=[(number(x['lo'])+number(x['hi']))/2 for x in roots];dd=number(radius);aa=mp.mpf(1)/25;mt=[]
            for v,row in zip(alpha,m['rows']):
                if v:
                    prime=next(c['prime'] for c in m['columns'] if c['n']==row['center'])
                    mt.append((number(str(v))*2*mp.sqrt(mp.pi*aa)*mp.sqrt(row['center'])/mp.log(prime),mp.log(row['center'])))
            def h(t):return mp.exp(-aa*t*t)*mp.fsum(w*mp.cos(u*t) for w,u in mt)
            directions=[1 if mp.diff(h,t)>=0 else -1 for t in centers];baseline=mp.fsum(h(t) for t in centers)
            for pattern in ['uniform_positive','uniform_negative','gradient_positive','gradient_negative']:
                sign=1 if pattern.endswith('positive') else -1
                values=[t+sign*dd*(direction if pattern.startswith('gradient') else 1) for t,direction in zip(centers,directions)]
                change=-2*(mp.fsum(h(t) for t in values)-baseline);numeric=arb(mp.nstr(change,80))
                assert numeric<=direct.upper()+arb('1e-70') and numeric.abs_upper()<=derivative.upper()+arb('1e-70')
                displaced.append({'observation_index':obs,'radius':radius,'multiplier_source':case['multiplier_source'],'pattern':pattern,'combined_change':mp.nstr(change,80),'within_direct_and_derivative_budgets':True})
            if delta and case['multiplier_source']=='noise_adapted' and not any(x['observation_index']==obs for x in grid_controls):
                fm=np.array([float(t) for t in centers]);fu=np.array([float(u) for w,u in mt]);fw=np.array([float(w) for w,u in mt])
                positions=fm[:,None]+np.linspace(-float(delta),float(delta),1025)[None,:]
                hv=np.exp(-.04*positions**2)*np.sum(fw[None,None,:]*np.cos(positions[:,:,None]*fu),axis=-1)
                errors=-2*(hv-np.exp(-.04*fm[:,None]**2)*np.sum(fw[None,None,:]*np.cos(fm[:,None,None]*fu),axis=-1))
                maxima=errors.max(axis=1);sampled=errors[:,::32].max(axis=1);root_index=int(np.argmax(maxima-sampled));site=int(np.argmax(errors[root_index]))
                if site%32 and maxima[root_index]-sampled[root_index]>1e-12:
                    root=roots[root_index];center=(F(root['lo'])+F(root['hi']))/2;base,_,_=complex_values(arb(str(center)),a,terms)
                    grid=[]
                    for k in range(33):
                        value,_,_=complex_values(arb(str(center-delta+2*delta*F(k,32))),a,terms);grid.append(-2*(value-base))
                    offset=-delta+2*delta*F(site,1024);value,_,_=complex_values(arb(str(center+offset)),a,terms);off_grid=-2*(value-base)
                    gap=off_grid-max(v.upper() for v in grid);assert gap>0
                    grid_controls.append({'observation_index':obs,'radius':radius,'root_index':root_index,'offset':str(offset),
                        'sampled_error_intervals':[encode(x) for x in grid],'off_grid_error_interval':encode(off_grid),'strict_gap':encode(gap),
                        'scope':'A float search locates this point; fresh complex interval evaluation proves that its error exceeds every one of the 33 proposal-grid values. The sampled maximum alone is therefore not a continuous-error certificate.'})
        if case['sign']==1 and case['multiplier_source']=='noise_adapted':print(json.dumps({'event':'independent_noise_replay','observation':obs,'radius':radius}),flush=True)
    assert fresh_leaves==126720 and len(displaced)==192 and len(grid_controls)==2
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in certificates+[measurements,recovery,proposals,truth_path]+inputs},
            'fresh_precision_bits':384,'fresh_partitions_per_active_root':128,'stored_midpoints_checked':midpoint_checks,'fresh_quadratic_interval_leaves':fresh_leaves,
            'exact_objective_bounds':2*len(replays),'precision_subdivision_differences':precision_differences,'objective_replays':replays,
            'independent_displaced_controls':displaced,'certified_off_grid_counterexamples':grid_controls,
            'scope':'Different complex-exponential first/second derivatives and quadratic Taylor covers confirm every recorded exclusion using exact integer nominal objectives and full tails. The two interval routes share FLINT. Mpmath displaced sums are independent samples. Certified off-grid points disprove using sampled proposal maxima as continuum bounds. Arithmetic is read only to validate the retained coefficient.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificates',type=Path,nargs=2,required=True)
    for n in ['measurements','recovery','proposals','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.certificates,a.measurements,a.recovery,a.proposals,a.inputs,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'stored_midpoints':r['stored_midpoints_checked'],'fresh_leaves':r['fresh_quadratic_interval_leaves'],'exact_bounds':r['exact_objective_bounds'],'off_grid_controls':len(r['certified_off_grid_counterexamples'])}))
