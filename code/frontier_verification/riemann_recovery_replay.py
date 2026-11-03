"""Replay every indexed Riemann interval at 224 bits, and three roots with mpmath."""
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from flint import acb,arb,ctx
import mpmath as mp
import riemann_recovery_certificate as producer


def run(path):
    raw=path.read_bytes();data=json.loads(raw)
    assert data['status']=='passed'
    assert data['source_sha256']==hashlib.sha256(Path(producer.__file__).read_bytes()).hexdigest()
    ctx.prec=224;top=data['top'];count=int(arb(top).zeta_nzeros().unique_fmpz())
    assert count==data['count']==len(data['root_intervals'])
    zeros=list(acb.zeta_zeros(1,count+1));rows=[]
    for j,(z,old) in enumerate(zip(zeros[:-1],data['root_intervals']),1):
        lo,hi=producer.dyadic(z.imag.lower()),producer.dyadic(z.imag.upper())
        assert z.real==arb('0.5') and 0<lo<hi<top
        assert not rows or F(rows[-1]['hi'])<lo
        assert arb(old['lo']).union(arb(old['hi'])).overlaps(z.imag)
        rows.append({'index':j,'lo':str(lo),'hi':str(hi),'overlaps_160_bits':True})
    assert zeros[-1].imag>top
    mp.mp.dps=90;checks=[]
    for index in [1,count//2,count]:
        value=mp.im(mp.zetazero(index));row=rows[index-1]
        def num(x):
            f=F(x);return mp.mpf(f.numerator)/f.denominator
        assert num(row['lo'])<value<num(row['hi'])
        checks.append({'index':index,'ordinate':mp.nstr(value,90),'inside_224_interval':True})
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),'top':top,'precision_bits':224,
            'count':count,'root_intervals':rows,'independent_checks':checks}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.certificate)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'count':r['count']}))
