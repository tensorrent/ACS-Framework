"""Complete gauge-only degree<=4 invariants for Phi(1,2,2)+Delta(bar10,1,3)."""
import itertools,json,math
from collections import defaultdict
import numpy as np
import sympy as s

# Route 1: exact Weyl constant-term count of the polynomial character.
# SU4 weights use e4=-(e1+e2+e3); SU2 doublets have weights +/-1.
fund=[(1,0,0),(0,1,0),(0,0,1),(-1,-1,-1)]
phi=[(0,0,0,a,b) for a,b in itertools.product([-1,1],repeat=2)]
delta=[tuple(-fund[i][j]-fund[k][j] for j in range(3))+(0,t)
       for i in range(4) for k in range(i,4) for t in [-2,0,2]]
weights=phi+phi+delta+[tuple(-x for x in w) for w in delta]
zero=(0,)*5;chars=[defaultdict(int) for _ in range(5)];chars[0][zero]=1
for w in weights:
 for degree in range(1,5):
  for v,count in chars[degree-1].items():chars[degree][tuple(a+b for a,b in zip(v,w))]+=count
positive=[tuple(fund[i][j]-fund[k][j] for j in range(3))+(0,0) for i in range(4) for k in range(i+1,4)]
positive += [(0,0,0,2,0),(0,0,0,0,2)]
den={zero:1}
for root in positive:
 new=defaultdict(int,den)
 for v,c in den.items():new[tuple(a-b for a,b in zip(v,root))]-=c
 den={v:c for v,c in new.items() if c}
counts=[sum(c*char.get(tuple(-a for a in v),0) for v,c in den.items()) for char in chars]
assert counts==[1,0,4,0,17],counts

# Route 2: explicit invariant tensors. Delta is a Cartesian SU2 spin-one vector
# of complex symmetric colour matrices; its Frobenius metric is invariant.
pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
perms=list(itertools.permutations(range(4)))
def invariants(P,D):
 M=P.conj().T@P;n=float(np.trace(M).real);d=np.linalg.det(P);nd=float(np.sum(abs(D)**2))
 K=np.einsum('aij,bkl->abijkl',D,D);S=(K+K.swapaxes(0,1))/2;A=(K-K.swapaxes(0,1))/2
 C35=sum(S.transpose((0,1)+tuple(p+2 for p in perm)) for perm in perms)/24
 C20=S-C35
 norms=[]
 for C in [C35,C20]:
  trace=np.einsum('aaijkl->ijkl',C);spin0=np.einsum('ab,ijkl->abijkl',np.eye(3)/3,trace)
  norms.extend([float(np.sum(abs(spin0)**2)),float(np.sum(abs(C-spin0)**2))])
 norms.append(float(np.sum(abs(A)**2)))
 assert abs(sum(norms)-nd**2)<1e-9*max(1,nd**2)
 dets=[np.linalg.det(D[a]) for a in range(3)]
 hol=3*sum(dets)
 for a,b in itertools.combinations(range(3),2):hol+=(np.linalg.det(D[a]+D[b])+np.linalg.det(D[a]-D[b]))/2-dets[a]-dets[b]
 jp=np.array([np.trace(M@t/2).real for t in pauli])
 jd=np.array([(-1j*(np.vdot(D[(a+1)%3],D[(a+2)%3])-np.vdot(D[(a+2)%3],D[(a+1)%3]))).real for a in range(3)])
 out=[n*n,abs(d)**2,(d*d).real,(d*d).imag,n*d.real,n*d.imag,*norms,hol.real,hol.imag,
      n*nd,d.real*nd,d.imag*nd,float(jp@jd)]
 return np.array(out),np.array([n,d.real,d.imag,nd]),hol
rng=np.random.default_rng(20260911)
def unitary(n):
 Q=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))[0]
 return Q*np.exp(-1j*np.angle(np.linalg.det(Q))/n)
evaluations=[];gauge_errors=[];hol_errors=[]
for sample in range(40):
 P=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
 D=rng.normal(size=(3,4,4))+1j*rng.normal(size=(3,4,4));D=(D+D.transpose(0,2,1))/2
 vals,quad,hol=invariants(P,D);evaluations.append(vals)
 UL,UR,UC=unitary(2),unitary(2),unitary(4)
 O=np.array([[np.trace(a@UR@b@UR.conj().T).real/2 for b in pauli] for a in pauli])
 assert np.max(abs(O@O.T-np.eye(3)))<1e-12
 newD=np.einsum('ab,bij->aij',O,np.array([UC.conj()@v@UC.conj().T for v in D]))
 vv,qq,_=invariants(UL@P@UR.conj().T,newD)
 err=max(np.max(abs(vals-vv))/max(1,np.max(abs(vals))),np.max(abs(quad-qq))/max(1,np.max(abs(quad))))
 assert err<1e-12;gauge_errors.append(float(err))
 # Independent Gaussian Wick quadrature for the holomorphic invariant.
 nodes=[-math.sqrt(3),0,math.sqrt(3)];ws=[1/6,2/3,1/6];moment=0j
 for inds in itertools.product(range(3),repeat=3):
  X=sum(nodes[inds[a]]*D[a] for a in range(3));moment+=math.prod(ws[i] for i in inds)*np.linalg.det(X)
 assert abs(moment-hol)<1e-10;hol_errors.append(float(abs(moment-hol)))
E=np.array(evaluations);scaled=E/np.linalg.norm(E,axis=0)
singular=np.linalg.svd(scaled,compute_uv=False);assert singular[-1]>1e-3

# Route 3 for completeness is a representation decomposition:
# Sym^2(bar10 x spin1) = (bar35,spin0)+(bar35,spin2)
# +(20',spin0)+(20',spin2)+(bar45,spin1).
# Five inequivalent summands -> five (2,2) quartics. One holomorphic quartic
# and its conjugate -> seven real Delta quartics. Phi contributes six, mixed four.
assert 35+35*5+20+20*5+45*3==30*31//2

# Gauge fluctuations already generate an angular quartic. Derive the complete
# six-vector mass Gram matrix at an arbitrary real neutral Phi background.
a,b,gL,gR=s.symbols('a b gL gR',real=True)
P=s.diag(a,b);sig=[s.Matrix(t) for t in [[[0,1],[1,0]],[[0,-s.I],[s.I,0]],[[1,0],[0,-1]]]]
operators=[gL*t*P/2 for t in sig]+[-gR*P*t/2 for t in sig]
mass=s.Matrix(6,6,lambda i,j:s.simplify(2*s.re(s.trace(operators[i].conjugate().T*operators[j]))))
trace4=s.expand(s.trace(mass*mass));N=a*a+b*b
pred=s.expand((s.Rational(3,4)*(gL**4+gR**4)+s.Rational(1,2)*gL*gL*gR*gR)*N*N+4*gL*gL*gR*gR*a*a*b*b)
assert s.expand(trace4-pred)==0
numeric=[]
for angle in [0,math.pi/12,math.pi/4]:
 M=np.array(mass.subs({a:math.cos(angle),b:math.sin(angle),gL:.7,gR:.9}),float)
 val=float(np.sum(np.linalg.eigvalsh(M)**2));direct=float(pred.subs({a:math.cos(angle),b:math.sin(angle),gL:.7,gR:.9}))
 assert abs(val-direct)<1e-12;numeric.append({'beta':angle,'sum_vector_mass_fourth_powers':val})

print(json.dumps({'field_content':'complex Phi(1,2,2) and complex Delta(bar10,1,3), canonical linear gauge action; no extra global, CP or discrete symmetry imposed',
 'weyl_character_counts_by_degree':counts,'character_weight_counts':[len(c) for c in chars],
 'independent_decomposition':{'Phi_quartics':6,'Delta_quartics':7,'mixed_quartics':4,'quadratic_real_parameters':4,'cubic_invariants':0,
 'Delta_pair_irreps':[['bar35',0],['bar35',2],["20prime",0],["20prime",2],['bar45',1]]},
 'explicit_basis_order':['Nphi^2','|detPhi|^2','Re(detPhi)^2','Im(detPhi)^2','Nphi Re(detPhi)','Nphi Im(detPhi)',
 'norm(35,spin0)^2','norm(35,spin2)^2','norm(20prime,spin0)^2','norm(20prime,spin2)^2','norm(45,spin1)^2','Re holDelta4','Im holDelta4',
 'Nphi NDelta','Re(detPhi) NDelta','Im(detPhi) NDelta','Jphi_R dot JDelta_R'],
 'basis_completeness_boundary':'Exact dimension count plus representation decomposition gives completeness; random evaluation rank and gauge transforms check the explicit implementation. Numerical rank is not the proof of symbolic independence.',
 'evaluation_singular_values':singular.tolist(),'maximum_relative_gauge_error':max(gauge_errors),'holomorphic_Wick_check_error':max(hol_errors),
 'radiative_angular_term':{'vector_mass_matrix':str(mass),'trace_M4':str(s.factor(trace4)),'determinant_quartic_coefficient':'4*gL^2*gR^2','crosscheck':numeric,
 'constraint':'Gauge contributions alone are angle-dependent when gL*gR != 0. Gauge symmetry does not protect the claimed flat direction. Cancellation by additional contributions is a separate equation, not an invariant-theory exclusion.'},
 'remaining_boundary':'Coefficients, extra symmetry, Yukawa matrices, renormalization conditions and full coupled vacuum/RG selection are not fixed by enumerating the invariant basis.'},indent=2))
