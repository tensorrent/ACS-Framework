"""Record kernel checks, theorem axioms, and rejected mathematical mutations.

Requires an installed Lean toolchain and (unless --core-only) a prepared project
with the supplied exact dependency lock and Mathlib caches. Never installs or
changes dependencies. The output directory must be new. Original sources are
checked against Source_Manifest.json and are never edited.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


CORE = ['LFBound', 'AxiomIII']
EXTRA = ['PerZero', 'LFReal', 'PerZeroBoundary']
MUTATIONS = [
    ('LFBound', 'wrong_attainment', 'theorem star_S_eq_four : S2 star = 8 := by decide',
     'theorem star_S_eq_four : S2 star = 9 := by decide'),
    ('LFBound', 'wrong_upper_bound', 'theorem S_le_four (hn : NonNeg B) (hs : Normalised B) : S2 B ≤ 8 := by',
     'theorem S_le_four (hn : NonNeg B) (hs : Normalised B) : S2 B ≤ 7 := by'),
    ('AxiomIII', 'diagonal_phi', 'def phi : Mat2 := ⟨1, 2, 0, 1⟩', 'def phi : Mat2 := ⟨1, 0, 0, 1⟩'),
    ('AxiomIII', 'wrong_power', 'Mat2.pow phi n = ⟨1, 2 * (n : Int), 0, 1⟩',
     'Mat2.pow phi n = ⟨1, 3 * (n : Int), 0, 1⟩'),
    ('PerZero', 'wrong_limit', 'Tendsto (contribution gamma T) (𝓝[>] 0) (𝓝 (2 * π)) := by',
     'Tendsto (contribution gamma T) (𝓝[>] 0) (𝓝 (3 * π)) := by'),
    ('PerZero', 'wrong_pi_bound',
     'theorem contribution_lt_two_pi (gamma T eps : ℝ) : contribution gamma T eps < 2 * π := by',
     'theorem contribution_lt_two_pi (gamma T eps : ℝ) : contribution gamma T eps < π := by'),
    ('PerZero', 'wrong_contribution_coefficient', '  2 * (arctan ((T - gamma) / eps) + arctan (gamma / eps))',
     '  3 * (arctan ((T - gamma) / eps) + arctan (gamma / eps))'),
    ('LFReal', 'wrong_real_bound', '(hs : Normalised B) : S B ≤ 4 := by',
     '(hs : Normalised B) : S B ≤ 3 := by'),
    ('LFReal', 'wrong_real_attainment', 'theorem star_attains_four : S star = 4 := by',
     'theorem star_attains_four : S star = 5 := by'),
    ('PerZeroBoundary', 'wrong_boundary_limit', '(𝓝[>] 0) (𝓝 (3 * π / 2)) := by',
     '(𝓝[>] 0) (𝓝 (2 * π)) := by'),
    ('PerZeroBoundary', 'wrong_scaled_path', 'PerZero.contribution (c * eps) 1 eps = scaled c eps := by',
     'PerZero.contribution (c * eps * eps) 1 eps = scaled c eps := by'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin', type=Path, required=True, help='directory containing lean and lake')
    parser.add_argument('--project', type=Path, default=Path(__file__).parent / 'proofs')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--core-only', action='store_true')
    args = parser.parse_args()
    binary, project, output = args.bin.resolve(), args.project.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((Path(__file__).parent / 'proofs/Source_Manifest.json').read_text())
    modules = CORE if args.core_only else CORE + EXTRA
    for name in [m + '.lean' for m in modules] + ([] if args.core_only else ['lake-manifest.json', 'lean-toolchain']):
        actual = hashlib.sha256((project / name).read_bytes()).hexdigest()
        if actual != manifest[name]['sha256']:
            raise ValueError(f'Unexpected source or lock hash: {name}')
    package_revisions = {}
    if not args.core_only:
        for package in json.loads((project / 'lake-manifest.json').read_text())['packages']:
            actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                             cwd=project / '.lake/packages' / package['name'], text=True).strip()
            if actual != package['rev']:
                raise ValueError(f'Unexpected dependency revision: {package["name"]}')
            package_revisions[package['name']] = actual
    compiled = (output / 'compiled') if args.core_only else (project / '.lake/build/lib/lean')
    compiled.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'PATH': str(binary) + os.pathsep + os.environ.get('PATH', '')}
    if args.core_only:
        env['LEAN_PATH'] = str(compiled)
    prefix = [str(binary / 'lean')] if args.core_only else [str(binary / 'lake'), 'env', 'lean']
    events = []

    def run(name, arguments, expect_rejection=False):
        command = prefix + arguments
        start = datetime.now(timezone.utc)
        try:
            proc = subprocess.run(command, cwd=project, env=env, text=True, capture_output=True, timeout=180)
            rc, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
            passed = (rc != 0 and 'error' in stdout) if expect_rejection else rc == 0
        except subprocess.TimeoutExpired as exc:
            rc, passed = None, False
            stdout = exc.stdout or ''
            stderr = exc.stderr or ''
            if isinstance(stdout, bytes):
                stdout = stdout.decode(errors='replace')
            if isinstance(stderr, bytes):
                stderr = stderr.decode(errors='replace')
        event = {'name': name, 'started_utc': start.isoformat(), 'command': command,
                 'elapsed_seconds': (datetime.now(timezone.utc) - start).total_seconds(),
                 'returncode': rc, 'expected_rejection': expect_rejection,
                 'passed': passed, 'stdout': stdout, 'stderr': stderr,
                 'input_sha256': hashlib.sha256((project / arguments[-1]).read_bytes()).hexdigest()}
        events.append(event)
        with (output / 'events.jsonl').open('a') as stream:
            stream.write(json.dumps(event) + '\n')
        if not passed:
            raise RuntimeError(f'{name} failed; see {output / "events.jsonl"}')
        return proc

    for module in modules:
        run(module, ['-o', str(compiled / (module + '.olean')), module + '.lean'])
    axiom_file = output / 'AuditAxioms.lean'
    lines = ['import ' + m for m in modules]
    for module in modules:
        names = re.findall(r'^theorem\s+(\w+)', (project / (module + '.lean')).read_text(), re.M)
        lines.extend(f'#print axioms {module}.{name}' for name in names)
    axiom_file.write_text('\n'.join(lines) + '\n')
    printed = run('axiom_dependencies', [str(axiom_file)])
    if 'sorryAx' in printed.stdout:
        raise RuntimeError('A theorem depends on sorryAx')
    mutation_dir = output / 'mutations'
    mutation_dir.mkdir()
    for module, name, old, new in MUTATIONS:
        if module not in modules:
            continue
        text = (project / (module + '.lean')).read_text()
        if text.count(old) != 1:
            raise ValueError(f'Mutation target is not unique: {name}')
        target = mutation_dir / (name + '.lean')
        target.write_text(text.replace(old, new))
        run(name, [str(target)], expect_rejection=True)
    record = {'runtime': subprocess.check_output([str(binary / 'lean'), '--version'], text=True).strip(),
              'core_only': args.core_only, 'all_passed': all(e['passed'] for e in events),
              'verified_modules': modules, 'rejected_mutations': sum(e['expected_rejection'] for e in events),
              'package_revisions': package_revisions,
              'source_hashes': {m: manifest[m + '.lean']['sha256'] for m in modules},
              'events': events}
    (output / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'events'}, indent=2))


if __name__ == '__main__':
    main()
