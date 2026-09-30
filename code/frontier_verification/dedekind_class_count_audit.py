"""Audit count-only field selection by attainable-count sets and independent local factorizations."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_integer_audit import arithmetic_vectors

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def attainable(roots,height,radius,top):
    h,r,T=map(F,[height,radius,top]);assert h>0 and r>=0 and T-r>=h
    totals={0}
    for x in roots:
        lo,hi=F(x['lo'])-r,F(x['hi'])+r;assert lo<=hi
        outcomes=set()
        if hi>0 and lo<h:outcomes.add(1)
        if lo<=0 or hi>=h:outcomes.add(0)
        assert outcomes;totals={n+b for n in totals for b in outcomes}
    return sorted(totals)

def run(decoded_path,class_path,class_audit_path,spectra,observations,arithmetic,old_decoding,measurements):
    read=lambda p:json.loads(p.read_text());data=read(decoded_path);classification=read(class_path);checked=read(class_audit_path);a=read(arithmetic);old=read(old_decoding);m=read(measurements)
    assert data['status']==classification['status']==checked['status']=='passed'
    assert data['inputs_sha256']=={p.name:sha(p) for p in [class_path,class_audit_path]+spectra+observations}
    assert data['columns']==m['columns'] and len(data['columns'])==604
    vectors,factorizations=arithmetic_vectors(arithmetic,data['columns']);assert len(factorizations)==1128
    labels={model['class_id']:next(label for label,v in a['fields'].items() if sorted(v['quadratic_discriminants'])==model['quadratic_discriminants']) for model in classification['retained_models']}
    assert set(labels)==set(data['derived_class_predictions']) and set(labels.values())=={'A','B'}
    assert all(data['derived_class_predictions'][k]==vectors[label] for k,label in labels.items())
    prior=[sorted({v[i] for v in vectors.values()}) for i in range(604)];assert prior==data['prior_coefficient_domains'] and sum(len(d)==1 for d in prior)==data['metadata_only_unique_coefficients']==456
    independent_roots={};cases=[];witnesses=[]
    for path,root_record in zip(spectra,data['candidate_roots']):
        spectrum=read(path);bits=spectrum['precision_bits'];assert root_record['precision_bits']==bits
        roots={k:spectrum['aggregate'][label]['unlabelled_ordinate_intervals'] for k,label in labels.items()};assert roots==root_record['roots_by_derived_class'];independent_roots[bits]=roots
        for k,r in roots.items():
            for direction in [-1,1]:
                shifted=[{'lo':str(F(x['lo'])+F(direction,2)),'hi':str(F(x['hi'])+F(direction,2))} for x in r]
                counts=attainable(shifted,'7/3','0','39/2');assert len(counts)==1
                witnesses.append({'precision_bits':bits,'class_id':k,'uniform_ordinate_displacement':str(F(direction,2)),'height':'7/3','verified_count':counts[0]})
        assert all({w['verified_count'] for w in witnesses if w['precision_bits']==bits and w['class_id']==k}=={0,1} for k in labels)
    expected=[(bits,h,r,i) for bits in [160,224] for h,r in [('20','0'),('2','0'),('7/3','0'),('7/3','1/3'),('7/3','1/2')] for i in [0,1]]
    assert [(c['spectrum_precision_bits'],c['height'],c['radius'],c['observation_index']) for c in data['cases']]==expected
    os=[read(p) for p in observations]
    for case in data['cases']:
        bits,h,r,i=[case[k] for k in ['spectrum_precision_bits','height','radius','observation_index']];roots=independent_roots[bits]
        possible={k:attainable(v,h,r,20) for k,v in roots.items()};observed=attainable(os[i]['positive_root_intervals'],h,r,20)
        for k,values in possible.items():
            assert case['candidate_count_envelopes'][k]=={'height':str(F(h)),'radius':str(F(r)),'minimum':min(values),'maximum':max(values),'completeness_margin':str(20-F(r)-F(h))}
        assert case['observed_count_envelope']=={'height':str(F(h)),'radius':str(F(r)),'minimum':min(observed),'maximum':max(observed),'completeness_margin':str(20-F(r)-F(h))}
        assert [q['measurement'] for q in case['selections']]==[{'height':h,'positive_zero_count':n} for n in observed]
        replays=[]
        for q in case['selections']:
            count=q['measurement']['positive_zero_count'];selected=sorted(k for k,values in possible.items() if count in values);assert selected==q['selected_class_ids']
            assert ['A','B'][i] in [labels[k] for k in selected]
            domains=[sorted({vectors[labels[k]][j] for k in selected}) for j in range(604)]
            assert digest(domains)==q['coefficient_domains_sha256'] and sum(len(d)==1 for d in domains)==q['unique_coefficients']
            assert sum(len(d)==1 for col,d in zip(data['columns'],domains) if col['n']<=31)==q['unique_target_coefficients']
            if F(r)<F(1,2):assert len(selected)==1 and q['unique_coefficients']==604 and q['unique_target_coefficients']==17
            else:assert len(selected)==2 and q['unique_coefficients']==456 and q['unique_target_coefficients']==12
            replays.append({'count':count,'selected_class_ids':selected,'unique_coefficients':q['unique_coefficients'],'unique_targets':q['unique_target_coefficients']})
        unique=all(len(q['selected_class_ids'])==1 for q in case['selections']);assert unique==case['field_unique_for_every_admissible_count']
        cases.append({**{k:case[k] for k in ['spectrum_precision_bits','height','radius','observation_index']},'attainable_observed_counts':observed,'field_unique_for_every_admissible_count':unique,'selection_replays':replays})
    assert len(cases)==20 and sum(c['field_unique_for_every_admissible_count'] for c in cases)==16
    assert all(v['first_distinguishing_integer_height']==2 for v in old['results'])
    assert [len(read(spectra[-1])['aggregate'][label]['unlabelled_ordinate_intervals']) for label in ['A','B']]==[23,22]
    assert [read(p)['positive_root_intervals'] for p in observations]==[read(spectra[-1])['aggregate'][label]['unlabelled_ordinate_intervals'] for label in ['A','B']]
    changed=[c['n'] for c,d in zip(data['columns'],prior) if len(d)>1]
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [decoded_path,class_path,class_audit_path,arithmetic,old_decoding,measurements]+spectra+observations},
            'independent_polynomial_factorizations':1128,'field_factorizations':factorizations,'heldout_class_mapping':labels,'coefficient_comparisons':1208,
            'metadata_only_unique_coefficients':456,'coefficients_resolved_by_distinguishing_count':len(changed),'differing_prime_powers':changed,'differing_targets':[n for n in changed if n<=31],
            'cases':cases,'exact_complete_T20_counts':[23,22],'radius_half_count_ambiguity_witnesses':witnesses,'previous_count_gate_recovered_without_Galois_group_input':True,
            'scope':'Independent attainable-count sets replay all decisions; 1128 fresh polynomial factorizations away from each chosen order index reconstruct both 604-coefficient vectors. Exact complete count through20 selects the derived class. Count below7/3 is uniformly separating at radius1/3; uniform plus/minus1/2 displacements show each field can produce either count0 or1 at radius1/2. This is a count-statistic limitation, not full-spectrum ambiguity or a self-certifying completeness test.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['decoded','classification','class-audit','arithmetic','old-decoding','measurements','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--spectra',type=Path,nargs=2,required=True);p.add_argument('--observations',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.decoded,a.classification,a.class_audit,a.spectra,a.observations,a.arithmetic,a.old_decoding,a.measurements);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','factorizations':1128,'coefficient_comparisons':1208,'newly_resolved_coefficients':r['coefficients_resolved_by_distinguishing_count']}))
