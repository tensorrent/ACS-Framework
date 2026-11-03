"""Independent cutoff, attainable-count, bipartite-matching and polynomial audits."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_integer_audit import arithmetic_vectors

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(p.read_text())
def attainable(roots,h,r):
    h,r=F(h),F(r);assert r>=0;counts={0}
    for lo,hi in roots:
        choices=[]
        if lo-r<h:choices.append(1)
        if hi+r>=h:choices.append(0)
        assert choices;counts={n+b for n in counts for b in choices}
    return sorted(counts)
def max_matching(costs,radius):
    owners={}
    def extend(i,seen):
        for j,c in enumerate(costs[i]):
            if c>radius or j in seen:continue
            seen.add(j)
            if j not in owners or extend(owners[j],seen):owners[j]=i;return True
        return False
    for i in range(len(costs)):extend(i,set())
    return len(owners),sorted([i,j] for j,i in owners.items())
def cutoff_audit(provenance,observations,parents,spectra):
    assert provenance['status']=='passed' and provenance['source_cutoff']=='20' and provenance['new_cutoff']=='39/2'
    assert len(provenance['cases'])==4;rows=[]
    expected=['E'+str(i)+'_'+str(bits)+'.json' for bits in [160,224] for i in [1,2]]
    assert set(observations)==set(expected) and [c['input_member'] for c in provenance['cases']]==expected
    for c in provenance['cases']:
        name=c['input_member'];index=int(name[1]);bits=c['nominal_precision_bits'];parent=parents[c['parent_member']];obs=observations[name]
        assert c['parent_member']=='S'+str(index)+'_'+str(bits)+'.json'
        assert set(obs)==set(parent)=={'degree','discriminant','real_places','complex_places','top','positive_root_intervals'}
        assert obs['top']=='39/2' and parent['top']==20
        assert {k:obs[k] for k in ['degree','discriminant','real_places','complex_places']}=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2}
        full=parent['positive_root_intervals'];factor_aggregate=spectra[bits]['aggregate'][['A','B'][index-1]]['unlabelled_ordinate_intervals'];assert full==factor_aggregate
        assert len(full)==c['parent_population']==(23 if index==1 else 22) and len(c['partition'])==len(full)
        keep=[];clearances=[];previous=F(0)
        for j,(x,p) in enumerate(zip(full,c['partition'])):
            lo,hi=F(x['lo']),F(x['hi']);assert previous<lo<hi<20;previous=hi
            inside=hi<F(39,2);outside=lo>F(39,2);assert inside!=outside
            clearance=F(39,2)-hi if inside else lo-F(39,2)
            assert p=={'source_index_zero_based':j,'side':'retained' if inside else 'excluded','cutoff_clearance':str(clearance),'source_interval':x}
            clearances.append(clearance)
            if inside:keep.append(x)
        assert obs['positive_root_intervals']==keep and len(keep)==c['retained_population']==22
        assert F(c['minimum_cutoff_clearance'])==min(clearances)>0
        rows.append({'input_member':name,'intervals_partitioned':len(full),'retained':22,'excluded':len(full)-22,'minimum_clearance':str(min(clearances))})
    return {'cases':rows,'partitioned_source_intervals':sum(r['intervals_partitioned'] for r in rows),'complete_prefix_intervals':88,'scope':'Independently repeats exact membership from the complete parent aggregate and its separately stored factor aggregate; all parent finite completeness premises remain inherited.'}
def decode_audit(data,classification,observations,spectra,vectors,labels):
    assert data['status']=='passed' and len(data['columns'])==604
    assert set(data['predictions'])==set(labels) and all(data['predictions'][k]==vectors[v] for k,v in labels.items())
    domains=[sorted({v[j] for v in vectors.values()}) for j in range(604)]
    assert data['metadata_only_domains']==domains and data['metadata_only_fixed_coefficients']==data['total_population_only_fixed_coefficients']==456
    assert data['total_population_only_selected_classes']==sorted(labels)
    assert data['contract']=={'source_cutoff':'39/2','population_size':22,'complete_preselected_population':True,'deletions':0,'insertions':0,'coordinate_error':'independent_absolute_bound','count_statistic':'all_retained_observed_entries_strictly_below_height','post_noise_window_censoring':False,'multiplicity':'preserved'}
    roots={};boundary=[];count_rows=[];endpoint_checks=0;strict_comparisons=0
    assert [m['precision_bits'] for m in data['matching_cases']]==[160,224]
    assert [t['precision_bits'] for t in data['templates_by_precision']]==[160,224]
    for bits in [160,224]:
        roots[bits]={k:[(F(x['lo']),F(x['hi'])) for x in spectra[bits]['aggregate'][label]['unlabelled_ordinate_intervals'] if F(x['hi'])<F(39,2)] for k,label in labels.items()}
        stored=next(t for t in data['templates_by_precision'] if t['precision_bits']==bits)
        assert stored['roots_by_class']=={k:[list(map(str,x)) for x in v] for k,v in roots[bits].items()}
        a,b=[roots[bits][next(k for k,v in labels.items() if v==label)] for label in ['A','B']]
        assert len(a)==len(b)==22
        m=next(m for m in data['matching_cases'] if m['precision_bits']==bits);assert m['population_sizes']==[22,22] and m['critical_index_zero_based']==1
        L,U,H=map(F,[m['radius_lower'],m['radius_upper'],m['rational_height']])
        assert L==(a[1][0]-b[1][1])/2>0 and U==(a[1][1]-b[1][0])/2 and H==(a[1][0]+b[1][1])/2
        assert F(m['bracket_width'])==U-L==F(2,10**30) and F(m['common_observation_radius'])==U
        assert m['certificate_boundary_scope']=='Overlapping closed-box count envelopes at radius_lower do not prove actual-field ambiguity there.'
        assert len(m['pairs'])==len(m['common_observation'])==22
        y=list(map(F,m['common_observation']));assert all(0<x<F(39,2) for x in y) and all(x<z for x,z in zip(y,y[1:]))
        assert y[1]==H and sum(x<H for x in y)==m['common_observation_strict_count']==1
        for i in range(22):
            p=m['pairs'][i];points=sorted(a[i]+b[i]);lower=max(F(0),a[i][0]-b[i][1],b[i][0]-a[i][1])/2;upper=(points[-1]-points[0])/2
            assert p=={'index':i,'A_interval':list(map(str,a[i])),'B_interval':list(map(str,b[i])),'radius_lower':str(lower),'uniform_radius_upper':str(upper),'common_ordinate':str(y[i])}
            assert y[i]==(points[-1]+points[0])/2
            for x in points:assert abs(x-y[i])<=U;endpoint_checks+=1
            if i!=1:assert upper<L;strict_comparisons+=1
        lower_cost=[[max(F(0),ar[0]-br[1],br[0]-ar[1])/2 for br in b] for ar in a]
        upper_cost=[[(max(ar+br)-min(ar+br))/2 for br in b] for ar in a]
        for mode,matrix,bound in [('lower',lower_cost,L),('uniform_upper',upper_cost,U)]:
            for r in [bound-F(1,10**100),bound]:
                n,edges=max_matching(matrix,r);assert (n==22)==(r==bound)
                boundary.append({'precision_bits':bits,'cost_model':mode,'radius':str(r),'maximum_matched_pairs':n,'matching':edges,'all_pair_costs_sha256':digest([[str(x) for x in row] for row in matrix])})
        assert min(a[0][0],b[0][0])>U and H+U<F(39,2)
    expected=[]
    for bits in [160,224]:
        m=next(m for m in data['matching_cases'] if m['precision_bits']==bits);L,U,H=map(F,[m['radius_lower'],m['radius_upper'],m['rational_height']])
        expected += [(bits,str(H),str(r),'E'+str(n)+'_'+str(bits)+'.json') for r in [F(0),F(1,3),F(1,2),F(57,100),L-F(1,10**100),L,L+F(1,10**100),U] for n in [1,2]]
    assert [(c['precision_bits'],c['height'],c['radius'],c['input_member']) for c in data['count_cases']]==expected
    for c in data['count_cases']:
        bits,h,r,name=[c[k] for k in ['precision_bits','height','radius','input_member']]
        possible={k:attainable(v,h,r) for k,v in roots[bits].items()};obs=observations[name]
        observed=attainable([(F(x['lo']),F(x['hi'])) for x in obs['positive_root_intervals']],h,r)
        def env(values):return {'height':h,'radius':r,'minimum':min(values),'maximum':max(values),'population_size':22}
        assert c['candidate_envelopes']=={k:env(v) for k,v in possible.items()} and c['observed_envelope']==env(observed)
        assert len(c['selections'])==len(observed)
        for q,n in zip(c['selections'],observed):
            assert q['measurement']=={'count':n,'height':h,'radius':r,'contract':data['contract']}
            selected=sorted(k for k,counts in possible.items() if n in counts);assert selected==q['selected_class_ids']
            heldout_label='A' if name[1]=='1' else 'B';assert heldout_label in [labels[k] for k in selected]
            ds=[sorted({vectors[labels[k]][j] for k in selected}) for j in range(604)]
            assert digest(ds)==q['coefficient_domains_sha256'] and sum(len(d)==1 for d in ds)==q['fixed_coefficients']
        unique=all(len(q['selected_class_ids'])==1 for q in c['selections']);assert unique==c['unique_for_every_admissible_count']
        count_rows.append({'precision_bits':bits,'input_member':name,'height':h,'radius':r,'attainable_counts':observed,'candidate_attainable_counts':possible,'uniformly_unique':unique})
    assert len(count_rows)==32 and sum(c['uniformly_unique'] for c in count_rows)==20
    return {'count_cases':count_rows,'uniformly_unique_count_cases':20,'polynomial_coefficient_comparisons':1208,'common_observation_endpoint_checks':endpoint_checks,'strict_noncritical_comparisons':strict_comparisons,'bipartite_boundary_checks':boundary,'all_pair_cost_entries':1936,'fixed_common_observation_coefficients':456,'ambiguous_common_observation_coefficients':148,'differing_targets':[c['n'] for c,d in zip(data['columns'],domains) if len(d)>1 and c['n']<=31]}
def load_data(input_dir,parent_archive,spectrum_archive):
    obs={p.name:read(p) for p in sorted(input_dir.glob('*.json'))}
    with zipfile.ZipFile(parent_archive) as z:parents={n:json.loads(z.read(n)) for n in z.namelist() if n.endswith('.json')}
    with zipfile.ZipFile(spectrum_archive) as z:spectra={bits:json.loads(z.read('Pair_Spectrum'+str(bits)+'.json')) for bits in [160,224]}
    return obs,parents,spectra
def run(decoded,provenance,classification,input_dir,parent_archive,spectrum_archive,arithmetic):
    data=read(decoded);pr=read(provenance);cl=read(classification);obs,parents,spectra=load_data(input_dir,parent_archive,spectrum_archive)
    assert pr['parent_archive_sha256']==sha(parent_archive)
    with zipfile.ZipFile(parent_archive) as z:
        for c in pr['cases']:
            assert c['input_sha256']==sha(input_dir/c['input_member']) and c['parent_member_sha256']==hashlib.sha256(z.read(c['parent_member'])).hexdigest()
    vectors,fac=arithmetic_vectors(arithmetic,data['columns']);ar=read(arithmetic)
    labels={m['class_id']:next(k for k,v in ar['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    assert set(labels.values())=={'A','B'} and len(fac)==1128
    cut=cutoff_audit(pr,obs,parents,spectra);checked=decode_audit(data,cl,obs,spectra,vectors,labels)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [decoded,provenance,classification,parent_archive,spectrum_archive,arithmetic]+sorted(input_dir.glob('*.json'))},'heldout_class_mapping':labels,'cutoff_audit':cut,'decode_audit':checked,'independent_polynomial_factorizations':1128,'polynomial_factorizations':fac,'scope':'Fresh modular polynomial factorization, independent aggregate restriction, attainable-count dynamic programming and full bipartite augmenting-path searches cross-check the proposed decoder and witness. The small enclosure gap remains epistemic; no actual ambiguity at its lower endpoint is inferred.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['decoded','provenance','classification','inputs','parent','spectra','arithmetic','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.decoded,a.provenance,a.classification,a.inputs,a.parent,a.spectra,a.arithmetic);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','factorizations':1128,'partitioned_intervals':90,'count_cases':32,'bipartite_boundary_checks':8,'endpoint_checks':176}))
