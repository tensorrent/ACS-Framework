"""Finite Dirichlet zero certificates using explicit vertical argument lifts.

On Re(s)=2, |L(s)-1| <= zeta(2)-1 < 1 supplies a global argument branch.
The primitive functional equation supplies the left side of the completed
function's contour. Only the two horizontal sides need interval subdivision.
"""
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time
from pathlib import Path
from flint import acb,arb,ctx,dirichlet_char
import flint
import lfunction_zero_certificate as core


def sha(raw):return hashlib.sha256(raw).hexdigest()
def dyadic(x):
    m,e=x.man_exp()
    return F(int(m))*F(2)**int(e)
def encode(x):
    return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def complex_encode(x):return {'real':encode(x.real),'imag':encode(x.imag)}


def completed(chi,z):
    argument=(z+int(chi.parity()))/2
    return (argument*acb(5/arb.pi()).log()).exp()*argument.gamma()*chi.l(z)


def contour(chi,top):
    number=int(chi.number())
    conjugate=dirichlet_char(5,pow(number,-1,5))
    assert chi.is_primitive() and not chi.is_principal()
    assert int(chi.modulus())==5 and int(chi.conductor())==5
    powers={1:0,2:1,3:3,4:2}
    expected={r:(powers[number]*powers[r])%4 for r in range(1,5)}
    assert chi(0)==0 and all(int(chi.chi_exponent(r))==expected[r] for r in range(1,5))
    assert all(conjugate(a).overlaps(chi(a).conjugate()) for a in range(5))
    bound=arb(2).zeta()-1
    assert bound<1
    points=[]
    def lift(character,t):
        z=acb(2,arb(str(t)))
        L=character.l(z)
        assert L.real>0
        gamma_arg=((z+int(character.parity()))/2).lgamma().imag
        value=arb(str(t))/2*(5/arb.pi()).log()+gamma_arg+L.arg()
        points.append({'character':int(character.number()),'height':str(t),
                       'L_value':complex_encode(L),'log_gamma_imag':encode(gamma_arg),'argument_lift':encode(value)})
        return value
    right=lift(chi,F(top))-lift(chi,F(-1,2))
    left=lift(conjugate,F(1,2))-lift(conjugate,F(-top))
    segments=[]
    cache={}
    def value(p):
        if p not in cache:cache[p]=completed(chi,core.point(p))
        return cache[p]
    def segment(a,b,depth=0):
        image=completed(chi,core.segment_box(a,b))
        if not image.contains(0):
            ratio=value(b)/value(a)
            if ratio.real>0:
                angle=ratio.arg()
                segments.append({'a':list(map(str,a)),'b':list(map(str,b)),
                                 'image':complex_encode(image),'ratio':complex_encode(ratio),
                                 'angle':encode(angle),'depth':depth})
                return angle
        assert depth<30,('Horizontal boundary needs more precision or has a zero',a,b)
        mid=tuple((x+y)/2 for x,y in zip(a,b))
        return segment(a,mid,depth+1)+segment(mid,b,depth+1)
    bottom=segment((F(-1),F(-1,2)),(F(2),F(-1,2)))
    upper=segment((F(2),F(top)),(F(-1),F(top)))
    winding=(right+left+bottom+upper)/(2*arb.pi())
    count=winding.unique_fmpz()
    assert count is not None and count>=0
    # The Gauss-sum convention and left/right endpoint agreement are numerical
    # checks of the sourced functional equation, not its analytic proof.
    tau=sum((chi(r)*(acb(0,2)*arb.pi()*r/5).exp() for r in range(1,5)),acb(0))
    epsilon=tau/(acb(0,1)**int(chi.parity())*arb(5).sqrt())
    fe=[]
    for t in [F(-1,2),F(1,3),F(top)]:
        z=acb(-1,arb(str(t)))
        direct=completed(chi,z)
        transformed=epsilon*completed(conjugate,1-z)
        assert direct.overlaps(transformed)
        fe.append({'height':str(t),'direct':complex_encode(direct),'functional':complex_encode(transformed)})
    return {'zero_count':int(count),'winding':encode(winding),'winding_printed':winding.str(60),
            'character_exponents':expected,
            'right_argument_change':encode(right),'left_argument_change':encode(left),
            'bottom_argument_change':encode(bottom),'top_argument_change':encode(upper),
            'euler_disk_radius':encode(bound),'vertical_endpoints':points,'horizontal_segments':segments,
            'functional_equation_controls':fe,'epsilon':complex_encode(epsilon),
            'rectangle':{'left':'-1','right':'2','bottom':'-1/2','top':str(top)},
            'scope':'Completed primitive nonprincipal function: trivial L-zeros cancel gamma poles.'}


def refine(chi,lo,hi):
    original_lo,original_hi=lo,hi
    f0,f1=core.hardy(chi,lo),core.hardy(chi,hi)
    assert core.sign(f0)*core.sign(f1)==-1
    x0,x1=lo,hi
    delta=F(1,10**30)
    grid=2**128
    mode='secant_proposal_with_verified_bracket'
    for iteration in range(20):
        denominator=dyadic(f1.mid())-dyadic(f0.mid())
        if not denominator:break
        proposal=x1-dyadic(f1.mid())*(x1-x0)/denominator
        proposal=F(round(proposal*grid),grid)
        if not original_lo<proposal<original_hi:break
        a,b=proposal-delta,proposal+delta
        if original_lo<a<b<original_hi:
            fa,fb=core.hardy(chi,a),core.hardy(chi,b)
            if core.sign(fa)*core.sign(fb)==-1:
                lo,hi,f0,f1=a,b,fa,fb
                break
        x0,x1=x1,proposal
        f0,f1=f1,core.hardy(chi,proposal)
    else:
        iteration=20
    if hi-lo>2*delta:
        mode='bisection_fallback'
        lo,hi=original_lo,original_hi
        f0,f1=core.hardy(chi,lo),core.hardy(chi,hi)
        while hi-lo>2*delta:
            mid=(lo+hi)/2
            fm=core.hardy(chi,mid)
            if not core.sign(fm):
                mid=(3*lo+hi)/4;fm=core.hardy(chi,mid)
            assert core.sign(fm)
            if core.sign(fm)==core.sign(f0):lo,f0=mid,fm
            else:hi,f1=mid,fm
    rounded=core.decimal_midpoint(lo,hi)
    radius=F(1,2*10**20)
    assert F(rounded)-radius<lo<hi<F(rounded)+radius
    assert core.sign(f0)*core.sign(f1)==-1
    return {'lo':str(lo),'hi':str(hi),'lo_Z':f0.str(60),'hi_Z':f1.str(60),
            'lo_sign':core.sign(f0),'hi_sign':core.sign(f1),'rounded':rounded,
            'rounding_cell_radius':str(radius),'refinement_route':mode,'secant_iterations':iteration+1}


def generate(number,top,bits,count_only=False):
    ctx.prec=bits
    chi=dirichlet_char(5,number)
    counted=contour(chi,top)
    print(json.dumps({'event':'count','character':number,'top':top,'count':counted['zero_count'],
                      'horizontal_segments':len(counted['horizontal_segments'])}),flush=True)
    roots=[];scans=[]
    if not count_only:
        for denominator in [10,20,40,80]:
            lo=F(0);slo=core.sign(core.hardy(chi,lo));assert slo
            brackets=[]
            for j in range(1,denominator*top+1):
                hi=F(j,denominator);shi=core.sign(core.hardy(chi,hi));assert shi
                if shi!=slo:brackets.append((lo,hi))
                lo,slo=hi,shi
                if j%(denominator*250)==0:
                    print(json.dumps({'event':'scan_progress','character':number,'denominator':denominator,'height':str(hi),'brackets':len(brackets)}),flush=True)
            scans.append({'denominator':denominator,'brackets':len(brackets)})
            assert len(brackets)<=counted['zero_count']
            if len(brackets)==counted['zero_count']:break
        else:raise AssertionError('The scan did not match the certified count')
        for j,(lo,hi) in enumerate(brackets,1):
            root=refine(chi,lo,hi);root['index']=j;roots.append(root)
            if j%100==0:print(json.dumps({'event':'refined','character':number,'roots':j}),flush=True)
        assert all(F(a['hi'])<F(b['lo']) for a,b in zip(roots,roots[1:]))
    return {'status':'passed','source_sha256':sha(Path(__file__).read_bytes()),
            'core_sha256':sha(Path(core.__file__).read_bytes()),'recorded_utc':datetime.now(timezone.utc).isoformat(),
            'character':number,'modulus':5,'parity':int(chi.parity()),'top':top,'precision_bits':bits,
            'python_flint':flint.__version__,'flint':flint.__FLINT_VERSION__,
            'count_only':count_only,'contour':counted,'scans':scans,'root_intervals':roots,
            'scope':'Finite completed-function rectangle. Count matching disjoint brackets proves completeness and simplicity; no global GRH claim.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--character',type=int,choices=[2,3,4],required=True)
    parser.add_argument('--top',type=int,required=True)
    parser.add_argument('--precision',type=int,choices=[160,224],required=True)
    parser.add_argument('--count-only',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert args.top>0
    result=generate(args.character,args.top,args.precision,args.count_only)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'count':result['contour']['zero_count'],'roots':len(result['root_intervals'])}),flush=True)
