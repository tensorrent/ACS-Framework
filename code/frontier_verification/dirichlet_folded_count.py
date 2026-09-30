"""Completed-function contour folded onto Re(s)>=1/2 using the functional equation.

Gamma argument changes are evaluated with analytic log-gamma endpoint lifts.
Only L-function images on four half-horizontal paths require subdivision.
"""
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from flint import acb,arb,ctx,dirichlet_char
import lfunction_zero_certificate as core
from dirichlet_strip_certificate import encode,complex_encode


def count(number,top,bits):
    ctx.prec=bits
    chi=dirichlet_char(5,number);conjugate=dirichlet_char(5,pow(number,-1,5))
    assert chi.is_primitive() and not chi.is_principal()
    logs={1:0,2:1,3:3,4:2}
    assert all(int(chi.chi_exponent(r))==(logs[number]*logs[r])%4 for r in range(1,5))
    radius=arb(2).zeta()-1;assert radius<1
    endpoints=[]
    def lift(c,t):
        z=acb(2,arb(str(t)));L=c.l(z);assert L.real>0
        lg=((z+int(c.parity()))/2).lgamma().imag
        v=arb(str(t))/2*(5/arb.pi()).log()+lg+L.arg()
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


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--character',type=int,choices=[2,3,4],required=True)
    p.add_argument('--top',type=int,required=True);p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r={'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'character':a.character,'top':a.top,'precision_bits':a.precision,'contour':count(a.character,a.top,a.precision)}
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'count':r['contour']['zero_count']}))
