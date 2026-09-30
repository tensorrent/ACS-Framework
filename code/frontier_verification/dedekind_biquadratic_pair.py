"""Exact arithmetic certificates for two fields sharing the analytic invariants."""
import argparse, hashlib, itertools, json, math
from fractions import Fraction
from pathlib import Path
import sympy as sp

FIELDS = {'A': {'a': 2, 'quadratic_discriminants': [8, -3, -24]},
          'B': {'a': -2, 'quadratic_discriminants': [-8, -3, 24]}}


def multiply(x, y, a):
    # Basis 1, alpha, beta, alpha beta; alpha^2=alpha-1, beta^2=a.
    out = [0]*4
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            s, t = i%2+j%2, i//2+j//2
            scale = a if t==2 else 1
            t %= 2
            for exponent, coefficient in ([(0,-1),(1,1)] if s==2 else [(s,1)]):
                out[exponent+2*t] += xi*yj*scale*coefficient
    return out


def matrix(v, a):
    basis = [[int(i==j) for i in range(4)] for j in range(4)]
    return sp.Matrix.hstack(*(sp.Matrix(multiply(v, b, a)) for b in basis))


def rat(q): return str(Fraction(int(sp.numer(q)), int(sp.denom(q))))


def field(label, spec):
    a = spec['a']; basis = [[int(i==j) for i in range(4)] for j in range(4)]
    mats = [matrix(b, a) for b in basis]
    gram = sp.Matrix(4,4,lambda i,j:sp.trace(mats[i]*mats[j]))
    discriminant = int(gram.det())
    assert discriminant == 576
    tests = []
    for p in [2,3]:
        for v in itertools.product(range(p), repeat=4):
            if not any(v): continue
            char = [sp.Rational(c) for c in (matrix(v,a)/p).charpoly().all_coeffs()]
            bad = next(i for i,c in enumerate(char) if c.q != 1)
            tests.append({'prime':p,'numerators':v,'characteristic_coefficients':list(map(rat,char)),
                          'nonintegral_coefficient_index':bad})
    assert len(tests)==95
    theta=[0,1,1,0]; powers=[basis[0]]
    for k in range(1,4): powers.append(multiply(powers[-1],theta,a))
    transition=sp.Matrix.hstack(*map(sp.Matrix,powers))
    index=abs(int(transition.det()))
    poly=matrix(theta,a).charpoly().as_poly()
    coefficients=list(map(int,poly.all_coeffs()))
    assert int(sp.discriminant(poly)) == discriminant*index**2
    assert index == (11 if label=='A' else 5)
    assert poly.count_roots(-sp.oo,sp.oo)==0
    # Character products encode the exact Euler factor, including ramified primes.
    Ds=spec['quadratic_discriminants']; local=[]; values=[]
    for p in sp.primerange(2,362):
        chi=[int(sp.kronecker_symbol(D,p)) for D in Ds]
        for k in range(1,13):
            values.append({'prime':int(p),'power':k,'n':int(p**k),'coefficient':1+sum(c**k for c in chi)})
        if p==2: e,f,g=2,2,1
        elif p==3: e,f,g=(2,2,1) if a==2 else (2,1,2)
        else:
            e=1;f=1 if all(c==1 for c in chi) else 2;g=4//f
        assert all((1+sum(c**k for c in chi))==(g*f if k%f==0 else 0) for k in range(1,13))
        local.append({'prime':int(p),'quadratic_character_values':chi,'e':e,'f':f,'g':g,
                      'coefficients_first_four':[1+sum(c**k for c in chi) for k in range(1,5)]})
    return {'label':label,'radicands':[a,-3], 'basis':['1','alpha','beta','alpha*beta'],
            'relations':{'alpha':'alpha^2-alpha+1=0','beta_square':a},
            'multiplication_matrices':[[list(map(int,m.row(i))) for i in range(4)] for m in mats],
            'trace_gram':[list(map(int,gram.row(i))) for i in range(4)], 'field_discriminant':discriminant,
            'maximal_order_coset_tests':tests,'primitive_element':'theta=alpha+beta',
            'primitive_polynomial_descending':coefficients,'polynomial_discriminant':int(sp.discriminant(poly)),
            'power_basis_index':index,'power_basis_columns':[list(map(int,transition.col(i))) for i in range(4)],
            'integral_basis_in_powers':[list(map(rat,transition.inv().col(i))) for i in range(4)],
            'degree':4,'signature':[0,2],'galois_group':'V4', 'quadratic_discriminants':Ds,
            'quadratic_character_conductors':sorted(map(abs,Ds)),
            'conductor_parity_pairs':sorted([[abs(D),int(D<0)] for D in Ds]),
            'local_factors':local, 'prime_power_coefficients':values}


def run():
    fields={name:field(name,spec) for name,spec in FIELDS.items()}
    assert fields['A']['quadratic_discriminants']!=fields['B']['quadratic_discriminants']
    differences=[]
    for x,y in zip(fields['A']['local_factors'],fields['B']['local_factors']):
        assert x['prime']==y['prime']
        if x['coefficients_first_four']!=y['coefficients_first_four']:
            differences.append({'prime':x['prime'],'A':x['coefficients_first_four'],'B':y['coefficients_first_four']})
    assert differences[0]['prime']==3 and next(r for r in differences if r['prime']==7)=={'prime':7,'A':[4,4,4,4],'B':[0,4,0,4]}
    contract={'candidate_labels':['A','B'],'degree':4,'signature':[0,2],'absolute_field_discriminant':576,
        'galois_group':'V4','ramified_prime_valuations':{'2':6,'3':2},'nontrivial_character_conductor_multiset':[3,8,24],
        'allowed_observation':'Unlabelled aggregate positive Dedekind-zero intervals through a declared cutoff, with certified multiplicities and completeness.',
        'not_supplied_as_observation':['defining polynomial of the observed field','quadratic subfield identities','factor-labelled zero lists','conductor-parity assignment','Euler coefficients'],
        'predeclared_measurement_grid':list(range(1,21)),
        'classification_scope':'Two explicitly certified candidate fields; no claim that they exhaust every quartic of discriminant 576.'}
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'fields':fields,'input_contract':contract,'differing_local_observables':differences,
            'scope':'Concrete nonisomorphic fields with shared permitted global inputs. Maximality is proved by all p-torsion coset integrality tests for p dividing the basis discriminant; a coprime-quadratic-discriminant theorem supplies another route. Finite spectral separation is a subsequent independent obligation.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run();a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'field_discriminants':[x['field_discriminant'] for x in r['fields'].values()],
                      'maximal_order_cosets':190,'differing_prime_observables':len(r['differing_local_observables'])}))
