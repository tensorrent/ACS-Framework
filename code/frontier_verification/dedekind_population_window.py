"""Audit finite-window ambiguity caused by coordinate noise alone and subsequent censoring."""
import argparse,copy,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path

CONTRACT={'observation_window':['0','20'],'window_endpoints':'open','source_population':'all_positive_nontrivial_zero_ordinates_with_multiplicity',
          'coordinate_error':'independent_absolute_error_before_window_selection','observe_every_transformed_entry_inside_window':True,
          'arbitrary_insertions_or_deletions':False,'unknown_source_ordinates_above20':'left_unchanged_in_the_constructive_witness'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(data,matching,critical,input_archive):
    assert data['status']==matching['status']==critical['status']=='passed' and data['contract']==CONTRACT
    assert data['contract']['observe_every_transformed_entry_inside_window'] is True and data['contract']['arbitrary_insertions_or_deletions'] is False
    assert [c['precision_bits'] for c in data['cases']]==[160,224];checked=0;results=[]
    with zipfile.ZipFile(input_archive) as z:
        for case,matched,gap in zip(data['cases'],matching['cases'],critical['cases']):
            bits=case['precision_bits'];assert bits==matched['precision_bits']==gap['precision_bits']
            sources=[json.loads(z.read('S'+str(i)+'_'+str(bits)+'.json'))['positive_root_intervals'] for i in [1,2]]
            a,b=[[(F(r['lo']),F(r['hi'])) for r in roots] for roots in sources];L,U=map(F,gap['root_gap_interval'])
            assert [len(a),len(b)]==[23,22] and case['threshold_interval']==[str(L),str(U)]
            assert case['exact_symbolic_threshold']==critical['exact_symbolic_threshold']
            assert [v['source'] for v in case['protected_prefixes']]==['A','B']
            for roots,record in zip([a,b],case['protected_prefixes']):
                assert record['always_retained_source_indices_zero_based']==[0,1]
                lower=roots[0][0]-U;upper=20-roots[1][1]-U
                assert lower>0 and upper>0 and record['lower_boundary_margin']==str(lower) and record['upper_boundary_margin']==str(upper)
                # Doubled endpoint arithmetic independently verifies both protected roots.
                for lo,hi in roots[:2]:assert lo-U>0 and hi+U<20;checked+=2
            exit_record=case['A_boundary_exit'];assert exit_record['source_index_zero_based']==22
            target=F(exit_record['observed_value_outside_window']);cost=max(abs(target-a[-1][0]),abs(target-a[-1][1]))
            assert target>20 and a[-1][1]<20 and cost<L
            assert F(exit_record['uniform_error_upper'])==cost and F(exit_record['critical_lower_minus_exit_error'])==L-cost
            expected=20+(L-(20-a[-1][0]))/2;assert target==expected;checked+=3
            row=matched['all_single_deletion_cases'][22];assert row['omitted_A_index_zero_based']==22 and 22 in gap['optimal_deletion_indices_zero_based']
            observed=list(map(F,case['common_observation']));assert len(observed)==22 and observed==[F(p['common_ordinate']) for p in row['pairs']]
            assert all(0<t<20 for t in observed) and all(t<u for t,u in zip(observed,observed[1:]))
            for roots in [a[:-1],b]:
                assert len(roots)==len(observed)
                for t,(lo,hi) in zip(observed,roots):assert t-U<=lo<=hi<=t+U;checked+=2
            assert case['A_after_noise_source_population_size_through20']==23 and case['B_after_noise_source_population_size_through20']==22
            assert case['visible_population_after_window_selection']==[22,22]
            assert case['unknown_tail_error']=='0' and case['complete_tail_coverage_argument']=='Every unrecorded positive source ordinate is at least20 by inherited finite completeness; leaving it unchanged keeps it outside the open window.'
            assert case['common_observation_compatible_actual_classes']==matched['distinct_actual_field_classes']
            results.append({'precision_bits':bits,'protected_prefix_root_checks':8,'exit_checks':3,'matched_endpoint_checks':88,
                            'window_membership_complete_for_constructed_noise_map':True,'unknown_tail_left_unchanged':True})
    assert data['no_new_zero_computations_required'] and data['allowed_arbitrary_deletions']==0
    return {'cases':results,'total_exact_inequalities':checked,
            'proof_scope':'The finite inequalities protect the first two source roots and construct an exit of A last source root. Completeness through20 identifies every source entry originally inside the window; outside entries are fixed. General lower and upper arguments are written and use elementary Lean interval/uncrossing lemmas.'}
def run(matching_path,critical_path,input_archive):
    matching=json.loads(matching_path.read_text());critical=json.loads(critical_path.read_text());cases=[]
    assert matching['status']==critical['status']=='passed'
    with zipfile.ZipFile(input_archive) as z:
        for matched,gap in zip(matching['cases'],critical['cases']):
            bits=matched['precision_bits'];assert gap['precision_bits']==bits;L,U=map(F,gap['root_gap_interval'])
            a,b=[[(F(r['lo']),F(r['hi'])) for r in json.loads(z.read('S'+str(i)+'_'+str(bits)+'.json'))['positive_root_intervals']] for i in [1,2]]
            prefixes=[]
            for label,roots in [('A',a),('B',b)]:
                lower=roots[0][0]-U;upper=20-roots[1][1]-U;assert lower>0 and upper>0
                prefixes.append({'source':label,'always_retained_source_indices_zero_based':[0,1],'lower_boundary_margin':str(lower),'upper_boundary_margin':str(upper)})
            eta=(L-(20-a[-1][0]))/2;assert eta>0;target=20+eta;exit_error=target-a[-1][0]
            assert exit_error<L and target>a[-1][1]
            row=matched['all_single_deletion_cases'][22];assert row['uniform_radius_upper']==str(U)
            cases.append({'precision_bits':bits,'threshold_interval':[str(L),str(U)],'exact_symbolic_threshold':critical['exact_symbolic_threshold'],
                          'protected_prefixes':prefixes,'A_boundary_exit':{'source_index_zero_based':22,'observed_value_outside_window':str(target),'uniform_error_upper':str(exit_error),'critical_lower_minus_exit_error':str(L-exit_error)},
                          'common_observation':[p['common_ordinate'] for p in row['pairs']],
                          'A_after_noise_source_population_size_through20':23,'B_after_noise_source_population_size_through20':22,
                          'visible_population_after_window_selection':[22,22],'unknown_tail_error':'0',
                          'complete_tail_coverage_argument':'Every unrecorded positive source ordinate is at least20 by inherited finite completeness; leaving it unchanged keeps it outside the open window.',
                          'common_observation_compatible_actual_classes':matched['distinct_actual_field_classes']})
    data={'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [matching_path,critical_path,input_archive]},
          'contract':CONTRACT,'cases':cases,'allowed_arbitrary_deletions':0,'no_new_zero_computations_required':True,
          'lower_bound_proof':'For any radius below the critical root gap, which is at most U, both source first two roots must remain inside the observed window. Every other retained source root has larger original ordinate. Any identical observed finite multisets induce a bijection between the retained source multisets with pair distances at most twice the radius. Uncrossing implies their sorted second roots must satisfy that bound, contradicting the critical gap. Tail entries may enter or leave; they cannot change the first two retained source ranks.',
          'upper_bound_proof':'Pair A first22 source roots with all22 recorded B roots using their actual midpoints. Critical-gap dominance bounds their errors by the exact symbolic threshold. Move A last recorded source root to the fixed rational exit value above20; its error is strictly below L. Leave every other positive source ordinate unchanged, outside the window. Both windowed observations are then identical, with no arbitrary insertion/deletion. The stored rational midpoint-hull observation gives the uniform certificate at U.',
          'scope':'An ideal complete observation of the open window after bounded coordinate noise has the same exact symbolic ambiguity threshold as the one-deletion model for this field pair. All zero entries remain in the transformed source family; one exits the displayed window. This is not a claim of infinite-spectrum equality, a physical detector implementation, or robustness under unmodeled missed/extra roots.'}
    data['independent_interval_audit']=verify(data,matching,critical,input_archive)
    tests=[]
    for name,change in [('exit_point_remains_inside_window',lambda d:d['cases'][0]['A_boundary_exit'].update(observed_value_outside_window='19')),
                         ('incorrect_protected_prefix',lambda d:d['cases'][0]['protected_prefixes'][0].update(always_retained_source_indices_zero_based=[1,2])),
                         ('unjustified_tail_shift',lambda d:d['cases'][0].update(unknown_tail_error='1')),
                         ('retain_original_window_count_after_exit',lambda d:d['cases'][0].update(visible_population_after_window_selection=[23,22])),
                         ('allow_unmodeled_deletions',lambda d:d.update(allowed_arbitrary_deletions=1))]:
        changed=copy.deepcopy(data);change(changed)
        try:verify(changed,matching,critical,input_archive)
        except (AssertionError,ValueError):tests.append({'mutation':name,'rejected':True})
        else:raise AssertionError('Window mutation accepted: '+name)
    data['mutations']=tests;assert len(tests)==5
    return data
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['matching','critical','inputs','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.matching,a.critical,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':'passed','arbitrary_deletions':0,'window_population':[22,22],'inequalities':r['independent_interval_audit']['total_exact_inequalities'],'new_roots':0,'mutations_rejected':5}))
