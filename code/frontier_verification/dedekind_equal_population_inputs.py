"""Create an anonymous equal-population spectral benchmark by certified cutoff restriction."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path

KEYS={'degree','discriminant','real_places','complex_places','top','positive_root_intervals'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def certified_prefix(data,cutoff):
    assert set(data)==KEYS and type(data['top']) is int and data['top']==20
    T=F(cutoff);assert 0<T<data['top']
    roots=data['positive_root_intervals'];kept=[];partition=[]
    last=None
    for index,r in enumerate(roots):
        assert set(r)=={'lo','hi'};lo,hi=F(r['lo']),F(r['hi']);assert 0<lo<hi<data['top']
        if last is not None:assert last<lo
        last=hi
        if hi<T:side='retained';clearance=T-hi;kept.append(dict(r))
        elif lo>T:side='excluded';clearance=lo-T
        else:raise ValueError('A source root enclosure meets the requested cutoff')
        partition.append({'source_index_zero_based':index,'side':side,'cutoff_clearance':str(clearance),'source_interval':dict(r)})
    assert [r['source_index_zero_based'] for r in partition if r['side']=='retained']==list(range(len(kept)))
    result={k:data[k] for k in ['degree','discriminant','real_places','complex_places']}
    result.update(top=str(T),positive_root_intervals=kept)
    return result,partition
def run(input_archive,cutoff,output_dir):
    T=F(cutoff);assert T==F(39,2);output_dir.mkdir(parents=True,exist_ok=False);cases=[]
    with zipfile.ZipFile(input_archive) as z:
        for bits in [160,224]:
            for index in [1,2]:
                parent='S'+str(index)+'_'+str(bits)+'.json';name='E'+str(index)+'_'+str(bits)+'.json'
                raw=z.read(parent);source=json.loads(raw);data,partition=certified_prefix(source,T)
                assert {k:data[k] for k in ['degree','discriminant','real_places','complex_places']}=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2}
                assert len(data['positive_root_intervals'])==22 and len(partition)==(23 if index==1 else 22)
                destination=output_dir/name;destination.write_text(json.dumps(data,indent=2)+'\n')
                cases.append({'input_member':name,'input_sha256':sha(destination.read_bytes()),'parent_member':parent,'parent_member_sha256':sha(raw),
                              'nominal_precision_bits':bits,'parent_population':len(partition),'retained_population':22,
                              'partition':partition,'minimum_cutoff_clearance':str(min(F(p['cutoff_clearance']) for p in partition)),
                              'completeness_transfer':'The parent contains every positive nontrivial ordinate below20. The smaller cutoff is below20 and meets no source enclosure; retaining precisely the boxes below it gives the complete prefix, with multiplicities.'})
    assert len(cases)==4
    return {'status':'passed','source_sha256':sha(Path(__file__).read_bytes()),'parent_archive_sha256':sha(input_archive.read_bytes()),
            'source_cutoff':'20','new_cutoff':str(T),'cases':cases,'new_roots_computed':0,
            'schema':'Exactly degree, discriminant, real_places, complex_places, top, positive_root_intervals. The new top is a rational string39/2; old consumers requiring an integer top are not silently reused.',
            'inference_boundary':'Parent names, source hashes, partition and research labels remain in this provenance record, outside anonymous input payloads. These known examples are not a blind or external unknown-field study.',
            'scope':'Certified restriction of inherited complete finite spectra to19.5 creates two22-entry populations with matching global metadata. It does not claim their interior count profiles or coordinates are equal, or reuse old Gaussian tail budgets at a new cutoff.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--cutoff',required=True);p.add_argument('--directory',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.inputs,a.cutoff,a.directory);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','cutoff':r['new_cutoff'],'input_files':4,'populations':[22,22,22,22],'new_roots':0}))
