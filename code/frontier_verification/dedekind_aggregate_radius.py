"""Validate frozen c7 duals after bounded loss of ordinate precision."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_coupled_dual import inequalities,bound

RADII=['0','1/10000000','1/1000000','1/100000','1/10000','1/1000']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def run(measurements,recovery,inputs):
    d=json.loads(measurements.read_text());r=json.loads(recovery.read_text());source=[json.loads(p.read_text()) for p in inputs]
    ctx.prec=256;results=[];T=d['global_inputs']['top'];C=decode(d['constant_moment_upper'])
    for observation,data in enumerate(source):
        assert d['input_sha256'][observation]==sha(inputs[observation])
        rs=[arb(x['lo']).union(arb(x['hi'])) for x in data['positive_root_intervals']]
        target=next(t for t in r['results'][observation]['dual_targets'] if t['n']==7)
        for text_radius in RADII:
            delta=arb(text_radius);enlarged=[x+arb(0,delta.upper()) for x in rs]
            assert all(x>0 and x<T for x in enlarged)
            known=sum((3/(arb('9/4')+x*x) for x in enlarged),arb(0));U=C-known;assert U>0
            rows=[];metadata=[]
            for row in d['rows']:
                a=arb(1)/row['denominator'];u=arb(row['center']).log();scale=decode(row['scale'])
                derivative=(2*a/arb(1).exp()).sqrt()+u
                input_error=2*scale*len(rs)*delta*derivative
                phi=(4+T*T)*(-a*T*T).exp() if a*(4+T*T)>=1 else (4*a-1).exp()/a
                zero_error=scale*U*phi*(a/4).exp()*(u/2).cosh()
                estimate=decode(row['observations'][observation]['unwidened'])
                R=estimate+arb(0,(input_error+zero_error).upper())
                rows.append({'weights':[decode(w) for w in row['weights']],'R':R,'B':decode(row['prime_tail'])})
                metadata.append({'center':row['center'],'input_error':encode(input_error),'zero_tail':encode(zero_error),'R':encode(R)})
            matrix,rhs=inequalities(rows);bounds=[]
            for cert in target['certificates']:
                multipliers=[F(0)]*len(rhs)
                for j,v in cert['multipliers']:multipliers[j]=F(v)
                bounds.append({'sign':cert['sign'],**bound(matrix,rhs,target['column'],cert['sign'],multipliers)})
            candidates=[c for c in range(5) if all(not arb(b['sign']*c)>decode(b['objective_upper_bound']).upper() for b in bounds)]
            assert candidates
            results.append({'observation_index':observation,'radius':text_radius,'known_moment':encode(known),'unknown_moment_upper':encode(U),
                            'measurements':metadata,'bounds':bounds,'c7_candidates':candidates})
        trials=[x for x in results if x['observation_index']==observation]
        assert trials[0]['c7_candidates']==target['candidates']
        assert all(set(a['c7_candidates'])<=set(b['c7_candidates']) for a,b in zip(trials,trials[1:]))
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements,recovery]+inputs},
            'radii':RADII,'results':results,
            'scope':'Frozen coefficient-seven duals under interval widening by an additional absolute radius. The finite root population and completeness cutoff are retained; all enlarged roots stay inside (0,T). A global derivative bound independently bounds each measurement before the dual combination, and the unknown-zero moment is recomputed. Failure to retain a singleton is a limitation of these certificates, not evidence of alternate fields or an information-theoretic noise limit.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--measurements',type=Path,required=True);p.add_argument('--recovery',type=Path,required=True);p.add_argument('--inputs',type=Path,nargs=2,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.measurements,a.recovery,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'c7':[{k:x[k] for k in ['observation_index','radius','c7_candidates']} for x in r['results']]}))
