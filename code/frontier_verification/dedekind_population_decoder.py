"""Identify the complete quartic class from a preserved source-population count."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
import sympy as s
from dedekind_class_count_decode import columns

CONTRACT={'source_cutoff':20,'count_stage':'complete_source_population_before_coordinate_error',
          'complete_source_population':True,'maximum_deletions':0,'maximum_insertions':0}
RADII=['0','1/3','1/2','1','10','1000000']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate_contract(contract):
    if set(contract)!=set(CONTRACT):raise ValueError('Explicit fixed-population contract required')
    for k in ['source_cutoff','maximum_deletions','maximum_insertions']:
        if type(contract[k]) is not int:raise ValueError('Integer contract fields required')
    if contract!=CONTRACT or contract['complete_source_population'] is not True:raise ValueError('Different observation contract')
def select_population(measurement,templates):
    if set(measurement)!={'population_size','contract'}:raise ValueError('Only population size and its contract enter selection')
    validate_contract(measurement['contract']);n=measurement['population_size']
    if type(n) is not int or n<0:raise ValueError('A nonnegative integer population size is required')
    assert all(type(count) is int and count>0 for count in templates.values())
    return sorted(k for k,count in templates.items() if count==n)
def template_counts(models,spectrum):
    assert spectrum['status']=='passed' and spectrum['top']==20
    counts={}
    for model in models:
        n=spectrum['zeta']['count'];assert type(n) is int and n==len(spectrum['zeta']['root_intervals'])
        for D in model['quadratic_discriminants']:
            factor=spectrum['factors'][str(D)];count=factor['contour']['zero_count']
            assert factor['discriminant']==D and type(count) is int and count==len(factor['root_intervals'])
            n+=count
        counts[model['class_id']]=n
    assert sorted(counts.values())==[22,23]
    return counts
def shifted(roots,radius,pattern):
    r=F(radius);assert r>=0
    result=[]
    for i,root in enumerate(roots):
        lo,hi=F(root['lo']),F(root['hi']);assert 0<lo<hi<20
        shift=r if pattern=='plus' or pattern=='alternating_reverse' and i%2==0 else -r
        result.append({'lo':str(lo+shift),'hi':str(hi+shift)})
    if pattern=='alternating_reverse':result.reverse()
    assert pattern in ['plus','minus','alternating_reverse']
    return result
def run(class_path,audit_path,input_archive,spectrum_archive):
    classified=json.loads(class_path.read_text());audit=json.loads(audit_path.read_text())
    assert classified['status']==audit['status']=='passed' and audit['inputs_sha256'][class_path.name]==sha(class_path)
    assert classified['Galois_group_derived']=='V4' and classified['complete_quartic_candidate_count']==2
    models=classified['retained_models'];cols=columns()
    predictions={m['class_id']:[1+sum(int(s.kronecker_symbol(D,c['prime']))**c['power'] for D in m['quadratic_discriminants']) for c in cols] for m in models}
    cases=[];templates_by_precision=[];population_failures=[]
    with zipfile.ZipFile(input_archive) as inputs,zipfile.ZipFile(spectrum_archive) as spectra:
        for bits in [160,224]:
            sp=json.loads(spectra.read('Pair_Spectrum'+str(bits)+'.json'));templates=template_counts(models,sp)
            templates_by_precision.append({'precision_bits':bits,'derived_class_population_counts':templates})
            for number in [1,2]:
                member='S'+str(number)+'_'+str(bits)+'.json';obs=json.loads(inputs.read(member));roots=obs['positive_root_intervals']
                assert {k:obs[k] for k in classified['metadata']}==classified['metadata'] and obs['top']==20
                measurement={'population_size':len(roots),'contract':dict(CONTRACT)};selected=select_population(measurement,templates);assert len(selected)==1
                result={'input_member':member,'input_member_sha256':hashlib.sha256(inputs.read(member)).hexdigest(),
                        'measurement':measurement,'selected_class_id':selected[0],'predicted_coefficients':predictions[selected[0]],'transformations':[]}
                for radius in RADII:
                    for pattern in ['plus','minus','alternating_reverse']:
                        changed=shifted(roots,radius,pattern);m={'population_size':len(changed),'contract':dict(CONTRACT)}
                        assert select_population(m,templates)==selected
                        result['transformations'].append({'radius':radius,'pattern':pattern,'population_size':len(changed),'geometry_sha256':digest(changed),'selected_class_id':selected[0]})
                # Every true source ordinate lies in (0,20). Moving all of them to 10 costs at most 10.
                assert all(F(0)<F(r['lo'])<F(r['hi'])<20 for r in roots)
                collapsed=[10]*len(roots);collapsed_m={'population_size':len(collapsed),'contract':dict(CONTRACT)}
                assert select_population(collapsed_m,templates)==selected
                result['collapsed_geometry_control']={'observed_ordinates':collapsed,'sufficient_radius':'10','selected_class_id':selected[0],
                    'scope':'The two collapsed lists have identical coordinate values and retain different lengths. The count result concerns preserved entries; it is not an explicit-formula certificate at radius ten.'}
                cases.append(result)
                # A false preservation claim cannot be diagnosed from count alone. Preserve that actual limitation.
                if len(roots)==23:
                    lost={'population_size':22,'contract':dict(CONTRACT)};wrong=select_population(lost,templates)
                    assert len(wrong)==1 and wrong!=selected
                    population_failures.append({'input_member':member,'actual_source_class_id':selected[0],'one_deletion_with_false_fixed_contract':lost,'wrong_class_id_if_contract_falsely_asserted':wrong[0],
                        'interpretation':'This is a deliberate false-premise counterexample, not an accepted fixed-population observation. The scalar selector cannot prove completeness or detect a forged preservation claim.'})
    assert len(cases)==4 and sum(len(c['transformations']) for c in cases)==72 and len(population_failures)==2
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [class_path,audit_path,input_archive,spectrum_archive]},
            'contract':CONTRACT,'columns':cols,'templates_by_precision':templates_by_precision,'cases':cases,
            'coordinate_transformations_checked':72,'collapsed_geometry_controls':4,'false_population_contract_counterexamples':population_failures,
            'general_statement':'As long as the source population is complete through the stated cutoff and no entries are inserted or deleted, any coordinate changes or permutation preserve its cardinality. The two completely classified fields have counts23/22, so this statistic selects the field independently of coordinate-error magnitude.',
            'scope':'The elementary cardinality invariance is supported by a Lean list lemma. General field classification and spectral completeness are inherited written/computational results. Contract flags are declarations, not self-authenticating evidence; all synthetic source populations have independently certified provenance. Post-noise censoring and missing/extra roots are different models.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['classification','audit','inputs','spectra','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.classification,a.audit,a.inputs,a.spectra);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':'passed','source_cases':len(r['cases']),'coordinate_transformations':72,'collapsed_controls':4,'false_contract_counterexamples':2}))
