#!/usr/bin/env python3
"""Finish the source's restored one-parameter TT fallback, without target fitting."""
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import brentq
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/input_closure'


def resolve_fallback_hierarchy():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    b=s.symbols('b',positive=True)
    # Divide every Yukawa magnitude by sqrt(2); ratios/Koide invariant.
    ys=[s.Integer(1),2*b,4*b*s.sqrt(1+b*b)]
    check('exact pair ratio bound expression',s.simplify((ys[2]/ys[1])**2-4*(1+b*b))==0)
    check('upper pair bound for b squared in [0,1]',s.simplify(8-(ys[2]/ys[1])**2)==4*(1-b*b))
    # Among any three positive numbers, the pair whose ratio is <=B either
    # is adjacent after sorting or brackets the third; at least one adjacent
    # ratio is then <=B. This suffices; no dense grid is the proof.
    masses=np.array([.51099895,105.6583755,1776.86]) # MeV, comparison inputs
    observed=np.sqrt(masses[1:]/masses[:-1]); bound=2*np.sqrt(2)
    check('both comparison lepton amplitude gaps exceed source pair bound',np.min(observed)>bound,
          {'comparison_adjacent_ratios':observed.tolist(),'source_uniform_bound':float(bound)})
    def numeric_y(beta):return np.sort(np.array([1.,2*beta,4*beta*np.sqrt(1+beta*beta)]))
    def koide(beta):
        y=numeric_y(beta);return np.sum(y*y)/np.sum(y)**2
    grid=np.geomspace(1e-8,1,2001)
    min_gaps=np.array([min(numeric_y(x)[1:]/numeric_y(x)[:-1]) for x in grid])
    check('finite grid independently checks uniform adjacent-ratio obstruction',max(min_gaps)<=bound,
          {'samples':len(grid),'largest_minimum_gap_sample':float(max(min_gaps))})
    check('zero b has two zero amplitudes',numeric_y(0).tolist()==[0.,0.,1.])
    # A Koide root exists, but it is not the observed hierarchy. No uniqueness claim.
    root=brentq(lambda x:koide(x)-2/3,1e-6,.1,xtol=1e-15)
    yy=numeric_y(root);ratios=yy[1:]/yy[:-1]
    check('one source-family Koide root exists',abs(koide(root)-2/3)<1e-13)
    check('Koide root does not match the two comparison ratios',np.max(abs(ratios/observed-1))>.1)
    mp.mp.dps=70
    def mpkoide(x):
        yy=[mp.mpf(1),2*x,4*x*mp.sqrt(1+x*x)]
        return sum(z*z for z in yy)/sum(yy)**2-mp.mpf(2)/3
    mroot=mp.findroot(mpkoide,(mp.mpf('.01'),mp.mpf('.1')))
    check('70-digit root confirms numerical root',abs(float(mroot)-root)<1e-13 and abs(mpkoide(mroot))<mp.mpf('1e-60'))
    report=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        exact_amplitudes=[str(x) for x in ys],comparison_masses_MeV=masses.tolist(),
        comparison_adjacent_amplitude_ratios=observed.tolist(),uniform_minimum_gap_upper_bound=float(bound),
        koide_root=str(mroot),koide_root_adjacent_ratios=ratios.tolist(),
        status='Normalized source fallback is nonzero but cannot yield the charged-lepton hierarchy under its stated mass~y^2 rule.',
        limits=['The chosen TT field family and fallback momentum projector are fixed source inputs.',
                'Other field families or an independent relative field scale are different hypotheses.',
                'This is not a no-go theorem for all ACS flavor models.'])
    (OUT/'fallback-resolution.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if report['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':
    resolve_fallback_hierarchy()
