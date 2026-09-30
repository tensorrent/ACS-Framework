"""Equal-population finite spectra: exact count gates and actual shared observations."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
import sympy as s
from dedekind_class_count_decode import columns,roots_for

CONTRACT={'source_cutoff':'39/2','population_size':22,'complete_preselected_population':True,
          'deletions':0,'insertions':0,'coordinate_error':'independent_absolute_bound',
          'count_statistic':'all_retained_observed_entries_strictly_below_height',
          'post_noise_window_censoring':False,'multiplicity':'preserved'}
KEYS={'degree','discriminant','real_places','complex_places','top','positive_root_intervals'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def intervals(data):
    assert set(data)==KEYS and data['top']=='39/2'
    values=[(F(x['lo']),F(x['hi'])) for x in data['positive_root_intervals']]
    assert len(values)==22 and all(0<lo<hi<F(39,2) for lo,hi in values)
    assert all(a[1]<b[0] for a,b in zip(values,values[1:]))
    return values
def clipped_template(model,spectrum):
    full=roots_for(model,spectrum);out=[]
    assert spectrum['status']=='passed' and spectrum['top']==20
    for x in full:
        lo,hi=F(x['lo']),F(x['hi']);assert 0<lo<hi<20
        if hi<F(39,2):out.append((lo,hi))
        else:assert lo>F(39,2)
    assert len(out)==22 and all(a[1]<b[0] for a,b in zip(out,out[1:]))
    return out
def envelope(roots,height,radius):
    h,r=F(height),F(radius);assert r>=0 and len(roots)==22
    return {'height':str(h),'radius':str(r),'minimum':sum(hi+r<h for lo,hi in roots),
            'maximum':sum(lo-r<h for lo,hi in roots),'population_size':len(roots)}
def select_count(measurement,templates):
    if set(measurement)!={'count','height','radius','contract'}:raise ValueError('Only count, height, radius and explicit contract enter selection')
    contract=measurement['contract']
    if set(contract)!=set(CONTRACT) or contract!=CONTRACT:raise ValueError('Different acquisition contract')
    if any(type(contract[k]) is not int for k in ['population_size','deletions','insertions']):raise ValueError('Integer population and edit budgets required')
    if contract['complete_preselected_population'] is not True or contract['post_noise_window_censoring'] is not False:raise ValueError('Boolean acquisition declarations required')
    n=measurement['count']
    if type(n) is not int or not 0<=n<=22:raise ValueError('Integer cumulative count required')
    if type(measurement['height']) is not str or type(measurement['radius']) is not str:raise ValueError('Exact rational text required')
    h,r=F(measurement['height']),F(measurement['radius'])
    if r<0:raise ValueError('Nonnegative error bound required')
    for v in templates.values():
        if set(v)!={'height','radius','minimum','maximum','population_size'}:raise ValueError('Invalid count envelope')
        if any(type(v[k]) is not int for k in ['minimum','maximum','population_size']):raise ValueError('Integer envelope required')
        if not (v['population_size']==22 and 0<=v['minimum']<=v['maximum']<=22 and F(v['height'])==h and F(v['radius'])==r):raise ValueError('Mismatched measurement or envelope')
    return sorted(k for k,v in templates.items() if v['minimum']<=n<=v['maximum'])
def matched(a,b):
    assert len(a)==len(b)==22
    alo,ahi=a[1];blo,bhi=b[1];assert alo>bhi
    L=(alo-bhi)/2;U=(ahi-blo)/2;H=(alo+bhi)/2
    pairs=[]
    for i,(ar,br) in enumerate(zip(a,b)):
        lower=max(F(0),ar[0]-br[1],br[0]-ar[1])/2
        upper=(max(ar[1],br[1])-min(ar[0],br[0]))/2
        center=(max(ar[1],br[1])+min(ar[0],br[0]))/2
        assert i==1 or upper<L
        assert all(abs(x-center)<=U for x in ar+br)
        pairs.append({'index':i,'A_interval':list(map(str,ar)),'B_interval':list(map(str,br)),
                      'radius_lower':str(lower),'uniform_radius_upper':str(upper),'common_ordinate':str(center)})
    assert max(F(p['radius_lower']) for p in pairs)==L and max(F(p['uniform_radius_upper']) for p in pairs)==U
    y=[F(p['common_ordinate']) for p in pairs]
    assert all(0<x<F(39,2) for x in y) and all(x<z for x,z in zip(y,y[1:]))
    assert y[1]==H and sum(x<H for x in y)==1 and U-L==F(2,10**30)
    assert min(a[0][0],b[0][0])-U>0 and H+U<F(39,2)
    return {'population_sizes':[22,22],'critical_index_zero_based':1,'radius_lower':str(L),'radius_upper':str(U),
            'bracket_width':str(U-L),'rational_height':str(H),'pairs':pairs,'common_observation':list(map(str,y)),
            'common_observation_strict_count':1,'common_observation_radius':str(U),
            'exact_symbolic_threshold':'(a_1 - b_1)/2, with zero-based sorted true source indices',
            'theoretical_optimal_height':'(a_1 + b_1)/2; not asserted equal to the stored rational height',
            'fixed_rational_gate_margin':'min(a_1-H,H-b_1) = delta_star - abs(H-h_star)',
            'guaranteed_rational_gate_regime':'0 <= radius < radius_lower',
            'certificate_boundary_scope':'Overlapping closed-box count envelopes at radius_lower do not prove actual-field ambiguity there.'}
def run(class_path,audit_path,input_dir,spectrum_archive):
    classified=json.loads(class_path.read_text());audit=json.loads(audit_path.read_text())
    assert classified['status']==audit['status']=='passed' and audit['inputs_sha256'][class_path.name]==sha(class_path)
    assert classified['Galois_group_derived']=='V4' and classified['complete_quartic_candidate_count']==2
    models=classified['retained_models'];cols=columns()
    predictions={m['class_id']:[1+sum(int(s.kronecker_symbol(D,c['prime']))**c['power'] for D in m['quadratic_discriminants']) for c in cols] for m in models}
    prior=[sorted({v[j] for v in predictions.values()}) for j in range(len(cols))];assert sum(len(d)==1 for d in prior)==456
    cases=[];matchings=[];templates_by_precision=[];inputs=[]
    with zipfile.ZipFile(spectrum_archive) as z:
        for bits in [160,224]:
            sp=json.loads(z.read('Pair_Spectrum'+str(bits)+'.json'));roots={m['class_id']:clipped_template(m,sp) for m in models}
            templates_by_precision.append({'precision_bits':bits,'roots_by_class':{k:[list(map(str,r)) for r in v] for k,v in roots.items()}})
            data=[]
            for n in [1,2]:
                path=input_dir/('E'+str(n)+'_'+str(bits)+'.json');inputs.append(path);obs=json.loads(path.read_text())
                assert {k:obs[k] for k in classified['metadata']}==classified['metadata'];data.append(intervals(obs))
            certificate=matched(*data);certificate['precision_bits']=bits;matchings.append(certificate)
            H,L,U=map(F,[certificate['rational_height'],certificate['radius_lower'],certificate['radius_upper']])
            radii=[F(0),F(1,3),F(1,2),F(57,100),L-F(1,10**100),L,L+F(1,10**100),U]
            for r in radii:
                templates={k:envelope(v,H,r) for k,v in roots.items()}
                for n,observed_roots in enumerate(data,1):
                    obs=envelope(observed_roots,H,r);selections=[]
                    for count in range(obs['minimum'],obs['maximum']+1):
                        measurement={'count':count,'height':str(H),'radius':str(r),'contract':dict(CONTRACT)}
                        selected=select_count(measurement,templates);assert selected
                        ds=[sorted({predictions[k][j] for k in selected}) for j in range(len(cols))]
                        selections.append({'measurement':measurement,'selected_class_ids':selected,'fixed_coefficients':sum(len(d)==1 for d in ds),'coefficient_domains_sha256':digest(ds)})
                    unique=all(len(q['selected_class_ids'])==1 for q in selections)
                    assert unique==(r<L)
                    cases.append({'precision_bits':bits,'input_member':'E'+str(n)+'_'+str(bits)+'.json','height':str(H),'radius':str(r),
                                  'candidate_envelopes':templates,'observed_envelope':obs,'selections':selections,'unique_for_every_admissible_count':unique})
            assert select_count({'count':1,'height':str(H),'radius':str(U),'contract':dict(CONTRACT)}, {k:envelope(v,H,U) for k,v in roots.items()})==sorted(predictions)
    assert len(cases)==32 and sum(c['unique_for_every_admissible_count'] for c in cases)==20
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [class_path,audit_path,spectrum_archive]+inputs},
            'contract':CONTRACT,'columns':cols,'predictions':predictions,'metadata_only_domains':prior,'metadata_only_fixed_coefficients':456,
            'total_population_only_selected_classes':sorted(predictions),'total_population_only_fixed_coefficients':456,
            'templates_by_precision':templates_by_precision,'count_cases':cases,'matching_cases':matchings,
            'new_roots_computed':0,'scope':'Known synthetic benchmark with certified complete source prefixes at19.5. Only declared cumulative count, height and error bound enter selection. Multiplicity and all preselected entries are preserved even if noisy coordinates leave the source window. Closed interval envelopes overapproximate unknown true roots. The rational common list at U is uniformly realizable by both actual fields; exact symbolic optimality uses ordered matching and the critical rank, as derived in the proof guide. No Gaussian tail or moment budgets are reused.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['classification','audit','inputs','spectra','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.classification,a.audit,a.inputs,a.spectra);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':'passed','count_cases':32,'uniformly_unique_cases':20,'populations':[22,22],'radius_approx_display':float(F(r['matching_cases'][0]['radius_lower']))}))
