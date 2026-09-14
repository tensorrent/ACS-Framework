"""Decode the metadata-derived complete quartic class using only certified aggregate counts."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import sympy as s

SCENARIOS=[('20','0'),('2','0'),('7/3','0'),('7/3','1/3'),('7/3','1/2')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def envelope(roots,height,radius,top):
    h,r,T=map(F,[height,radius,top]);assert 0<h and r>=0 and T-r>=h
    intervals=[(F(x['lo'])-r,F(x['hi'])+r) for x in roots];assert all(lo<=hi for lo,hi in intervals)
    return {'height':str(h),'radius':str(r),'minimum':sum(0<lo and hi<h for lo,hi in intervals),
            'maximum':sum(hi>0 and lo<h for lo,hi in intervals),'completeness_margin':str(T-r-h)}
def select(measurement,templates):
    if set(measurement)!={'height','positive_zero_count'}:raise ValueError('Only height and aggregate count may enter the selector')
    n=measurement['positive_zero_count']
    if type(n) is not int or n<0:raise ValueError('Count must be a nonnegative integer')
    h=F(measurement['height']);assert all(F(v['height'])==h for v in templates.values())
    return sorted(k for k,v in templates.items() if v['minimum']<=n<=v['maximum'])
def columns():
    result=[]
    for p in s.primerange(2,4097):
        k=1
        while p**k<=4096:result.append({'n':int(p**k),'prime':int(p),'power':k});k+=1
    result.sort(key=lambda c:c['n']);assert len(result)==604;return result
def roots_for(model,spectrum):
    roots=[{'lo':r['lo'],'hi':r['hi']} for r in spectrum['zeta']['root_intervals']]
    assert len(roots)==spectrum['zeta']['count']
    for D in model['quadratic_discriminants']:
        factor=spectrum['factors'][str(D)];assert factor['discriminant']==D and len(factor['root_intervals'])==factor['contour']['zero_count']
        roots += [{'lo':r['lo'],'hi':r['hi']} for r in factor['root_intervals']]
    return sorted(roots,key=lambda r:F(r['lo']))

def run(class_path,audit_path,spectra,observations):
    data=json.loads(class_path.read_text());audit=json.loads(audit_path.read_text());obs=[json.loads(p.read_text()) for p in observations]
    assert data['status']==audit['status']=='passed' and audit['inputs_sha256'][class_path.name]==sha(class_path)
    assert data['Galois_group_derived']=='V4' and data['complete_quartic_candidate_count']==2 and audit['independent_character_audit']['complete_quartic_candidate_count']==2
    for o in obs:assert {k:o[k] for k in data['metadata']}==data['metadata'] and o['top']==20
    cols=columns();models=data['retained_models'];predictions={m['class_id']:[1+sum(int(s.kronecker_symbol(D,c['prime']))**c['power'] for D in m['quadratic_discriminants']) for c in cols] for m in models}
    prior_domains=[sorted({v[i] for v in predictions.values()}) for i in range(len(cols))];cases=[];source_roots=[]
    for path in spectra:
        spectrum=json.loads(path.read_text());assert spectrum['status']=='passed' and spectrum['top']==20
        roots={m['class_id']:roots_for(m,spectrum) for m in models};source_roots.append({'precision_bits':spectrum['precision_bits'],'roots_by_derived_class':roots})
        for h,r in SCENARIOS:
            templates={k:envelope(v,h,r,20) for k,v in roots.items()}
            for index,o in enumerate(obs):
                observed=envelope(o['positive_root_intervals'],h,r,o['top']);selections=[]
                for count in range(observed['minimum'],observed['maximum']+1):
                    measurement={'height':h,'positive_zero_count':count};selected=select(measurement,templates);assert selected
                    domains=[sorted({predictions[k][i] for k in selected}) for i in range(len(cols))]
                    selections.append({'measurement':measurement,'selected_class_ids':selected,'unique_coefficients':sum(len(d)==1 for d in domains),
                                       'unique_target_coefficients':sum(len(d)==1 for c,d in zip(cols,domains) if c['n']<=31),'coefficient_domains_sha256':digest(domains)})
                cases.append({'spectrum_precision_bits':spectrum['precision_bits'],'height':h,'radius':r,'observation_index':index,
                              'candidate_count_envelopes':templates,'observed_count_envelope':observed,'selections':selections,
                              'field_unique_for_every_admissible_count':all(len(q['selected_class_ids'])==1 for q in selections)})
    assert len(cases)==20 and sum(c['field_unique_for_every_admissible_count'] for c in cases)==16
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [class_path,audit_path]+spectra+observations},
            'columns':cols,'derived_class_predictions':predictions,'coefficient_formula':'c_(p^k) = 1 + sum over the three derived quadratic discriminants D of Kronecker(D,p)^k',
            'prior_coefficient_domains':prior_domains,'metadata_only_unique_coefficients':sum(len(d)==1 for d in prior_domains),'candidate_roots':source_roots,'cases':cases,
            'exact_count_through_20_suffices':True,'robust_count_gate':{'height':'7/3','ordinate_radius':'1/3','all_604_coefficients_determined':True},
            'scope':'The complete field class is derived from metadata, then certified spectral templates are rebuilt from its quadratic factors and zeta. Only height and aggregate count enter select. The exact complete count through20, or the count below7/3 with ordinate errors at most1/3, selects one field and its Euler coefficient formula. Radius1/2 leaves this count statistic ambiguous. No arbitrary count certifies its own completeness, and ambiguity of this count is not ambiguity of full spectra.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['classification','audit','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--spectra',type=Path,nargs=2,required=True);p.add_argument('--observations',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.classification,a.audit,a.spectra,a.observations);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','cases':len(r['cases']),'uniquely_decoded_cases':sum(c['field_unique_for_every_admissible_count'] for c in r['cases']),'metadata_only_unique_coefficients':r['metadata_only_unique_coefficients']}))
