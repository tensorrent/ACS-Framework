"""Independent radical-basis arithmetic, Newton identities and local factor audit."""
import argparse, hashlib, itertools, json, math
from fractions import Fraction as F
from pathlib import Path
import sympy as sp


def product(A,B): return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def trace(A): return sum(A[i][i] for i in range(4))
def identity(): return [[F(i==j) for j in range(4)] for i in range(4)]
def combine(coefficients, matrices):
    return [[sum(c*M[i][j] for c,M in zip(coefficients,matrices)) for j in range(4)] for i in range(4)]
def determinant(A):
    total=F(0)
    for p in itertools.permutations(range(4)):
        inversions=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        total+=(-1)**inversions*math.prod(A[i][p[i]] for i in range(4))
    return total
def charpoly(A):
    powers=identity();traces=[None]
    for k in range(1,5):powers=product(powers,A);traces.append(trace(powers))
    elementary=[F(1)]
    for k in range(1,5):
        elementary.append(sum((-1)**(i-1)*elementary[k-i]*traces[i] for i in range(1,k+1))/k)
    return [(-1)**k*elementary[k] for k in range(5)]


def run(path):
    raw=path.read_bytes();data=json.loads(raw);x,T=sp.symbols('x T');rows=[];controls=[]
    for label,a in [('A',2),('B',-2)]:
        given=data['fields'][label]
        # Radical basis 1,v,u,uv, with u^2=a and v^2=-3.
        U=[[0,0,a,0],[0,0,0,a],[1,0,0,0],[0,1,0,0]]
        V=[[0,-3,0,0],[1,0,0,0],[0,0,0,-3],[0,0,1,0]]
        alpha=combine([F(1,2),F(1,2)],[identity(),V])
        matrices=[identity(),alpha,U,product(U,alpha)]
        gram=[[trace(product(A,B)) for B in matrices] for A in matrices]
        assert gram==given['trace_gram'] and determinant(gram)==given['field_discriminant']==576
        assert math.gcd(abs(4*a),3)==1 and (4*a)**2*(-3)**2==576
        tested=set()
        for case in given['maximal_order_coset_tests']:
            p=case['prime'];v=tuple(case['numerators']);tested.add((p,v))
            char=charpoly(combine([F(c,p) for c in v],matrices))
            assert char==list(map(F,case['characteristic_coefficients']))
            assert char[case['nonintegral_coefficient_index']].denominator>1
        assert tested=={(p,v) for p in [2,3] for v in itertools.product(range(p),repeat=4) if any(v)}
        assert len(tested)==95
        polynomials={}
        for c in [1,2]:
            theta=combine([1,c],[alpha,U]);coefficients=charpoly(theta)
            expression=(x*x-x+1+c*c*a)**2-c*c*a*(1-2*x)**2
            poly=sp.Poly(expression,x)
            assert list(map(F,poly.all_coeffs()))==coefficients
            polynomials[c]=poly
        assert list(map(int,polynomials[1].all_coeffs()))==given['primitive_polynomial_descending']
        assert polynomials[1].is_irreducible
        assert given['power_basis_index']**2*576==int(sp.discriminant(polynomials[1]))
        local=[]
        for entry in given['local_factors']:
            p=entry['prime'];selected=None
            for c,poly in polynomials.items():
                index_square=int(sp.discriminant(poly))//576
                index=math.isqrt(index_square);assert index*index==index_square
                if index%p: selected=(c,poly,index);break
            assert selected is not None
            c,poly,index=selected
            reduced=sp.Poly(poly,modulus=p);unit,factors=reduced.factor_list()
            back=sp.Poly(unit,x,modulus=p);model=[]
            for factor,e in factors:
                assert factor.is_irreducible;back*=factor**e;model.append([int(e),int(factor.degree())])
            assert back==reduced
            expected=[[entry['e'],entry['f']]]*entry['g'];assert sorted(model)==sorted(expected)
            inverse_euler=sp.prod((1-T**f) for e,f in model)
            character_euler=(1-T)*sp.prod(1-v*T for v in entry['quadratic_character_values'])
            assert sp.expand(inverse_euler-character_euler)==0
            local.append({'prime':p,'primitive_beta_multiplier':c,'order_index':index,'model':model,
                          'inverse_euler_polynomial':str(sp.expand(inverse_euler))})
        # These index primes are unramified in the field despite repeated polynomial factors.
        p=given['power_basis_index'];bad=sp.Poly(polynomials[1],modulus=p).factor_list()[1]
        assert any(e>1 for f,e in bad) and 576%p!=0
        controls.append({'field':label,'polynomial_index_prime':p,'field_unramified':True,
                         'naive_polynomial_model':[[int(e),int(f.degree())] for f,e in bad],
                         'correct_model':next(r['model'] for r in local if r['prime']==p)})
        assert sorted(given['quadratic_discriminants'])==sorted([4*a,-3,-12*a])
        rows.append({'field':label,'maximal_cosets_replayed':95,'local_factorizations':local,
                     'independent_trace_determinant':int(determinant(gram)),'coprime_discriminant_basis_route':[4*a,-3]})
    # Legendre calculations directly from squares, independent of Kronecker symbols.
    split=[]
    for label,a in [('A',2),('B',-2)]:
        roots_u=[r for r in range(7) if (r*r-a)%7==0]
        roots_v=[r for r in range(7) if (r*r+3)%7==0]
        split.append({'field':label,'sqrt_a_mod7':roots_u,'sqrt_minus3_mod7':roots_v})
    assert len(split[0]['sqrt_a_mod7'])==2 and split[1]['sqrt_a_mod7']==[]
    assert split[0]['sqrt_minus3_mod7']==split[1]['sqrt_minus3_mod7'] and len(split[0]['sqrt_minus3_mod7'])==2
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256(raw).hexdigest(),'maximal_order_cosets_replayed':190,
            'local_polynomial_factorizations':144,'field_audits':rows,'order_index_controls':controls,'mod7_square_controls':split,
            'nonisomorphism':'Different sets of quadratic subfields in Galois V4 extensions, independently witnessed by different splitting at seven.',
            'scope':'Exact Newton identities and radical-basis arithmetic verify maximal orders independently of the producer characteristic-polynomial calculation. Polynomial local factors are used only away from the selected power-basis index.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--arithmetic',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.arithmetic);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['status','maximal_order_cosets_replayed','local_polynomial_factorizations']}))
