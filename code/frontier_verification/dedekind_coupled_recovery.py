"""Couple positive Gaussian measurements with integer coefficient domains.

Every coefficient through X starts in {0,1,2,3,4}. Only spectral inequalities
remove candidates; there are no local degree partitions or power relations.
"""
import argparse,hashlib,json,math,time
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx


def sha(raw):return hashlib.sha256(raw).hexdigest()
def encode(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def decode(x):return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def support(limit):
    rows=[]
    for n in range(2,limit+1):
        p=next((d for d in range(2,math.isqrt(n)+1) if n%d==0),n)
        rest,k=n,0
        while rest%p==0:rest//=p;k+=1
        if rest==1:rows.append((n,p,k))
    return rows


def prepare(data,top,bits,delta='0'):
    ctx.prec=bits;delta=arb(delta);assert delta>=0
    assert data['degree']==4 and data['discriminant']==125 and data['prime_cutoff']==4096
    powers=support(data['prime_cutoff'])
    roots=[(F(r['hi']),arb(r['lo']).union(arb(r['hi']))) for r in data['roots']]
    selected=[r for hi,r in roots if hi<top]
    # This perturbation study preserves the certified membership at the cutoff.
    assert all((r+arb(0,delta.upper())).upper()<top for r in selected)
    assert all((r+arb(0,delta.upper())).lower()>top for hi,r in roots if hi>top)
    assert all((r+arb(0,delta.upper())).lower()>0 for r in selected)
    C=arb(3)/2+arb(125).log()/2-2*(2*arb.pi()).log()+2*arb(2).digamma()
    enlarged=[r+arb(0,delta.upper()) for r in selected]
    known=sum((3/(arb('9/4')+r*r) for r in enlarged),arb(0));U=C-known;assert U>0
    columns=[(n,p,k,arb(n).log(),arb(p).log()/arb(n).sqrt()) for n,p,k in powers]
    rows=[]
    for item in data['measurements']:
        if item['height']!=top:continue
        m,p=item['n'],item['prime'];a=arb(1)/item['denominator'];u=arb(m).log()
        scale0=arb(m).sqrt()/arb(p).log();scale=2*(arb.pi()*a).sqrt()*scale0
        weights=[]
        for n,q,k,v,w in columns:
            d,e=v-u,v+u
            weight=scale0*w*((-d*d/(4*a)).exp()+(-e*e/(4*a)).exp())
            assert weight>=0
            weights.append(weight)
        R0=scale*(arb(item['pole'])+arb(item['discriminant_term'])+arb(item['gamma'])-arb(item['finite_zero_sum']))
        phi=(4+top*top)*(-a*top*top).exp() if a*(4+top*top)>=1 else (4*a-1).exp()/a
        zero_error=scale*U*phi*(a/4).exp()*(u/2).cosh()
        # Uniform derivative bound for h(t)=exp(-a*t*t) cos(u*t).
        derivative=(2*a/arb(1).exp()).sqrt()+u
        input_error=2*scale*len(selected)*delta*derivative
        R=R0+arb(0,(zero_error+input_error).upper())
        y=arb(data['prime_cutoff']).log()-u-a;assert y>0
        prime_error=scale*8*(a/arb.pi()).sqrt()*(u/2+a/4-y*y/(4*a)).exp()*(1+(u+a)/y)
        metadata={**item,'R0':encode(R0),'R':encode(R),'zero_error':encode(zero_error),
                  'input_error':encode(input_error),'prime_error':encode(prime_error),'scale':encode(scale),
                  'weights_sha256':sha(canonical([encode(w) for w in weights]))}
        rows.append({'weights':weights,'R':R,'B':prime_error,'metadata':metadata})
    assert len(rows)==91
    return powers,rows,{'top':top,'precision_bits':bits,'delta':encode(delta),'count':len(selected),
                       'known_moment':encode(known),'unknown_moment_upper':encode(U)}


def eliminate(powers,rows):
    domains=[list(range(5)) for _ in powers];rounds=[]
    for round_number in range(1,4*len(powers)+2):
        removed={};old=[list(d) for d in domains]
        for j,row in enumerate(rows):
            weights,R,B=row['weights'],row['R'],row['B']
            low=sum((w*d[0] for w,d in zip(weights,old)),arb(0))
            high=sum((w*d[-1] for w,d in zip(weights,old)),arb(0))+B
            if R>high or R<low:
                return {'status':'inconsistent','round':round_number,'row':j,'reason':'complete row range excludes observation','rounds':rounds}
            for i,(w,d) in enumerate(zip(weights,old)):
                if len(d)==1:continue
                lo_without=low-w*d[0];hi_without=high-w*d[-1]
                for candidate in d:
                    key=(i,candidate)
                    if key in removed:continue
                    lo=lo_without+w*candidate;hi=hi_without+w*candidate
                    if R<lo:side='candidate_minimum_above_observation';gap=lo-R
                    elif R>hi:side='candidate_maximum_below_observation';gap=R-hi
                    else:continue
                    assert gap>0
                    removed[key]={'column':i,'n':powers[i][0],'candidate':candidate,'measurement_index':j,
                                  'measurement_target':row['metadata']['n'],'side':side,'strict_gap':encode(gap)}
        if not removed:break
        for i,c in removed:domains[i].remove(c)
        if any(not d for d in domains):return {'status':'inconsistent','round':round_number,'reason':'empty candidate domain','rounds':rounds,'removals':list(removed.values())}
        rounds.append({'round':round_number,'prior_domains_sha256':sha(canonical(old)),
                       'removals':list(removed.values()),'remaining_domains_sha256':sha(canonical(domains)),
                       'unique_target_coefficients':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),
                       'unique_support_coefficients':sum(len(d)==1 for d in domains)})
    else:raise AssertionError('Finite domains did not stabilize')
    return {'status':'passed','rounds':rounds,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
            'unique_target_coefficients':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),
            'unique_support_coefficients':sum(len(d)==1 for d in domains),
            'scope':'Monotone exclusion fixed point; surviving candidates are conservative, not a proof of joint integer feasibility.'}


def run(path,bits,heights,deltas):
    raw=path.read_bytes();data=json.loads(raw);results=[]
    for top in heights:
        for delta in deltas:
            start=time.monotonic();powers,rows,settings=prepare(data,top,bits,delta)
            result=eliminate(powers,rows);assert result['status']=='passed',result
            results.append({'settings':settings,'additional_radius':delta,'measurements':[r['metadata'] for r in rows],**result})
            print(json.dumps({'height':top,'delta':delta,'targets':result['unique_target_coefficients'],
                              'support':result['unique_support_coefficients'],'rounds':len(result['rounds']),
                              'elapsed_seconds':time.monotonic()-start}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__).read_bytes()),'input_sha256':sha(raw),'cases':results,
            'scope':'Only Gaussian measurements, coefficient integrality and 0..4 bounds; no local-power relations, residue classes or oracle coefficient seeds. Additional radius enlarges both the finite-sum error and moment bound.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--heights',type=int,nargs='+',default=[220,600,1000,1500,2000])
    p.add_argument('--deltas',nargs='+',default=['0']);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.input,a.precision,a.heights,a.deltas)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
