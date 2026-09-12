"""Independent real-probability LP and exact rational primal/dual certificates.

This checks the explicitly defined deterministic-friend no-signalling branches.
It does not infer an experimental or quantum bound from this abstract polytope.
Run with the pinned requirements; JSON is written to stdout.
"""
from fractions import Fraction as Q
from itertools import product
import json

import numpy as np
from scipy.optimize import linprog

VARIABLES = list(product(range(3), range(3), range(2), range(2)))
INDEX = {key: i for i, key in enumerate(VARIABLES)}


def row(entries):
    result = [0] * 36
    for key, coefficient in entries:
        result[INDEX[key]] += coefficient
    return result


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


objective = [0] * 36
for x, y in product([1, 2], repeat=2):
    sign = -1 if x == y == 2 else 1
    for a, b in product(range(2), repeat=2):
        objective[INDEX[x, y, a, b]] = sign * (-1) ** (a + b)


def constraints(a0, b0):
    matrix, rhs = [], []
    for x, y in product(range(3), repeat=2):
        matrix.append(row([((x, y, a, b), 1) for a, b in product(range(2), repeat=2)]))
        rhs.append(1)
    for x, a, y in product(range(3), range(2), [1, 2]):
        matrix.append(row([((x, y, a, b), 1) for b in range(2)]
                          + [((x, 0, a, b), -1) for b in range(2)]))
        rhs.append(0)
    for y, b, x in product(range(3), range(2), [1, 2]):
        matrix.append(row([((x, y, a, b), 1) for a in range(2)]
                          + [((0, y, a, b), -1) for a in range(2)]))
        rhs.append(0)
    for y in range(3):
        matrix.append(row([((0, y, a0, b), 1) for b in range(2)]))
        rhs.append(1)
    for x in range(3):
        matrix.append(row([((x, 0, a, b0), 1) for a in range(2)]))
        rhs.append(1)
    return matrix, rhs


def witness(a0, b0, pr=True):
    result = []
    for x, y, a, b in VARIABLES:
        if x == y == 0:
            p = Q(int(a == a0 and b == b0))
        elif x == 0:
            p = Q(int(a == a0), 2)
        elif y == 0:
            p = Q(int(b == b0), 2)
        elif pr:
            p = Q(int((a ^ b) == int(x == y == 2)), 2)
        else:
            p = Q(1, 4)
        result.append(p)
    return result


def main():
    results = []
    for a0, b0 in product(range(2), repeat=2):
        matrix, rhs = constraints(a0, b0)
        exact = witness(a0, b0)
        assert all(p >= 0 for p in exact)
        assert [dot(r, exact) for r in matrix] == rhs
        assert dot(objective, exact) == 4

        # A certificate independently constructed from four normalisation rows.
        # For maximisation, A^T y >= c and b^T y = 4 prove the upper bound.
        dual = [int(i in [4, 5, 7, 8]) for i in range(len(matrix))]
        slack = [sum(matrix[i][j] * dual[i] for i in range(len(matrix))) - objective[j]
                 for j in range(36)]
        assert min(slack) >= 0 and dot(rhs, dual) == 4

        lp = linprog(-np.array(objective, dtype=float), A_eq=np.array(matrix),
                     b_eq=np.array(rhs), bounds=(0, None), method='highs')
        assert lp.success and abs(lp.fun + 4) < 1e-10
        assert np.max(np.abs(np.array(matrix) @ lp.x - rhs)) < 1e-10

        # A feasible distribution outside the old integer-half-unit carrier.
        mixed = [p / 3 + Q(2, 3) * q for p, q in zip(exact, witness(a0, b0, pr=False))]
        assert [dot(r, mixed) for r in matrix] == rhs
        assert any((2 * p).denominator != 1 for p in mixed)
        assert dot(objective, mixed) == Q(4, 3)

        # Mutations must break the appropriate independent certificate.
        bad = exact.copy()
        bad[INDEX[0, 0, a0, b0]] = 0
        assert [dot(r, bad) for r in matrix] != rhs
        assert dot(objective, exact) > 2
        results.append({'friend_outcomes': [a0, b0], 'lp_maximum': -float(lp.fun),
                        'exact_primal': [str(p) for p in exact], 'dual': dual,
                        'dual_slack': slack, 'exact_bound': 4,
                        'outside_half_unit_example_value': str(dot(objective, mixed)),
                        'mutations_rejected': ['broken_normalisation', 'upper_bound_two']})
    print(json.dumps({'status': 'passed', 'carrier': 'arbitrary real probabilities',
                      'variables': 36, 'branches': results,
                      'routes': ['HiGHS linear programming',
                                 'exact rational primal witness and symbolic dual certificate'],
                      'scope': 'The defined no-signalling deterministic-friend branches; no quantum theorem.'}, indent=2))


if __name__ == '__main__':
    main()
