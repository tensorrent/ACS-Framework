"""Replay the saved direct paths with fresh interval evaluations and exact hashes."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
from flint import arb, acb, ctx, dirichlet_char
import lfunction_zero_certificate as core
from dirichlet_strip_certificate import complex_encode, encode


def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def validate(data):
    assert data['top']==20 and set(data['factors'])=={'-3','8','-8','24','-24'}
    assert data['zeta']['count']==len(data['zeta']['root_intervals'])==1
    for D,number in [(-3,2),(8,5),(-8,3),(24,11),(-24,5)]:
        row=data['factors'][str(D)];roots=row['root_intervals']
        assert row['discriminant']==D and row['modulus']==abs(D) and row['conrey_number']==number
        assert row['contour']['zero_count']==len(roots)
        assert all(0<F(r['lo'])<F(r['hi'])<20 and r['lo_sign']*r['hi_sign']==-1 for r in roots)
        assert all(F(a['hi'])<F(b['lo']) for a,b in zip(roots,roots[1:]))
    for label,Ds in [('A',[8,-3,-24]),('B',[-8,-3,24])]:
        union=[{'lo':r['lo'],'hi':r['hi']} for D in Ds for r in data['factors'][str(D)]['root_intervals']]+data['zeta']['root_intervals']
        union.sort(key=lambda r:F(r['lo']))
        assert union==data['aggregate'][label]['unlabelled_ordinate_intervals']
        assert all(F(a['hi'])<F(b['lo']) for a,b in zip(union,union[1:]))
        expected=[]
        for h in range(1,21):
            assert all(F(r['hi'])<h or F(r['lo'])>h for r in union)
            expected.append({'height':h,'positive_zero_count':sum(F(r['hi'])<h for r in union)})
        assert expected==data['aggregate'][label]['integer_height_counts']


def run(paths,direct_path):
    data=[json.loads(p.read_text()) for p in paths];direct=json.loads(direct_path.read_text())
    for d in data:validate(d)
    ctx.prec=256;replays=[];endpoint_checks=0
    for saved in direct['direct_L_contours']:
        D=saved['D'];factor=data[0]['factors'][str(D)];chi=dirichlet_char(abs(D),factor['conrey_number'])
        contour=saved['contour'];corners=[tuple(map(F,p)) for p in contour['corners']]
        assert corners==[(F(-1,4),F(-1,2)),(F(5,4),F(-1,2)),(F(5,4),F(20)),(F(-1,4),F(20))]
        previous=corners[0];edge=0;cache={};total=arb(0);digest=hashlib.sha256();fresh_leaves=0;subdivisions=0
        def value(p):
            if p not in cache:cache[p]=chi.l(core.point(p))
            return cache[p]
        def fresh(a,b,depth=0):
            nonlocal fresh_leaves,subdivisions
            image=chi.l(core.segment_box(a,b));ratio=value(b)/value(a)
            if not image.contains(0) and ratio.real>0:
                angle=ratio.arg();fresh_leaves+=1
                digest.update(canonical({'a':list(map(str,a)),'b':list(map(str,b)),'image':complex_encode(image),'ratio':complex_encode(ratio),'angle':encode(angle)})+b'\n')
                return angle
            assert depth<20
            subdivisions+=1;mid=tuple((x+y)/2 for x,y in zip(a,b))
            return fresh(a,mid,depth+1)+fresh(mid,b,depth+1)
        for row in contour['segments']:
            a,b=(tuple(map(F,row[key])) for key in ['a','b'])
            assert a==previous and a!=b and edge<4
            c0,c1=corners[edge],corners[(edge+1)%4]
            changing=0 if c0[0]!=c1[0] else 1;fixed=1-changing
            assert a[fixed]==b[fixed]==c0[fixed]
            if c0[changing]<c1[changing]:assert c0[changing]<=a[changing]<b[changing]<=c1[changing]
            else:assert c1[changing]<=b[changing]<a[changing]<=c0[changing]
            angle=fresh(a,b);assert angle.overlaps(arb(row['angle']))
            total+=angle
            previous=b
            if b==c1:edge+=1
        assert previous==corners[0] and edge==4
        winding=total/(2*arb.pi());integer=winding.unique_fmpz()
        assert integer is not None and int(integer)==contour['zero_count']==saved['positive_count']+int(D>0)
        assert saved['positive_count']==len(factor['root_intervals'])
        # Origin zeros follow the quadratic functional equation. Recheck L(0).
        assert (F(saved['exact_L_at_zero'])==0)==(D>0)
        assert chi.l(acb(0)).contains(arb(saved['exact_L_at_zero']))
        for d in data:
            for root in d['factors'][str(D)]['root_intervals']:
                for end in ['lo','hi']:
                    assert core.sign(core.hardy(chi,F(root[end])))==root[end+'_sign'];endpoint_checks+=1
        replays.append({'D':D,'stored_segments':len(contour['segments']),'fresh_leaves':fresh_leaves,'subdivisions':subdivisions,'exact_evaluation_stream_sha256':digest.hexdigest(),
                        'winding':encode(winding),'contour_count':int(integer),'positive_count':saved['positive_count']})
        print(json.dumps({'event':'fresh_path_replay','D':D,'segments':len(contour['segments'])}),flush=True)
    assert sum(r['stored_segments'] for r in replays)==63405 and endpoint_checks==156
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in paths+[direct_path]},
            'bits':256,'stored_segments_replayed':63405,'fresh_certified_leaves':sum(r['fresh_leaves'] for r in replays),'endpoint_sign_replays':endpoint_checks,'direct_paths':replays,
            'scope':'Recompute every stored direct-contour path at 256 bits, adaptively subdividing as needed, and verify full ordered boundary coverage, zero exclusion, ratio branch and winding. Interval widths are not monotone in precision. Original direct image printouts are lossy diagnostics and are not parsed as interval certificates. Exact dyadic encodings of each accepted fresh leaf are hashed in traversal order. Execution and the hash depend on the pinned FLINT runtime.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['spectrum160','spectrum224','direct','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run([a.spectrum160,a.spectrum224],a.direct);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'stored_segments':r['stored_segments_replayed'],'fresh_leaves':r['fresh_certified_leaves'],'endpoint_replays':r['endpoint_sign_replays']}))
