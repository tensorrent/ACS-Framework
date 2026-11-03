"""Elementary certificates for the quartic that defeats an unsupported Galois premise."""
import argparse,hashlib,itertools,json,math
from pathlib import Path

def remainder(a,b,p):
    a=[v%p for v in a];b=[v%p for v in b]
    while a and a[-1]==0:a.pop()
    while len(a)>=len(b):
        factor=a[-1]*pow(b[-1],-1,p)%p;shift=len(a)-len(b)
        for j,v in enumerate(b):a[j+shift]=(a[j+shift]-factor*v)%p
        while a and a[-1]==0:a.pop()
    return a

def multiply(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):out[i+j]+=u*v
    return out

def determinant(matrix):
    a=[list(r) for r in matrix];sign=1;previous=1;pivots=[]
    for k in range(len(a)-1):
        if a[k][k]==0:
            r=next(r for r in range(k+1,len(a)) if a[r][k])
            a[k],a[r]=a[r],a[k];sign=-sign
        pivot=a[k][k];pivots.append(pivot)
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator%previous==0
                a[i][j]=numerator//previous
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1],pivots

def run():
    f=[-1,-1,0,0,1];division=[]
    for degree in [1,2]:
        for coefficients in itertools.product(range(2),repeat=degree):
            divisor=list(coefficients)+[1];r=remainder(f,divisor,2);assert r
            division.append({'divisor_ascending_mod2':divisor,'remainder_ascending_mod2':r})
    assert len(division)==6
    linear=[-3,1];cubic=[-2,2,3,1];product=multiply(linear,cubic)
    assert [v%7 for v in product]==[v%7 for v in f]
    residues=[sum(v*t**j for j,v in enumerate(cubic))%7 for t in range(7)]
    assert all(residues)
    fd=list(reversed(f));gd=[4,0,0,-1]
    sylvester=[[0]*i+fd+[0]*(2-i) for i in range(3)]+[[0]*i+gd+[0]*(3-i) for i in range(4)]
    disc,pivots=determinant(sylvester);assert disc==-283
    trial=[{'divisor':d,'remainder':283%d} for d in range(2,math.isqrt(283)+1)]
    assert all(t['remainder'] for t in trial) and disc%7!=0
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'polynomial_ascending':f,'mod2_nondivisibility':division,
        'irreducibility_argument':'A reducible quartic over a field has a factor of degree one or two. All six monic candidates over F2 leave a nonzero remainder.',
        'mod7_linear_factor_ascending':linear,'mod7_cubic_factor_ascending':cubic,'integer_factor_product':product,
        'cubic_residues_at_0_through_6_mod7':residues,
        'cubic_irreducibility_argument':'A cubic over a field is reducible exactly when it has a root; all seven residues are nonzero.',
        'sylvester_matrix':sylvester,'bareiss_pivots':pivots,'polynomial_discriminant':disc,'trial_divisions_for_283':trial,
        'field_discriminant':disc,'maximal_order_argument':'The square of the order index divides the polynomial discriminant. Its absolute value is prime, so the index is one.',
        'unramified_prime':7,'local_residue_degrees':[1,3],'coefficient_at_7':1,
        'non_galois_argument':'In a Galois number-field extension every residue degree above a fixed rational prime is equal. The certified unramified degrees 1 and 3 contradict that condition.',
        'scope':'An elementary independent counterexample to imposing a Galois profile on a general quartic. It does not contradict the Galois property of the cyclotomic witness used in the recovery experiment.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run();a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'discriminant':r['polynomial_discriminant']}))
