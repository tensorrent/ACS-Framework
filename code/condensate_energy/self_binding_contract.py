#!/usr/bin/env python3
"""Exact mechanism inequalities and the scope of a possible ACS identification."""
import hashlib
import json
from pathlib import Path

import sympy as s

from self_binding import ROOT,OUT


def main():
    c,f,v,g,lam,b=s.symbols('chi f v g lambda_chi b',real=True,positive=True)
    potential=lam*(c*c-v*v)**2/4+g*g*c*c*f*f/2+b*f**4/4
    square=lam*((c*c-v*v)+g*g/lam*f*f)**2/4+(b-g**4/lam)*f**4/4
    x,y,eps,phase=s.symbols('x y epsilon theta',real=True)
    symmetric=lam*(c*c-v*v)**2/4+g*g*c*c*(x*x+y*y)/2+b*(x*x+y*y)**2/4
    charge_source=s.simplify(y*s.diff(symmetric,x)-x*s.diff(symmetric,y))
    breaking=eps*(x*x-y*y)/2
    broken_source=s.expand(y*s.diff(breaking,x)-x*s.diff(breaking,y))
    left,right,phi=s.symbols('q_L q_R q_Phi',real=True)
    yukawa=s.linsolve([-left+phi+right,-left-phi+right],(left,right,phi))
    scale=s.symbols('a',positive=True)
    F=s.diag(1,-1,0,0)
    G=s.zeros(4);G[0,1]=1;G[1,0]=-1
    comm=F*G-G*F
    quadratic=s.expand(scale**2*s.trace((F-G).T*(F-G))-scale**4*s.trace(comm.T*comm))
    checks={
        'general_no_binding_square_identity':s.simplify(potential-g*g*v*v*f*f/2-square)==0,
        'phase_invariant_potential_has_zero_Noether_charge_source':charge_source==0,
        'explicit_phase_breaking_supplies_charge_source':s.simplify(broken_source-2*eps*x*y)==0,
        'both_bidoublet_Yukawas_force_zero_overall_Phi_phase_charge':list(yukawa)[0][2]==0,
        'historical_norm_proxy_quadratic_changes_with_unmatched_generator_scale':s.simplify(quadratic-(4*scale**2-8*scale**4))==0,
    }
    assert all(checks.values()),checks
    sources=[Path(__file__).resolve(),ROOT/'papers/core_trilogy/Palatini_Gauge_Attractor.tex',
             ROOT/'code/acs_codebase/extras/task2_lagrangian.py',
             ROOT/'code/acs_codebase/extras/higgs_potential.py',
             ROOT/'docs/frontier/2026-09-11/Branch_Catalog.json']
    result=dict(sympy=s.__version__,checks=checks,
                no_binding_condition='b >= g^4/lambda_chi implies E >= g v |Q|',
                charge_breaking_source=str(broken_source),
                bidoublet_phase_solutions=str(yukawa),historical_proxy_quadratic=str(quadratic),
                source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                ACS_embedding=dict(polynomial_ingredients='present in source scalar sector',
                                   reduced_field_identification='not established',
                                   conserved_charge='required; not automatically supplied by scalar norm terms',
                                   direct_overall_bidoublet_phase='obstructed if both displayed Yukawa couplings are nonzero',
                                   gauge_fields_and_other_scalar_directions='not included in reduced-model tests',
                                   dimensionful_scale='input, not predicted',
                                   generic_formation_from_zero_charge='not demonstrated or implied'))
    (OUT/'source-contract.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
