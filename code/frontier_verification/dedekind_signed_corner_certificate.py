"""Signed resolvents and a corner certificate for the full convex column family.

The mathematical implication from these numerical premises is derived in
SIGNED_CORNER_README.md. This program checks the premises; it is not a proof
assistant for the analytic/convexity bridge.
"""
import argparse, hashlib, json, zipfile
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from flint import arb, arb_mat, ctx
from dedekind_weighted_region_certificate import derivatives, av, enc, dyadic_upper, solve_exact
from dedekind_augmented_feature_audit import SPECS, input_geometry, modular_det

ROOT = Path(__file__).absolute().parents[2]
ANCHOR = 'docs/frontier/2026-09-14-aggregate-augmented-feature-delta/Augmented_Proposals_Local.json'
REGION = 'docs/frontier/2026-09-14-aggregate-weighted-feature-delta/Weighted_Region_Certificate.json'
UPPER = 'docs/frontier/2026-09-14-aggregate-variable-noise-delta/Variable_Noise_Certificate.json'
INPUTS = 'docs/frontier/2026-09-14-aggregate-equal-population-delta/Equal_Population_Inputs.zip'
N = 22
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def sign(x): return 1 if x > 0 else -1 if x < 0 else 0

def resolvent(R, region):
    B = [list(map(F, row)) for row in region['exact_nonnegative_majorant']]
    w = list(map(F, region['positive_rational_weights']))
    assert len(B) == len(w) == N and all(len(row) == N for row in B)
    assert all(x >= 0 for row in B for x in row) and all(x > 0 for x in w)
    assert all(sum(B[i][j]*w[j] for j in range(N)) < w[i]/2 for i in range(N))
    M = [[F(int(i == j))-B[i][j] for j in range(N)] for i in range(N)]
    row = solve_exact(list(map(list, zip(*M))), [F(int(i == 1)) for i in range(N)])
    CminusI = [row[i]-int(i == 1) for i in range(N)]
    assert all(x >= 0 for x in CminusI)
    assert all(sum(row[i]*M[i][j] for i in range(N)) == int(j == 1) for j in range(N))
    v = list(map(sign, R[1])); assert all(abs(x) == 1 for x in v)
    u0 = [sum(R[i][k]*v[k] for k in range(N)) for i in range(N)]
    h = solve_exact(M, list(map(abs, u0)))
    assert all(x > 0 for x in h)
    assert all(h[i]-sum(B[i][j]*h[j] for j in range(N)) == abs(u0[i]) for i in range(N))
    delta = [sum(CminusI[i]*abs(R[i][k]) for i in range(N)) for k in range(N)]
    margins = [abs(R[1][k])-delta[k] for k in range(N)]
    urad = [h[i]-abs(u0[i]) for i in range(N)]; assert all(x >= 0 for x in urad)
    intervals = [(u0[i]-urad[i], u0[i]+urad[i]) for i in range(N)]
    penalty = 2*sum(max(F(0), -x) for x in margins)
    K = h[1]+penalty; old = F(region['critical_inverse_bound'])
    gap = F(region['source_threshold_lower'])-F(region['root_coordinate_error_radius'])
    assert 0 < K < old and gap > 0
    return {'radius': region['radius'], 'positive_resolvent_critical_row': list(map(str, row)),
        'resolvent_minus_identity_row': list(map(str, CminusI)),
        'critical_inverse_row_deviation_bounds': list(map(str, delta)),
        'critical_inverse_row_sign_margins': list(map(str, margins)),
        'unresolved_row_sign_indices': [i for i, x in enumerate(margins) if x <= 0],
        'signed_R_times_v': list(map(str, u0)), 'signed_vector_supersolution': list(map(str, h)),
        'inverse_direction_intervals': [list(map(str, x)) for x in intervals],
        'sign_flip_penalty': str(penalty), 'signed_uniform_inverse_bound': str(K),
        'signed_bound_display': float(K), 'previous_inverse_bound': str(old),
        'signed_noise_guarantee_strictly_below': str(gap/K), 'signed_guarantee_display': float(gap/K)}

def curvature(c, R, resolved, bits):
    ctx.prec = bits; eta = F(1, 100)
    row = list(map(F, resolved['resolvent_minus_identity_row']))
    RR = arb_mat([[av(x) for x in r] for r in R])
    absR = arb_mat([[abs(RR[i, j]) for j in range(N)] for i in range(N)])
    point = [[derivatives(spec, av(x), 8) for x in c] for spec in SPECS]
    coefficients = [RR*arb_mat([[point[k][j][t+2] for j in range(N)] for k in range(N)]) for t in range(6)]
    high = arb_mat([[abs(derivatives(spec, av(x)+arb(0, av(eta).upper()), 8)[8]) for x in c] for spec in SPECS])
    remainder = absR*high*av(eta)**6/factorial(6)
    columns = []
    for j in range(N):
        rad = [sum((abs(coefficients[t][i,j])*av(eta)**t/factorial(t) for t in range(1,6)), arb(0))+remainder[i,j] for i in range(N)]
        perturb = sum((av(row[i])*(abs(coefficients[0][i,j])+rad[i]) for i in range(N)), arb(0))
        bound = coefficients[0][1,j]+arb(0, (rad[1]+perturb).upper())
        lo, hi = map(F, resolved['inverse_direction_intervals'][j])
        us = 1 if lo > 0 else -1 if hi < 0 else 0
        a = sign(bound); assert a != 0
        columns.append({'coordinate': j, 'curvature_factor_interval': enc(bound), 'curvature_sign': a,
            'inverse_direction_sign': us, 'endpoint_direction': -a*us})
    assert [x['coordinate'] for x in columns if x['inverse_direction_sign'] == 0] == [12]
    assert columns[12]['curvature_sign'] == -1
    return {'precision_bits': bits, 'columns': columns}

def point_corner(c, directions, v, bits):
    ctx.prec = bits; eta = F(1,100)
    reference = [x+eta*s for x,s in zip(c,directions)]
    assert reference[12] == c[12]
    def invert(y):
        J = arb_mat([[derivatives(spec,av(x),1)[1] for x in y] for spec in SPECS])
        d = J.det(); assert sign(d) != 0
        return J.inv(), d
    Y, d = invert(reference)
    u12 = sum((Y[12,k]*v[k] for k in range(N)), arb(0)); assert u12 < 0
    corner = list(reference); corner[12] = c[12]-eta
    Z, dc = invert(corner); assert sign(d) == sign(dc)
    assert [sign(Z[1,k]) for k in range(N)] == v
    K = sum((abs(Z[1,k]) for k in range(N)), arb(0)); ku = dyadic_upper(K,80)
    assert 0 < K < av(ku)
    return {'precision_bits': bits, 'face_reference_coordinates': list(map(str,reference)),
        'reference_determinant': enc(d), 'reference_direction_12': enc(u12),
        'corner_coordinates': list(map(str,corner)), 'corner_determinant': enc(dc),
        'corner_critical_inverse_row': [enc(Z[1,k]) for k in range(N)],
        'corner_norm': enc(K), 'corner_norm_upper': str(ku), 'corner_norm_display': float(K.mid())}

def run(root=ROOT):
    paths = [root/p for p in [ANCHOR, REGION, UPPER, INPUTS]]
    a, reg, upper = map(read,paths[:3])
    with zipfile.ZipFile(paths[3]) as z: data = {n:json.loads(z.read(n)) for n in z.namelist()}
    c, L, U = input_geometry(data)
    assert reg['status'] == upper['status'] == 'passed'
    assert a['full_rank_proposal']['features'] == SPECS and list(map(F,a['common_rational_coordinates'])) == c
    assert F(a['source_threshold_lower']) == L and F(a['source_threshold_upper']) == U
    R = [list(map(F,row)) for row in a['full_rank_proposal']['preconditioner']]
    assert len(R) == N and all(len(row) == N for row in R)
    detR = modular_det(R); v = list(map(sign,R[1])); r = U-F('1e-8'); gap = L-r
    assert gap > 0 and U-L == F('2e-30') and F(upper['contract']['root_coordinate_error_radius']) == r
    assert [x['radius'] for x in reg['regions']] == ['1/100','3/100']
    for x in reg['regions']:
        assert x['features'] == SPECS and x['domain'] == 'standard_coordinate_cube_centered_at_c'
        assert F(x['source_threshold_lower']) == L and F(x['root_coordinate_error_radius']) == r
    signed = [resolvent(R,x) for x in reg['regions']]
    assert signed[0]['unresolved_row_sign_indices'] == []
    checks = [curvature(c,R,signed[0],b) for b in [896,1152]]
    directions = [x['endpoint_direction'] for x in checks[0]['columns']]
    assert directions == [x['endpoint_direction'] for x in checks[1]['columns']]
    points = [point_corner(c,directions,v,b) for b in [1024,1536]]
    K = max(F(x['corner_norm_upper']) for x in points)
    assert 0 < K < F(signed[0]['signed_uniform_inverse_bound'])
    lower = gap/K; old = F(upper['uniform_identification_below']); high = F(upper['best_certified_tau_upper'])
    assert old < lower < high
    return {'status':'passed','source_sha256':sha(Path(__file__)), 'inputs_sha256':{p.name:sha(p) for p in paths},
        'contract':{k:v for k,v in upper['contract'].items() if k != 'common_release_type'},
        'matrix_family':'product_of_closed_convex_hulls_of_coordinate_derivative_curves',
        'secants_in_family':True, 'common_root_center':list(map(str,c)), 'critical_index':1,
        'critical_sign_vector':v, 'modular_preconditioner':detR, 'signed_regions':signed,
        'curvature_Taylor_orders':list(range(2,8)), 'curvature_remainder_derivative_order':8,
        'curvature_remainder_power':6, 'curvature_remainder_factorial':720,
        'uniform_curvature_checks':checks, 'corner_checks':points,
        'first_replacement_order':[i for i in range(N) if i != 12], 'last_replacement_coordinate':12,
        'last_replacement_direction':-1, 'last_direction_scope':'face_with_other_21_columns_at_certified_endpoints',
        'corner_uniform_inverse_bound':str(K), 'corner_bound_display':float(K),
        'uniform_identification_strictly_below':str(lower), 'guarantee_display':float(lower),
        'previous_uniform_guarantee':str(old), 'inherited_ambiguity_upper_endpoint':str(high),
        'upper_to_guarantee_ratio':str(high/lower), 'ratio_display':float(high/lower),
        'relative_guarantee_increase_display':float(lower/old-1),
        'entire_bridge_Lean_formalized':False,'optimal_source_feasible_threshold_proved':False,
        'scope':'Numerical premises for the written convex column-hull, inverse-difference and Cramer proof. This establishes a local uniform secant bound under inherited source/region premises. The corner maximizes the outer matrix-family norm; it need not be a source-feasible pair or the sharp ambiguity threshold. Both interval routes share FLINT.'}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=run();a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','corner_bound_display','guarantee_display','ratio_display']},indent=2))
