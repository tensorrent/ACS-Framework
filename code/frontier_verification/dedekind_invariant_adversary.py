"""Replay corrupted invariant certificates through the independent auditor."""
import argparse, copy, hashlib, json
from pathlib import Path
from dedekind_invariant_audit import audit


def run(path, root):
    data = json.loads(path.read_text())
    mutants = []
    altered = copy.deepcopy(data); altered['overgroups'] = altered['overgroups'][:-1]
    mutants.append(('omit_possible_s4', altered))
    altered = copy.deepcopy(data); altered['matching_kernel'] = altered['matching_kernel'][:-1]
    mutants.append(('incorrect_resolvent_kernel', altered))
    altered = copy.deepcopy(data)
    next(c for c in altered['subdirect_composita'] if c['degree']==8)['survives_no_unramified_extension'] = True
    mutants.append(('retain_unramified_quadratic_quotient', altered))
    altered = copy.deepcopy(data); altered['minkowski_squared_bounds'][0]['squared_bound_upper'] = [1, 8]
    mutants.append(('invent_stronger_minkowski_bound', altered))
    altered = copy.deepcopy(data)
    next(c for c in altered['coefficient_predictions'] if c['n']==5)['coefficient'] = 4
    mutants.append(('ramification_index_in_euler_weight', altered))
    altered = copy.deepcopy(data)
    next(c for c in altered['local_factors'] if c['prime']==23)['model'] = [[1, 2], [1, 2]]
    mutants.append(('wrong_unobserved_local_factor', altered))
    checks = []
    for name, value in mutants:
        try:
            audit(value, root)
        except AssertionError:
            checks.append({'mutation': name, 'rejected_by_independent_auditor': True})
        else:
            raise AssertionError('Mutation survived: '+name)
    return {'status': 'passed', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'auditor_sha256': hashlib.sha256(Path(__file__).with_name('dedekind_invariant_audit.py').read_bytes()).hexdigest(),
            'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'checks': checks,
            'scope': 'Six actual corrupted transcripts are rejected by the independent auditor. This audits finite certificates; it does not mechanize the cited arithmetic theorems.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--predictions', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.predictions, args.root)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'mutated_transcripts_rejected': len(result['checks'])}))
