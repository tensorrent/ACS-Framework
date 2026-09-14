"""Challenge cardinality contracts, missing-root certificates and ordered matching."""
import argparse,copy,hashlib,itertools,json,zipfile
from fractions import Fraction as F
from pathlib import Path
import dedekind_population_decoder as decoder
import dedekind_population_matching as matching
import dedekind_population_audit as audit

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reject(name,fn):
    try:fn()
    except (AssertionError,ValueError):return {'mutation':name,'rejected':True}
    raise AssertionError('Mutation was accepted: '+name)
def exhaustive_ordered_matching():
    grid=[-1,0,1];problems=0;assignments=0;maximum_size=4
    for size in range(1,maximum_size+1):
        for a in itertools.combinations_with_replacement(grid,size+1):
            for b in itertools.combinations_with_replacement(grid,size):
                literal=[]
                for omitted in range(len(a)):
                    kept=a[:omitted]+a[omitted+1:]
                    for permutation in itertools.permutations(range(size)):
                        literal.append(max(abs(kept[i]-b[permutation[i]]) for i in range(size)));assignments+=1
                expected=F(min(literal),2)
                for mode in ['lower','upper']:
                    cost,path,states=audit.minimax([(F(v),F(v)) for v in a],[(F(v),F(v)) for v in b],mode)
                    assert cost==expected
                problems+=1
    assert problems==543 and assignments==41796
    # Ordering is a necessary premise of the uncrossing lemma.
    a,ap,b,bp=1,0,0,1
    crossed=max(abs(a-bp),abs(ap-b));straight=max(abs(a-b),abs(ap-bp))
    assert crossed==0 and straight==1 and not a<=ap
    return {'sorted_multiset_problems':problems,'arbitrary_indexed_matchings_enumerated':assignments,'largest_retained_population':maximum_size,
            'coordinate_grid':grid,'duplicates_and_negative_coordinates_included':True,
            'uncrossing_without_order_counterexample':{'A':[a,ap],'B':[b,bp],'crossed_max_distance':crossed,'straight_max_distance':straight}}
def run(population_path,matching_path,class_path,input_archive,spectrum_archive,arithmetic_path,measurements_archive):
    pop=json.loads(population_path.read_text());match=json.loads(matching_path.read_text());classified=json.loads(class_path.read_text())
    def pa(d):return audit.audit_population(d,classified,input_archive,spectrum_archive,arithmetic_path,measurements_archive)
    def ma(d):return audit.audit_matching(d,pop,input_archive)
    pa(pop);ma(match);mutations=[]
    templates=pop['templates_by_precision'][0]['derived_class_population_counts'];measurement=copy.deepcopy(pop['cases'][0]['measurement'])
    assert len(decoder.select_population(measurement,templates))==1
    for name,key,value in [('false_completeness','complete_source_population',False),('deletion_budget_in_fixed_population','maximum_deletions',1),
                           ('insertion_budget_in_fixed_population','maximum_insertions',1),('count_after_noise_censoring','count_stage','observed_window_after_coordinate_error')]:
        m=copy.deepcopy(measurement);m['contract'][key]=value
        mutations.append(reject(name,lambda m=m:decoder.select_population(m,templates)))
    for name,modify in [('leaked_ordinates',lambda m:m.update(ordinates=[10])),('Boolean_population_count',lambda m:m.update(population_size=True)),
                        ('negative_population_count',lambda m:m.update(population_size=-1))]:
        m=copy.deepcopy(measurement);modify(m);mutations.append(reject(name,lambda m=m:decoder.select_population(m,templates)))
    d=copy.deepcopy(pop);d['templates_by_precision'][0]['derived_class_population_counts'].pop(next(iter(templates)))
    mutations.append(reject('omit_a_complete_field_candidate',lambda:pa(d)))
    d=copy.deepcopy(pop);index=next(i for i,c in enumerate(d['columns']) if c['n']==7);d['cases'][0]['predicted_coefficients'][index]+=1
    mutations.append(reject('corrupt_arithmetic_after_population_selection',lambda:pa(d)))
    d=copy.deepcopy(pop);d['cases'][0]['collapsed_geometry_control']['observed_ordinates']=[10]
    mutations.append(reject('deduplicate_root_multiplicities',lambda:pa(d)))
    for name,key,value in [('zero_deletion_budget_for_shared_observation','maximum_deletions_per_field',0),
                           ('allow_an_insertion','maximum_insertions_per_field',1),('Boolean_deletion_budget','maximum_deletions_per_field',True),
                           ('missing_source_completeness','complete_source_population',False)]:
        c=copy.deepcopy(match['contract']);c[key]=value
        mutations.append(reject(name,lambda c=c:matching.validate_contract(c)))
    d=copy.deepcopy(match);d['cases'][0]['common_observation'].pop()
    mutations.append(reject('zip_truncation_loses_an_observed_root',lambda:ma(d)))
    d=copy.deepcopy(match);d['cases'][0]['required_deletions']=[2,1];d['cases'][0]['possible_common_population_sizes']=[21]
    mutations.append(reject('silently_delete_from_both_sources',lambda:ma(d)))
    d=copy.deepcopy(match);d['cases'][0]['all_single_deletion_cases'].pop()
    mutations.append(reject('omit_a_deletion_case',lambda:ma(d)))
    d=copy.deepcopy(match);d['cases'][0]['all_single_deletion_cases'][0]['pairs'][0]['source_A_index']=0
    mutations.append(reject('wrong_source_matching_index',lambda:ma(d)))
    d=copy.deepcopy(match);p=d['cases'][0]['all_single_deletion_cases'][0]['pairs'][0];p['A_interval'][0]=str(F(p['A_interval'][0])+1)
    mutations.append(reject('forged_source_interval_endpoint',lambda:ma(d)))
    d=copy.deepcopy(match);c=d['cases'][0];c['constructive_common_observation_radius']=str(F(c['constructive_common_observation_radius'])-F(1,10**12))
    mutations.append(reject('understate_common_observation_radius',lambda:ma(d)))
    d=copy.deepcopy(match);c=d['cases'][0];c['true_ambiguity_threshold_lower']=str(F(c['true_ambiguity_threshold_lower'])+F(1,10**12))
    mutations.append(reject('overstate_impossibility_threshold',lambda:ma(d)))
    d=copy.deepcopy(match);c=d['cases'][0];c['common_observation'][0]=str(F(c['common_observation'][0])+1)
    mutations.append(reject('corrupt_shared_ordinate',lambda:ma(d)))
    d=copy.deepcopy(match);d['cases'][0]['distinct_actual_field_classes']*=0
    mutations.append(reject('erase_actual_field_distinction',lambda:ma(d)))
    d=copy.deepcopy(match);d['cases'][0]['claims']['exact_threshold_inside_bracket_not_claimed_known']=False
    mutations.append(reject('claim_exact_threshold_inside_unresolved_bracket',lambda:ma(d)))
    d=copy.deepcopy(match);d['cases'].pop()
    mutations.append(reject('omit_second_precision',lambda:ma(d)))
    assert len(mutations)==25
    # A literal zip-only endpoint loop accepts this invalid shortened witness.
    case=match['cases'][0];observed=list(map(F,case['common_observation']))[:-1];omit=case['witness_omitted_A_index_zero_based'];radius=F(case['constructive_common_observation_radius'])
    with zipfile.ZipFile(input_archive) as z:
        roots=[]
        for name in ['S1_160.json','S2_160.json']:
            roots.append([(F(r['lo']),F(r['hi'])) for r in json.loads(z.read(name))['positive_root_intervals']])
    retained=[roots[0][:omit]+roots[0][omit+1:],roots[1]]
    naive=all(abs(t-x)<=radius for source in retained for t,pair in zip(observed,source) for x in pair)
    assert naive and len(observed)==21 and [len(r)-len(observed) for r in roots]==[2,1]
    finite=exhaustive_ordered_matching()
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [population_path,matching_path,class_path,input_archive,spectrum_archive,arithmetic_path,measurements_archive]},
            'actual_component_mutations_rejected':len(mutations),'mutations':mutations,'finite_arbitrary_matching_crosscheck':finite,
            'actual_zip_truncation_counterexample':{'naive_endpoint_loop_accepts':naive,'observed_population':21,'required_deletions':[2,1],'permitted_deletions_per_field':1,'correct_auditor_rejects':True},
            'unverifiable_contract_limitation':'The intact population selector can be deceived by a false completeness/preservation declaration. Two concrete A-to-B misclassifications after a deletion are preserved in Population_Decoder.json and independently audited; a scalar count cannot authenticate those premises.',
            'scope':'Twenty-five actual mutations, an accepted-by-zip invalid witness and 41796 arbitrary finite matchings supplement the exact real-field certificates and Lean observation lemmas. Finite grid exhaustion does not replace the written general matching proof or certify unknown external input completeness.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['population','matching','classification','inputs','spectra','arithmetic','measurements','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.population,a.matching,a.classification,a.inputs,a.spectra,a.arithmetic,a.measurements)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','mutations_rejected':25,'finite_matching_problems':543,'literal_matchings':41796,'zip_truncation_false_acceptance_verified':True}))
