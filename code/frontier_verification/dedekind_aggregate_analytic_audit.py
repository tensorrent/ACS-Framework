"""Independent numerical sums, alternate gamma integrals and formula controls."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from flint import arb,ctx
from dedekind_coupled_recovery import decode,encode
from dedekind_explicit_crosscheck import mp_gamma,digamma_route


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def number(s):
    f=F(s);return mp.mpf(f.numerator)/f.denominator
def contains(encoded,value):return decode(encoded).contains(arb(mp.nstr(value,80)))


def run(measurements,inputs,integer_audit):
    ds=[json.loads(p.read_text()) for p in measurements];roots=[json.loads(p.read_text())['positive_root_intervals'] for p in inputs]
    truth=json.loads(integer_audit.read_text())['arithmetic_vectors'];mp.mp.dps=85;ctx.prec=256
    rows=[];variants=[];checks=0;alternates=[]
    assert len(ds[0]['rows'])==len(ds[1]['rows'])==17
    for index,row in enumerate(ds[1]['rows']):
        m=row['center'];a=mp.mpf(1)/row['denominator'];u=mp.log(m)
        p=next(c['prime'] for c in ds[1]['columns'] if c['n']==m)
        scale=2*mp.sqrt(mp.pi*a)*mp.sqrt(m)/mp.log(p)
        def g(x):return (mp.exp(-(x-u)**2/(4*a))+mp.exp(-(x+u)**2/(4*a)))/(4*mp.sqrt(mp.pi*a))
        gamma=mp_gamma(a,u);pole=2*mp.exp(a/4)*mp.cosh(u/2);disc=mp.log(576)*g(0)
        weights=[scale*2*mp.log(c['prime'])/mp.sqrt(c['n'])*g(mp.log(c['n'])) for c in ds[1]['columns']]
        for d in ds:
            r=d['rows'][index]
            assert r['center']==m and r['denominator']==row['denominator']
            assert arb(r['gamma']['enclosure']).contains(arb(mp.nstr(gamma,80)))
            assert contains(r['scale'],scale) and contains(r['pole'],pole) and contains(r['discriminant_term'],disc)
            for expected,value in zip(r['weights'],weights):assert contains(expected,value);checks+=1
        alt=digamma_route(arb(1)/row['denominator'],arb(m).log())
        assert arb(alt['enclosure']).overlaps(arb(row['gamma']['enclosure']))
        alternates.append({'center':m,'denominator':row['denominator'],**alt})
        for observation,label in enumerate(['A','B']):
            zero=mp.fsum(2*mp.exp(-a*t*t)*mp.cos(u*t) for r in roots[observation] for t in [(number(r['lo'])+number(r['hi']))/2])
            prime=mp.fsum(w*c for w,c in zip(weights,truth[label]));estimate=scale*(pole+disc+gamma-zero)
            for d in ds:
                r=d['rows'][index]['observations'][observation]
                assert contains(r['finite_sum'],zero) and contains(r['unwidened'],estimate)
            residual=estimate-prime;error=decode(row['observations'][observation]['zero_tail'])+decode(row['prime_tail'])
            assert arb(mp.nstr(abs(residual),80))<error
            rows.append({'center':m,'observation_index':observation,'held_out_field':label,'finite_zero_sum':mp.nstr(zero,80),
                         'scaled_prime_sum':mp.nstr(prime,80),'gamma':mp.nstr(gamma,80),'unwidened_estimate':mp.nstr(estimate,80),
                         'finite_formula_residual':mp.nstr(residual,80),'absolute_error_budget':encode(error),'inside_both_measurement_certificates':True})
            R=decode(row['observations'][observation]['R']);S=arb(mp.nstr(prime,80));B=decode(row['prime_tail'])
            shifts={'omit_negative_zeros':decode(row['scale'])*decode(row['observations'][observation]['finite_sum'])/2,
                    'omit_pole':-decode(row['scale'])*decode(row['pole']),
                    'omit_gamma':-decode(row['scale'])*arb(row['gamma']['enclosure']),
                    'old_discriminant_125':decode(row['scale'])*(arb(125).log()-arb(576).log())*arb(mp.nstr(g(0),80)),
                    'omit_gamma_normalization':decode(row['scale'])*4*(2*arb.pi()).log()*arb(mp.nstr(g(0),80))}
            for name,shift in shifts.items():
                changed=R+shift;rejected=not changed.overlaps(S+arb(B/2,B.upper()/2))
                variants.append({'center':m,'observation_index':observation,'mutation':name,'mutated_R':encode(changed),'rejected_by_held_out_formula':rejected})
        print(json.dumps({'event':'analytic_crosscheck','center':m,'observations':2,'gamma_routes':2}),flush=True)
    counts={name:sum(r['rejected_by_held_out_formula'] for r in variants if r['mutation']==name) for name in shifts}
    assert checks==20536 and all(v>0 for v in counts.values())
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in measurements+inputs+[integer_audit]},
            'mpmath_digits':85,'independent_weight_checks':checks,'finite_formula_cases':len(rows),'alternate_gamma_integrals':len(alternates),
            'cases':rows,'alternate_gamma':alternates,'mutated_measurements':variants,'mutation_rejection_counts':counts,
            'scope':'Independent mpmath midpoint sums and all weights checked against both precision enclosures; a different digamma integral checks every gamma term. This numerical route does not certify root completeness. Actual altered observation intervals are compared with held-out arithmetic; mutations that remain inside the error budget are reported, not called rejected.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--measurements',type=Path,nargs=2,required=True);p.add_argument('--inputs',type=Path,nargs=2,required=True)
    p.add_argument('--integer-audit',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.measurements,a.inputs,a.integer_audit);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'weight_checks':r['independent_weight_checks'],'formula_cases':r['finite_formula_cases'],'gamma_routes':r['alternate_gamma_integrals'],'mutations':r['mutation_rejection_counts']}))
