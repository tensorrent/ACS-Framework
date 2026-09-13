"""Direct L-contours, higher-precision endpoints and independent Hurwitz roots."""
import argparse, hashlib, json
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
from flint import acb, arb, ctx, dirichlet_char
import mpmath as mp
from sympy import kronecker_symbol
import lfunction_zero_certificate as core


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def mpf(s):
    q=F(s);return mp.mpf(q.numerator)/q.denominator


def run(paths):
    data=[json.loads(p.read_text()) for p in paths]
    assert [d['precision_bits'] for d in data]==[160,224]
    assert all(d['top']==20 for d in data)
    direct=[];endpoint_checks=0;independent=[];mp.mp.dps=85
    for D,number in [(-3,2),(8,5),(-8,3),(24,11),(-24,5)]:
        ctx.prec=224;q=abs(D);chi=dirichlet_char(q,number)
        expected=[int(kronecker_symbol(D,r)) for r in range(q)]
        assert chi.is_real() and chi.is_primitive() and int(chi.parity())==int(D<0)
        assert all(chi(r)==expected[r] for r in range(q))
        value0=sum((F(1,2)-F(r,q))*expected[r] for r in range(1,q))
        assert chi.l(acb(0)).contains(arb(str(value0)))
        assert (value0==0)==(D>0)
        contour=core.contour_count(chi,20)
        n=contour['zero_count']-int(D>0)
        assert n==len(data[0]['factors'][str(D)]['root_intervals'])==len(data[1]['factors'][str(D)]['root_intervals'])
        direct.append({'D':D,'contour':contour,'exact_L_at_zero':str(value0),'trivial_origin_zero_count':int(D>0),'positive_count':n})
        ctx.prec=256
        for index in range(n):
            pair=[d['factors'][str(D)]['root_intervals'][index] for d in data]
            assert max(F(r['lo']) for r in pair)<min(F(r['hi']) for r in pair)
            for r in pair:
                assert core.sign(core.hardy(chi,F(r['lo'])))==r['lo_sign']
                assert core.sign(core.hardy(chi,F(r['hi'])))==r['hi_sign']
                assert r['lo_sign']*r['hi_sign']==-1;endpoint_checks+=2
        def L(t):
            s=mp.mpc('0.5',t)
            return mp.power(q,-s)*mp.fsum(expected[r]*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q) if expected[r])
        for index in sorted({0,n//2,n-1}):
            row=data[0]['factors'][str(D)]['root_intervals'][index]
            center=(mpf(row['lo'])+mpf(row['hi']))/2
            derivative=mp.diff(L,center);projection=mp.re if abs(mp.re(derivative))>abs(mp.im(derivative)) else mp.im
            root=mp.findroot(lambda t:projection(L(t)),(center-mp.mpf('0.0001'),center+mp.mpf('0.0001')),tol=mp.mpf('1e-78'))
            residual=abs(L(root));assert residual<mp.mpf('1e-74')
            assert all(mpf(d['factors'][str(D)]['root_intervals'][index]['lo'])<root<mpf(d['factors'][str(D)]['root_intervals'][index]['hi']) for d in data)
            independent.append({'D':D,'index':index+1,'root':mp.nstr(root,70),'residual':mp.nstr(residual,12),'inside_both_certificates':True})
        print(json.dumps({'event':'independent_factor','D':D,'direct_count':n,'mpmath_roots':3}),flush=True)
    z=mp.im(mp.zetazero(1))
    assert all(len(d['zeta']['root_intervals'])==1 and mpf(d['zeta']['root_intervals'][0]['lo'])<z<mpf(d['zeta']['root_intervals'][0]['hi']) for d in data)
    independent.append({'D':'zeta','index':1,'root':mp.nstr(z,70),'residual':mp.nstr(abs(mp.zeta(mp.mpc('0.5',z))),12),'inside_both_certificates':True})
    for label in ['A','B']:
        assert data[0]['aggregate'][label]['integer_height_counts']==data[1]['aggregate'][label]['integer_height_counts']
    return {'status':'passed','recorded_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':sha(Path(__file__)),
            'core_sha256':sha(Path(core.__file__)),'inputs_sha256':{p.name:sha(p) for p in paths},
            'direct_contour_bits':224,'endpoint_bits':256,'mpmath_digits':85,
            'direct_L_contours':direct,'endpoint_sign_replays':endpoint_checks,'independent_roots':independent,
            'integer_height_count_comparisons':40,
            'scope':'Direct L-function rectangles count zeros independently of the producer folded completed-function argument lifts. Both interval routes share FLINT. Exact origin values account for even-character trivial zeros. Selected mpmath roots supply an independent numerical backend, not independent completeness.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spectrum160',type=Path,required=True);p.add_argument('--spectrum224',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run([a.spectrum160,a.spectrum224]);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'direct_contours':len(r['direct_L_contours']),'endpoint_replays':r['endpoint_sign_replays'],'independent_roots':len(r['independent_roots'])}))
