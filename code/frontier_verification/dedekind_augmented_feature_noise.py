"""Certify a shared noisy 22-feature release inside the exact local injectivity box."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,acb,ctx

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def run(certificate_path,audit_path):
    cert=json.loads(certificate_path.read_text());audit=json.loads(audit_path.read_text())
    assert cert['status']==audit['status']=='passed' and audit['inputs_sha256'][certificate_path.name]==sha(certificate_path)
    c=cert['collisions'][-1];ind=audit['cases']['Local'];assert c['dimension']==21 and c['both_observations_inside_injective_22_feature_neighborhood'] is True
    assert ind['local_memberships']==[True]*4 and F(c['critical_split_epsilon'])==F('1e-18')
    assert cert['rank_and_local_injectivity']['features'][-1]=={'kind':'gaussian','center':43,'a':'1/25'}
    assert c['contract']['included_unknown_tail'] is False and c['contract']['released_raw_coordinates'] is False
    boxes=[tuple(map(F,b)) for b in c['A_observed_coordinate_boxes']];B=list(map(F,c['B_fixed_observed_coordinates']))
    offset=F('-4.5e-18');tau=F('5e-18');assert abs(offset)<tau
    checks=[]
    for bits in [640,896]:
        ctx.prec=bits;u=arb(43).log();aa=[av(lo).union(av(hi)) for lo,hi in boxes];bb=list(map(av,B))
        for method in ['real_trigonometric','complex_exponential']:
            def g(x):return 2*(-x*x/25).exp()*(u*x).cos() if method=='real_trigonometric' else 2*acb(-x*x/25,u*x).exp().real
            a=sum((g(x) for x in aa),arb(0));b=sum((g(x) for x in bb),arb(0));delta=a-b
            error_a=av(offset)-delta;error_b=av(offset)
            assert delta<0 and abs(error_a)<av(tau) and abs(error_b)<av(tau)
            assert abs(delta)>av('1e-18') and abs(delta)<av('1e-17')
            checks.append({'precision_bits':bits,'method':method,'exact_feature_difference':enc(delta),'A_final_feature_error':enc(error_a),
                           'B_final_feature_error':enc(error_b),'A_strict_error_margin':enc(av(tau)-abs(error_a)),
                           'B_strict_error_margin':str(tau-abs(offset)),'feature_difference_display':float(delta.mid())})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [certificate_path,audit_path]},
            'root_coordinate_error_radius':c['radius'],'feature_release_error_bound':str(tau),'final_feature_offset_from_B':str(offset),
            'common_release':{'first_21_entries':'The exact 21-feature vector of the fixed rational B observation, which equals that of the certified A witness.',
                              'entry_22':'The exact center-43 Gaussian feature of B plus the specified rational offset.'},
            'contract':{'root_observations':'Inherited complete 22-entry source prefixes selected before bounded coordinate errors.',
                        'released_observables':cert['rank_and_local_injectivity']['features'],'additional_feature_errors':'Independent absolute error at most tau in each released component; this witness uses zero error in the first 21 components.',
                        'exact_feature_map_locally_injective':True,'both_root_observations_inside_certified_neighborhood':True,'raw_coordinates_or_counts_released':False,'unknown_tails_included':False},
            'checks':checks,'fixed_arithmetic_coefficients':audit['fixed_coefficients'],'ambiguous_arithmetic_coefficients':audit['ambiguous_coefficients'],
            'scope':'Exact 22-feature injectivity and noisy-release ambiguity are compatible because they use different observation contracts. The first 21 exact feature equalities come from the audited existence certificate; interval bounds prove the explicit last component is within tau of both actual features. No global optimal measurement error, physical precision model or unrecorded-tail equality is asserted.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['certificate','audit','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.certificate,a.audit);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'feature_error_bound':r['feature_release_error_bound'],'offset':r['final_feature_offset_from_B'],'arithmetic_ambiguities':r['ambiguous_arithmetic_coefficients']}))
