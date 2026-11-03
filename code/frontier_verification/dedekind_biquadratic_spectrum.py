"""Completed-function contour folded onto Re(s)>=1/2 using the functional equation.

Gamma argument changes are evaluated with analytic log-gamma endpoint lifts.
Only L-function images on four half-horizontal paths require subdivision.
"""
import argparse,hashlib,json
from datetime import datetime,timezone
from sympy import kronecker_symbol
import dirichlet_strip_certificate as refinement
from pathlib import Path
from fractions import Fraction as F
from flint import acb,arb,ctx,dirichlet_char
import lfunction_zero_certificate as core
from dirichlet_strip_certificate import encode,complex_encode


CHARACTERS = {-3:2, 8:5, -8:3, 24:11, -24:5}


def count(discriminant,top,bits):
    ctx.prec=bits
    q=abs(discriminant);number=CHARACTERS[discriminant]
    chi=dirichlet_char(q,number);conjugate=dirichlet_char(q,pow(number,-1,q))
    assert chi.is_primitive() and not chi.is_principal()
    assert chi.is_real() and int(chi.conductor())==q and int(chi.order())==2
    assert all(chi(r)==int(kronecker_symbol(discriminant,r)) for r in range(q))
    radius=arb(2).zeta()-1;assert radius<1
    endpoints=[]
    def lift(c,t):
        z=acb(2,arb(str(t)));L=c.l(z);assert L.real>0
        lg=((z+int(c.parity()))/2).lgamma().imag
        v=arb(str(t))/2*(q/arb.pi()).log()+lg+L.arg()
        endpoints.append({'character':int(c.number()),'height':str(t),'L_value':complex_encode(L),
                          'log_gamma_imag':encode(lg),'argument_lift':encode(v)})
        return v
    right=lift(chi,F(top))-lift(chi,F(-1,2))
    left=lift(conjugate,F(1,2))-lift(conjugate,F(-top))
    pieces=[]
    specs=[('bottom_left_folded',conjugate,(F(2),F(1,2)),(F(1,2),F(1,2))),
           ('bottom_right',chi,(F(1,2),F(-1,2)),(F(2),F(-1,2))),
           ('top_right',chi,(F(2),F(top)),(F(1,2),F(top))),
           ('top_left_folded',conjugate,(F(1,2),F(-top)),(F(2),F(-top)))]
    for name,c,a,b in specs:
        segments=[];cache={}
        def value(p):
            if p not in cache:cache[p]=c.l(core.point(p))
            return cache[p]
        def segment(lo,hi,depth=0):
            image=c.l(core.segment_box(lo,hi))
            if not image.contains(0):
                ratio=value(hi)/value(lo)
                if ratio.real>0:
                    angle=ratio.arg()
                    segments.append({'a':list(map(str,lo)),'b':list(map(str,hi)),
                                     'image':complex_encode(image),'ratio':complex_encode(ratio),
                                     'angle':encode(angle),'depth':depth})
                    return angle
            assert depth<30,('Unresolved half-horizontal boundary',name,lo,hi)
            mid=tuple((x+y)/2 for x,y in zip(lo,hi))
            return segment(lo,mid,depth+1)+segment(mid,hi,depth+1)
        # Seed before native evaluation: a wide real-part ball can make the
        # Hurwitz evaluator pathological at high imaginary height.
        seed_partitions=64 if bits==160 else 96
        nodes=[tuple(x+(y-x)*F(j,seed_partitions) for x,y in zip(a,b))
               for j in range(seed_partitions+1)]
        L_change=sum((segment(lo,hi) for lo,hi in zip(nodes,nodes[1:])),arb(0))
        za=(core.point(a)+int(c.parity()))/2;zb=(core.point(b)+int(c.parity()))/2
        gamma_change=(zb.lgamma()-za.lgamma()).imag
        change=L_change+gamma_change
        pieces.append({'name':name,'character':int(c.number()),'a':list(map(str,a)),'b':list(map(str,b)),
                       'seed_partitions':seed_partitions,'segments':segments,'L_argument_change':encode(L_change),
                       'gamma_argument_change':encode(gamma_change),'completed_argument_change':encode(change)})
        print(json.dumps({'event':'folded_piece','character':number,'top':top,'piece':name,'segments':len(segments)}),flush=True)
    def decode(x):
        mid=arb((x['mid'][0],x['mid'][1]));rad=arb((x['rad'][0],x['rad'][1]))
        return arb(mid,rad)
    winding=(right+left+sum((decode(p['completed_argument_change']) for p in pieces),arb(0)))/(2*arb.pi())
    integer=winding.unique_fmpz();assert integer is not None and integer>=0
    return {'zero_count':int(integer),'winding':encode(winding),'winding_printed':winding.str(60),
            'euler_disk_radius':encode(radius),'vertical_endpoints':endpoints,
            'right_argument_change':encode(right),'left_argument_change':encode(left),'horizontal_pieces':pieces,
            'scope':'Completed primitive nonprincipal rectangle [-1,2] x [-1/2,T], using analytic gamma and functional-equation lifts.'}



def generate(bits,top):
    ctx.prec=bits;result={}
    for D,number in CHARACTERS.items():
        q=abs(D);chi=dirichlet_char(q,number)
        counted=count(D,top,bits)
        lo=F(0);slo=core.sign(core.hardy(chi,lo));assert slo
        brackets=[]
        for j in range(1,10*top+1):
            hi=F(j,10);shi=core.sign(core.hardy(chi,hi));assert shi
            if shi!=slo:brackets.append((lo,hi))
            lo,slo=hi,shi
        assert len(brackets)==counted['zero_count'],(D,len(brackets),counted['zero_count'])
        roots=[refinement.refine(chi,lo,hi) for lo,hi in brackets]
        assert all(F(a['hi'])<F(b['lo']) for a,b in zip(roots,roots[1:]))
        result[str(D)]={'discriminant':D,'modulus':q,'conrey_number':number,'parity':int(chi.parity()),
                        'character_values':[int(kronecker_symbol(D,r)) for r in range(q)],
                        'contour':counted,'root_intervals':roots}
        print(json.dumps({'event':'factor_complete','D':D,'roots':len(roots)}),flush=True)
    n=arb(top).zeta_nzeros().unique_fmpz();assert n is not None
    zr=[];allroots=list(acb.zeta_zeros(1,int(n)+1))
    for z in allroots[:-1]:
        assert z.real==arb('0.5') and 0<z.imag<top
        zr.append({'lo':str(refinement.dyadic(z.imag.lower())),'hi':str(refinement.dyadic(z.imag.upper()))})
    assert allroots[-1].imag>top
    aggregate={}
    for name,Ds in {'A':[8,-3,-24],'B':[-8,-3,24]}.items():
        roots=[{'lo':r['lo'],'hi':r['hi']} for D in Ds for r in result[str(D)]['root_intervals']]+zr
        roots.sort(key=lambda r:F(r['lo']))
        assert all(F(a['hi'])<F(b['lo']) for a,b in zip(roots,roots[1:]))
        counts=[]
        for t in range(1,top+1):
            assert all(F(r['hi'])<t or F(r['lo'])>t for r in roots)
            counts.append({'height':t,'positive_zero_count':sum(F(r['hi'])<t for r in roots)})
        aggregate[name]={'unlabelled_ordinate_intervals':roots,'integer_height_counts':counts}
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dependencies_sha256':{Path(m.__file__).name:hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in [core,refinement]},
            'recorded_utc':datetime.now(timezone.utc).isoformat(),'precision_bits':bits,'top':top,
            'factors':result,'zeta':{'count':int(n),'root_intervals':zr,'next_zero':allroots[-1].str(60)},
            'aggregate':aggregate,
            'scope':'Five primitive quadratic factors and Riemann zeta through the declared height. Labelled factors certify generation; inference receives only the aggregate intervals and common invariants. No global GRH assumption or claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--top',type=int,default=20);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=generate(a.precision,a.top);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'factor_counts':{D:len(v['root_intervals']) for D,v in r['factors'].items()},
                      'aggregate_counts':{k:len(v['unlabelled_ordinate_intervals']) for k,v in r['aggregate'].items()}}))
