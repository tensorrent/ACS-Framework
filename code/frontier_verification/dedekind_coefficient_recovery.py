"""Recover coefficient candidates from zeros without a splitting-coefficient oracle.

Inputs: a complete finite zero union, degree four, discriminant and signature.
All other prime-power coefficients are bounded by 0..4, without using residues
modulo the field conductor. Local partitions are a separate inference stage.
"""
import argparse,hashlib,json,math,time
from fractions import Fraction as F
from pathlib import Path
from flint import acb,arb,ctx

DENOMINATORS=[25,50,100,200,400,800,1200,1600,2000,3000,4000,6000,8000,10000,
              16000,24000,32000,48000,64000,96000,128000,192000,256000,384000,
              512000,768000,1024000]
X=4096
TARGET_LIMIT=361


def text(x):return x.str(65)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def widen(x,error):
    assert error>=0
    return x+arb(0,error.upper())


def prime_powers(limit):
    sieve=bytearray(b'\x01')*(limit+1);sieve[:2]=b'\x00\x00'
    for p in range(2,math.isqrt(limit)+1):
        if sieve[p]:sieve[p*p:limit+1:p]=b'\x00'*((limit-p*p)//p+1)
    rows=[]
    for p in range(2,limit+1):
        if sieve[p]:
            n,k=p,1
            while n<=limit:
                rows.append((n,p,k));n*=p;k+=1
    return sorted(rows)


def kernel(a,u,x):
    d,e=x-u,x+u
    return ((-d*d/(4*a)).exp()+(-e*e/(4*a)).exp())/(4*(arb.pi()*a).sqrt())


def zero_tail(a,u,top,U):
    if a*(4+top*top)>=1:phi=(4+top*top)*(-a*top*top).exp()
    else:phi=(4*a-1).exp()/a
    return U*phi*(a/4).exp()*(u/2).cosh()


def prime_tail(a,u):
    y=arb(X).log()-u-a
    assert arb(X).log()>2 and y>0
    return 8*(a/arb.pi()).sqrt()*(u/2+a/4-y*y/(4*a)).exp()*(1+(u+a)/y)


def gamma(a,u,bits):
    g0=kernel(a,u,arb(0));delta=arb('1e-20');end=180
    def integrand(x,analytic):
        if x.abs_upper()<arb('0.01'):
            bx=x*u/(2*a);sh=(bx/2).sinh()
            numerator=-g0*((-x*x/(4*a)).expm1()*bx.cosh()+2*sh*sh)
        else:numerator=g0-kernel(a,u,x)
        return numerator/(2*(x/2).sinh())
    cuts={F(v) for v in ['1e-20','0.01','0.1','0.5','1','2','3','4','5','6','8','12','20','40','80','180']}
    # Floats only propose exact rational integration breakpoints; interval
    # quadrature proves each entire segment regardless of proposal quality.
    center,width=float(u),math.sqrt(float(a))
    offsets=[-16,-8,-4,-2,-1,0,1,2,4,8,16] if bits==160 else [-18,-12,-6,-3,-1.5,0,1.5,3,6,12,18]
    for offset in offsets:
        x=F(round((center+offset*width)*10**12),10**12)
        if F('1e-20')<x<180:cuts.add(x)
    if bits>160:cuts.update(map(F,['0.03','0.3','1.5','2.5','3.5','4.5','5.5','7','10','30','60','120']))
    cuts=sorted(cuts);total=acb(0);segments=[]
    tolerance=arb('1e-29') if bits==160 else arb('1e-37')
    for lo,hi in zip(cuts,cuts[1:]):
        value=acb.integral(integrand,acb(str(lo)),acb(str(hi)),abs_tol=tolerance,rel_tol=tolerance,
                           eval_limit=100000,depth_limit=50)
        assert value.is_finite() and value.imag.contains(0),(str(a),str(u),lo,hi,value)
        total+=value
        segments.append({'lo':str(lo),'hi':str(hi),'real':text(value.real),'imag':text(value.imag)})
    constant=-4*(arb.const_euler()+(8*arb.pi()).log())*g0
    lower=3/(4*a*(arb.pi()*a).sqrt())*delta*delta
    upper=8*(g0+1/(2*(arb.pi()*a).sqrt()))*arb(-90).exp()/(1-arb(-180).exp())
    finite=constant+4*total.real
    return {'constant':text(constant),'finite_value':text(finite),'lower_tail':text(lower),
            'upper_tail':text(upper),'enclosure':text(widen(finite,lower+upper)),'segments':segments}


def local_models(degree,ramified):
    types=[(e,f) for e in range(1,degree+1) for f in range(1,degree+1) if e*f<=degree]
    def rec(left,start,chosen):
        if not left:
            if any(e>1 for e,f in chosen)==ramified:yield tuple(chosen)
            return
        for j in range(start,len(types)):
            e,f=types[j]
            if e*f<=left:yield from rec(left-e*f,j,chosen+[(e,f)])
    return list(rec(degree,0,[]))


def local_inference(rows,discriminant):
    result=[]
    for p in sorted({r['prime'] for r in rows}):
        relevant=[r for r in rows if r['prime']==p]
        models=local_models(4,discriminant%p==0)
        def coefficient(model,k):return sum(f for e,f in model if k%f==0)
        retained=[model for model in models if all(coefficient(model,r['power']) in r['candidates'] for r in relevant)]
        assert retained,('Inconsistent local models',p)
        result.append({'prime':p,'ramified_from_discriminant':discriminant%p==0,
                       'initial_models':[list(map(list,m)) for m in models],
                       'retained_models':[list(map(list,m)) for m in retained],
                       'powers':[{'n':r['n'],'power':r['power'],'input_candidates':r['candidates'],
                                  'candidates':sorted({coefficient(m,r['power']) for m in retained})}
                                 for r in relevant]})
    return result


def run(path,bits,heights):
    ctx.prec=bits;raw=path.read_bytes();data=json.loads(raw)
    assert data['status']=='passed' and data['degree']==4 and data['discriminant']==125
    assert data['real_places']==0 and data['complex_places']==2
    assert all(T in data['heights'] and T<=data['top'] for T in heights)
    roots=[(F(r['hi']),arb(r['lo']).union(arb(r['hi']))) for r in data['positive_root_intervals']]
    C=arb(3)/2+arb(125).log()/2-2*(2*arb.pi()).log()+2*arb(2).digamma()
    moments={}
    for T in heights:
        known=sum((3/(arb('9/4')+r*r) for hi,r in roots if hi<T),arb(0))
        U=C-known;assert U>0
        moments[T]={'known':text(known),'unknown_upper':text(U),'count':sum(hi<T for hi,r in roots)}
    powers=prime_powers(X);targets=[r for r in powers if r[0]<=TARGET_LIMIT]
    support=[(n,p,k,arb(n).log(),4*arb(p).log()/arb(n).sqrt()) for n,p,k in powers]
    reports=[];cache={};start=time.monotonic()
    for m,p,k in targets:
        u=arb(m).log();scale0=arb(m).sqrt()/arb(p).log();budgets={T:[] for T in heights}
        for denominator in DENOMINATORS:
            a=arb(1)/denominator;scale=2*(arb.pi()*a).sqrt()*scale0
            leak=arb(0)
            for n,q,j,v,weight in support:
                if n!=m:
                    d,e=v-u,v+u
                    leak+=scale0*weight*((-d*d/(4*a)).exp()+(-e*e/(4*a)).exp())
            prime_error=scale*prime_tail(a,u);leak_upper=(leak+prime_error).upper()
            for T in heights:
                ze=scale*zero_tail(a,u,T,arb(moments[T]['unknown_upper']))
                width=2*ze+leak_upper
                budgets[T].append({'denominator':denominator,'scaled_zero_tail':text(ze),
                                   'finite_leakage':text(leak),'prime_tail':text(prime_error),
                                   'leakage_upper':text(leak_upper),'planned_width_bound':text(width)})
        for T in heights:
            selected=min(budgets[T],key=lambda r:float(arb(r['planned_width_bound']).upper()))
            denominator=selected['denominator'];a=arb(1)/denominator;key=(m,denominator)
            scale=2*(arb.pi()*a).sqrt()*scale0
            if key not in cache:
                gam=gamma(a,u,bits)
                pole=2*(a/4).exp()*(u/2).cosh();disc=arb(125).log()*kernel(a,u,arb(0))
                sums={};running=arb(0);index=0
                for height in sorted(heights):
                    while index<len(roots) and roots[index][0]<height:
                        r=roots[index][1];running+=2*(-a*r*r).exp()*(u*r).cos();index+=1
                    sums[height]=text(running)
                cache[key]={'gamma':gam,'pole':text(pole),'discriminant':text(disc),'finite_sums':sums}
            values=cache[key];finite=arb(values['finite_sums'][T])
            R0=scale*(arb(values['pole'])+arb(values['discriminant'])+arb(values['gamma']['enclosure'])-finite)
            E=arb(selected['scaled_zero_tail']);R=widen(R0,E)
            D=1+(-u*u/a).exp();L=arb(selected['leakage_upper'])
            candidates=[c for c in range(5) if R.overlaps(c*D+arb(L/2,L.upper()/2))]
            assert candidates,('No viable coefficient',m,T,R,L)
            reports.append({'n':m,'prime':p,'power':k,'height':T,'denominator':denominator,
                            'scale':text(scale),'unwidened_estimate':text(R0),'estimate':text(R),
                            'diagonal_multiplier':text(D),'candidates':candidates,
                            'selected_budget':selected,'all_width_budgets':budgets[T]})
        print(json.dumps({'event':'target','n':m,'candidates_by_height':{r['height']:r['candidates'] for r in reports if r['n']==m},
                          'elapsed_seconds':time.monotonic()-start}),flush=True)
    inferences={}
    for T in heights:
        rows=[r for r in reports if r['height']==T]
        local=local_inference(rows,data['discriminant'])
        inferences[T]={'direct_unique':sum(len(r['candidates'])==1 for r in rows),
                       'local_unique':sum(len(r['candidates'])==1 for p in local for r in p['powers']),
                       'models':local}
    combined=[]
    for m,p,k in targets:
        candidates=set(range(5))
        for r in reports:
            if r['n']==m:candidates.intersection_update(r['candidates'])
        assert candidates
        combined.append({'n':m,'prime':p,'power':k,'candidates':sorted(candidates)})
    return {'status':'passed','source_sha256':sha(Path(__file__).read_bytes()),'input_sha256':sha(raw),
            'precision_bits':bits,'heights':heights,'target_limit':TARGET_LIMIT,'prime_cutoff':X,
            'target_count':len(targets),'generic_prime_power_count':len(powers),'denominators':DENOMINATORS,
            'constant_moment_upper':text(C),'moments':moments,'cases':reports,
            'evaluations':[{'n':m,'denominator':d,**v} for (m,d),v in sorted(cache.items())],
            'inferences_by_height':inferences,'combined_direct':combined,
            'combined_local':local_inference(combined,data['discriminant']),
            'scope':'Conditional on the stated field invariants, analytic identity and finite certificates; decoder uses no splitting formula or actual neighboring coefficients. Local inference uses only sum(e*f)=4 and ramification from the discriminant.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--heights',type=int,nargs='+',default=[220,600,1000,1500,2000])
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.input,a.precision,a.heights);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':len(r['cases']),
                      'unique':{T:(v['direct_unique'],v['local_unique']) for T,v in r['inferences_by_height'].items()}}),flush=True)
