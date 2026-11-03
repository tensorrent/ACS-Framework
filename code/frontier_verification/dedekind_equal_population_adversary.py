"""Semantic mutations and literal finite checks of the sharp interior-count argument."""
import argparse,copy,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
import dedekind_equal_population_audit as audit
import dedekind_equal_population_decode as decode
from dedekind_equal_population_inputs import certified_prefix
from dedekind_population_matching import intervals as old_integer_top_consumer

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def finite_check():
    problems=matchings=gates=0
    for n in range(1,5):
        lists=list(itertools.combinations_with_replacement([-1,0,1,2],n))
        for aa in lists:
            for bb in lists:
                a,b=list(map(F,aa)),list(map(F,bb));D=max(abs(x-y) for x,y in zip(a,b))/2
                costs=[max(abs(a[i]-b[j]) for i,j in enumerate(p))/2 for p in itertools.permutations(range(n))]
                assert min(costs)==D;problems+=1;matchings+=len(costs)
                common=[(x+y)/2 for x,y in zip(a,b)];assert all(abs(x-z)<=D and abs(y-z)<=D for x,y,z in zip(a,b,common))
                if D==0:continue
                k=next(i for i in range(n) if abs(a[i]-b[i])/2==D)
                if a[k]<b[k]:a,b=b,a
                h=(a[k]+b[k])/2;r=D-F(1,100)
                possible_a=audit.attainable([(x,x) for x in a],h,r);possible_b=audit.attainable([(x,x) for x in b],h,r)
                assert max(possible_a)<=k and min(possible_b)>=k+1
                for values,possible in [(a,possible_a),(b,possible_b)]:
                    literal=sorted({sum(y<h for y in ys) for ys in itertools.product(*[(x-r,x+r) for x in values])})
                    assert literal==possible
                gates+=1
    return {'equal_length_multiset_pairs':problems,'literal_indexed_matchings':matchings,'positive_gap_count_gates':gates,'scope':'Exhaustive small finite tests, including repeated and negative coordinates, independently compare every indexed permutation and endpoint-generated count. This supports but does not replace the general written proof.'}
def run(decoded,provenance,classification,input_dir,parent_archive,spectrum_archive,arithmetic):
    data=audit.read(decoded);pr=audit.read(provenance);cl=audit.read(classification);obs,parents,spectra=audit.load_data(input_dir,parent_archive,spectrum_archive)
    vectors,fac=audit.arithmetic_vectors(arithmetic,data['columns']);ar=audit.read(arithmetic)
    labels={m['class_id']:next(k for k,v in ar['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    mutations=[]
    def reject(name,call):
        try:call()
        except (AssertionError,ValueError,KeyError,IndexError,TypeError) as e:mutations.append({'name':name,'rejected':True,'exception':type(e).__name__})
        else:raise AssertionError('Mutation accepted: '+name)
    def changed_decode(name,change):
        d=copy.deepcopy(data);change(d);reject(name,lambda:audit.decode_audit(d,cl,obs,spectra,vectors,labels))
    def changed_input(name,change):
        o=copy.deepcopy(obs);change(o);reject(name,lambda:audit.cutoff_audit(pr,o,parents,spectra))
    changed_input('missing retained root',lambda o:o['E1_160.json']['positive_root_intervals'].pop())
    changed_input('retained excluded parent root',lambda o:o['E1_160.json']['positive_root_intervals'].append(parents['S1_160.json']['positive_root_intervals'][-1]))
    changed_input('parent population leaked into anonymous payload',lambda o:o['E1_160.json'].update(parent_population=23))
    changed_input('old cutoff attached to smaller dataset',lambda o:o['E1_160.json'].update(top=20))
    changed_input('root multiplicity duplicated',lambda o:o['E1_160.json']['positive_root_intervals'].__setitem__(1,o['E1_160.json']['positive_root_intervals'][0]))
    for label,T in [('cutoff at interval lower endpoint',parents['S1_160.json']['positive_root_intervals'][1]['lo']),('cutoff at interval upper endpoint',parents['S1_160.json']['positive_root_intervals'][1]['hi'])]:
        reject(label,lambda T=T:certified_prefix(parents['S1_160.json'],T))
    reject('new rational cutoff sent to old integer-T20 consumer',lambda:old_integer_top_consumer(obs['E1_160.json']))
    changed_decode('candidate class removed',lambda d:d['predictions'].pop(next(iter(d['predictions']))))
    changed_decode('wrong Euler coefficient',lambda d:d['predictions'][next(iter(d['predictions']))].__setitem__(0,999))
    changed_decode('false total-count identification',lambda d:d.update(total_population_only_fixed_coefficients=604))
    changed_decode('lost common-observation entry',lambda d:d['matching_cases'][0]['common_observation'].pop())
    changed_decode('shared ordinate outside radius',lambda d:d['matching_cases'][0]['common_observation'].__setitem__(0,'100'))
    changed_decode('wrong critical rank',lambda d:d['matching_cases'][0].update(critical_index_zero_based=0))
    changed_decode('lower endpoint substituted for witness radius',lambda d:d['matching_cases'][0].update(common_observation_radius=d['matching_cases'][0]['radius_lower']))
    changed_decode('box-overlap claimed as actual ambiguity',lambda d:d['matching_cases'][0].update(certificate_boundary_scope='Actual fields already share an observation at L'))
    changed_decode('post-noise censoring substituted',lambda d:d['contract'].update(post_noise_window_censoring=True))
    changed_decode('false boundary uniqueness',lambda d:d['count_cases'][10].update(unique_for_every_admissible_count=True))
    changed_decode('count envelope corrupted',lambda d:d['count_cases'][0]['candidate_envelopes'][next(iter(d['predictions']))].update(maximum=22))
    changed_decode('decision removed from case',lambda d:d['count_cases'][0]['selections'].clear())
    c=data['count_cases'][0];measurement=c['selections'][0]['measurement'];templates=c['candidate_envelopes']
    for label,change in [
        ('boolean count',lambda m:m.update(count=True)),('negative count',lambda m:m.update(count=-1)),('count above population',lambda m:m.update(count=23)),
        ('parent filename leaked to selector',lambda m:m.update(filename='S1_160.json')),('field label leaked to selector',lambda m:m.update(field='A')),
        ('wrong scalar height',lambda m:m.update(height='3')),('negative radius',lambda m:m.update(radius='-1')),('binary64 radius',lambda m:m.update(radius=0.0)),
        ('deletion allowance',lambda m:m['contract'].update(deletions=1)),('boolean deletion budget',lambda m:m['contract'].update(deletions=False)),
        ('false completeness declaration',lambda m:m['contract'].update(complete_preselected_population=False)),('wrong population size',lambda m:m['contract'].update(population_size=23))]:
        m=copy.deepcopy(measurement);change(m);reject(label,lambda m=m:decode.select_count(m,templates))
    m=data['matching_cases'][0];L,H=F(m['radius_lower']),F(m['rational_height']);inside=L-F(1,10**100);outside=L+F(1,10**100)
    assert float(inside)==float(L)==float(outside)
    below=next(c for c in data['count_cases'] if c['precision_bits']==160 and F(c['radius'])==inside)
    above=next(c for c in data['count_cases'] if c['precision_bits']==160 and F(c['radius'])==outside)
    assert below['unique_for_every_admissible_count'] and not above['unique_for_every_admissible_count']
    y=list(map(F,m['common_observation']));strict=sum(x<H for x in y);closed=sum(x<=H for x in y);assert (strict,closed)==(1,2)
    finite=finite_check()
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [decoded,provenance,classification,parent_archive,spectrum_archive,arithmetic]+sorted(input_dir.glob('*.json'))},'mutations':mutations,'mutations_rejected':len(mutations),'finite_crosscheck':finite,
            'floating_point_boundary_counterexample':{'r_below':str(inside),'r_above':str(outside),'same_binary64':float(inside),'below_certificate_unique':True,'above_certificate_unique':False,'scope':'Distinct closed-box certificate outcomes, not a claim of actual ambiguity immediately above L.'},
            'strict_versus_closed_gate_control':{'height':str(H),'shared_observation_strict_count':strict,'shared_observation_closed_count':closed},
            'scope':'These semantic mutations are exercised against actual decoder and audit functions. A finite list count still cannot authenticate a false external completeness premise. The two supplied benchmark inputs remain known examples, not statistically blind data.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['decoded','provenance','classification','inputs','parent','spectra','arithmetic','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.decoded,a.provenance,a.classification,a.inputs,a.parent,a.spectra,a.arithmetic);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','mutations_rejected':r['mutations_rejected'],'finite_crosscheck':r['finite_crosscheck']}))
