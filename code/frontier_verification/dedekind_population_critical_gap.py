"""Identify the exact root-gap formula behind the one-deletion ambiguity threshold."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_certificate(data,matching,input_archive):
    assert data['status']==matching['status']=='passed' and [c['precision_bits'] for c in data['cases']]==[160,224]
    checked=0;cases=[]
    with zipfile.ZipFile(input_archive) as z:
        for cert,case in zip(data['cases'],matching['cases']):
            assert cert['precision_bits']==case['precision_bits'];bits=cert['precision_bits']
            a,b=[[(F(r['lo']),F(r['hi'])) for r in json.loads(z.read('S'+str(i)+'_'+str(bits)+'.json'))['positive_root_intervals']] for i in [1,2]]
            assert cert['critical_pair_zero_based']==[1,1] and a[1][0]>b[1][1]
            L=(a[1][0]-b[1][1])/2;U=(a[1][1]-b[1][0])/2
            assert cert['root_gap_interval']==[str(L),str(U)] and str(L)==case['true_ambiguity_threshold_lower'] and str(U)==case['constructive_common_observation_radius']
            optimal=[];excluded=[]
            for row in case['all_single_deletion_cases']:
                omit=row['omitted_A_index_zero_based'];retained=[v for i,v in enumerate(a) if i!=omit]
                # Reconstruct bounds from the immutable source intervals using doubled inequalities.
                rows=[]
                for i,(ar,br) in enumerate(zip(retained,b)):
                    ai=i if i<omit else i+1
                    lo=max(F(0),ar[0]-br[1],br[0]-ar[1]);hi=max(ar[1],br[1])-min(ar[0],br[0])
                    rows.append((ai,i,lo,hi))
                if omit in cert['optimal_deletion_indices_zero_based']:
                    assert any(ai==bi==1 for ai,bi,lo,hi in rows)
                    others=[hi for ai,bi,lo,hi in rows if (ai,bi)!=(1,1)]
                    assert len(others)==21 and all(hi<2*L for hi in others);checked+=len(others)
                    expected=next(v for v in cert['dominance_margins'] if v['omitted_A_index_zero_based']==omit)
                    assert F(expected['critical_lower_minus_other_uniform_upper'])==L-max(others)/2
                    optimal.append(omit)
                else:
                    lower=max(lo for ai,bi,lo,hi in rows)/2;assert lower>U;checked+=1
                    expected=next(v for v in cert['excluded_deletion_margins'] if v['omitted_A_index_zero_based']==omit)
                    assert F(expected['row_lower_minus_critical_upper'])==lower-U;excluded.append(omit)
            assert optimal==list(range(17,23)) and excluded==list(range(17))
            assert [v['omitted_A_index_zero_based'] for v in cert['dominance_margins']]==optimal
            assert [v['omitted_A_index_zero_based'] for v in cert['excluded_deletion_margins']]==excluded
            cases.append({'precision_bits':bits,'dominance_inequalities':126,'excluded_deletion_inequalities':17,'optimal_deletion_indices_zero_based':optimal})
        equality={label:z.read('S'+str(i)+'_160.json')==z.read('S'+str(i)+'_224.json') for i,label in [(1,'A'),(2,'B')]}
    assert data['nominal_precision_input_bytes_equal_by_field']==equality
    assert data['exact_symbolic_threshold']=='(second_positive_ordinate_A - second_positive_ordinate_B) / 2'
    assert data['numerical_threshold_bracket_width']==str(F(2,10**30))
    return {'cases':cases,'total_strict_inequalities':checked,'source_interval_reconstruction':'passed','numeric_bracket_remains_nonzero':True}
def run(matching_path,input_archive):
    matching=json.loads(matching_path.read_text());assert matching['status']=='passed';cases=[]
    for case in matching['cases']:
        L=F(case['true_ambiguity_threshold_lower']);U=F(case['constructive_common_observation_radius']);dominance=[];excluded=[]
        for row in case['all_single_deletion_cases']:
            omit=row['omitted_A_index_zero_based']
            if omit in case['minimizing_upper_deletion_indices']:
                critical=[p for p in row['pairs'] if p['source_A_index']==p['source_B_index']==1];assert len(critical)==1
                c=critical[0];assert F(c['radius_lower'])==L and F(c['uniform_radius_upper'])==U and F(c['A_interval'][0])>F(c['B_interval'][1])
                other=max(F(p['uniform_radius_upper']) for p in row['pairs'] if p is not c);assert other<L
                dominance.append({'omitted_A_index_zero_based':omit,'critical_lower_minus_other_uniform_upper':str(L-other)})
            else:
                lower=F(row['radius_lower']);assert lower>U
                excluded.append({'omitted_A_index_zero_based':omit,'row_lower_minus_critical_upper':str(lower-U)})
        cases.append({'precision_bits':case['precision_bits'],'critical_pair_zero_based':[1,1],'root_gap_interval':[str(L),str(U)],
                      'optimal_deletion_indices_zero_based':[v['omitted_A_index_zero_based'] for v in dominance],
                      'dominance_margins':dominance,'excluded_deletion_margins':excluded})
    with zipfile.ZipFile(input_archive) as z:
        equal={label:z.read('S'+str(i)+'_160.json')==z.read('S'+str(i)+'_224.json') for i,label in [(1,'A'),(2,'B')]}
    data={'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [matching_path,input_archive]},'cases':cases,
          'exact_symbolic_threshold':'(second_positive_ordinate_A - second_positive_ordinate_B) / 2',
          'numerical_threshold_bracket_width':str(F(2,10**30)),'nominal_precision_input_bytes_equal_by_field':equal,
          'proof':['Each of the six retained optimal deletions pairs the second source roots together, whose intervals have A strictly above B.',
                   'For every actual root choice in the certified intervals, every other pair distance is strictly smaller than that critical pair distance.',
                   'For every other deletion, a certified lower bound is strictly larger than the critical pair upper bound.',
                   'Ordered matching is optimal by uncrossing, so the global deletion/matching threshold equals exactly half the second-root difference. Six deletion indices are exactly optimal; arbitrary coordinate matchings with those deletions need not be unique.',
                   'Midpoints of the actual paired roots give a common observation at this exact symbolic threshold. The separately stored rational observation works at the certified upper bound uniformly over all source intervals.'],
          'scope':'This strengthens a numerical bracket to an exact expression in two well-defined source ordinates under the same one-deletion model. It does not replace the ordinates with exact numerical constants. Nominal160/224 exported input equality is checked explicitly; duplicate inputs are not independent new root certificates.'}
    data['independent_source_interval_audit']=verify_certificate(data,matching,input_archive)
    # Challenge the actual strict dominance certificate and proposed critical identity.
    import copy
    tests=[]
    for name,change in [('wrong_critical_pair',lambda d:d['cases'][0].update(critical_pair_zero_based=[0,0])),
                         ('omit_optimal_deletion',lambda d:d['cases'][0]['optimal_deletion_indices_zero_based'].pop()),
                         ('forge_strict_dominance_margin',lambda d:d['cases'][0]['dominance_margins'][0].update(critical_lower_minus_other_uniform_upper='0')),
                         ('claim_collapsed_numerical_interval',lambda d:d.update(numerical_threshold_bracket_width='0'))]:
        changed=copy.deepcopy(data);change(changed)
        try:verify_certificate(changed,matching,input_archive)
        except (AssertionError,ValueError):tests.append({'mutation':name,'rejected':True})
        else:raise AssertionError('Critical-gap mutation accepted: '+name)
    data['mutations']=tests;assert len(tests)==4
    return data
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['matching','inputs','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.matching,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':'passed','critical_pair_zero_based':[1,1],'optimal_deletions_zero_based':list(range(17,23)),'strict_inequalities':r['independent_source_interval_audit']['total_strict_inequalities'],'precision_input_byte_equality':r['nominal_precision_input_bytes_equal_by_field'],'mutations_rejected':4}))
