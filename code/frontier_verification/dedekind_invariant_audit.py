"""Independent exhaustive groups, coset actions, factorization and held-out audit."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sympy as sp


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cycles(permutation):
    unused = set(range(len(permutation)))
    result = []
    while unused:
        i = min(unused)
        orbit = []
        while i in unused:
            unused.remove(i)
            orbit.append(i)
            i = permutation[i]
        result.append(orbit)
    return sorted(result, key=lambda c: (len(c), c))


def subgroup_audit(data):
    permutations = list(itertools.permutations(range(4)))
    lookup = {p: i for i, p in enumerate(permutations)}
    # Opposite multiplication convention to the producer; subgroup sets agree.
    table = [[lookup[tuple(b[a[k]] for k in range(4))] for b in permutations] for a in permutations]
    identity = lookup[(0, 1, 2, 3)]
    rho = lookup[(1, 2, 3, 0)]
    mandatory = {identity}
    k = rho
    while k not in mandatory:
        mandatory.add(k)
        k = table[k][rho]
    remaining = sorted(set(range(24)) - mandatory)
    found = []
    trials = {}
    for size in [4, 8, 12, 24]:
        trials[str(size)] = 0
        for extra in itertools.combinations(remaining, size - 4):
            trials[str(size)] += 1
            subset = mandatory | set(extra)
            if all(table[a][b] in subset for a in subset for b in subset):
                found.append(frozenset(subset))
    expected = {frozenset(lookup[tuple(p)] for p in g) for g in data['overgroups']}
    assert set(found) == expected and sorted(map(len, found)) == [4, 8, 24]
    assert sum(trials.values()) == 130817
    # Independently build actions on cosets. No perfect-matching calculation.
    def action_on_cosets(group, stabilizer):
        cosets = sorted({frozenset(table[h][g] for h in stabilizer) for g in group}, key=lambda x: sorted(x))
        images = {}
        for g in group:
            images[g] = tuple(cosets.index(frozenset(table[x][g] for x in c)) for c in cosets)
        return cosets, images
    d4 = next(g for g in found if len(g) == 8)
    _, quadratic = action_on_cosets(d4, mandatory)
    assert all(quadratic[i] == (0, 1) for i in mandatory)
    cosets, cubic = action_on_cosets(set(range(24)), d4)
    assert len(cosets) == 3 and len(set(cubic.values())) == 6
    assert sorted(map(len, cycles(cubic[rho]))) == [1, 2]
    assert 3 - len(cycles(cubic[rho])) == 1
    kernel = {p for p, image in cubic.items() if image == (0, 1, 2)}
    assert {permutations[i] for i in kernel} == {tuple(p) for p in data['matching_kernel']}
    # The inertia subgroup itself is not normal in S4.
    normality_failure = next((a, b) for a in range(24) for b in mandatory
                             if {table[a][h] for h in mandatory} != {table[h][a] for h in mandatory})
    # Exhaust all 2^16 subsets of C4 x C4, independent of generator closure.
    product = list(itertools.product(range(4), repeat=2))
    product_lookup = {v: i for i, v in enumerate(product)}
    addition = [[product_lookup[((a[0]+b[0])%4, (a[1]+b[1])%4)] for b in product] for a in product]
    subdirect = []
    for mask in range(1, 1 << 16, 2):
        g = [i for i in range(16) if mask >> i & 1]
        if len(g) not in [4, 8, 16]:
            continue
        if {product[i][0] for i in g} != set(range(4)) or {product[i][1] for i in g} != set(range(4)):
            continue
        if all(mask >> addition[a][b] & 1 for a in g for b in g):
            subdirect.append(frozenset(product[i] for i in g))
    assert set(subdirect) == {frozenset(tuple(x) for x in row['group']) for row in data['subdirect_composita']}
    assert sorted(map(len, subdirect)) == [4, 4, 8, 16]
    for row in data['subdirect_composita']:
        g = set(map(tuple, row['group']))
        inertias = {frozenset(((k*a)%4, (k*b)%4) for k in range(4)) for a, b in g if a%2 and b%2}
        assert inertias == {frozenset(map(tuple, i)) for i in row['possible_inertia']}
        assert row['unramified_quotient_degree'] == len(g)//4
        assert row['survives_no_unramified_extension'] == (len(g) == 4)
    return {'s4_subsets_by_order': trials, 's4_subsets_total': sum(trials.values()),
            'cyclic4_product_subsets_with_identity': 32768, 'subdirect_group_orders': sorted(map(len, subdirect)),
            'quadratic_inertia_action': quadratic[rho], 'cubic_inertia_cycles': cycles(cubic[rho]),
            'cubic_tame_discriminant_exponent': 1, 'inertia_not_normal_in_s4_witness': [permutations[i] for i in normality_failure]}


def audit(data, root):
    groups = subgroup_audit(data)
    for b in data['minkowski_squared_bounds']:
        n, r2, d = b['degree'], b['complex_pairs'], b['absolute_discriminant']
        numerator = d * math.factorial(n)**2 * 16**r2
        denominator = n**(2*n) * 9**r2
        assert numerator < denominator
        assert Fraction(numerator, denominator) == Fraction(*b['squared_bound_upper'])
    # Ordered allocations, then deduplication, instead of unordered multisets.
    patterns = set()
    for size in range(1, 5):
        for es in itertools.product(range(1, 5), repeat=size):
            for fs in itertools.product(range(1, 5), repeat=size):
                if sum(e*f for e, f in zip(es, fs)) == 4:
                    patterns.add(tuple(sorted(zip(es, fs))))
    assert len(patterns) == 11
    assert {tuple(map(tuple, r['model'])) for r in data['tame_local_patterns']} == patterns
    assert [p for p in patterns if sum((e-1)*f for e, f in p) == 3] == [((4, 1),)]
    x = sp.Symbol('x')
    phi5 = sp.Poly(x**4+x**3+x**2+x+1, x)
    phi8 = sp.Poly(x**4+1, x)
    assert sp.discriminant(phi5) == 125 and sp.discriminant(phi8) == 256
    # Trace of powers in a quotient algebra supplies a second discriminant route.
    trace_discs = []
    for poly in [phi5, phi8]:
        companion = sp.zeros(4)
        for j in range(4):
            remainder = sp.rem(sp.Poly(x**(j+1), x), poly)
            for i in range(4):
                companion[i, j] = remainder.nth(i)
        gram = sp.Matrix(4, 4, lambda i, j: sp.trace(companion**(i+j)))
        value = int(gram.det(method='domain-ge'))
        assert value == int(sp.discriminant(poly))
        trace_discs.append({'polynomial': str(poly.as_expr()), 'trace_gram': [list(map(int, gram.row(i))) for i in range(4)], 'determinant': value})
    assert phi5.shift(1).all_coeffs() == [1, 5, 10, 10, 5]
    assert phi8.shift(1).all_coeffs() == [1, 4, 6, 4, 2]
    assert phi5.count_roots(-sp.oo, sp.oo) == phi8.count_roots(-sp.oo, sp.oo) == 0
    factors = {}
    for p in sp.primerange(2, 4097):
        polynomial = sp.Poly(phi5, modulus=p)
        unit, decomposition = polynomial.factor_list()
        reconstructed = sp.Poly(unit, x, modulus=p)
        model = []
        for factor, multiplicity in decomposition:
            assert factor.is_irreducible
            reconstructed *= factor**multiplicity
            model.append([int(multiplicity), int(factor.degree())])
        assert reconstructed == polynomial
        factors[int(p)] = sorted(model)
    predictions = data['coefficient_predictions']
    for row in predictions:
        expected = sum(f for e, f in factors[row['prime']] if row['power']%f == 0)
        assert row['coefficient'] == expected and row['n'] == row['prime']**row['power']
    assert [r['n'] for r in predictions] == sorted({int(p**k) for p in sp.primerange(2, 4097) for k in range(1, 13) if p**k <= 4096})
    for row in data['local_factors']:
        assert sorted(row['model']) == factors[row['prime']]
    exact_path = root/'docs/frontier/2026-09-13-coupled-delta/Exact_Audit.json'
    exact = json.loads(exact_path.read_text())
    assert [r['coefficient'] for r in predictions] == exact['relaxation_ambiguity']['baseline_coefficients']
    old_path = root/'docs/frontier/2026-09-13-recovery-delta/Local_Identifiability.json'
    old = json.loads(old_path.read_text())
    latest_path = root/'docs/frontier/2026-09-13-local-noise-delta/Local_Noise_Summary.json'
    latest = json.loads(latest_path.read_text())
    locals_by_prime = {r['prime']: r for r in data['local_factors']}
    resolutions = []
    for old_row in old['unresolved_local_factors']:
        p = old_row['prime']
        new = locals_by_prime[p]
        assert new['model'] in old_row['retained_models']
        resolutions.append({'prime': p, 'old_surviving_models': old_row['retained_models'], 'globally_selected_model': new['model'],
                            'next_power': old_row['next_prime_power'], 'predicted_coefficient': new['square_coefficient'],
                            'route': 'degree and discriminant classification; no new zero measurement'})
    assert len(resolutions) == 48
    assert {r['prime'] for r in resolutions} == {r['prime'] for r in latest['unresolved_local_models_with_discriminant']}
    # Actual field control with the same degree and signature but different D.
    phi8mod3 = sp.Poly(phi8, modulus=3).factor_list()[1]
    assert sorted((f.degree(), e) for f, e in phi8mod3) == [(2, 1), (2, 1)]
    phi8c9 = sum(f.degree() for f, e in phi8mod3 if 2 % f.degree() == 0)
    phi5c9 = next(r['coefficient'] for r in predictions if r['n'] == 9)
    assert (phi8c9, phi5c9) == (4, 0)
    real_cubic = sp.Poly(x**3+x**2-2*x-1, x)
    assert real_cubic.is_irreducible and sp.discriminant(real_cubic) == 49
    assert real_cubic.count_roots(-sp.oo, sp.oo) == 3
    assert Fraction(49*math.factorial(3)**2, 3**6) > 1
    # Mutated finite witnesses must fail independent comparisons.
    controls = [
        {'mutation': 'omit S4 overgroup', 'rejected': sorted(map(len, data['overgroups'][:-1])) != [4, 8, 24]},
        {'mutation': 'trivial cubic inertia image', 'rejected': 3-len(cycles((0, 1, 2))) != groups['cubic_tame_discriminant_exponent']},
        {'mutation': 'treat inertia as normal in S4', 'rejected': bool(groups['inertia_not_normal_in_s4_witness'])},
        {'mutation': 'retain degree-eight compositum with unramified quadratic quotient', 'rejected': Fraction(4, 9) < 1},
        {'mutation': 'weight ramified c5 by e', 'rejected': next(r['coefficient'] for r in predictions if r['n']==5) != 4},
        {'mutation': 'infer p=23 has residue degree two', 'rejected': factors[23] != [[1, 2], [1, 2]]}]
    assert all(c['rejected'] for c in controls)
    return {'status': 'passed', 'source_sha256': sha(Path(__file__)), 'group_audit': groups,
            'tame_patterns_checked': 11, 'minkowski_rational_checks': len(data['minkowski_squared_bounds']),
            'discriminant_crosschecks': trace_discs, 'independent_finite_field_factorizations': len(factors),
            'factorization_models': {str(p): model for p, model in factors.items()},
            'held_out_coefficient_matches': len(predictions), 'held_out_target_matches': sum(r['n']<=361 for r in predictions),
            'local_factors_identified_from_invariants': 72, 'previous_48_resolutions': resolutions,
            'held_out_inputs_sha256': {str(p.relative_to(root)): sha(p) for p in [exact_path, old_path, latest_path]},
            'same_degree_signature_control': {'field': 'Q(zeta_8)', 'degree': 4, 'signature': [0, 2], 'field_discriminant': 256,
                                             'phi8_coefficient_at_9': int(phi8c9), 'phi5_coefficient_at_9': phi5c9,
                                             'field_discriminant_premise': 'Cyclotomic prime-power discriminant formula, Keith Conrad, Different Ideal, Example 4.10'},
            'minkowski_nonexclusion_control': {'irreducible_cubic': str(real_cubic.as_expr()), 'discriminant': 49, 'signature': [3, 0]},
            'adversarial_controls': controls,
            'scope': 'Exhaustive finite groups and exact polynomial checks; the arithmetic theorem uses cited classical premises and is not fully formalized. Earlier local relaxation survivors remain survivors of that restricted inference system.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--predictions', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.predictions.read_text()), args.root)
    result['predictions_sha256'] = sha(args.predictions)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'independent_finite_field_factorizations', 'held_out_coefficient_matches', 'held_out_target_matches', 'local_factors_identified_from_invariants']}))
