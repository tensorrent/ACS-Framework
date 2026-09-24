"""Normalized Weyl mass map for the maximal minimal Pati-Salam Yukawa sector.

L:(4,2,1), R:(bar4,1,2), n families. Phi -> UL Phi UR^dagger;
Delta_a -> O_ab UC* Delta_b UC*^T. Every fermion is left-handed.
M_LR = 1_color tensor [epsilon Phi Y + Phi* epsilon Z].
M_RR = sum_a Delta_a* tensor (epsilon sigma_a) tensor F, F^T=F.
L_Y=-1/2 psi^T M psi+h.c. Coordinates x+i y have metric G, as before.
"""
import numpy as np
from itertools import product
eps=np.array([[0,1],[-1,0]],complex)
sigma=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
spin=np.array([eps@s for s in sigma])
metric=np.array([2]*8+[g for a in range(3) for i in range(4) for j in range(i,4) for g in [2 if i==j else 4]*2])

def fields(x):
 P=np.array([x[i]+1j*x[i+1] for i in range(0,8,2)]).reshape(2,2)
 D=np.zeros((3,4,4),complex);v=8
 for a in range(3):
  for i in range(4):
   for j in range(i,4):D[a,i,j]=D[a,j,i]=x[v]+1j*x[v+1];v+=2
 return P,D

def mass(P,D,Y,Z,F):
 n=len(Y);LR=np.kron(np.eye(4),np.kron(eps@P,Y)+np.kron(P.conj()@eps,Z))
 RR=sum(np.kron(D[a].conj(),np.kron(spin[a],F)) for a in range(3))
 out=np.zeros((16*n,16*n),complex);out[:8*n,8*n:]=LR;out[8*n:,:8*n]=LR.T;out[8*n:,8*n:]=RR
 return out

def tensors(Y,Z,F):
 n=len(Y);out=np.zeros((68,16*n,16*n),complex)
 for a in range(68):
  x=np.zeros(68);x[a]=1;P,D=fields(x);out[a]=mass(P,D,Y,Z,F)
 return out

def yukawa_beta_tensors(T,g=(0.,0.,0.)):
 """16 pi^2 beta(T_a), ordered external Weyl indices retained explicitly."""
 n=T.shape[1]//16;Ti=T.conj().transpose(0,2,1);invg=1/metric
 left=np.einsum('a,aij,ajk->ik',invg,T,Ti,optimize=True)
 right=np.einsum('a,aij,ajk->ik',invg,Ti,T,optimize=True)
 trace=np.einsum('aij,bij->ab',T.conj(),T,optimize=True).real
 C=np.diag([15/8*g[0]**2+3/4*g[1]**2]*(8*n)+[15/8*g[0]**2+3/4*g[2]**2]*(8*n))
 result=[]
 for a in range(68):
  vertex=sum(invg[b]*(T[b]@Ti[a]@T[b]) for b in range(68))
  scalar=np.einsum('b,bij->ij',trace[a]*invg,T,optimize=True)
  result.append((left@T[a]+T[a]@right)/2+2*vertex+scalar-3*(C@T[a]+T[a]@C))
 return np.array(result)

def extract(B):
 n=B.shape[1]//16;LR=(B[0]-1j*B[1])/2;anti=(B[0]+1j*B[1])/2
 Y=-LR[n:2*n,8*n:9*n];Z=anti[:n,9*n:10*n]
 # Delta_0, color 00: epsilon sigma_0=diag(1,-1).
 F=B[8,8*n:9*n,8*n:9*n]
 return Y,Z,F

def candidates(Y,Z,F):
 Yd=Y.conj().T;Zd=Z.conj().T;Fd=F.conj().T
 return [Y@Yd@Y,Z@Zd@Y,Y@Zd@Z,Y@Fd@F,Y*np.trace(Yd@Y),Y*np.trace(Zd@Z),Z*np.trace(Zd@Y)]

def closed_beta(Y,Z,F,g=(0.,0.,0.)):
 """Filled with independently inferred and symbolically verified coefficients."""
 y=2*(Y@Y.conj().T@Y)-(Z@Z.conj().T@Y)-(Y@Z.conj().T@Z)+15/4*(Y@F.conj().T@F)
 z=2*(Z@Z.conj().T@Z)-(Y@Y.conj().T@Z)-(Z@Y.conj().T@Y)+15/4*(Z@F.conj().T@F)
 tr=np.trace(Y.conj().T@Y+Z.conj().T@Z)
 y+=4*tr*Y+8*np.trace(Z.conj().T@Y)*Z
 z+=4*tr*Z+8*np.trace(Y.conj().T@Z)*Y
 A=Y.conj().T@Y+Z.conj().T@Z
 f=A.T@F+F@A+15/2*(F@F.conj().T@F)+np.trace(F.conj().T@F)*F
 gy=45/4*g[0]**2+9/4*(g[1]**2+g[2]**2);gf=45/4*g[0]**2+9/2*g[2]**2
 return y-gy*Y,z-gy*Z,f-gf*F
