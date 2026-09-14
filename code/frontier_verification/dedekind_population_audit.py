"""Audit preserved cardinality, local arithmetic and single-deletion matching independently."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_integer_audit import arithmetic_vectors

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def fixed_contract(c):
    assert c=={'source_cutoff':20,'count_stage':'complete_source_population_before_coordinate_error','complete_source_population':True,'maximum_deletions':0,'maximum_insertions':0}
    assert c['complete_source_population'] is True and all(type(c[k]) is int for k in ['source_cutoff','maximum_deletions','maximum_insertions'])
def deletion_contract(c):
    assert c=={'source_cutoff':20,'population_stage':'complete_source_population_before_coordinate_error','complete_source_population':True,'maximum_deletions_per_field':1,'maximum_insertions_per_field':0,'coordinate_error':'independent_absolute_error_on_retained_roots','root_multiplicities':'preserved_except_declared_deletions'}
    assert c['complete_source_population'] is True and all(type(c[k]) is int for k in ['source_cutoff','maximum_deletions_per_field','maximum_insertions_per_field'])
def pair_cost(a,b,mode):
    if mode=='lower':return max([F(0),a[0]-b[1],b[0]-a[1]])/2
    if mode=='upper':return (max(a[1],b[1])-min(a[0],b[0]))/2
    raise ValueError(mode)
def next_states(state,n,m):
    i,j,da,db=state;out=[]
    if i<n and j<m:out.append(((i+1,j+1,da,db),'match'))
    if i<n and da<1:out.append(((i+1,j,da+1,db),'delete_A'))
    if j<m and db<1:out.append(((i,j+1,da,db+1),'delete_B'))
    return out
def minimax(a,b,mode):
    n,m=len(a),len(b);costs={(0,0,0,0):F(0)};parents={}
    for total in range(n+m+1):
        for state in sorted(k for k in costs if k[0]+k[1]==total):
            i,j,da,db=state;assert i-da==j-db
            for nxt,move in next_states(state,n,m):
                cost=costs[state] if move!='match' else max(costs[state],pair_cost(a[i],b[j],mode))
                if nxt not in costs or cost<costs[nxt]:costs[nxt]=cost;parents[nxt]=(state,move)
    terminals=[s for s in costs if s[0]==n and s[1]==m];assert terminals==[(n,m,1,0)]
    end=terminals[0];bound=costs[end];moves=[]
    while end!=(0,0,0,0):
        prev,move=parents[end];moves.append({'move':move,'A_index':prev[0],'B_index':prev[1]});end=prev
    return bound,list(reversed(moves)),len(costs)
def threshold(a,b,mode,radius):
    todo=[(0,0,0,0)];seen=set(todo);n,m=len(a),len(b)
    while todo:
        state=todo.pop();i,j,da,db=state
        if i==n and j==m:return True
        for nxt,move in next_states(state,n,m):
            if nxt in seen:continue
            if move=='match' and pair_cost(a[i],b[j],mode)>radius:continue
            seen.add(nxt);todo.append(nxt)
    return False
def audit_population(data,classification,input_archive,spectrum_archive,arithmetic_path,measurements_archive):
    assert data['status']==classification['status']=='passed';fixed_contract(data['contract'])
    with zipfile.ZipFile(measurements_archive) as z:columns=json.loads(z.read('Measurements224.json'))['columns']
    assert data['columns']==columns and len(columns)==604
    vectors,factors=arithmetic_vectors(arithmetic_path,columns);assert len(factors)==1128
    arithmetic=json.loads(arithmetic_path.read_text())
    labels={m['class_id']:next(k for k,v in arithmetic['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in classification['retained_models']}
    assert set(labels.values())=={'A','B'}
    expected_names=['S'+str(i)+'_'+str(bits)+'.json' for bits in [160,224] for i in [1,2]]
    assert [c['input_member'] for c in data['cases']]==expected_names
    assert [c['precision_bits'] for c in data['templates_by_precision']]==[160,224]
    replays=[];false_contracts=[]
    with zipfile.ZipFile(input_archive) as inputs,zipfile.ZipFile(spectrum_archive) as spectra:
        for bits in [160,224]:
            spec=json.loads(spectra.read('Pair_Spectrum'+str(bits)+'.json'))
            # This route counts held-out aggregate lists, not the producer's individual factor contours.
            templates={k:len(spec['aggregate'][v]['unlabelled_ordinate_intervals']) for k,v in labels.items()}
            tr=next(t for t in data['templates_by_precision'] if t['precision_bits']==bits);assert templates==tr['derived_class_population_counts']
            for number,label in [(1,'A'),(2,'B')]:
                name='S'+str(number)+'_'+str(bits)+'.json';obs=json.loads(inputs.read(name));roots=obs['positive_root_intervals'];case=next(c for c in data['cases'] if c['input_member']==name)
                assert roots==spec['aggregate'][label]['unlabelled_ordinate_intervals']
                assert {k:obs[k] for k in classification['metadata']}==classification['metadata'] and obs['top']==20
                assert case['input_member_sha256']==hashlib.sha256(inputs.read(name)).hexdigest()
                n=sum(1 for _ in roots);measurement=case['measurement'];fixed_contract(measurement['contract'])
                assert set(measurement)=={'population_size','contract'} and type(measurement['population_size']) is int and measurement['population_size']==n
                selected=[k for k,v in templates.items() if v==n];assert len(selected)==1 and case['selected_class_id']==selected[0] and labels[selected[0]]==label
                assert case['predicted_coefficients']==vectors[label]
                expected=[(r,p) for r in ['0','1/3','1/2','1','10','1000000'] for p in ['plus','minus','alternating_reverse']]
                assert [(v['radius'],v['pattern']) for v in case['transformations']]==expected
                for row in case['transformations']:
                    r=F(row['radius']);pattern=row['pattern'];shifted=[]
                    for i,root in enumerate(roots):
                        direction={'plus':1,'minus':-1,'alternating_reverse':(-1)**i}[pattern]
                        shifted.append({'lo':str(F(root['lo'])+r*direction),'hi':str(F(root['hi'])+r*direction)})
                    if pattern.endswith('reverse'):shifted=list(reversed(shifted))
                    assert len(shifted)==row['population_size']==n and digest(shifted)==row['geometry_sha256'] and row['selected_class_id']==selected[0]
                collapsed=case['collapsed_geometry_control'];assert collapsed['observed_ordinates']==[10]*n and F(collapsed['sufficient_radius'])==10 and collapsed['selected_class_id']==selected[0]
                assert all(10-10<=F(root['lo'])<=F(root['hi'])<=10+10 for root in roots)
                if n==23:
                    counter=next(c for c in data['false_population_contract_counterexamples'] if c['input_member']==name)
                    fixed_contract(counter['one_deletion_with_false_fixed_contract']['contract'])
                    assert counter['one_deletion_with_false_fixed_contract']['population_size']==22 and counter['actual_source_class_id']==selected[0]
                    wrong=[k for k,v in templates.items() if v==22];assert len(wrong)==1 and wrong[0]==counter['wrong_class_id_if_contract_falsely_asserted'] and wrong[0]!=selected[0]
                    false_contracts.append({'input_member':name,'wrong_field_selection_under_false_preservation_claim_verified':True})
                replays.append({'input_member':name,'source_population':n,'selected_class_id':selected[0],'coefficient_comparisons':604,'coordinate_transformations':18,'collapsed_radius':'10'})
    assert data['coordinate_transformations_checked']==72 and data['collapsed_geometry_controls']==4 and len(data['false_population_contract_counterexamples'])==2
    return {'cases':replays,'independent_polynomial_factorizations':len(factors),'field_factorizations':factors,'unique_field_coefficient_comparisons':1208,
            'observation_coefficient_comparisons':2416,'coordinate_transformations':72,'collapsed_geometry_controls':4,'false_contract_counterexamples':false_contracts,'heldout_class_mapping':labels}
def audit_matching(data,population,input_archive):
    assert data['status']==population['status']=='passed';deletion_contract(data['contract'])
    assert [c['precision_bits'] for c in data['cases']]==[160,224];results=[]
    with zipfile.ZipFile(input_archive) as z:
        for case in data['cases']:
            bits=case['precision_bits'];deletion_contract(case['contract'])
            names=['S1_'+str(bits)+'.json','S2_'+str(bits)+'.json'];sources=[json.loads(z.read(n)) for n in names]
            a,b=[[(F(x['lo']),F(x['hi'])) for x in v['positive_root_intervals']] for v in sources]
            assert [len(a),len(b)]==case['source_population_sizes']==[23,22]
            assert case['input_members_sha256']=={n:hashlib.sha256(z.read(n)).hexdigest() for n in names}
            for roots in [a,b]:assert all(0<lo<hi<20 for lo,hi in roots) and all(x[1]<y[0] for x,y in zip(roots,roots[1:]))
            possible=[]
            for count in range(24):
                if all(0<=length-count<=1 for length in [23,22]):possible.append(count)
            assert possible==case['possible_common_population_sizes']==[22] and case['required_deletions']==[1,0]
            lower,lp,ls=minimax(a,b,'lower');upper,up,us=minimax(a,b,'upper')
            assert lower==F(case['true_ambiguity_threshold_lower']) and upper==F(case['constructive_common_observation_radius'])
            assert 0<lower<=upper and F(case['threshold_bracket_width'])==upper-lower==F(2,10**30)
            eps=F(1,10**100)
            for mode,cost in [('lower',lower),('upper',upper)]:assert threshold(a,b,mode,cost) and not threshold(a,b,mode,cost-eps)
            omit=case['witness_omitted_A_index_zero_based'];assert type(omit) is int and 0<=omit<23
            retained=a[:omit]+a[omit+1:];observed=list(map(F,case['common_observation']))
            assert len(observed)==len(retained)==len(b)==22 and all(0<x<20 for x in observed) and all(x<y for x,y in zip(observed,observed[1:]))
            checks=0
            for roots in [retained,b]:
                for t,(lo,hi) in zip(observed,roots):assert t-upper<=lo<=hi<=t+upper;checks+=2
            rows=case['all_single_deletion_cases'];assert [r['omitted_A_index_zero_based'] for r in rows]==list(range(23))
            replayed=0;all_lower=[];all_upper=[]
            for deleted,r in enumerate(rows):
                ar=a[:deleted]+a[deleted+1:];assert len(r['pairs'])==22;actual_lower=[];actual_upper=[]
                for index,(pa,pb,p) in enumerate(zip(ar,b,r['pairs'])):
                    assert p['retained_index']==index and p['source_A_index']==(index if index<deleted else index+1) and p['source_B_index']==index
                    assert list(map(F,p['A_interval']))==list(pa) and list(map(F,p['B_interval']))==list(pb)
                    lo=pair_cost(pa,pb,'lower');hi=pair_cost(pa,pb,'upper');center=(min(pa[0],pb[0])+max(pa[1],pb[1]))/2
                    assert F(p['radius_lower'])==lo and F(p['uniform_radius_upper'])==hi and F(p['common_ordinate'])==center
                    actual_lower.append(lo);actual_upper.append(hi);replayed+=1
                assert max(actual_lower)==F(r['radius_lower']) and max(actual_upper)==F(r['uniform_radius_upper'])
                all_lower.append(max(actual_lower));all_upper.append(max(actual_upper))
            assert min(all_lower)==lower and min(all_upper)==upper
            assert case['minimizing_lower_deletion_indices']==[i for i,c in enumerate(all_lower) if c==lower]
            assert case['minimizing_upper_deletion_indices']==[i for i,c in enumerate(all_upper) if c==upper] and omit==case['minimizing_upper_deletion_indices'][0]
            assert observed==[F(p['common_ordinate']) for p in rows[omit]['pairs']]
            pc=[next(c for c in population['cases'] if c['input_member']==n) for n in names]
            assert case['distinct_actual_field_classes']==[p['selected_class_id'] for p in pc] and len(set(case['distinct_actual_field_classes']))==2
            differing=[col['n'] for col,x,y in zip(population['columns'],pc[0]['predicted_coefficients'],pc[1]['predicted_coefficients']) if x!=y]
            assert differing==case['differing_coefficient_indices'] and len(differing)==148
            assert case['differing_target_indices']==[n for n in differing if n<=31]==[3,7,19,27,31]
            assert case['claims']=={'no_common_observation_at_any_radius_strictly_below_lower':True,'explicit_common_observation_at_upper_and_all_larger_radii':True,'exact_threshold_inside_bracket_not_claimed_known':True}
            results.append({'precision_bits':bits,'DP_lower':str(lower),'DP_upper':str(upper),'bound_gap':str(upper-lower),'DP_states':[ls,us],
                            'lower_path':lp,'upper_path':up,'endpoint_inclusions':checks,'pair_rows_replayed':replayed,'threshold_boundary_checks':4,
                            'common_population':22,'verified_actual_class_ids':case['distinct_actual_field_classes'],'differing_coefficients':148,'differing_targets':[3,7,19,27,31]})
    assert data['new_roots_computed']==0
    return {'cases':results,'total_pair_rows_replayed':1012,'total_endpoint_inclusions':176,'total_threshold_boundary_checks':8,
            'DP_scope':'Minimax costs and independent boolean reachability cover all ordered match/delete paths under the exact one-deletion budget. Written uncrossing reduces arbitrary matchings to this ordered problem.'}
def run(population_path,matching_path,class_path,input_archive,spectrum_archive,arithmetic_path,measurements_archive,proposal_path):
    population=json.loads(population_path.read_text());matching=json.loads(matching_path.read_text());classification=json.loads(class_path.read_text())
    assert matching['inputs_sha256']=={p.name:sha(p) for p in [input_archive,population_path,proposal_path]}
    assert population['inputs_sha256'][class_path.name]==sha(class_path) and population['inputs_sha256'][input_archive.name]==sha(input_archive) and population['inputs_sha256'][spectrum_archive.name]==sha(spectrum_archive)
    pa=audit_population(population,classification,input_archive,spectrum_archive,arithmetic_path,measurements_archive)
    ma=audit_matching(matching,population,input_archive)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [population_path,matching_path,class_path,input_archive,spectrum_archive,arithmetic_path,measurements_archive,proposal_path]},
            'population_audit':pa,'matching_audit':ma,
            'scope':'Fresh polynomial arithmetic, held-out aggregate cardinalities, coordinate-erasure controls, minimax dynamic programming, independent boolean reachability and exact interval witness checks support the two distinct observation models. General field classification, spectral completeness and the written matching argument retain their separately declared proof scope.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['population','matching','classification','inputs','spectra','arithmetic','measurements','proposal','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.population,a.matching,a.classification,a.inputs,a.spectra,a.arithmetic,a.measurements,a.proposal)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','polynomial_factorizations':1128,'observation_coefficient_comparisons':2416,'matching_pair_rows':1012,'endpoint_inclusions':176,'threshold_boundary_checks':8}))
