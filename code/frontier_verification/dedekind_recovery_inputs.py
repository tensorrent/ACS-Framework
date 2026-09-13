"""Validate extended finite factor identities and preserve the height-220 prefix."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_inputs import load_factors


def sha(raw):return hashlib.sha256(raw).hexdigest()


def build(directory,extra,prior):
    ctx.prec=224
    old,old_identity=load_factors(extra,prior)
    names={'zeta':'riemann-160.json','chi1':'character-2.json',
           'chi2':'character-4.json','chi3':'character-3.json'}
    rows=[];identities={};counts={};prefix=[]
    for name,filename in names.items():
        raw=(directory/filename).read_bytes();data=json.loads(raw)
        assert data['status']=='passed' and data['top']==2000
        expected={'chi1':2,'chi2':4,'chi3':3}
        if name!='zeta':assert data['character']==expected[name] and data['modulus']==5
        values=data['root_intervals']
        count=data['count'] if name=='zeta' else data['contour']['zero_count']
        assert len(values)==count
        counts[name]=count;identities[filename]=sha(raw)
        for j,r in enumerate(values,1):
            lo,hi=F(r['lo']),F(r['hi'])
            assert r['index']==j and 0<lo<hi<2000
            assert j==1 or F(values[j-2]['hi'])<lo
            assert F(r['rounded'])-F(r['rounding_cell_radius'])<lo<hi<F(r['rounded'])+F(r['rounding_cell_radius'])
            rows.append({'factor':name,'index':j,'lo':r['lo'],'hi':r['hi']})
        previous=[r for r in values if F(r['hi'])<220]
        assert len(previous)==len(old[name])
        for a,b in zip(previous,old[name]):
            assert a['rounded']==b['rounded']
            assert arb(a['lo']).union(arb(a['hi'])).overlaps(arb(b['lo']).union(arb(b['hi'])))
        prefix.append({'factor':name,'count':len(previous),'all_intervals_overlap':True,'all_20_digit_rows_equal':True})
    rows.sort(key=lambda r:F(r['lo']))
    assert all(F(a['hi'])<F(b['lo']) for a,b in zip(rows,rows[1:]))
    heights=[220,600,1000,1500,2000]
    for top in heights:assert all(not F(r['lo'])<=top<=F(r['hi']) for r in rows)
    return {'status':'passed','source_sha256':sha(Path(__file__).read_bytes()),
            'degree':4,'discriminant':125,'real_places':0,'complex_places':2,'top':2000,
            'heights':heights,'counts':counts,'input_sha256':identities,'prior_identity':old_identity,
            'prefix_checks':prefix,'positive_root_intervals':rows,
            'scope':'Complete positive union of four factors through 2000; conjugate factors supply the negative union. All cross-factor intervals disjoint.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['directory','extra','prior','output']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=build(a.directory,a.extra,a.prior);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'counts':r['counts'],'total':len(r['positive_root_intervals'])}))
