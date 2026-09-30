"""Independent count bounds and actual malformed-certificate rejection controls."""
import argparse, copy, hashlib, json, tempfile
from fractions import Fraction as F
from pathlib import Path
import dedekind_biquadratic_arithmetic_audit as arithmetic_audit
import dedekind_biquadratic_decoding as decoder
from dedekind_biquadratic_replay import validate


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def independent_bounds(roots,h,r):
    # Count membership of each expanded interval in the open gate (0,h).
    inside=possible=0
    for row in roots:
        left,right=F(row['lo'])-r,F(row['hi'])+r
        if left>0 and right<h:inside+=1
        if max(left,F(0))<min(right,h):possible+=1
    return inside,possible


def run(arithmetic,paths,decoded):
    original=json.loads(arithmetic.read_text());data=[json.loads(p.read_text()) for p in paths]
    output=json.loads(decoded.read_text());controls=[];grid=robust=0
    for index,d in enumerate(data):
        validate(d);result=output['results'][index]
        for row in result['grid_measurements']:
            h=F(row['measurement']['height']);truth=row['held_out_field']
            low,high=independent_bounds(d['aggregate'][truth]['unlabelled_ordinate_intervals'],h,F(0))
            assert low==high==row['measurement']['positive_zero_count'];grid+=1
        for trial in result['robust_gate']:
            radius=F(trial['radius'])
            for label in ['A','B']:
                low,high=independent_bounds(d['aggregate'][label]['unlabelled_ordinate_intervals'],F(7,3),radius)
                assert (low,high)==(trial['templates'][label]['minimum'],trial['templates'][label]['maximum']);robust+=1
            if radius==F(1,2):
                for label in ['A','B']:
                    counts={r['measurement']['positive_zero_count'] for r in trial['uniform_displacement_controls'] if r['held_out_field']==label}
                    assert counts=={0,1}
    for name,alter in [
        ('drop_aggregate_zero',lambda d:d['aggregate']['A']['unlabelled_ordinate_intervals'].pop(0)),
        ('duplicate_aggregate_zero',lambda d:d['aggregate']['A']['unlabelled_ordinate_intervals'].insert(0,copy.deepcopy(d['aggregate']['A']['unlabelled_ordinate_intervals'][0]))),
        ('false_complete_factor_count',lambda d:d['factors']['-24']['root_intervals'].pop()),
        ('wrong_integer_height_count',lambda d:d['aggregate']['B']['integer_height_counts'][1].update(positive_zero_count=1)),
        ('wrong_character_identity',lambda d:d['factors']['8'].update(conrey_number=3))]:
        changed=copy.deepcopy(data[0]);alter(changed)
        try:validate(changed)
        except AssertionError:controls.append({'mutation':name,'rejected_by':'factor-union and count validation','mutated_json_sha256':hashlib.sha256(canonical(changed)).hexdigest()})
        else:raise AssertionError('Accepted mutation '+name)
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'mutant.json'
        for name,alter in [
            ('omit_maximal_order_coset',lambda d:d['fields']['A']['maximal_order_coset_tests'].pop()),
            ('polynomial_discriminant_as_field_discriminant',lambda d:d['fields']['A'].update(field_discriminant=d['fields']['A']['polynomial_discriminant'])),
            ('bad_index_prime_local_model',lambda d:next(r for r in d['fields']['A']['local_factors'] if r['prime']==11).update(e=2,f=1,g=2))]:
            changed=copy.deepcopy(original);alter(changed);path.write_text(json.dumps(changed))
            try:arithmetic_audit.run(path)
            except AssertionError:controls.append({'mutation':name,'rejected_by':'independent arithmetic auditor on mutated file','mutated_file_sha256':sha(path)})
            else:raise AssertionError('Accepted mutation '+name)
    templates=output['results'][0]['robust_gate'][0]['templates']
    for name,measurement in [('field_label_leak',{'height':'7/3','positive_zero_count':1,'field_hint':'A'}),
                              ('boolean_count',{'height':'7/3','positive_zero_count':True}),
                              ('negative_count',{'height':'7/3','positive_zero_count':-1})]:
        try:decoder.select(measurement,templates)
        except ValueError:controls.append({'mutation':name,'measurement':measurement,'rejected_by':'observation schema'})
        else:raise AssertionError('Accepted mutation '+name)
    assert len(controls)==11 and grid==80 and robust==12
    return {'status':'passed','source_sha256':sha(Path(__file__)),
            'inputs_sha256':{p.name:sha(p) for p in [arithmetic]+paths+[decoded]},
            'independent_grid_counts':grid,'independent_robust_candidate_bounds':robust,
            'actual_mutated_inputs_rejected':len(controls),'controls':controls,
            'scope':'Mutations exercise the actual validators. Aggregate completeness is checked against certified factor unions, not inferred from a bare count. The count selector cannot detect an omitted observation when its input merely asserts a plausible count; trusted completeness and displacement bounds remain explicit measurement premises.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['arithmetic','spectrum160','spectrum224','decoded','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.arithmetic,[a.spectrum160,a.spectrum224],a.decoded);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'rejected_mutations':r['actual_mutated_inputs_rejected'],'independent_grid_counts':r['independent_grid_counts']}))
