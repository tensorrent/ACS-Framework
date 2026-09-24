#!/usr/bin/env python3
"""Independent precision checks and controls for the recovered input proposals."""
import json
from pathlib import Path
import subprocess

import mpmath as mp
import numpy as np
from scipy.integrate import quad
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/input_closure'


def verify_selectors_independently():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    result=json.loads((OUT/'selector-results.json').read_text())
    mp.mp.dps=85
    f=mp.matrix([[1,mp.mpf('.3'),0,0],[0,-1,0,0],[0,0,0,0],[0,0,0,0]])
    g=mp.mpf('1.22')*mp.matrix([[0,0,0,0],[0,mp.mpf('.3'),1,0],[0,0,-mp.mpf('.3'),0],[0,0,0,0]])
    bases=[]
    for ds in [(1,-1,0,0),(0,1,-1,0),(1,1,-1,-1)]:bases.append(mp.diag(ds))
    for sign in [1,-1]:
        for i in range(4):
            for j in range(i+1,4):
                b=mp.zeros(4);b[i,j]=1;b[j,i]=sign;bases.append(b)
    def evaluate_i(matrix):
        c=matrix*g-g*matrix
        d=c*(matrix+g)-(matrix+g)*c
        return sum(x*x for x in matrix)-sum(x*x for x in c)+sum(x*x for x in d)
    def exact_mp(text):
        n,d=sp.fraction(sp.Rational(text));return mp.mpf(str(n))/mp.mpf(str(d))
    hh=mp.matrix([[exact_mp(x) for x in row] for row in result['curvature']['hessian_I']])
    gg=mp.matrix([exact_mp(x) for x in result['curvature']['gradient_I']])
    iv=evaluate_i(f)
    check('independent 85-digit invariant matches rational',abs(iv-exact_mp(result['curvature']['I_exact']))<mp.mpf('1e-80'))
    rng=np.random.default_rng(830921)
    errors=[]
    for j in range(12):
        direction=mp.matrix([int(n) for n in rng.integers(-3,4,size=15)])
        matrix=sum([direction[i]*bases[i] for i in range(15)],mp.zeros(4))
        first=mp.diff(lambda t:evaluate_i(f+t*matrix),0,1)
        second=mp.diff(lambda t:evaluate_i(f+t*matrix),0,2)
        squared=mp.diff(lambda t:evaluate_i(f+t*matrix)**2,0,2)
        expect_first=(direction.T*gg)[0];expect_second=(direction.T*hh*direction)[0]
        err=max(abs(first-expect_first),abs(second-expect_second),abs(squared-2*first**2-2*iv*expect_second))
        errors.append(float(err));check('independent directional derivatives '+str(j),err<mp.mpf('1e-72'))

    # Exact evaluation of the already-corrected source's claimed annihilation.
    aa,bb=sp.symbols('a b',real=True)
    h=sp.Matrix([[aa,bb,0,0],[bb,-aa,0,0],[0,0,0,0],[0,0,0,0]])
    kz=sp.diag(0,0,1,0);kt=sp.diag(1,0,0,0)
    comm=lambda a,b:a*b-b*a
    fallback=comm(kt,h);l2=comm(h,fallback);l3=comm(l2,h)+comm(l2,fallback)
    normsq=lambda x:sp.expand(sp.trace(x.T*x))
    q=aa**2+bb**2
    norms=[normsq(x) for x in [h,l2,l3]]
    predicted=[2*q,8*bb**2*q,32*bb**2*q*(aa**2+2*bb**2)]
    check('primary wave-direction selector vanishes for stated TT matrices',comm(kz,h)==sp.zeros(4))
    check('source fallback selector does not vanish identically',fallback!=sp.zeros(4))
    for i,(actual,wanted) in enumerate(zip(norms,predicted)):
        check('fallback exact BCH squared norm '+str(i+1),sp.expand(actual-wanted)==0)
    example=[float(x.subs({aa:sp.Rational(3,5),bb:sp.Rational(4,5)})) for x in norms]
    check('nondegenerate normalized fallback example',min(example)>0 and example[0]==2)

    # Project archive correlation: source values are inputs, not predictions.
    snap=OUT/'source-snapshots/physics-validation-export.txt'
    text=snap.read_text()
    first=text.split('// THERMODYNAMICS:')[0]
    replay=OUT/'attempts/export-quantum';replay.mkdir(parents=True,exist_ok=True)
    js=first+'\nconsole.log(JSON.stringify({quantumWallace,fineWallace,quantumFineCorr}));\n'
    (replay/'quantum-source-excerpt.js').write_text(js)
    # The excerpt has only Math, iteration and console output; no IO except stdout.
    run=subprocess.run(['node',str(replay/'quantum-source-excerpt.js')],capture_output=True,text=True,timeout=15)
    (replay/'stdout.txt').write_text(run.stdout);(replay/'stderr.txt').write_text(run.stderr)
    check('recovered JS quantum section runs',run.returncode==0)
    observed=json.loads(run.stdout.strip().splitlines()[-1]) if run.returncode==0 else {}
    phi=(1+np.sqrt(5))/2
    def wallace(values):
        logarithm=np.log(np.array(values)+1e-6)
        return phi*abs(logarithm)**phi*np.sign(logarithm)+1
    constants=np.array([6.626e-34,1.055e-34,1.602e-19,9.109e-31,1.673e-27,7.297e-3,5.292e-11,2.818e-15])
    x=wallace(constants*1e30);y=wallace((7.297e-3)**(np.arange(8)/2)*1e6)
    correlation=float(np.corrcoef(x,y)[0,1])
    check('independent NumPy reproduces source JS correlation',abs(observed.get('quantumFineCorr',10)-correlation)<1e-14)
    check('fine structure value already appears as source input',"'Fine structure α': 7.297e-3" in text)
    check('summary Kepler score is hardcoded',"domain: \"Kepler's Laws\", correlation: 0.999999" in text)
    # Convert every dimensional constant consistently from kg,m,s,C to g,cm,s,C.
    converted=constants*np.array([1e7,1e7,1,1e3,1e3,1,1e2,1e2])
    unitcorr=float(np.corrcoef(wallace(converted*1e30),y)[0,1])
    check('source correlation is not unit invariant',abs(unitcorr-correlation)>1e-4,
          dict(original=correlation,consistent_g_cm_s_C=unitcorr))
    # The fixed-p source derivative assertion cannot follow without K/domain.
    # An allowed smooth K=1 on [exp(2)-epsilon,exp(3)-epsilon] x [0,1]
    # gives strictly positive first AND second p derivatives for all p>0.
    # Changing variable u=log(lambda+epsilon) leaves Jacobian exp(u).
    derivative=quad(lambda u:np.exp(u)*u**phi*np.log(u),2,3,epsabs=1e-10)[0]
    second=quad(lambda u:np.exp(u)*u**phi*np.log(u)**2,2,3,epsabs=1e-10)[0]
    check('unspecified-kernel formula permits positive first derivative at phi',derivative>0)
    check('same allowed kernel contradicts asserted negative second derivative',second>0)
    # Logarithms of dimensional quantities require a reference with same units.
    # Adding a numerical rescaling doesn't supply a physically selected scale.
    report=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        independent_derivative_max_error=max(errors),
        fallback_selector=dict(squared_norms=[str(x) for x in predicted],normalized_example_squared_norms=example,
            verdict='Primary projector vanishes; implemented fallback does not. Historical blanket annihilation claim is too strong. This does not make the remaining target-fit a prediction.'),
        export_quantum=dict(source_correlation=correlation,converted_units_correlation=unitcorr,
            inputs='The source inserts both the dimensional constants and fine-structure value; no parameter-selection equation appears in this test.'),
        unspecified_kernel=dict(first_derivative_at_phi=derivative,second_derivative_at_phi=second,
            domain='u=log(lambda+epsilon) in [2,3], gamma in [0,1], K=1',
            limitation='Counterexample to an inference without kernel/domain hypotheses; not a theorem about every specified spectral-correlation kernel.'))
    (OUT/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=report['checks_passed'],
        failures=[c for c in checks if not c['passed']],fallback_selector=report['fallback_selector'],
        export_quantum=report['export_quantum'],unspecified_kernel=report['unspecified_kernel']),indent=2))
    if report['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':
    verify_selectors_independently()
