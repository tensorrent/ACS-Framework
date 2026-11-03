"""Certify a common finite observation of two actual fields when one root may be missing."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path

CONTRACT={'source_cutoff':20,'population_stage':'complete_source_population_before_coordinate_error',
          'complete_source_population':True,'maximum_deletions_per_field':1,'maximum_insertions_per_field':0,
          'coordinate_error':'independent_absolute_error_on_retained_roots','root_multiplicities':'preserved_except_declared_deletions'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_contract(contract):
    if set(contract)!=set(CONTRACT):raise ValueError('Explicit deletion model required')
    for k in ['source_cutoff','maximum_deletions_per_field','maximum_insertions_per_field']:
        if type(contract[k]) is not int:raise ValueError('Integer cutoff and edit budgets required')
    if contract!=CONTRACT or contract['complete_source_population'] is not True:raise ValueError('Different observation contract')
def common_population_sizes(n,m,deletions):
    assert all(type(x) is int and x>=0 for x in [n,m,deletions])
    return sorted(set(range(max(0,n-deletions),n+1))&set(range(max(0,m-deletions),m+1)))
def intervals(data):
    assert data['top']==20
    result=[(F(r['lo']),F(r['hi'])) for r in data['positive_root_intervals']]
    assert all(0<lo<hi<20 for lo,hi in result) and all(a[1]<b[0] for a,b in zip(result,result[1:]))
    return result
def matching_certificate(a,b,contract):
    validate_contract(contract);assert [len(a),len(b)]==[23,22]
    populations=common_population_sizes(len(a),len(b),contract['maximum_deletions_per_field']);assert populations==[22]
    rows=[]
    for omit in range(len(a)):
        retained=[r for i,r in enumerate(a) if i!=omit];pairs=[]
        assert len(retained)==len(b)==22
        for index,(ar,br) in enumerate(zip(retained,b)):
            alo,ahi=ar;blo,bhi=br;lo=min(alo,blo);hi=max(ahi,bhi);center=(lo+hi)/2
            lower=max(F(0),alo-bhi,blo-ahi)/2;upper=(hi-lo)/2
            assert all(abs(center-x)<=upper for x in [alo,ahi,blo,bhi])
            pairs.append({'retained_index':index,'source_A_index':index if index<omit else index+1,'source_B_index':index,
                          'A_interval':list(map(str,ar)),'B_interval':list(map(str,br)),
                          'common_ordinate':str(center),'radius_lower':str(lower),'uniform_radius_upper':str(upper)})
        lower=max(F(p['radius_lower']) for p in pairs);upper=max(F(p['uniform_radius_upper']) for p in pairs)
        centers=[F(p['common_ordinate']) for p in pairs]
        assert all(0<c<20 for c in centers) and all(x<y for x,y in zip(centers,centers[1:]))
        rows.append({'omitted_A_index_zero_based':omit,'radius_lower':str(lower),'uniform_radius_upper':str(upper),'pairs':pairs})
    L=min(F(r['radius_lower']) for r in rows);U=min(F(r['uniform_radius_upper']) for r in rows)
    best=next(r for r in rows if F(r['uniform_radius_upper'])==U);assert 0<L<=U
    return {'contract':contract,'source_population_sizes':[len(a),len(b)],'possible_common_population_sizes':populations,
            'required_deletions':[1,0],'all_single_deletion_cases':rows,
            'true_ambiguity_threshold_lower':str(L),'constructive_common_observation_radius':str(U),'threshold_bracket_width':str(U-L),
            'minimizing_lower_deletion_indices':[r['omitted_A_index_zero_based'] for r in rows if F(r['radius_lower'])==L],
            'minimizing_upper_deletion_indices':[r['omitted_A_index_zero_based'] for r in rows if F(r['uniform_radius_upper'])==U],
            'witness_omitted_A_index_zero_based':best['omitted_A_index_zero_based'],
            'common_observation':[p['common_ordinate'] for p in best['pairs']],
            'claims':{'no_common_observation_at_any_radius_strictly_below_lower':True,'explicit_common_observation_at_upper_and_all_larger_radii':True,
                      'exact_threshold_inside_bracket_not_claimed_known':True}}
def run(input_archive,population_path,proposal_path):
    population=json.loads(population_path.read_text());proposal=json.loads(proposal_path.read_text())
    assert population['status']=='passed' and population['inputs_sha256'][input_archive.name]==sha(input_archive)
    assert proposal['status']=='proposal_pending_independent_audit'
    cases=[]
    with zipfile.ZipFile(input_archive) as z:
        for bits in [160,224]:
            names=['S1_'+str(bits)+'.json','S2_'+str(bits)+'.json'];data=[json.loads(z.read(n)) for n in names]
            for k in ['degree','discriminant','real_places','complex_places','top']:assert data[0][k]==data[1][k]
            a,b=map(intervals,data);result=matching_certificate(a,b,dict(CONTRACT));result['precision_bits']=bits
            result['input_members_sha256']={n:hashlib.sha256(z.read(n)).hexdigest() for n in names}
            pc=[next(c for c in population['cases'] if c['input_member']==n) for n in names]
            assert all(p['input_member_sha256']==result['input_members_sha256'][n] for p,n in zip(pc,names))
            result['distinct_actual_field_classes']=[p['selected_class_id'] for p in pc];assert len(set(result['distinct_actual_field_classes']))==2
            different=[col['n'] for col,x,y in zip(population['columns'],pc[0]['predicted_coefficients'],pc[1]['predicted_coefficients']) if x!=y]
            assert len(different)==148 and 7 in different
            result['differing_coefficient_indices']=different
            result['differing_target_indices']=[n for n in different if n<=31]
            old=next(r for r in proposal['cases'] if r['precision_bits']==bits)
            assert result['true_ambiguity_threshold_lower']==old['optimal_radius_lower'] and result['constructive_common_observation_radius']==old['constructive_radius_upper']
            assert result['common_observation']==old['common_observation']
            cases.append(result)
    assert all(c['threshold_bracket_width']==str(F(2,10**30)) for c in cases)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [input_archive,population_path,proposal_path]},
            'contract':CONTRACT,'cases':cases,'new_roots_computed':0,
            'derivation':['Without deletions, unequal cardinalities exclude common observations for every coordinate-error radius.',
                          'With at most one deletion per source and no insertions, any common list has22members: delete one from A and none from B.',
                          'For sorted real lists, uncrossing any inverted matching never increases the maximum paired distance. Finite inversion removal yields an ordered matching.',
                          'Two retained source roots within radius delta of a common observed point are at distance at most2delta. Each stored interval pair supplies a rational lower bound on that distance.',
                          'For each deletion, max over ordered pairs and then min over all23deletions yields a lower bound on the true ambiguity threshold.',
                          'The midpoint of each pair union hull lies within half its span of every possible true source value. The best deletion therefore supplies an explicit common observation uniformly over all certified source intervals.'],
            'scope':'This is a finite actual-field ambiguity result under the stated one-deletion observation model, conditional on inherited source classification and complete finite spectral certificates. The interval bracket has width2e-30; the exact threshold inside it is not determined. No post-noise censoring, additional roots, global infinite-spectrum ambiguity or optimal Gaussian deduction radius is claimed. Elementary uncrossing and interval lemmas are Lean-checked; the whole matching theorem and arithmetic bridge are written proofs.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['inputs','population','proposal','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.inputs,a.population,a.proposal);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':'passed','cases':[{'precision_bits':c['precision_bits'],'radius_approx':str(float(F(c['constructive_common_observation_radius']))),'bracket_width':c['threshold_bracket_width'],'witness_deleted_index':c['witness_omitted_A_index_zero_based'],'all_minimizing_deletions':c['minimizing_upper_deletion_indices']} for c in r['cases']]}))
