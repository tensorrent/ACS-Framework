"""Bound each shared-root error after combining a frozen Gaussian dual."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_coupled_dual import inequalities,bound

RADII=['0','1/100000','1/10000','1/1000','1/500','1/200','1/100','1/50','3/100','1/20','1/10','1/5']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def combine(data,certificate):
    count=len(data['rows']);lambdas=[F(0)]*(2*count)
    for index,value in certificate['multipliers']:
        assert type(index) is int and 0<=index<2*count and lambdas[index]==0 and F(value)>=0
        lambdas[index]=F(value)
    alpha=[lambdas[2*j]-lambdas[2*j+1] for j in range(count)]
    sigma=[lambdas[2*j]+lambdas[2*j+1] for j in range(count)]
    terms=[{'center':row['center'],'alpha':str(a),'sigma':str(s),'scale':row['scale']} for row,a,s in zip(data['rows'],alpha,sigma)]
    return lambdas,alpha,sigma,terms


def derivative_range(t,a,terms):
    inside=arb(0);triangle=arb(0)
    for w,u in terms:
        trig=-2*a*t*(u*t).cos()-u*(u*t).sin()
        inside+=w*trig;triangle+=w.abs_upper()*trig.abs_upper()
    gaussian=(-a*t*t).exp()
    return gaussian*inside,(gaussian.abs_upper()*triangle).upper()


def run(measurements,recovery,inputs,bits):
    ctx.prec=bits;data=json.loads(measurements.read_text());decoded=json.loads(recovery.read_text());source=[json.loads(p.read_text()) for p in inputs]
    assert data['status']=='passed' and all(r['denominator']==25 for r in data['rows'])
    a=arb(1)/25;T=data['global_inputs']['top'];C=decode(data['constant_moment_upper']);cases=[]
    partitions=32 if bits==224 else 48
    for observation,d in enumerate(source):
        assert data['input_sha256'][observation]==sha(inputs[observation])
        roots=d['positive_root_intervals'];target=next(t for t in decoded['results'][observation]['dual_targets'] if t['n']==7)
        nominal_rows=[{'weights':[decode(w) for w in row['weights']],'R':decode(row['observations'][observation]['unwidened']),'B':decode(row['prime_tail'])} for row in data['rows']]
        matrix,rhs=inequalities(nominal_rows)
        for certificate in target['certificates']:
            lambdas,alpha,sigma,description=combine(data,certificate)
            nominal=bound(matrix,rhs,target['column'],certificate['sign'],lambdas)
            terms=[(arb(str(v))*decode(row['scale']),arb(row['center']).log()) for row,v in zip(data['rows'],alpha) if v]
            global_per_root=sum((arb(str(v))*decode(row['scale'])*((2*a/arb(1).exp()).sqrt()+arb(row['center']).log()) for row,v in zip(data['rows'],sigma)),arb(0)).upper()
            for radius in RADII:
                delta=F(radius);enlarged=[arb(str(F(r['lo'])-delta)).union(arb(str(F(r['hi'])+delta))) for r in roots]
                assert all(t>0 and t<T for t in enlarged)
                known=sum((3/(arb('9/4')+t*t) for t in enlarged),arb(0));U=C-known;assert U>0
                phi=(4+T*T)*(-a*T*T).exp();assert a*(4+T*T)>=1
                tails=[arb(str(v))*decode(row['scale'])*U*phi*(a/4).exp()*(arb(row['center']).log()/2).cosh() for row,v in zip(data['rows'],sigma)]
                zero_tail=sum(tails,arb(0));root_bounds=[]
                for index,r in enumerate(roots):
                    lo,hi=F(r['lo'])-delta,F(r['hi'])+delta;leaves=[]
                    if terms and delta:
                        for j in range(partitions):
                            left=lo+(hi-lo)*F(j,partitions);right=lo+(hi-lo)*F(j+1,partitions)
                            t=arb(str(left)).union(arb(str(right)));value,triangle=derivative_range(t,a,terms)
                            leaves.append({'lo':str(left),'hi':str(right),'combined_derivative':encode(value),'triangle_upper':encode(triangle)})
                        triangle=min(global_per_root,max(decode(r['triangle_upper']) for r in leaves))
                        shared=min(triangle,max(decode(r['combined_derivative']).abs_upper() for r in leaves))
                    else:triangle=shared=arb(0)
                    root_bounds.append({'root_index':index,'lo':str(lo),'hi':str(hi),'leaves':leaves,
                                        'triangle_upper':encode(triangle),'shared_upper':encode(shared)})
                global_error=2*arb(radius)*len(roots)*global_per_root
                local_error=2*arb(radius)*sum((decode(r['triangle_upper']) for r in root_bounds),arb(0))
                shared_error=2*arb(radius)*sum((decode(r['shared_upper']) for r in root_bounds),arb(0))
                methods={}
                for name,error in [('global_rows',global_error),('local_rows',local_error),('shared_roots',shared_error)]:
                    upper=decode(nominal['objective_upper_bound'])+zero_tail+error
                    candidates=[c for c in range(5) if not arb(certificate['sign']*c)>upper.upper()]
                    assert candidates
                    methods[name]={'input_error':encode(error),'objective_upper_bound':encode(upper),'c7_candidates':candidates}
                assert set(methods['shared_roots']['c7_candidates'])<=set(methods['local_rows']['c7_candidates'])<=set(methods['global_rows']['c7_candidates'])
                cases.append({'observation_index':observation,'sign':certificate['sign'],'column':target['column'],'radius':radius,
                              'multipliers':certificate['multipliers'],'terms':description,'nominal_bound':nominal,
                              'global_derivative_per_root':encode(global_per_root),'known_moment':encode(known),'unknown_moment_upper':encode(U),
                              'zero_tail_terms':[encode(x) for x in tails],'zero_tail':encode(zero_tail),'root_bounds':root_bounds,'methods':methods})
            print(json.dumps({'event':'shared_dual','observation':observation,'sign':certificate['sign'],'radii':len(RADII)}),flush=True)
    results=[]
    for observation in range(2):
        for radius in RADII:
            selected=[c for c in cases if c['observation_index']==observation and c['radius']==radius]
            assert len(selected)==2
            results.append({'observation_index':observation,'radius':radius,'methods':{name:sorted(set(selected[0]['methods'][name]['c7_candidates'])&set(selected[1]['methods'][name]['c7_candidates'])) for name in ['global_rows','local_rows','shared_roots']}})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements,recovery]+inputs},
            'precision_bits':bits,'partitions_per_root':partitions,'radii':RADII,'cases':cases,'results':results,
            'scope':'Frozen coefficient-seven duals. The finite error uses the same displacement for a root in every Gaussian measurement, bounded after signed combination. Global and local independent-row controls separate localization from cancellation. Unknown-zero tails retain the nonnegative sum of original row budgets with an inflated moment. Finite population and cutoff are retained; tested certificate failures do not prove information-theoretic ambiguity.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','recovery','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);p.add_argument('--precision',type=int,choices=[224,320],required=True);a=p.parse_args()
    r=run(a.measurements,a.recovery,a.inputs,a.precision);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'results':r['results']}))
