"""Higher-precision contour and every-root endpoint replay, with selected mpmath roots."""
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
from flint import ctx,dirichlet_char
import dirichlet_extended_certificate as producer
import dirichlet_folded_count as counter
import lfunction_zero_certificate as core


def number(value):
    value=F(value);return mp.mpf(value.numerator)/value.denominator


def run(path):
    raw=path.read_bytes();data=json.loads(raw);assert data['status']=='passed'
    assert data['source_sha256']==hashlib.sha256(Path(producer.__file__).read_bytes()).hexdigest()
    assert data['dependencies_sha256']==producer.sources()
    ctx.prec=224;chi=dirichlet_char(5,data['character']);count=counter.count(data['character'],data['top'],224)
    assert count['zero_count']==data['contour']['zero_count']==len(data['root_intervals'])
    checks=[]
    for row in data['root_intervals']:
        lo,hi=F(row['lo']),F(row['hi']);vl,vh=core.hardy(chi,lo),core.hardy(chi,hi)
        assert core.sign(vl)==row['lo_sign'] and core.sign(vh)==row['hi_sign'] and core.sign(vl)*core.sign(vh)==-1
        checks.append({'index':row['index'],'lo_Z':vl.str(65),'hi_Z':vh.str(65),'opposite_signs':True})
    rows=data['root_intervals'];n=len(rows)
    closest=min(range(n-1),key=lambda i:F(rows[i+1]['lo'])-F(rows[i]['hi']))
    indices=sorted({1,n//4,n//2,3*n//4,n,closest+1,closest+2})
    mp.mp.dps=60
    logs={1:0,2:1,3:3,4:2};exponent=logs[data['character']]
    values={a:mp.j**((exponent*logs[a])%4) for a in range(1,5)}
    def L(t):
        s=mp.mpc('0.5',t)
        return mp.power(5,-s)*mp.fsum(values[a]*mp.zeta(s,mp.mpf(a)/5) for a in range(1,5))
    independent=[]
    for index in indices:
        row=rows[index-1];center=(number(row['lo'])+number(row['hi']))/2
        slope=mp.diff(L,center);projection=mp.re if abs(mp.re(slope))>abs(mp.im(slope)) else mp.im
        root=mp.findroot(lambda t:projection(L(t)),(center-mp.mpf('1e-5'),center+mp.mpf('1e-5')),tol=mp.mpf('1e-55'))
        residual=abs(L(root));assert number(row['lo'])<root<number(row['hi']) and residual<mp.mpf('1e-50')
        independent.append({'index':index,'mpmath_ordinate':mp.nstr(root,60),'L_residual':mp.nstr(residual,15),'inside_interval':True})
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'producer_sha256':data['source_sha256'],'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'character':data['character'],'top':data['top'],'precision_bits':224,'contour':count,
            'root_endpoint_checks':checks,'independent_roots':independent,
            'scope':'All endpoints and count replayed with the shared interval kernel; selected roots use a separate Hurwitz implementation.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.certificate);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'character':r['character'],'endpoints':len(r['root_endpoint_checks']),'independent_roots':len(r['independent_roots'])}))
