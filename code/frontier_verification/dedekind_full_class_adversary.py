"""Challenge the full-class derivation and the exact scope of count-only decoding."""
import argparse,copy,hashlib,json,tempfile
from pathlib import Path
import dedekind_full_quartic_audit as class_audit
import dedekind_class_count_audit as count_audit
from dedekind_full_quartic_class import check_metadata
from dedekind_class_count_decode import select,envelope

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(class_path,metadata_path,controls_path,decoded_path,class_audit_path,spectra,observations,arithmetic,old_decoding,measurements):
    read=lambda p:json.loads(p.read_text());data=read(class_path);decoded=read(decoded_path);controls=read(controls_path);records=[]
    def reject(name,call):
        try:call()
        except (AssertionError,ValueError):records.append({'mutation':name,'rejected':True});return
        raise AssertionError('Accepted mutation: '+name)
    def group_mutation(name,mutate):
        d=copy.deepcopy(data['group_certificate']);mutate(d);reject(name,lambda:class_audit.audit_groups(d))
    group_mutation('omit_transitive_A4_candidate',lambda d:d['transitive_subgroups'].pop())
    group_mutation('invent_normal_wild_C3_inside_A4',lambda d:d['cubic_quotient_ramified_at_3_candidates'][-1].__setitem__('normal_wild_3_subgroups',d['cubic_quotient_ramified_at_3_candidates'][0]['normal_wild_3_subgroups']))
    group_mutation('enlarge_C3_normalizer_to_A4',lambda d:d['cubic_quotient_ramified_at_3_candidates'][0].__setitem__('normalizer',d['even_indices']))
    group_mutation('use_tame_exponent_two_at_wild_prime_three',lambda d:d['cubic_quotient_ramified_at_3_candidates'][0].__setitem__('minimum_discriminant_exponent',2))
    group_mutation('replace_strict_Minkowski_obstruction_by_one',lambda d:d['unramified_cubic_minkowski_bound'].__setitem__('ideal_norm_upper','1'))
    d=copy.deepcopy(data);d['retained_models'].pop();reject('drop_one_complete_field_candidate',lambda:class_audit.audit_characters(d))
    metadata=read(metadata_path);bad={**metadata,'Galois_group':'V4'};reject('supply_Galois_group_as_metadata_input',lambda:check_metadata(bad))
    templates=decoded['cases'][0]['candidate_count_envelopes']
    reject('leak_field_label_to_count_selector',lambda:select({'height':'20','positive_zero_count':23,'field':'A'},templates))
    reject('accept_boolean_count_as_integer',lambda:select({'height':'20','positive_zero_count':True},templates))
    roots=read(observations[0])['positive_root_intervals'];reject('assume_no_unknown_roots_enter_noisy_cutoff_20',lambda:envelope(roots,'20','1/3','20'))
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/decoded_path.name
        def count_mutation(name,mutate):
            d=copy.deepcopy(decoded);mutate(d);p.write_text(json.dumps(d))
            reject(name,lambda:count_audit.run(p,class_path,class_audit_path,spectra,observations,arithmetic,old_decoding,measurements))
        index=next(i for i,c in enumerate(decoded['columns']) if c['n']==7);key=next(iter(decoded['derived_class_predictions']))
        count_mutation('corrupt_predicted_coefficient_at_seven',lambda d:d['derived_class_predictions'][key].__setitem__(index,1))
        count_mutation('claim_unique_field_from_ambiguous_half_radius_count',lambda d:next(c for c in d['cases'] if c['radius']=='1/2').__setitem__('field_unique_for_every_admissible_count',True))
        count_mutation('drop_an_observation_precision_case',lambda d:d['cases'].pop())
    assert len(records)==13 and select({'height':'20','positive_zero_count':0},templates)==[]
    negative=check_metadata({'degree':4,'discriminant':400,'real_places':2,'complex_places':1});assert not negative['signed_discriminant_square'] and not negative['A4_excluded_by_cubic_quotient_obstruction']
    fields=[]
    for c in controls['fields']:
        assert c['Galois_group']=='A4' and c['round_two_lattice_agreement']
        m={'degree':4,'discriminant':c['field_discriminant'],'real_places':0,'complex_places':2};decision=check_metadata(m)
        assert decision==c['metadata_guard_result'] and not decision['A4_excluded_by_cubic_quotient_obstruction']
        fields.append({'actual_A4_discriminant':c['field_discriminant'],'guarded_A4_exclusion':False,'reason':'extra_ramified_prime_7' if c['field_discriminant']==3136 else 'wild_exponent_4_at_3'})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [class_path,metadata_path,controls_path,decoded_path,class_audit_path,arithmetic,old_decoding,measurements]+spectra+observations},
            'actual_component_mutations_rejected':13,'mutations':records,'actual_A4_hypothesis_controls':fields,'signed_discriminant_guard':negative,'incompatible_count_returns_empty':True,
            'scope':'Semantic checks reject broken group coverage, normality, wild exponent, Minkowski bound, class completeness, leaked labels, malformed counts, insufficient completeness margin and forged decoding results. Two certified A4 fields remain allowed when the exact metadata hypotheses are relaxed. Count-statistic ambiguity is not asserted for full spectra.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['classification','metadata','controls','decoded','class-audit','arithmetic','old-decoding','measurements','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--spectra',type=Path,nargs=2,required=True);p.add_argument('--observations',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.classification,a.metadata,a.controls,a.decoded,a.class_audit,a.spectra,a.observations,a.arithmetic,a.old_decoding,a.measurements);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','mutations_rejected':13,'actual_A4_controls':2}))
