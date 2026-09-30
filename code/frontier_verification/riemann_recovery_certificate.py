"""Certified indexed Riemann roots and total count for recovery experiments."""
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from flint import acb,arb,ctx
import mpmath as mp
import lfunction_zero_certificate as core


def dyadic(x):
    m,e=x.man_exp();return F(int(m))*F(2)**int(e)


def run(top,bits):
    ctx.prec=bits
    count=arb(top).zeta_nzeros().unique_fmpz();assert count is not None
    count=int(count);zs=list(acb.zeta_zeros(1,count+1));rows=[]
    for j,z in enumerate(zs[:-1],1):
        assert z.real==arb('0.5')
        lo,hi=dyadic(z.imag.lower()),dyadic(z.imag.upper())
        assert 0<lo<hi<top and (not rows or F(rows[-1]['hi'])<lo)
        rounded=core.decimal_midpoint(lo,hi);radius=F(1,2*10**20)
        assert F(rounded)-radius<lo<hi<F(rounded)+radius
        rows.append({'index':j,'lo':str(lo),'hi':str(hi),'rounded':rounded,'rounding_cell_radius':str(radius)})
    assert zs[-1].imag>top
    checks=[];mp.mp.dps=60
    for index in [1,count//2,count]:
        value=mp.im(mp.zetazero(index));row=rows[index-1]
        assert mp.mpf(F(row['lo']).numerator)/F(row['lo']).denominator<value<mp.mpf(F(row['hi']).numerator)/F(row['hi']).denominator
        checks.append({'index':index,'mpmath_ordinate':mp.nstr(value,60),'inside_interval':True})
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'core_sha256':hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
            'top':top,'precision_bits':bits,'count':count,'count_ball':arb(top).zeta_nzeros().str(65),
            'next_zero':zs[-1].str(65),'root_intervals':rows,'independent_checks':checks,
            'scope':'Indexed interval roots matched to total count through the stated finite height; no global RH claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--top',type=int,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert a.top>20
    r=run(a.top,a.precision);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'roots':r['count'],'precision_bits':a.precision}))
