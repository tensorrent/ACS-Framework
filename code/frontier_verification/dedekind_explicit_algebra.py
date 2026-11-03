"""Exact algebra and numerical controls for the explicit-formula derivation.

Symbolic identities do not by themselves prove the inequalities or analytic
identity; those premises and arguments are written in EXPLICIT_README.md.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
from flint import acb, arb, ctx


def audit():
    ctx.prec = 224
    x, t, v, a, u = s.symbols('x t v a u', positive=True)
    polynomial = x**4 + x**3 + x**2 + x + 1
    assert s.discriminant(polynomial, x) == 125
    numerator = v * (4 + t**2) - (v**2 + t**2)
    positive_form = v * (4 - v) + (v - 1) * t**2
    assert s.expand(numerator - positive_form) == 0
    derivative = s.diff((4 + t**2) * s.exp(-a * t**2), t)
    assert s.simplify(derivative - 2 * t * s.exp(-a*t**2) * (1 - a*(4+t**2))) == 0
    completed_square = v/2 - (v-u)**2/(4*a)
    assert s.expand(completed_square - (u/2+a/4-(v-u-a)**2/(4*a))) == 0
    majorant = s.log(x) * x**(-s.Rational(1, 2)) * s.exp(-(s.log(x)-u)**2/(4*a))
    log_slope = 1/s.log(x) - s.Rational(1, 2) - (s.log(x)-u)/(2*a)
    assert s.simplify(x*s.diff(majorant, x)/majorant - log_slope) == 0
    normal = 1/(4*s.sqrt(s.pi*a))
    g = normal*(s.exp(-(x-u)**2/(4*a))+s.exp(-(x+u)**2/(4*a)))
    assert s.simplify(s.diff(g,x).subs(x,0)) == 0
    h_fourier = s.integrate(s.exp(-a*x*x)*s.exp(s.I*u*x),(x,-s.oo,s.oo))
    assert s.simplify(h_fourier-s.sqrt(s.pi/a)*s.exp(-u*u/(4*a))) == 0

    gamma_checks = []
    for re, im in [('0.25','0.3'),('0.5','0'),('1','0'),('1.5','2'),('2','0'),('2','7')]:
        z = acb(re,im)
        primitive = acb(arb.pi())**(-z/2) * (z/2).gamma()
        for parity in [1,0,1]:
            primitive *= acb(5/arb.pi())**((z+parity)/2) * ((z+parity)/2).gamma()
        field = acb(125)**(z/2) * acb(2*arb.pi())**(-2*z) * z.gamma()**2
        ratio = primitive/field
        assert ratio.contains(20)
        gamma_checks.append({'s':str(z),'completed_gamma_ratio':ratio.str(60),'contains_20':True})
    half = arb('0.5')
    assert (half.digamma()+arb.const_euler()+2*arb(2).log()).contains(0)
    assert arb.const_euler()+2*arb(2).log()+2<4
    digamma_bounds = []
    for value in ['0','0.01','0.1','0.5','1','2','10','100','1000']:
        y=arb(value)
        psi=acb(half,y).digamma().real
        bound=4+2*y
        assert abs(psi)<bound
        digamma_bounds.append({'t':value,'real_digamma':psi.str(55),'bound':bound.str(55)})
    straddling=arb(11).log()-arb(11).log()
    assert not (straddling**2).is_finite() and (straddling*straddling).is_finite()
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'discriminant':125,'symbolic_identities':{
                'moment_numerator':str(positive_form), 'zero_tail_derivative':str(s.factor(derivative)),
                'completed_square':str(s.expand(completed_square)), 'prime_majorant_log_slope':str(log_slope),
                'gaussian_transform':str(s.simplify(h_fourier)), 'even_gaussian_derivative_at_zero':'0'},
            'gamma_duplication_controls':gamma_checks,'digamma_bound_controls':digamma_bounds,
            'runtime_straddling_power_control':{'generic_real_power_is_nonfinite':True,'multiplication_is_finite':True},
            'scope':'Exact polynomial/calculus identities plus finite numerical controls; see written analytic and inequality proofs.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=audit()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'symbolic_identities':len(result['symbolic_identities']),
                      'gamma_duplication_controls':len(result['gamma_duplication_controls']),
                      'digamma_bound_controls':len(result['digamma_bound_controls'])}))
