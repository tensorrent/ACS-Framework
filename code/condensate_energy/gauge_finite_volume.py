#!/usr/bin/env python3
"""Independent fixed-Q minimization with the electric potential eliminated."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import solve, solve_banded
from scipy.sparse import bmat, diags

from self_binding import RadialGrid
from gauge_completion import ROOT, OUT, B


class GaugeFiniteVolume:
    def __init__(self, radius, dr, charge, coupling):
        self.grid = RadialGrid(radius, dr)
        self.charge = charge
        self.coupling = coupling
        grid = self.grid
        # Half a cell in series with the exact exterior Coulomb resistance.
        self.robin = 4 * math.pi * radius ** 2 / (radius + dr / 2)
        self.electric_diag = grid.diag.copy()
        self.electric_diag[-1] += self.robin - grid.outer

    def electrostatic(self, f):
        grid, e = self.grid, self.coupling
        band = np.zeros((3, grid.n))
        band[0, 1:] = band[2, :-1] = -grid.k
        band[1] = self.electric_diag + e * e * grid.w * f * f
        rhs = np.zeros(grid.n)
        rhs[-1] = self.robin
        h = solve_banded((1, 1), band, rhs)
        inertia = float(grid.w @ (f * f * h))
        omega = self.charge / inertia
        return h, inertia, omega, band

    def value_gradient(self, z):
        grid = self.grid
        c, f = z[:grid.n] / grid.sw, z[grid.n:] / grid.sw
        h, inertia, omega, band = self.electrostatic(f)
        potential = float(grid.w @ (.25 * (c * c - 1) ** 2 + .5 * c * c * f * f + B / 4 * f ** 4))
        energy = potential + grid.gradient_energy(c, 1.) + grid.gradient_energy(f, 0.) + .5 * omega * self.charge
        gc = grid.gradient(c, 1.) / grid.sw + grid.sw * c * (c * c - 1 + f * f)
        gf = grid.gradient(f, 0.) / grid.sw + grid.sw * ((c * c - omega * omega * h * h) * f + B * f ** 3)
        return float(energy), np.concatenate((gc, gf))

    def exact_hessian(self, z):
        grid, e = self.grid, self.coupling
        c, f = z[:grid.n] / grid.sw, z[grid.n:] / grid.sw
        h, inertia, omega, band = self.electrostatic(f)
        cross = diags(2 * c * f)
        matrix = bmat([[grid.L + diags(3 * c * c - 1 + f * f), cross],
                       [cross, grid.L + diags(c * c + 3 * B * f * f - omega * omega * h * h)]], format='csc').toarray()
        vector = grid.sw * f * h * h
        matrix[grid.n:, grid.n:] += 4 * omega * omega / inertia * np.outer(vector, vector)
        if e:
            vector = grid.sw * f * h
            inverse_term = solve_banded((1, 1), band, np.diag(vector))
            matrix[grid.n:, grid.n:] += 4 * e * e * omega * omega * vector[:, None] * inverse_term
        return matrix

    def measure(self, z):
        grid, e = self.grid, self.coupling
        c, f = z[:grid.n] / grid.sw, z[grid.n:] / grid.sw
        h, inertia, omega, band = self.electrostatic(f)
        energy, gradient = self.value_gradient(z)
        rotation = .5 * float(grid.w @ (omega * omega * h * h * f * f))
        electric = .5 * omega * omega * (float(grid.k @ np.diff(h) ** 2) + self.robin * (h[-1] - 1) ** 2) / e ** 2 if e else 0.
        gauss = self.robin * omega * (1 - h[-1]) / e ** 2 if e else self.charge
        return dict(charge=self.charge, coupling=e, dr=grid.dr, radius=grid.radius,
                    energy=energy, energy_per_charge=energy / self.charge, omega=omega,
                    gradient_infinity_norm=float(max(abs(gradient))),
                    rotation_energy=rotation, electric_energy=electric,
                    energy_identity_relative=abs(rotation + electric - .5 * omega * self.charge) / energy,
                    gauss_relative=abs(gauss / self.charge - 1),
                    profile=dict(r=grid.r.tolist(), chi=c.tolist(), f=f.tolist(), Omega=(omega * h).tolist()))


def minimize_gauged(seed, dr):
    system = GaugeFiniteVolume(40., dr, seed['charge'], seed['coupling'])
    grid = system.grid
    old = seed['profile']
    z = np.concatenate((grid.sw * np.interp(grid.r, old['r'], old['chi']),
                        grid.sw * np.interp(grid.r, old['r'], old['f'])))
    history = []
    for _ in range(12):
        energy, gradient = system.value_gradient(z)
        history.append(float(max(abs(gradient))))
        if history[-1] < 1e-8:
            break
        delta = solve(system.exact_hessian(z), -gradient, assume_a='pos')
        for power in range(20):
            trial = z + delta * 2 ** (-power)
            et, gt = system.value_gradient(trial)
            if et <= energy + 1e-9 and max(abs(gt)) < history[-1]:
                z = trial
                break
        else:
            break
    row = system.measure(z)
    row['gradient_history'] = history
    row['relative_energy_difference'] = abs(row['energy'] / seed['energy'] - 1)
    row['relative_frequency_difference'] = abs(row['omega'] / seed['omega'] - 1)
    return row


def verify_gauged_derivatives():
    system = GaugeFiniteVolume(12., .2, 100., .12)
    grid = system.grid
    c = .5 * (1 + np.tanh(grid.r - 2.5))
    f = 1.5 * np.exp(-grid.r * grid.r / 16)
    z = np.concatenate((grid.sw * c, grid.sw * f))
    rng = np.random.default_rng(20260924)
    v = rng.normal(size=len(z))
    v /= np.linalg.norm(v)
    _, gradient = system.value_gradient(z)
    hessian = system.exact_hessian(z)
    eps = 1e-4
    ep, gp = system.value_gradient(z + eps * v)
    em, gm = system.value_gradient(z - eps * v)
    gradient_error = abs((ep - em) / (2 * eps) - gradient @ v) / max(1., abs(gradient @ v))
    hessian_error = float(np.linalg.norm((gp - gm) / (2 * eps) - hessian @ v) / np.linalg.norm(hessian @ v))
    return dict(gradient_error=float(gradient_error), hessian_error=hessian_error,
                passed=bool(max(gradient_error, hessian_error) < 1e-6))


def run_finite_volume():
    paths = [Path(__file__).resolve(), OUT / 'protocol.md', OUT / 'results.json', ROOT / 'code/condensate_energy/self_binding.py']
    survey = json.loads((OUT / 'results.json').read_text())
    result = dict(source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                  derivative_check=verify_gauged_derivatives(), cases={}, checks=[])
    assert result['derivative_check']['passed'], result['derivative_check']
    for e in [0., .08, .12]:
        for dr in [.1, .05]:
            label = f'e{e:g}-dr{dr:g}'
            row = minimize_gauged(survey['cases'][f'Q1000-e{e:g}'], dr)
            result['cases'][label] = row
            print(label, row['energy'], row['gradient_infinity_norm'], row['relative_energy_difference'], flush=True)
            (OUT / 'finite-volume-results.json').write_text(json.dumps(result) + '\n')
        coarse = result['cases'][f'e{e:g}-dr0.1']
        fine = result['cases'][f'e{e:g}-dr0.05']
        result['checks'].append(dict(name=f'finite-volume-e{e:g}',
            passed=bool(max(coarse['gradient_infinity_norm'], fine['gradient_infinity_norm']) < 1e-5
                        and fine['relative_energy_difference'] < 1e-3
                        and fine['relative_energy_difference'] < coarse['relative_energy_difference'])))
    result['checks'].append(dict(name='independent-gradient-and-hessian', passed=result['derivative_check']['passed']))
    result['checks'].append(dict(name='discrete-Gauss-and-electric-energy', passed=all(max(r['gauss_relative'], r['energy_identity_relative']) < 1e-8 for r in result['cases'].values())))
    result['all_checks_passed'] = all(row['passed'] for row in result['checks'])
    (OUT / 'finite-volume-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['checks'], indent=2), flush=True)


if __name__ == '__main__':
    run_finite_volume()
