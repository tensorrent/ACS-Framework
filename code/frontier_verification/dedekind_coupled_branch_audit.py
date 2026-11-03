"""Exact integer replay of target-pair separation and feasible relaxed models."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
import dedekind_coupled_recovery as core
from dedekind_coupled_audit import integers,GRID,DUAL_GRID


def run(directory):
    names=['Measurements.json','Dual_Refined.json','Target_Branches.json','Integer_Witnesses.json']
    raws={n:(directory/n).read_bytes() for n in names};data,refined,branches,witnesses=[json.loads(raws[n]) for n in names]
    assert branches['refined_sha256']==witnesses['refined_sha256']==core.sha(raws['Dual_Refined.json'])
    assert witnesses['branches_sha256']==core.sha(raws['Target_Branches.json'])
    powers,rows,settings=core.prepare(data,220,224,'0');ir=integers(rows)
    domains=[r['candidates'] for r in next(c for c in refined['cases'] if c['settings']['top']==220)['domains']]
    column_of={n:i for i,(n,p,k) in enumerate(powers)};separations=[]
    for branch in branches['branches']:
        box=[list(d) for d in domains]
        for n,v in branch['target_assignment'].items():box[column_of[int(n)]]=[v]
        assert core.sha(core.canonical(box))==branch['domains_sha256']
        vector=[0]*len(powers);beta=0
        for index,value in branch['multipliers']:
            multiplier=F(value)*DUAL_GRID;assert multiplier.denominator==1 and multiplier>=0
            scalar=multiplier.numerator;row=ir[index//2]
            coeffs=row['lo'] if index%2==0 else [-v for v in row['hi']]
            rhs=row['rhi'] if index%2==0 else -row['rlo']+row['tail']
            vector=[v+scalar*a for v,a in zip(vector,coeffs)];beta+=scalar*rhs
        minimum=sum(min(v*d[0],v*d[-1]) for v,d in zip(vector,box));gap=minimum-beta
        assert (gap>0)==branch['excluded']
        separations.append({'assignment':branch['target_assignment'],'excluded':gap>0,'exact_gap_lower_bound':str(F(gap,GRID*DUAL_GRID))})
    feasible=[]
    for proposal in witnesses['proposals']:
        assert proposal['verified_feasible'];values=proposal['coefficients']
        assert len(values)==len(domains) and all(type(v) is int and v in d for v,d in zip(values,domains))
        for n,v in proposal['assignment'].items():assert values[column_of[int(n)]]==v
        margins=[]
        for row in ir:
            lower=sum(w*c for w,c in zip(row['lo'],values))-row['rlo']
            upper=row['rhi']-sum(w*c for w,c in zip(row['hi'],values))
            assert lower>0 and upper>0
            margins.append(min(lower,upper))
        feasible.append({'assignment':proposal['assignment'],'all_91_measurements_strictly_satisfied':True,
                         'smallest_margin_lower_bound':str(F(min(margins),GRID)),
                         'coefficient_vector_sha256':core.sha(core.canonical(values))})
    a,b=witnesses['proposals']
    changes=[{'n':n,'first':x,'second':y} for (n,p,k),x,y in zip(powers,a['coefficients'],b['coefficients']) if x!=y]
    assert len(feasible)==2 and sum(r['excluded'] for r in separations)==6
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),
            'inputs_sha256':{n:core.sha(r) for n,r in raws.items()},'fixed_point_scale_bits':192,
            'separations':separations,'feasible_models':feasible,'changed_coordinates_between_models':changes,
            'scope':'Two distinct integer coefficient vectors satisfy every retained height-220 measurement inequality; six other target pairs are excluded by exact separation bounds. This proves non-identifiability within the stated relaxation, not existence of alternative number fields or zero spectra.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.directory)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'excluded_pairs':6,'feasible_models':2,'changed_coordinates':len(r['changed_coordinates_between_models'])}))
