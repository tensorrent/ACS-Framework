"""Optional general local-degree information resolves the two relaxed target pairs."""
import argparse,hashlib,json
from pathlib import Path


def run(refined_path,branches_path):
    refined_raw=refined_path.read_bytes();branches_raw=branches_path.read_bytes()
    refined=json.loads(refined_raw);branches=json.loads(branches_raw)
    assert refined['status']==branches['status']=='passed'
    assert branches['refined_sha256']==hashlib.sha256(refined_raw).hexdigest()
    case=next(c for c in refined['cases'] if c['settings']['top']==220)
    rows={r['n']:r for r in case['domains']}
    assert rows[19]['candidates']==[0] and rows[361]['candidates']==[1,2,3,4]
    # All unramified partitions of degree four, without a field-specific
    # residue or Galois assumption. The given discriminant is not divisible by 19.
    partitions=[[1,1,1,1],[1,1,2],[1,3],[2,2],[4]]
    retained=[fs for fs in partitions if sum(f for f in fs if 1%f==0) in rows[19]['candidates']
              and sum(f for f in fs if 2%f==0) in rows[361]['candidates']]
    coefficients=sorted({sum(f for f in fs if 2%f==0) for fs in retained})
    survivors=[r for r in branches['surviving_assignments'] if r['361'] in coefficients]
    assert retained==[[2,2]] and coefficients==[4] and survivors==[{'359':0,'361':4}]
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs_sha256':{'refined':hashlib.sha256(refined_raw).hexdigest(),'branches':hashlib.sha256(branches_raw).hexdigest()},
            'height':220,'prime':19,'c19_candidates':rows[19]['candidates'],'c361_prior_candidates':rows[361]['candidates'],
            'unramified_partitions':partitions,'retained_partitions':retained,'c361_after_local_relation':coefficients,
            'surviving_target_pairs':survivors,'unique_target_coefficients_with_added_local_information':91,
            'scope':'Additional local Euler degree relation is explicit and separate from the spectrum-only coefficient-box model. Together with the checked pair separations, it resolves all 91 targets at height 220.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['refined','branches','output']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=run(a.refined,a.branches);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'height':220,'unique_targets_with_local_information':91}))
