"""Certify actual A4 control fields that violate specific discriminant hypotheses."""
import argparse,hashlib,itertools,json,math
from pathlib import Path
import sympy as s
from sympy.polys.numberfields import round_two,galois_group
from dedekind_full_quartic_class import check_metadata

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rational_matrix(m):return [[str(v) for v in row] for row in m.tolist()]
def certify(coefficients,basis,expected_disc,cycle_prime,ramified_prime):
    x=s.symbols('x');poly=s.Poly.from_list(coefficients,x);basis=s.Matrix(basis)
    C=s.zeros(4)
    for j in range(4):
        r=s.rem(s.Poly(x**(j+1),x),poly)
        for i in range(4):C[i,j]=r.nth(i)
    def power_matrix(v):return sum((a*C**j for j,a in enumerate(v)),s.zeros(4))
    matrices=[basis.inv()*power_matrix(basis[:,j])*basis for j in range(4)]
    assert basis[:,0]==s.Matrix([1,0,0,0]) and all(v.q==1 for M in matrices for v in M)
    gram=s.Matrix(4,4,lambda i,j:s.trace(matrices[i]*matrices[j]));D=int(gram.det());assert D==expected_disc
    polynomial_disc=int(s.discriminant(poly));index=abs(int(1/basis.det()));assert polynomial_disc==D*index**2
    computed,computed_D=round_two(poly);assert computed_D==D
    conversion=basis.inv()*(computed.matrix.to_Matrix()/computed.denom);assert all(v.q==1 for v in conversion) and abs(conversion.det())==1
    checks=[];covered=0
    for prime in s.factorint(D):
        p=int(prime);representatives=[v for v in itertools.product(range(p),repeat=4) if any(v) and next(a for a in v if a)!=0 and next(a for a in v if a)==1]
        assert len(representatives)==(p**4-1)//(p-1);covered+=p**4-1
        for v in representatives:
            M=sum((a*T for a,T in zip(v,matrices)),s.zeros(4))/p
            char=list(M.charpoly().all_coeffs());newton=[s.Integer(1)];power=s.eye(4);traces=[]
            for k in range(1,5):
                power=power*M;traces.append(s.trace(power));newton.append(-sum(newton[k-j]*traces[j-1] for j in range(1,k+1))/k)
            assert char==newton
            bad=next((i for i,a in enumerate(char) if a.q!=1),None);assert bad is not None
            checks.append({'prime':p,'projective_numerators':v,'characteristic_coefficients':list(map(str,char)),'nonintegral_coefficient_index':bad,'Newton_trace_check':True})
    # Eisenstein or exhaustive rational linear/quadratic factor obstruction, independent of CAS irreducibility.
    assert poly.is_irreducible
    if coefficients==[1,-2,2,0,2]:
        assert all(a%2==0 for a in coefficients[1:]) and coefficients[-1]%4!=0
        assert s.expand((x*x-x)**2+x*x+2)==poly.as_expr();irred='Eisenstein at2';positive_lower=2
    else:
        assert coefficients==[1,0,0,8,12]
        for b in list(s.divisors(12))+[-d for d in s.divisors(12)]:
            assert poly.eval(b)!=0;d=12//b
            possible=[a for a in range(-8,9) if a*(d-b)==8 and b+d==a*a]
            assert not possible
        assert s.expand((x*x-2)**2+4*(x+1)**2+4)==poly.as_expr();irred='Rational roots and all monic quadratic factors excluded';positive_lower=4
    assert poly.count_roots(-s.oo,s.oo)==0 and math.isqrt(D)**2==D
    cycle_factors=s.Poly(poly,modulus=cycle_prime).factor_list()[1]
    assert D%cycle_prime and index%cycle_prime and sorted(f.degree() for f,e in cycle_factors)==[1,3] and all(e==1 and f.is_irreducible for f,e in cycle_factors)
    group,contained=galois_group(poly);assert contained and group.order()==12
    ramified_factors=s.Poly(poly,modulus=ramified_prime).factor_list()[1]
    assert index%ramified_prime and sorted([e,f.degree()] for f,e in ramified_factors)==[[1,1],[3,1]]
    metadata={'degree':4,'discriminant':D,'real_places':0,'complex_places':2};decision=check_metadata(metadata);assert not decision['A4_excluded_by_cubic_quotient_obstruction']
    return {'polynomial_coefficients':coefficients,'basis_columns_in_power_basis':rational_matrix(basis),'integral_multiplication_matrices':[rational_matrix(m) for m in matrices],
            'trace_gram':rational_matrix(gram),'polynomial_discriminant':polynomial_disc,'field_discriminant':D,'power_basis_index':index,
            'round_two_lattice_agreement':True,'projective_maximality_checks':checks,'all_nonzero_mod_prime_cosets_covered':covered,
            'independent_irreducibility_proof':irred,'sum_of_squares_positive_lower_bound':positive_lower,'signature':[0,2],
            'unramified_three_cycle_prime':cycle_prime,'unramified_factor_degrees':[1,3],'CAS_Galois_group_order':int(group.order()),'Galois_group':'A4',
            'ramified_prime':ramified_prime,'ramified_local_ef':[[1,1],[3,1]],'discriminant_exponent_at_ramified_prime':int(s.factorint(D)[ramified_prime]),
            'metadata_guard_result':decision,
            'scope':'Concrete number field with independently certified maximal order and A4 group. Integral multiplication, characteristic polynomial versus Newton traces and exhaustive projective nonintegrality cosets certify the proposed order; round_two checks its lattice separately.'}

def run():
    one=certify([1,-2,2,0,2],s.eye(4),3136,3,7)
    two=certify([1,0,0,8,12],[[1,0,0,0],[0,1,0,s.Rational(1,2)],[0,0,s.Rational(1,2),0],[0,0,0,s.Rational(1,4)]],5184,5,3)
    assert one['metadata_guard_result']['prime_factorization']==[[2,6],[7,2]]
    assert two['metadata_guard_result']['prime_factorization']==[[2,6],[3,4]]
    count=sum(len(c['projective_maximality_checks']) for c in [one,two]);covered=sum(c['all_nonzero_mod_prime_cosets_covered'] for c in [one,two]);assert count==470 and covered==2510
    return {'status':'passed','source_sha256':sha(Path(__file__)),'fields':[one,two],'projective_maximality_checks':count,'nonzero_residue_cosets_covered':covered,
            'scope':'Two genuine A4 quartic controls show why both the ramified-prime support and the small exponent at3 matter. D3136 introduces7 with tame cubic ramification; D5184 retains only2,3 but has exponent4 at3 with wild cubic ramification. Their square discriminants and signature match the square-class condition, not the exact576 metadata.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run();a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','control_fields':2,'maximality_checks':r['projective_maximality_checks'],'covered_cosets':r['nonzero_residue_cosets_covered']}))
