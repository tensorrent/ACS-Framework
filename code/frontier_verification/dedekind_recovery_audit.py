"""Held-out polynomial arithmetic, independent numerics, and recovery mutations.

The decoder results are read and hashed before the arithmetic validator runs.
The validator never writes coefficients back to the decoder or its inputs.
"""
import argparse,ast,hashlib,itertools,json,math,time,warnings
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from flint import arb,ctx
from sympy import Poly,cyclotomic_poly,symbols


def sha(raw):return hashlib.sha256(raw).hexdigest()
def txt(x):return x.str(65)
def num(x):
    f=F(x);return mp.mpf(f.numerator)/f.denominator


def powers(limit):
    result=[]
    for n in range(2,limit+1):
        p=next((d for d in range(2,math.isqrt(n)+1) if n%d==0),n)
        rest,k=n,0
        while rest%p==0:rest//=p;k+=1
        if rest==1:result.append((n,p,k))
    return result


def ordered_models(ramified):
    # Independent enumeration: ordered compositions of degree, then all
    # divisors e of each composition part ef, finally remove permutations.
    def compositions(total):
        if total==0:yield ()
        for first in range(1,total+1):
            for tail in compositions(total-first):yield (first,)+tail
    models=set()
    for composition in compositions(4):
        choices=[[(e,v//e) for e in range(1,v+1) if v%e==0] for v in composition]
        for model in itertools.product(*choices):
            if any(e>1 for e,f in model)==ramified:models.add(tuple(sorted(model)))
    return models


def independent_gamma(a,u):
    normal=1/(4*mp.sqrt(mp.pi*a));g0=2*normal*mp.exp(-u*u/(4*a))
    def integrand(x):
        if x==0:return mp.mpf(0)
        g=normal*(mp.exp(-(x-u)**2/(4*a))+mp.exp(-(x+u)**2/(4*a)))
        if x<mp.mpf('0.001'):
            bx=x*u/(2*a)
            numerator=-g0*(mp.expm1(-x*x/(4*a))*mp.cosh(bx)+2*mp.sinh(bx/2)**2)
        else:numerator=g0-g
        return numerator/(2*mp.sinh(x/2))
    w=mp.sqrt(a)
    cuts=sorted(set([mp.mpf(0),mp.mpf('0.001'),mp.mpf('0.1'),mp.mpf(20),mp.mpf(100)] +
                    [u+j*w for j in [-24,-16,-8,-4,-2,0,2,4,8,16,24] if u+j*w>0]))
    return -4*(mp.euler+mp.log(8*mp.pi))*g0+4*mp.quad(integrand,cuts+[mp.inf])


def run(input_path,low_path,high_path,decoder_path):
    ctx.prec=256;mp.mp.dps=70
    raw_input=input_path.read_bytes();raw_low=low_path.read_bytes();raw_high=high_path.read_bytes()
    data,low,high=map(json.loads,[raw_input,raw_low,raw_high])
    source=decoder_path.read_bytes();source_hash=sha(source)
    assert low['source_sha256']==high['source_sha256']==source_hash
    assert low['input_sha256']==high['input_sha256']==sha(raw_input)
    tree=ast.parse(source)
    imports=sorted({n.names[0].name if isinstance(n,ast.Import) else n.module
                    for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))})
    assert all(x in ['argparse','hashlib','json','math','time','fractions','pathlib','flint'] for x in imports)
    modulo_expressions=sorted({ast.unparse(n) for n in ast.walk(tree) if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Mod)})
    assert modulo_expressions==['discriminant % p','k % f']
    high_by={r['n']:r for r in high['cases']}
    for r in low['cases']:
        if r['height']==2000:
            h=high_by[r['n']]
            assert r['denominator']==h['denominator'] and r['candidates']==h['candidates']
            assert arb(r['estimate']).overlaps(arb(h['estimate']))
    targets=powers(361);support=powers(4096)
    assert len(targets)==low['target_count']==high['target_count']==91
    assert len(support)==low['generic_prime_power_count']
    # The field polynomial is introduced only here, after frozen inference.
    x=symbols('x');phi=cyclotomic_poly(5,x);factorizations={};expected={}
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for p in sorted({p for n,p,k in targets}):
            unit,factors=Poly(phi,x,modulus=p).factor_list()
            product=Poly(unit,x,modulus=p)
            degrees=[]
            for f,e in factors:
                polynomial=Poly(f,x,modulus=p);product*=polynomial**e
                degrees.append((int(e),polynomial.degree()))
            assert product==Poly(phi,x,modulus=p) and sum(e*f for e,f in degrees)==4
            factorizations[p]={'factors':[{'polynomial':str(f),'multiplicity':int(e),'degree':Poly(f,x).degree()} for f,e in factors],
                               'ramification_residue_pairs':sorted(map(list,degrees))}
            for n,q,k in targets:
                if q==p:expected[n]=sum(f for e,f in degrees if k%f==0)
    comparisons=[]
    for r in low['cases']:
        c=expected[r['n']];assert c in r['candidates']
        comparisons.append({'n':r['n'],'height':r['height'],'expected':c,'candidates':r['candidates'],'retained':True})
    models_audit=[]
    for height,inference in low['inferences_by_height'].items():
        for p in inference['models']:
            models=ordered_models(p['ramified_from_discriminant'])
            assert models=={tuple(map(tuple,m)) for m in p['initial_models']}
            retained={model for model in models if all(sum(f for e,f in model if r['power']%f==0) in r['input_candidates'] for r in p['powers'])}
            assert retained=={tuple(map(tuple,m)) for m in p['retained_models']}
            for r in p['powers']:
                assert expected[r['n']] in r['candidates']
                assert r['candidates']==sorted({sum(f for e,f in m if r['power']%f==0) for m in retained})
            models_audit.append({'height':height,'prime':p['prime'],'enumerations_equal':True,'retained':len(retained)})
    evaluations={(r['n'],r['denominator']):r for r in low['evaluations']}
    mutations=[]
    for row in low['cases']:
        v=evaluations[row['n'],row['denominator']];s=arb(row['scale']);T=str(row['height'])
        R0=arb(row['unwidened_estimate']);E=arb(row['selected_budget']['scaled_zero_tail'])
        L=arb(row['selected_budget']['leakage_upper']);D=arb(row['diagonal_multiplier']);Z=arb(v['finite_sums'][T])
        variants={'omit_pole':(R0-s*arb(v['pole']),E,L),
                  'omit_gamma':(R0-s*arb(v['gamma']['enclosure']),E,L),
                  'omit_discriminant':(R0-s*arb(v['discriminant']),E,L),
                  'omit_negative_zeros':(R0+s*Z/2,3*E/2,L),
                  'reverse_zero_sign':(R0+2*s*Z,2*E,L),
                  'omit_zero_tail':(R0,arb(0),L),
                  'omit_leakage':(R0,E,arb(0))}
        tests={}
        for name,(center,error,leak) in variants.items():
            estimate=center+arb(0,error.upper())
            candidates=[c for c in range(5) if estimate.overlaps(c*D+arb(leak/2,leak.upper()/2))]
            tests[name]={'estimate':txt(estimate),'error_allowance':txt(error),'leakage_allowance':txt(leak),
                         'candidates':candidates,'true_coefficient_excluded':expected[row['n']] not in candidates}
        mutations.append({'n':row['n'],'height':row['height'],'expected':expected[row['n']],'variants':tests})
    mutation_counts={name:sum(r['variants'][name]['true_coefficient_excluded'] for r in mutations) for name in mutations[0]['variants']}
    # All final target estimates use a separately implemented prime-power
    # inventory, zero sum and gamma quadrature, with 70-digit mpmath arithmetic.
    roots=[(num(r['lo'])+num(r['hi']))/2 for r in data['positive_root_intervals']]
    high_eval={(r['n'],r['denominator']):r for r in high['evaluations']}
    cross=[];start=time.monotonic()
    for row in high['cases']:
        m,p=row['n'],row['prime'];a=mp.mpf(1)/row['denominator'];u=mp.log(m)
        v=high_eval[m,row['denominator']]
        zero=mp.fsum(2*mp.exp(-a*t*t)*mp.cos(u*t) for t in roots)
        gamma=independent_gamma(a,u)
        leak=mp.fsum(4*mp.log(q)/mp.log(p)*mp.sqrt(mp.mpf(m)/n)*
                     (mp.exp(-(mp.log(n)-u)**2/(4*a))+mp.exp(-(mp.log(n)+u)**2/(4*a)))
                     for n,q,k in support if n!=m)
        scale=2*mp.sqrt(mp.pi*a*m)/mp.log(p)
        pole=2*mp.exp(a/4)*mp.cosh(u/2)
        disc=mp.log(125)*mp.exp(-u*u/(4*a))/(2*mp.sqrt(mp.pi*a))
        estimate=scale*(pole+disc+gamma-zero)
        for label,enclosure,value in [('zero',v['finite_sums']['2000'],zero),('gamma',v['gamma']['enclosure'],gamma),
                                       ('leakage',row['selected_budget']['finite_leakage'],leak),
                                       ('estimate',row['unwidened_estimate'],estimate)]:
            assert arb(enclosure).contains(arb(mp.nstr(value,70))),(m,label,enclosure,mp.nstr(value,70))
        cross.append({'n':m,'denominator':row['denominator'],'zero_sum':mp.nstr(zero,70),'gamma':mp.nstr(gamma,70),
                      'finite_leakage':mp.nstr(leak,70),'unwidened_estimate':mp.nstr(estimate,70),'within_enclosures':True})
        print(json.dumps({'event':'independent_target','n':m,'elapsed_seconds':time.monotonic()-start}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__).read_bytes()),'decoder_sha256':source_hash,
            'inputs_sha256':{'zero_input':sha(raw_input),'160':sha(raw_low),'224':sha(raw_high)},
            'decoder_imports':imports,'decoder_modulo_expressions':modulo_expressions,
            'factorizations':factorizations,'holdout_comparisons':comparisons,'local_model_audit':models_audit,
            'independent_final_targets':cross,'mpmath_decimal_digits':70,'mutations':mutations,
            'mutation_exclusion_counts':mutation_counts,
            'scope':'Noncircular executable dataflow, not statistical blinding or recovery of an unknown field. Polynomial coefficients validate frozen candidates. Mpmath does not independently certify completeness.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['input','low','high','decoder','output']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=run(a.input,a.low,a.high,a.decoder);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'independent_targets':len(r['independent_final_targets']),
                      'mutation_exclusions':r['mutation_exclusion_counts']}))
