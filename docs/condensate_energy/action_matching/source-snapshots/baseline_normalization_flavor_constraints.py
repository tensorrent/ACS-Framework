"""Gauge/kinetic identifiability, Yukawa alignment, finite spin constraints."""
import itertools,json,math
import numpy as np
import sympy as s

T=s.diag(s.Rational(1,3),s.Rational(1,3),s.Rational(1,3),-1)
norm=s.sqrt(s.Rational(3,8));t=norm*T
assert s.trace(T*T)==s.Rational(4,3) and s.trace(t*t)==s.Rational(1,2)
assert s.simplify(t[0,0]-t[3,3]-s.sqrt(s.Rational(2,3)))==0
Z,lam,g0=s.symbols('Z lambda g0',positive=True)
normalization={'Tr_TBL2':str(s.trace(T*T)),'canonical_generator_scale':str(norm),
 'canonical_charge_gap':str(t[0,0]-t[3,3]),'gauge_coupling':'g_physical=g0/sqrt(Z_gauge)',
 'scalar_quartic':'lambda_physical=lambda_bare/Z_phi^2','constraint':'The algebra fixes charge ratios and commutators; an action metric/kinetic coefficient is required to fix canonical couplings.'}

# Exact inversion of the two-Yukawa map and its singular alignment branches.
k1,k2=s.symbols('k1 k2',real=True);mix=s.Matrix([[k1,k2],[k2,k1]])
assert s.factor(mix.det())==(k1-k2)*(k1+k2)
inverse=s.simplify(mix.inv());assert s.simplify(mix*inverse)==s.eye(2)
rng=np.random.default_rng(20260911);alignment=[]
for _ in range(12):
 h=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));ht=2*h/3
 Mu=.9*h+.4*ht;Md=.4*h+.9*ht
 Uu,_,_=np.linalg.svd(Mu);Ud,_,_=np.linalg.svd(Md);ckm=Uu.conj().T@Ud
 err=float(np.max(abs(abs(ckm)-np.eye(3))));assert err<2e-13
 alignment.append(err)
reconstruction=[]
for _ in range(12):
 Mu=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));Md=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
 a,b=.9,.4;h=(a*Mu-b*Md)/(a*a-b*b);ht=(a*Md-b*Mu)/(a*a-b*b)
 err=max(np.max(abs(a*h+b*ht-Mu)),np.max(abs(b*h+a*ht-Md)));assert err<2e-14
 reconstruction.append(float(err))
strongCP=[]
for phase in [.1,.4,.9]:
 h=np.diag([1,2,np.exp(1j*phase)]);Mu=(.9+2*.4/3)*h;Md=(.4+2*.9/3)*h
 arg=float(np.angle(np.linalg.det(Mu)*np.linalg.det(Md)));assert abs(arg-2*phase)<1e-14
 strongCP.append({'Yukawa_phase':phase,'arg_det_MuMd':arg,'bare_theta':0})

# General gauge one-loop coefficients under conventional canonical normalization.
# The field content is exactly Phi+Delta from the manuscript, with m PS families.
m=s.symbols('m',integer=True,positive=True)
beta={'SU4':s.Rational(-11,3)*4+s.Rational(2,3)*(2*m)+s.Rational(1,3)*9,
      'SU2L':s.Rational(-11,3)*2+s.Rational(2,3)*(2*m)+s.Rational(1,3),
      'SU2R':s.Rational(-11,3)*2+s.Rational(2,3)*(2*m)+s.Rational(1,3)*21}
assert beta=={'SU4':(4*m-35)/3,'SU2L':(4*m-21)/3,'SU2R':(4*m-1)/3}
# Independent explicit index of Sym^2 fundamental of SU4, using an orthonormal
# symmetric tensor basis and the induced generator t tensor I + I tensor t.
basis=[]
for i in range(4):
 for j in range(i,4):
  v=s.zeros(16,1);v[i*4+j]=1 if i==j else 1/s.sqrt(2)
  if i!=j:v[j*4+i]=1/s.sqrt(2)
  basis.append(v)
B=s.Matrix.hstack(*basis);tf=s.diag(s.Rational(1,2),-s.Rational(1,2),0,0)
rep=B.T*(s.kronecker_product(tf,s.eye(4))+s.kronecker_product(s.eye(4),tf))*B
assert s.trace(rep*rep)==3 and s.trace(tf*tf)==s.Rational(1,2)

# Finite Gauss/Hamiltonian branch: adding a fourth spin solves Gauss alone but
# not the same H_123 constraint. Six spins admit one joint zero state.
def perm(n,a,b):
 P=s.zeros(2**n)
 for j in range(2**n):
  bits=[(j>>(n-1-i))&1 for i in range(n)];bits[a],bits[b]=bits[b],bits[a]
  k=sum(v<<(n-1-i) for i,v in enumerate(bits));P[k,j]=1
 return P
def gauss(n):
 size=2**n;Jz=s.zeros(size);Jp=s.zeros(size)
 for j in range(size):
  bits=[(j>>(n-1-i))&1 for i in range(n)];Jz[j,j]=s.Rational(n-2*sum(bits),2)
  for a in range(n):
   if bits[a]:Jp[j-(1<<(n-1-a)),j]=1
 Jm=Jp.T;return Jz*Jz+(Jp*Jm+Jm*Jp)/2,Jz,Jp,Jm
spin=[]
for n in [3,4,6]:
 G,Jz,Jp,Jm=gauss(n);P12=perm(n,0,1);P23=perm(n,1,2);H=s.I*(P12*P23-P23*P12)/4
 assert G*H==H*G
 ng=len(G.nullspace());joint=2**n-s.Matrix.vstack(G,H).rank()
 spin.append({'spins':n,'Gauss_kernel_dimension':ng,'joint_Gauss_H123_kernel_dimension':joint})
 if n==6:
  v=s.zeros(64,1)
  for index in range(64):
   bits=[(index>>(5-i))&1 for i in range(6)];k=sum(bits[:3])
   if sum(bits[3:])==3-k:v[index]=s.Rational((-1)**k,2*math.comb(3,k))
  assert (v.T*v)[0]==1 and G*v==H*v==s.zeros(64,1)
  witness=[str(a) for a in v]
assert [(r['Gauss_kernel_dimension'],r['joint_Gauss_H123_kernel_dimension']) for r in spin]==[(0,0),(2,0),(5,1)]
def choose(n,k):return math.comb(n,k) if 0<=k<=n else 0
representation=[]
for n in range(2,13,2):
 singlet=choose(n,n//2)-choose(n,n//2-1)
 joint=choose(n-3,(n-6)//2)-choose(n-3,(n-8)//2) if n>=6 else 0
 representation.append({'spins':n,'singlets_from_spin_addition':singlet,'H123_joint_kernel_from_spin_3_over_2_coupling':joint})

# Connection principal symbol and equilibrium/stability are separate inputs.
e,ep,omega,omegap=s.symbols('e ep omega omegap',real=True)
torsion=(ep+omega*e)**2;curvature=omegap**2
assert s.diff(torsion,omegap,2)==0 and s.diff(curvature,omegap,2)==2
print(json.dumps({'normalization':normalization,
 'flavor':{'Yukawa_map_determinant':str(s.factor(mix.det())),'inverse':str(inverse),
 'proportional_Yukawa_max_CKM_error':max(alignment),'arbitrary_mass_reconstruction_error':max(reconstruction),
 'constraint':'A literal matrix lock tilde_h=(2/3)h forces alignment even with unequal VEVs. With independent matrices and k1^2!=k2^2, arbitrary Mu,Md are reconstructible, so the gauge algebra does not predict their flavor data.',
 'scope':'If the quoted ratio refers only to a scalar channel rather than the full matrices, that channel-to-matrix map remains to be supplied.'},
 'strong_CP_counterfamily':strongCP,
 'gauge_running':{'convention':'16*pi^2 beta(g_i)=b_i*g_i^3; complex scalar coefficient 1/3, left-Weyl coefficient 2/3',
 'coefficients':{k:str(v) for k,v in beta.items()},'at_three_families':{k:str(v.subs(m,3)) for k,v in beta.items()},
 'symmetric_SU4_index_exact_trace':str(s.trace(rep*rep)),
 'scope':'Gauge-only one-loop result for this explicit field content. Full scalar/Yukawa beta functions and threshold matching require the complete interactions and renormalization prescription.'},
 'finite_constraint_repair':{'direct_matrices':spin,'independent_spin_addition':representation,'six_spin_witness':witness,
 'proof':'H123 vanishes exactly on the symmetric spin-3/2 first triple. A total singlet then requires spin 3/2 in the remaining n-3 spins. This first occurs at n=6, with multiplicity one.',
 'boundary':'This repairs the stated finite Gauss plus H123 model. It is not a derivation of a full gravitational constraint algebra.'},
 'connection_dynamics':{'torsion_squared_toy':str(torsion),'connection_derivative_Hessian':str(s.diff(torsion,omegap,2)),
 'curvature_squared_derivative_Hessian':str(s.diff(curvature,omegap,2)),
 'second_route':'For T=de+omega wedge e, Fourier perturbations of omega enter algebraically; R=domega+omega wedge omega contains wave-number factors. T^2 alone cannot supply the missing connection kinetic principal part.',
 'equilibrium_boundary':'T=0 is shared by T_dot=-T and T_dot=+T; their opposite linear stability proves that an equilibrium constraint does not specify an attractor.'}},indent=2))
