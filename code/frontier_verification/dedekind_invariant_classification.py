"""Exact finite ingredients and prior-only predictions for quartic |D|=125.

This is not a formal proof of the number-theoretic premises; see INVARIANT_README.
No spectrum, old coefficient, local survivor, or field database is an input.
"""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


def closure(seed, multiply):
    group = set(seed)
    while True:
        enlarged = group | {multiply(a, b) for a in group for b in group}
        if enlarged == group:
            return frozenset(group)
        group = enlarged


def overgroups(start, universe, multiply):
    seen = {closure(start, multiply)}
    todo = list(seen)
    while todo:
        group = todo.pop()
        for x in universe:
            if x not in group:
                candidate = closure(group | {x}, multiply)
                if candidate not in seen:
                    seen.add(candidate)
                    todo.append(candidate)
    return sorted(seen, key=lambda g: (len(g), sorted(g)))


def prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def order(a, modulus):
    value = 1
    for k in range(1, modulus + 1):
        value = value * a % modulus
        if value == 1:
            return k
    raise ValueError('not a unit')


def run():
    permutations = list(itertools.permutations(range(4)))
    multiply = lambda a, b: tuple(a[b[i]] for i in range(4))
    identity = tuple(range(4))
    rho = (1, 2, 3, 0)
    inertia = closure({identity, rho}, multiply)
    groups = overgroups(inertia, permutations, multiply)
    assert [len(g) for g in groups] == [4, 8, 24]
    matchings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    def action(p):
        return tuple(matchings.index(tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in m))) for m in matchings)
    images = {action(p) for p in permutations}
    kernel = [p for p in permutations if action(p) == (0, 1, 2)]
    assert len(images) == 6 and len(kernel) == 4
    d4 = groups[1]
    assert all(closure({g}, multiply) <= d4 for g in d4)
    assert all({multiply(g, h) for h in inertia} == {multiply(h, g) for h in inertia} for g in d4)
    # The compositum of two cyclic quartics embeds in C4 x C4.
    product = list(itertools.product(range(4), repeat=2))
    add = lambda a, b: ((a[0] + b[0]) % 4, (a[1] + b[1]) % 4)
    subdirect = [g for g in overgroups({(0, 0)}, product, add)
                 if {x[0] for x in g} == set(range(4)) and {x[1] for x in g} == set(range(4))]
    composita = []
    for g in subdirect:
        cyclic = {closure({(0, 0), x}, add) for x in g}
        possible = sorted((i for i in cyclic if {x[0] for x in i} == set(range(4)) and {x[1] for x in i} == set(range(4))), key=lambda i: sorted(i))
        assert possible and all(len(i) == 4 for i in possible)
        composita.append({'group': sorted(g), 'degree': len(g), 'possible_inertia': [sorted(i) for i in possible],
                          'unramified_quotient_degree': len(g) // 4, 'survives_no_unramified_extension': len(g) == 4})
    # Square the rational upper bound obtained by replacing pi with 3.
    bounds = []
    for n, discriminant in [(2, 1), (3, 5), (4, 1), (4, 5)]:
        for r2 in range(n // 2 + 1):
            factor = Fraction(math.factorial(n), n ** n) * Fraction(4, 3) ** r2
            squared = discriminant * factor ** 2
            assert squared < 1
            bounds.append({'degree': n, 'absolute_discriminant': discriminant, 'complex_pairs': r2,
                           'squared_bound_upper': [squared.numerator, squared.denominator]})
    patterns = []
    pairs = [(e, f) for e in range(1, 5) for f in range(1, 5) if e * f <= 4]
    for size in range(1, 5):
        for model in itertools.combinations_with_replacement(pairs, size):
            if sum(e * f for e, f in model) == 4:
                patterns.append({'model': model, 'discriminant_exponent': sum((e - 1) * f for e, f in model)})
    assert [x['model'] for x in patterns if x['discriminant_exponent'] == 3] == [((4, 1),)]
    local = []
    coefficients = []
    for p in range(2, 4097):
        if not prime(p):
            continue
        e, f, g = (4, 1, 1) if p == 5 else (1, order(p % 5, 5), 4 // order(p % 5, 5))
        if p <= 361:
            local.append({'prime': p, 'ramification_index': e, 'residue_degree': f, 'prime_count': g,
                          'model': [[e, f]] * g, 'square_coefficient': f * g if 2 % f == 0 else 0})
        n, k = p, 1
        while n <= 4096:
            coefficients.append({'n': n, 'prime': p, 'power': k, 'coefficient': f * g if k % f == 0 else 0})
            n *= p
            k += 1
    coefficients.sort(key=lambda x: x['n'])
    assert len(local) == 72 and len(coefficients) == 604
    return {'status': 'passed', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs': {'degree': 4, 'absolute_field_discriminant': 125, 'coefficient_limit': 4096, 'local_prime_limit': 361},
            'scope': 'Exact finite ingredients supporting the written uniqueness proof. Standard arithmetic theorems are explicit premises, not machine-checked here. Predictions use global invariant classification and zero spectral observations.',
            'permutations': permutations, 'inertia': sorted(inertia), 'overgroups': [sorted(g) for g in groups],
            'matching_action': [{'permutation': p, 'image': action(p)} for p in permutations],
            'matching_kernel': kernel, 'inertia_matching_image': sorted({action(p) for p in inertia}),
            'tame_local_patterns': patterns, 'minkowski_squared_bounds': bounds, 'subdirect_composita': composita,
            'local_factors': local, 'coefficient_predictions': coefficients,
            'residue_orders_mod5': {str(a): order(a, 5) for a in range(1, 5)}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'overgroup_orders': [len(g) for g in result['overgroups']],
                      'subdirect_composita': len(result['subdirect_composita']), 'prior_only_coefficients': 604, 'prior_only_local_factors': 72}))
