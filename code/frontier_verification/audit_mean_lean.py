"""Record kernel checks, theorem axioms, and rejected mathematical mutations.

Requires an installed Lean toolchain and (unless --core-only) a prepared project
with the supplied exact dependency lock and Mathlib caches. Never installs or
changes dependencies. The output directory must be new. Original sources are
checked against Mean_Source_Manifest.json and are never edited.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


CORE = ['PerZero', 'PerZeroIntegral', 'PerZeroError', 'PerZeroSums', 'PerZeroMean', 'PerZeroCounterfamily']
EXTRA = []
MUTATIONS = [('PerZeroMean', 'double_point_lower_coefficient', '2 * arctan (1 / L) * indicator gamma T eps L ≤ PerZeroError.deficit gamma T eps ∧\n    PerZeroError.deficit gamma T eps ≤ 2 * π * indicator gamma T eps L + 4 / L := by', '4 * arctan (1 / L) * indicator gamma T eps L ≤ PerZeroError.deficit gamma T eps ∧\n    PerZeroError.deficit gamma T eps ≤ 2 * π * indicator gamma T eps L + 4 / L := by'), ('PerZeroMean', 'delete_far_layer_tail', 'PerZeroError.deficit gamma T eps ≤ 2 * π * indicator gamma T eps L + 4 / L := by', 'PerZeroError.deficit gamma T eps ≤ 2 * π * indicator gamma T eps L + 0 := by'), ('PerZeroMean', 'unscaled_layer_count', '(∑ k ∈ s, indicator (gamma k) T eps L) / s.card', '(∑ k ∈ s, indicator (gamma k) T eps L) / 1'), ('PerZeroMean', 'total_in_place_of_mean', '(∑ k ∈ s, PerZeroError.deficit (gamma k) T eps) / s.card', '(∑ k ∈ s, PerZeroError.deficit (gamma k) T eps) / 1'), ('PerZeroCounterfamily', 'zero_total_limit', 'Tendsto total atTop (𝓝 (π / 2)) := by', 'Tendsto total atTop (𝓝 0) := by'), ('PerZeroCounterfamily', 'extra_midpoint_in_exact_formula', 'π / 2 + 2 * arctan (1 / (r ^ 2 - 1)) + 4 * (r - 1) * arctan (2 / r ^ 2)\n', 'π / 2 + 2 * arctan (1 / (r ^ 2 - 1)) + 4 * r * arctan (2 / r ^ 2)\n'), ('PerZeroCounterfamily', 'wrong_resolution_power', 'noncomputable def resolution (N : ℕ) : ℝ := 1 / (N : ℝ) ^ 2', 'noncomputable def resolution (N : ℕ) : ℝ := 1 / (N : ℝ) ^ 3'), ('PerZeroCounterfamily', 'miss_endpoint_layer_at_threshold', 'PerZeroMean.indicator (2 * eps) 1 eps 1 = 0 ∧', 'PerZeroMean.indicator eps 1 eps 1 = 0 ∧')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin', type=Path, required=True, help='directory containing lean and lake')
    parser.add_argument('--project', type=Path, default=Path(__file__).parent / 'proofs')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--core-only', action='store_true')
    args = parser.parse_args()
    if args.core_only:
        parser.error("These mean-error proofs require the full pinned Mathlib project.")
    binary, project, output = args.bin.resolve(), args.project.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((Path(__file__).parent / 'proofs/Mean_Source_Manifest.json').read_text())
    modules = CORE if args.core_only else CORE + EXTRA
    for name in manifest:
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
            passed = (rc != 0 and 'error:' in stdout and not any(t in stdout.lower() for t in ['unknown module', 'unknown package', 'file not found'])) if expect_rejection else rc == 0
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
              'audit_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'events': events}
    (output / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'events'}, indent=2))


if __name__ == '__main__':
    main()
