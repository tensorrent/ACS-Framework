"""Executable full one-loop MS running for the declared unbroken minimal model.

V4=sum_{i=0}^{16} lambda_i Q_i/18; V2=mu0*Nphi+mu1*Re detPhi+
mu2*Im detPhi+mu3*NDelta. See quartics.json for exact basis/metric.
All returned values are derivatives with respect to log(mu_scale).
The mass parameters are dimensionful coefficients, not divided by scale^2.
"""
from pathlib import Path
import json
from fractions import Fraction
import numpy as np
from yukawa_model import closed_beta
ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def rational(x):return float(Fraction(str(x)))
S=read('scalar_coefficients.json');G=read('gauge_coefficients.json');M=read('mass_coefficients.json');YUK=read('yukawa_scalar_coefficients.json')
SC=np.array([[rational(x) for x in row] for row in S['coefficients']])
GC=np.array([[rational(x) for x in row] for row in G['gauge_quartic_coefficients']]);GL=np.array(G['gauge_linear_coefficients'])
def parse(x):
    x=str(x)
    if 'I' in x:return 1j*rational(x.replace('*I','').replace('I','1'))
    return rational(x)
def trace(word,mats):
    z=np.eye(len(mats['Y']),dtype=complex)
    for label in word:
        a=mats[label[0]]
        if label.endswith('^dag'):a=a.conj().T
        elif label.endswith('^T'):a=a.T
        elif label.endswith('^*'):a=a.conj()
        z=z@a
    return np.trace(z)
def correction(rows,mats,weights=None,key=None):
    ans=np.zeros(len(rows[0]['coefficients']),complex)
    for row in rows:
        t=trace(row['trace_word'],mats)
        if weights is not None:t*=weights[row[key]]
        ans+=t*np.array([parse(x) for x in row['coefficients']])
    if np.max(abs(ans.imag))>1e-10*max(1,np.max(abs(ans.real))):raise ArithmeticError('Nonreal scalar beta: check flavor input and coefficient provenance')
    return ans.real
def beta(lam,mu,g,Y,Z,F):
    lam=np.asarray(lam,float);mu=np.asarray(mu,float);g=np.asarray(g,float)
    Y,Z,F=[np.asarray(q,complex) for q in (Y,Z,F)];n=len(Y)
    if lam.shape!=(17,) or mu.shape!=(4,) or g.shape!=(3,):raise ValueError('Expected 17 quartics, 4 masses, 3 gauge couplings')
    if any(q.shape!=(n,n) for q in (Y,Z,F)) or not np.allclose(F,F.T,atol=1e-13,rtol=0):raise ValueError('Square equal-sized matrices and symmetric F required')
    mats=dict(Y=Y,Z=Z,F=F);g2=g*g
    quartic=SC@np.array([lam[a]*lam[b] for a,b in S['coupling_pairs']])+lam*(GL@g2)+GC@np.array([g2[a]*g2[b] for a,b in G['gauge_square_pairs']])
    quartic+=correction(YUK['fermion_box'],mats)+correction(YUK['quartic_wave'],mats,lam,'input_quartic')
    masses=sum((lam[r['quartic']]*mu[r['mass']]*np.array([rational(x) for x in r['output']]) for r in M['entries']),np.zeros(4))
    masses+=mu*np.array([-9*(g2[1]+g2[2])]*3+[-54*g2[0]-24*g2[2]])
    masses+=correction(YUK['quadratic_wave'],mats,mu,'input_mass')
    b=np.array([35/3-4*n/3,7-4*n/3,1/3-4*n/3]);by=closed_beta(Y,Z,F,g)
    return {'quartics':quartic/(32*np.pi**2),'masses':masses/(32*np.pi**2),'gauges':-b*g**3/(16*np.pi**2),'Y':by[0]/(16*np.pi**2),'Z':by[1]/(16*np.pi**2),'F':by[2]/(16*np.pi**2),'vacuum_constant':(8*mu[0]**2+2*mu[1]**2+2*mu[2]**2+60*mu[3]**2)/(32*np.pi**2)}
