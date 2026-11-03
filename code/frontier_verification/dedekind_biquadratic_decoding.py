"""Select the certified candidate field from one unlabelled zero-count statistic."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path


def envelope(roots, height, radius, complete_through):
    h,r,T=map(F,[height,radius,complete_through])
    assert r>=0 and 0<h and T-r>=h
    intervals=[(F(x['lo'])-r,F(x['hi'])+r) for x in roots]
    lower=sum(0<lo and hi<h for lo,hi in intervals)
    upper=sum(hi>0 and lo<h for lo,hi in intervals)
    return {'height':str(h),'radius':str(r),'minimum':lower,'maximum':upper,
            'scope':'Sufficient count enclosure for independent ordinate displacements bounded by the declared radius; unknown ordinates above the completeness cutoff cannot enter the gate.'}


def select(measurement, candidates):
    # The observation schema contains no field, polynomial or factor label.
    if set(measurement)!={'height','positive_zero_count'}:
        raise ValueError('Observation may contain only the height and aggregate count')
    count=measurement['positive_zero_count']
    if type(count) is not int or count<0:raise ValueError('Count must be a nonnegative integer')
    assert all(F(b['height'])==F(measurement['height']) for b in candidates.values())
    return sorted(name for name,b in candidates.items() if b['minimum']<=count<=b['maximum'])


def run(arithmetic, classification, spectra):
    a=json.loads(arithmetic.read_text());c=json.loads(classification.read_text())
    assert c['complete_candidate_count']==2 and a['input_contract']['predeclared_measurement_grid']==list(range(1,21))
    results=[]
    for path in spectra:
        data=json.loads(path.read_text());aggregates=data['aggregate'];grid=[]
        for height in range(1,21):
            templates={k:envelope(v['unlabelled_ordinate_intervals'],height,0,20) for k,v in aggregates.items()}
            for truth in ['A','B']:
                count=templates[truth]['minimum'];assert count==templates[truth]['maximum']
                measurement={'height':str(height),'positive_zero_count':count}
                selected=select(measurement,templates);assert truth in selected
                grid.append({'held_out_field':truth,'measurement':measurement,'selected':selected})
        first=next(h for h in range(1,21) if all(len(row['selected'])==1 for row in grid if row['measurement']['height']==str(h)))
        assert first==2
        robust=[]
        for radius in ['0','1/3','1/2']:
            templates={k:envelope(v['unlabelled_ordinate_intervals'],'7/3',radius,20) for k,v in aggregates.items()}
            checks=[]
            for truth in ['A','B']:
                roots=aggregates[truth]['unlabelled_ordinate_intervals']
                for direction in [-1,1]:
                    shift=direction*F(radius)
                    shifted=[{'lo':str(F(r['lo'])+shift),'hi':str(F(r['hi'])+shift)} for r in roots]
                    count=envelope(shifted,'7/3',0,20)
                    assert count['minimum']==count['maximum']
                    measurement={'height':'7/3','positive_zero_count':count['minimum']}
                    selected=select(measurement,templates);assert truth in selected
                    assert len(selected)==(2 if radius=='1/2' else 1)
                    checks.append({'held_out_field':truth,'uniform_displacement':str(shift),'measurement':measurement,'selected':selected})
            robust.append({'radius':radius,'templates':templates,'uniform_displacement_controls':checks})
        ra=aggregates['A']['unlabelled_ordinate_intervals'];rb=aggregates['B']['unlabelled_ordinate_intervals']
        assert F(ra[0]['hi'])<2 and F(rb[0]['lo'])>F(8,3) and F(ra[1]['lo'])>F(8,3)
        assert min(F(ra[0]['lo']),F(rb[0]['lo']))>F(1,3)
        critical={'radius_lower':str((F(rb[0]['lo'])-F(ra[0]['hi']))/2),
                  'radius_upper':str((F(rb[0]['hi'])-F(ra[0]['lo']))/2),
                  'threshold_lower':str((F(rb[0]['lo'])+F(ra[0]['lo']))/2),
                  'threshold_upper':str((F(rb[0]['hi'])+F(ra[0]['hi']))/2),
                  'scope':'Sharp supremum for separating the first-positive-zero pair by a single threshold under independent absolute displacements. No claim of optimality over all count gates or full spectral statistics.'}
        results.append({'precision_bits':data['precision_bits'],'grid_measurements':grid,'first_distinguishing_integer_height':first,
                        'robust_gate':robust,'first_zero_gate_critical_radius':critical})
    assert results[0]['grid_measurements']==results[1]['grid_measurements']
    assert results[0]['robust_gate']==results[1]['robust_gate']
    bad_observation={'height':'7/3','positive_zero_count':1,'field_hint':'A'}
    try:select(bad_observation,results[0]['robust_gate'][0]['templates'])
    except ValueError: label_control=True
    else:raise AssertionError('Leaked field identity was accepted')
    exact_gate=results[0]['robust_gate'][0]['templates']
    assert select({'height':'7/3','positive_zero_count':2},exact_gate)==[]
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [arithmetic,classification]+spectra},
            'no_spectral_observation_candidates':['A','B'],'prior_coefficient_at_7_candidates':[0,4],
            'coefficient_at_7_by_selected_field':{k:next(r['coefficients_first_four'][0] for r in v['local_factors'] if r['prime']==7) for k,v in a['fields'].items()},
            'results':results,'forbidden_label_control_rejected':label_control,'incompatible_count_returns_empty':True,
            'scope':'Closed-class discrimination after exact enumeration of the V4 prior. Only the aggregate count enters select(). Candidate spectral templates are certified separately. The measurement is assumed complete with the declared displacement bound; a bare count cannot itself establish completeness or validate arbitrary data.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['arithmetic','classification','spectrum160','spectrum224','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.arithmetic,a.classification,[a.spectrum160,a.spectrum224]);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'first_integer_height':2,'robust_height':'7/3','robust_radius':'1/3','radius_half_count_statistic':'ambiguous','grid_replays':80}))
