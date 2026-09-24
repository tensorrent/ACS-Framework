"""Exact sparse quartics, integer coefficients after multiplying every invariant by 18.

Coordinates are unscaled complex entries x+i*y. Kinetic metric is 2 on Phi
and diagonal Delta coordinates, 4 on off-diagonal symmetric Delta coordinates.
Complex arithmetic here contains Gaussian integers only; every output is
checked to be an exactly representable real integer.
"""
from collections import defaultdict,Counter
from itertools import product,permutations,combinations
from pathlib import Path
import json,os,sys,math
import numpy as np

def add(*ps):
 d=defaultdict(complex)
 for p in ps:
  for m,c in p.items():d[m]+=c
 return {m:c for m,c in d.items() if c}
def scale(p,c):return {m:v*c for m,v in p.items() if v*c}
def mul(p,q):
 d=defaultdict(complex)
 for m,c in p.items():
  for n,v in q.items():d[tuple(sorted(m+n))]+=c*v
 return {m:c for m,c in d.items() if c}
def conj(p):return {m:c.conjugate() for m,c in p.items()}
def re(p):return {m:c.real for m,c in p.items() if c.real}
def im(p):return {m:c.imag for m,c in p.items() if c.imag}
def norm(p):return mul(conj(p),p)
def entry(i):return {(i,):1+0j,(i+1,):1j}
def sumps(ps):return add(*list(ps))
def det(M):
 out=[]
 for p in permutations(range(len(M))):
  sign=(-1)**sum(p[i]>p[j] for i in range(len(M)) for j in range(i+1,len(M)))
  q={():sign+0j}
  for i,j in enumerate(p):q=mul(q,M[i][j])
  out.append(q)
 return sumps(out)

def build():
 P=[[entry(2*(2*i+j)) for j in range(2)] for i in range(2)]
 D=[[[None]*4 for _ in range(4)] for _ in range(3)]
 metric=[2]*8;v=8
 for a in range(3):
  for i in range(4):
   for j in range(i,4):
    D[a][i][j]=D[a][j][i]=entry(v);v+=2;metric.extend([2 if i==j else 4]*2)
 N=sumps(norm(p) for row in P for p in row);d=det(P)
 nd=sumps(norm(D[a][i][j]) for a,i,j in product(range(3),range(4),range(4)))
 n2=mul(nd,nd)
 gram=[[sumps(mul(conj(D[a][i][j]),D[b][i][j]) for i,j in product(range(4),repeat=2)) for b in range(3)] for a in range(3)]
 gn=sumps(norm(gram[a][b]) for a,b in product(range(3),repeat=2))
 tn=sumps(mul(gram[a][b],gram[a][b]) for a,b in product(range(3),repeat=2))
 c35x6=defaultdict(complex);s35x9=defaultdict(complex)
 for a,b,i,j,k,l in product(range(3),range(3),range(4),range(4),range(4),range(4)):
  lhs=conj(mul(D[a][i][j],D[b][k][l]))
  rhs=sumps(mul(D[u][r][s],D[w][t][z]) for u,w in [(a,b),(b,a)] for r,s,t,z in [(i,j,k,l),(i,k,j,l),(i,l,j,k)])
  for m,c in mul(lhs,rhs).items():c35x6[m]+=c
  lhs=conj(mul(D[a][i][j],D[a][k][l]))
  rhs=sumps(mul(D[b][r][s],D[b][t][z]) for r,s,t,z in [(i,j,k,l),(i,k,j,l),(i,l,j,k)])
  for m,c in mul(lhs,rhs).items():s35x9[m]+=c
 # 18 * each projected norm; all expressions are integer polynomials.
 q0=scale(s35x9,2)
 q1=add(scale(c35x6,3),scale(q0,-1))
 q2=add(scale(tn,6),scale(q0,-1))
 q3=add(scale(n2,9),scale(gn,9),scale(c35x6,-3),scale(q2,-1))
 q4=add(scale(n2,9),scale(gn,-9))
 hol=scale(sumps(det(D[a]) for a in range(3)),18)
 for a,b in combinations(range(3),2):
  for sign in [-1,1]:hol=add(hol,scale(det([[add(D[a][i][j],scale(D[b][i][j],sign)) for j in range(4)] for i in range(4)]),9))
 M=[[sumps(mul(conj(P[i][j]),P[i][k]) for i in range(2)) for k in range(2)] for j in range(2)]
 # Twice J_phi: Tr(M sigma_a). J_delta=-i(<D_b,D_c>-<D_c,D_b>).
 jp2=[add(M[0][1],M[1][0]),scale(add(M[0][1],scale(M[1][0],-1)),1j),add(M[0][0],scale(M[1][1],-1))]
 jd=[scale(add(gram[(a+1)%3][(a+2)%3],scale(gram[(a+2)%3][(a+1)%3],-1)),-1j) for a in range(3)]
 polys=[scale(mul(N,N),18),scale(norm(d),18),scale(re(mul(d,d)),18),scale(im(mul(d,d)),18),scale(mul(N,re(d)),18),scale(mul(N,im(d)),18),q0,q1,q2,q3,q4,re(hol),im(hol),scale(mul(N,nd),18),scale(mul(re(d),nd),18),scale(mul(im(d),nd),18),scale(sumps(mul(jp2[a],jd[a]) for a in range(3)),9)]
 result=[]
 for p in polys:
  assert all(abs(c)<2**52 and complex(c).imag==0 and int(complex(c).real)==complex(c).real for c in p.values())
  result.append({m:int(complex(c).real) for m,c in p.items() if c})
 return result,metric

def eval_poly(p,x):return sum(c*math.prod(x[i] for i in m) for m,c in p.items())

if __name__=='__main__':
 ps,metric=build()
 # Independent prior projector evaluator, with no Weyl-count/CLI side effects.
 import ast
 old=Path(__file__).resolve().parents[1]/'support/scalar_invariant_basis.py'
 tree=ast.parse(old.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='invariants')
 env={'np':np,'itertools':__import__('itertools'),'math':math,'perms':list(permutations(range(4))),
 'pauli':[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]}
 exec(compile(ast.Module(body=[fn],type_ignores=[]),str(old),'exec'),env)
 rng=np.random.default_rng(20260916);errs=[]
 for _ in range(8):
  x=rng.integers(-2,3,size=68).tolist();P=np.array([x[i]+1j*x[i+1] for i in range(0,8,2)]).reshape(2,2);D=np.zeros((3,4,4),complex);v=8
  for a in range(3):
   for i in range(4):
    for j in range(i,4):D[a,i,j]=D[a,j,i]=x[v]+1j*x[v+1];v+=2
  expected=18*env['invariants'](P,D)[0];actual=np.array([eval_poly(p,x) for p in ps])
  err=float(np.max(abs(expected-actual)));assert err<1e-7,(err,expected-actual);errs.append(err)
 payload={'scale':18,'coordinate_convention':'unscaled complex x+i*y; kinetic 1/2 G_ab dx_a dx_b','kinetic_metric':metric,'quartics':[[[list(m),c] for m,c in sorted(p.items())] for p in ps]}
 out=Path(os.environ['ACS_ATTEMPT_DIR'])/'quartics.json';out.write_text(json.dumps(payload,separators=(',',':')))
 print(json.dumps({'monomial_counts':[len(p) for p in ps],'basis_scale':18,'independent_projector_max_absolute_errors':errs,'output':'quartics.json'}))
