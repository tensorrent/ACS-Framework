"""Gaussian explicit-formula measurements from a strict aggregate-only input."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coefficient_recovery import gamma,kernel,prime_powers
from dedekind_coupled_recovery import encode

KEYS={'degree','discriminant','real_places','complex_places','top','positive_root_intervals'}


def validate(data):
    if set(data)!=KEYS:raise ValueError('Only aggregate roots and common global invariants are accepted')
    assert data['degree']==4 and data['real_places']==0 and data['complex_places']==2
    assert type(data['discriminant']) is int and data['discriminant']>0 and type(data['top']) is int and data['top']>0
    roots=data['positive_root_intervals']
    assert all(set(r)=={'lo','hi'} and 0<F(r['lo'])<F(r['hi'])<data['top'] for r in roots)
    assert all(F(a['hi'])<F(b['lo']) for a,b in zip(roots,roots[1:]))


def run(paths,bits,limit,denominators):
    assert paths and 1<limit<4096 and denominators and all(type(d) is int and d>0 for d in denominators)
    ctx.prec=bits;datasets=[json.loads(p.read_text()) for p in paths]
    for data in datasets:validate(data)
    reference={k:datasets[0][k] for k in KEYS if k!='positive_root_intervals'}
    assert all({k:d[k] for k in reference}==reference for d in datasets)
    T=reference['top'];disc=reference['discriminant'];X=4096
    C=arb(3)/2+arb(disc).log()/2-2*(2*arb.pi()).log()+2*arb(2).digamma()
    roots=[[arb(r['lo']).union(arb(r['hi'])) for r in d['positive_root_intervals']] for d in datasets]
    moments=[]
    for rs in roots:
        known=sum((3/(arb('9/4')+r*r) for r in rs),arb(0));U=C-known;assert U>0
        moments.append({'known':encode(known),'unknown_upper':encode(U)})
    powers=prime_powers(X);centers=prime_powers(limit);rows=[]
    for m,p,k in centers:
        u=arb(m).log();scale0=arb(m).sqrt()/arb(p).log()
        for denominator in denominators:
            a=arb(1)/denominator;scale=2*(arb.pi()*a).sqrt()*scale0
            gam=gamma(a,u,bits);g=arb(gam['enclosure']);pole=2*(a/4).exp()*(u/2).cosh();D=arb(disc).log()*kernel(a,u,arb(0))
            weights=[]
            for n,q,j in powers:
                v=arb(n).log();d,e=v-u,v+u
                weights.append(scale0*arb(q).log()/arb(n).sqrt()*((-d*d/(4*a)).exp()+(-e*e/(4*a)).exp()))
            y=arb(X).log()-u-a;assert y>0 and arb(X).log()>2
            tail=scale*8*(a/arb.pi()).sqrt()*(u/2+a/4-y*y/(4*a)).exp()*(1+(u+a)/y)
            phi=(4+T*T)*(-a*T*T).exp() if a*(4+T*T)>=1 else (4*a-1).exp()/a
            measurements=[]
            for rs,moment in zip(roots,moments):
                U=arb(arb(tuple(moment['unknown_upper']['mid'])),arb(tuple(moment['unknown_upper']['rad'])))
                finite=2*sum(((-a*r*r).exp()*(u*r).cos() for r in rs),arb(0))
                zero_tail=scale*U*phi*(a/4).exp()*(u/2).cosh()
                estimate=scale*(pole+D+g-finite);R=estimate+arb(0,zero_tail.upper())
                measurements.append({'finite_sum':encode(finite),'unwidened':encode(estimate),'zero_tail':encode(zero_tail),'R':encode(R)})
            rows.append({'center':m,'denominator':denominator,'scale':encode(scale),'pole':encode(pole),'discriminant_term':encode(D),
                         'gamma':gam,'weights':[encode(w) for w in weights],'prime_tail':encode(tail),'observations':measurements})
        print(json.dumps({'event':'measurement_center','n':m,'rows':len(rows)}),flush=True)
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
            'precision_bits':bits,'global_inputs':reference,'center_limit':limit,'denominators':denominators,'prime_cutoff':X,
            'columns':[{'n':n,'prime':p,'power':k} for n,p,k in powers],
            'constant_moment_upper':encode(C),'moments':moments,'rows':rows,
            'scope':'Same Gaussian kernel and signature-specific gamma identity as the prior explicit-formula derivation; discriminant comes only from the input. Every prime-power coefficient starts in [0,4], and unknown-zero and prime tails are unconditional. No field classification, local-power relations or factor-labelled data are used.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,nargs='+',required=True);p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--center-limit',type=int,default=31);p.add_argument('--denominators',type=int,nargs='+',default=[25]);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.input,a.precision,a.center_limit,a.denominators);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'rows':len(r['rows']),'observations':len(a.input)}))
