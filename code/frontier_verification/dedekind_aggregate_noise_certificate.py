"""Certify nonlinear common-root errors for frozen and noise-adapted rational duals."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_coupled_dual import inequalities,bound
from dedekind_aggregate_shared import combine,derivative_range

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def H(t,a,terms):return (-a*t*t).exp()*sum((w*(u*t).cos() for w,u in terms),arb(0))

def certify(data,source,certificate,radius,bits):
    ctx.prec=bits;a=arb(1)/25;delta=F(radius);obs=certificate['observation_index'];roots=source['positive_root_intervals'];partitions=64 if bits==224 else 96
    lambdas,alpha,sigma,description=combine(data,certificate)
    terms=[(arb(str(v))*decode(row['scale']),arb(row['center']).log()) for row,v in zip(data['rows'],alpha) if v]
    rows=[{'weights':[decode(w) for w in row['weights']],'R':decode(row['observations'][obs]['unwidened']),'B':decode(row['prime_tail'])} for row in data['rows']]
    matrix,rhs=inequalities(rows);nominal=bound(matrix,rhs,certificate['column'],certificate['sign'],lambdas)
    wide=[arb(str(F(r['lo'])-delta)).union(arb(str(F(r['hi'])+delta))) for r in roots];assert all(t>0 and t<20 for t in wide)
    U=decode(data['constant_moment_upper'])-sum((3/(arb('9/4')+t*t) for t in wide),arb(0));assert U>0
    tail=sum((arb(str(v))*decode(row['scale'])*U*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh() for row,v in zip(data['rows'],sigma)),arb(0))
    global_bound=sum((arb(str(v))*decode(row['scale'])*((2*a/arb(1).exp()).sqrt()+arb(row['center']).log()) for row,v in zip(data['rows'],sigma)),arb(0)).upper()
    root_bounds=[];direct=derivative=arb(0)
    for index,root in enumerate(roots):
        original=arb(root['lo']).union(arb(root['hi']));base=H(original,a,terms);lo,hi=F(root['lo'])-delta,F(root['hi'])+delta
        leaves=[];upper=derivative_upper=arb(0)
        if delta and terms:
            for j in range(partitions):
                left=lo+(hi-lo)*F(j,partitions);right=lo+(hi-lo)*F(j+1,partitions);middle=(left+right)/2
                interval=arb(str(left)).union(arb(str(right)));value,_=derivative_range(interval,a,terms)
                offset=arb(0,arb(str((right-left)/2)))
                center_change=-2*(H(arb(str(middle)),a,terms)-base)
                change=center_change-2*value*offset
                leaves.append({'lo':str(left),'hi':str(right),'midpoint_change':encode(center_change),'derivative':encode(value),'change':encode(change)})
                upper=max(upper,change.upper());derivative_upper=max(derivative_upper,value.abs_upper())
            derivative_upper=min(global_bound,derivative_upper)
        direct+=upper;derivative+=2*arb(radius)*derivative_upper
        root_bounds.append({'root_index':index,'lo':str(lo),'hi':str(hi),'base_H':encode(base),'leaves':leaves,'direct_error_upper':encode(upper),'derivative_upper':encode(derivative_upper)})
    methods={}
    for name,error in [('direct_one_sided',direct),('symmetric_derivative',derivative)]:
        upper=decode(nominal['objective_upper_bound'])+tail+error
        candidates=[v for v in range(5) if not arb(certificate['sign']*v)>upper.upper()];assert candidates
        methods[name]={'input_error_upper':encode(error),'objective_upper_bound':encode(upper),'c7_candidates':candidates}
    return {'observation_index':obs,'radius':radius,'sign':certificate['sign'],'column':certificate['column'],'multipliers':certificate['multipliers'],
            'terms':description,'nominal_bound':nominal,'unknown_moment_upper':encode(U),'zero_tail':encode(tail),'root_bounds':root_bounds,'methods':methods}

def run(measurements,recovery,proposals,inputs,bits):
    d=json.loads(measurements.read_text());r=json.loads(recovery.read_text());p=json.loads(proposals.read_text());sources=[json.loads(x.read_text()) for x in inputs]
    assert p['status']=='proposed' and p['inputs_sha256']=={x.name:sha(x) for x in [measurements]+inputs}
    assert r['measurement_sha256']==sha(measurements)
    cases=[]
    for candidate in p['cases']:
        obs=candidate['observation_index'];target=next(t for t in r['results'][obs]['dual_targets'] if t['n']==7)
        frozen=next(x for x in target['certificates'] if x['sign']==candidate['sign'])
        for name,c in [('frozen',{**frozen,'column':target['column'],'observation_index':obs}),('noise_adapted',candidate)]:
            result=certify(d,sources[obs],c,candidate['radius'],bits);result['multiplier_source']=name;cases.append(result)
        if candidate['sign']==1:print(json.dumps({'event':'certified','observation':obs,'radius':candidate['radius'],'precision':bits}),flush=True)
    results=[]
    for obs in range(2):
        for radius in p['radii']:
            methods={}
            for name in ['frozen','noise_adapted']:
                selected=[c for c in cases if c['observation_index']==obs and c['radius']==radius and c['multiplier_source']==name];assert len(selected)==2
                for method in ['direct_one_sided','symmetric_derivative']:
                    methods[name+'_'+method]=sorted(set(selected[0]['methods'][method]['c7_candidates'])&set(selected[1]['methods'][method]['c7_candidates']))
            results.append({'observation_index':obs,'radius':radius,'methods':methods})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [measurements,recovery,proposals]+inputs},
            'precision_bits':bits,'partitions_per_active_root':64 if bits==224 else 96,'cases':cases,'results':results,
            'scope':'Exact rational multipliers are checked with nominal interval inequalities, all 604 residual boxes, inflated unconditional unknown-zero budgets and a complete interval cover of finite common-root changes. First-order midpoint Taylor enclosures cover nonlinear changes; derivative bounds are a separate ablation. One-sided root errors are capped below by zero. No sampled LP score is used as a certificate, and no local arithmetic relation is imposed.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','recovery','proposals','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);p.add_argument('--precision',type=int,choices=[224,320],required=True)
    a=p.parse_args();r=run(a.measurements,a.recovery,a.proposals,a.inputs,a.precision);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'results':r['results']}))
