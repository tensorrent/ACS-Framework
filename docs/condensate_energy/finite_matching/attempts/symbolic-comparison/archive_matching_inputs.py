#!/usr/bin/env python3
"""Audit recovered proposed vacuum/flavor inputs without changing originals."""
import ast
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import sympy as s

from finite_light_matching import OUT


def main():
    checks, result = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    snap = OUT / 'source-snapshots'
    provenance = json.loads((snap / 'provenance.json').read_text())
    check('recovered-source-hashes', all(sha256((snap / Path(row['snapshot']).name).read_bytes()).hexdigest() == row['sha256'] for row in provenance))
    replays = []
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    for filename in ['electroweak_vacuum_selection.py', 'neutrino_honest.py']:
        dest = OUT / 'attempts/source-replays' / Path(filename).stem
        dest.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run([sys.executable, str(snap / filename)], cwd=dest,
                              capture_output=True, text=True, env=env, timeout=60)
        (dest / 'stdout.txt').write_text(proc.stdout)
        (dest / 'stderr.txt').write_text(proc.stderr)
        check(filename + '-source-replay-completes', proc.returncode == 0, proc.returncode)
        replays.append(dict(filename=filename, returncode=proc.returncode, directory=str(dest)))
    scan = json.loads((OUT / 'attempts/source-replays/electroweak_vacuum_selection/electroweak_vacuum_koide.json').read_text())
    result['original_scan'] = scan

    # Reconstruct the exact displayed generators, retaining the source's .3=3/10.
    H1, H2 = s.diag(1, -1, 0, 0), s.diag(0, 1, -1, 0)
    E01, E12 = s.zeros(4), s.zeros(4)
    E01[0, 1], E12[1, 2] = 1, 1
    form, function = H1 + s.Rational(3, 10) * E01, E12 + s.Rational(3, 10) * H2
    bracket = lambda a, b: a * b - b * a
    L1, L2 = form, bracket(form, function)
    L3 = bracket(L2, form) + bracket(L2, function)
    phi, z = s.symbols('phi z', real=True)
    T = L1 + phi * L2 + phi ** 2 * L3
    M = (T - T.T) / 2  # Exactly Re[i Sym(T)+Anti(T)] for real source T.
    omega2 = s.factor(-s.trace(M * M) / 2)
    check('source-effective-matrix-is-exactly-skew-symmetric', M.T == -M)
    characteristic = M.charpoly(z)
    check('exact-characteristic-has-two-zero-modes', s.factor(characteristic.as_expr().subs(characteristic.gen, z) - z ** 2 * (z ** 2 + omega2)) == 0)
    check('correct-Hermitian-conversion-has-paired-nonzero-spectrum', (-s.I * M).conjugate().T == -s.I * M)
    check('source-fourth-direction-is-inactive', M[:, 3] == s.zeros(4, 1) and M[3, :] == s.zeros(1, 4))
    # Obtain source L1,L2,L3 through a scoped AST evaluation to verify the
    # independent rational transcription. No scan or file writes are executed.
    tree = ast.parse((snap / 'electroweak_vacuum_selection.py').read_text())
    names = {'H1', 'H2', 'E01', 'E12', 'f_phys', 'g_phys', 'L1', 'L2', 'L3'}
    nodes = [node for node in tree.body if
             isinstance(node, ast.FunctionDef) and node.name in {'bracket', 'chirality_map'} or
             isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets)]
    namespace = dict(np=np)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<scoped-source-generators>', 'exec'), namespace)
    check('exact-transcription-matches-recovered-generators', all(np.max(abs(np.array(a, float) - namespace[name])) < 1e-14 for a, name in [(L1, 'L1'), (L2, 'L2'), (L3, 'L3')]))
    rows = []
    for value in [0., .5, 1.1, 1.2, 1.3, 2.]:
        matrix = np.array(M.subs(phi, value), float)
        wrong = np.sort(abs(np.linalg.eigvalsh(matrix)))[::-1]
        actual = np.sort(abs(np.linalg.eigvals(matrix)))[::-1]
        singular = np.linalg.svd(matrix, compute_uv=False)
        hermitian = np.sort(abs(np.linalg.eigvalsh(-1j * matrix)))[::-1]
        check('correct-spectral-instruments-agree-phi-' + str(value),
              max(abs(actual - singular)) < 1e-12 and max(abs(actual - hermitian)) < 1e-12)
        check('at-most-two-nonzero-magnitudes-phi-' + str(value), singular[2] < 1e-12 and abs(singular[0] - singular[1]) < 1e-12)
        rows.append(dict(phi=value, source_eigvalsh_magnitudes=wrong.tolist(),
            true_eigenvalue_magnitudes=actual.tolist(), singular_values=singular.tolist(),
            non_Hermitian_residual=float(np.linalg.norm(matrix - matrix.T))))
    check('claimed-third-magnitude-is-an-eigensolver-artifact', any(r['source_eigvalsh_magnitudes'][2] > 1e-4 for r in rows) and all(r['singular_values'][2] < 1e-12 for r in rows))
    result['vacuum_selection'] = dict(exact_effective_matrix=str(M), omega_squared=str(omega2), samples=rows,
        finding='The Re chirality-map matrix is skew-symmetric. Its true nonzero eigenvalue magnitudes are paired and its rank is at most two. '
        'eigvalsh treats a triangle as a Hermitian matrix and creates a spurious third magnitude. No three positive generation masses emerge from this operator.',
        independent_input='The script inserts target theta0=12.73 and arbitrary generator admixtures .3, then scans phi; it contains no normalized action or energy minimization selecting phi.')

    tree = ast.parse((snap / 'neutrino_honest.py').read_text())
    numbers = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {'m_e', 'm_tau', 'm_nu_obs'}:
                numbers[name] = float(ast.literal_eval(node.value))
    me, mtau, archived_MeV = [numbers[k] for k in ['m_e', 'm_tau', 'm_nu_obs']]
    dirac_eV = me * me / mtau / 3 * 1e6
    target_eV = .049
    requested_MeV = target_eV * 1e-6
    consistent_MR_eV = dirac_eV ** 2 / target_eV
    inconsistent_MR_eV = dirac_eV ** 2 / (archived_MeV * 1e6)
    check('archived-neutrino-MeV-literal-has-factor-1000-error', abs(archived_MeV / requested_MeV - 1000) < 1e-10)
    check('two-archived-Majorana-calculations-differ-by-factor-1000', abs(consistent_MR_eV / inconsistent_MR_eV - 1000) < 1e-10)
    inferred = [dict(target_eV=t, inferred_MR_eV=dirac_eV ** 2 / t) for t in [.0245, .049, .098]]
    check('Majorana-value-is-inferred-from-input-neutrino-target', abs(inferred[0]['inferred_MR_eV'] / inferred[1]['inferred_MR_eV'] - 2) < 1e-12 and abs(inferred[2]['inferred_MR_eV'] / inferred[1]['inferred_MR_eV'] - .5) < 1e-12)
    result['Majorana_input'] = dict(source_literals=numbers, target_eV=target_eV, correct_target_MeV=requested_MeV,
        inferred_Dirac_eV=dirac_eV, consistent_inferred_Majorana_eV=consistent_MR_eV,
        inconsistent_inferred_Majorana_eV=inconsistent_MR_eV, target_variation=inferred,
        finding='The later eV calculation gives about 49 keV after inserting the target .049 eV. This is inverse parameter inference, not an independent prediction of F or d. '
        'The earlier MeV literal describes 49 eV instead and is inconsistent by 1000. The target is treated here as an archived numerical input, not an absolute neutrino-mass measurement.')
    result['replays'] = replays
    result['checks'] = checks
    result['checks_passed'] = sum(c['passed'] for c in checks)
    result['checks_total'] = len(checks)
    result['scope'] = 'Two newly recovered source proposals relevant to the missing vacuum/scale inputs; not an exhaustive drive or chat search.'
    (OUT / 'archive-inputs.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=result['checks_passed'], checks_total=len(checks))))
    assert all(c['passed'] for c in checks), 'Failed checks retained in archive-inputs.json'


if __name__ == '__main__':
    main()
