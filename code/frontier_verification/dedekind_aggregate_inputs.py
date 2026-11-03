"""Extract only aggregate ordinates and shared global inputs from certificates."""
import argparse,hashlib,json,zipfile
from pathlib import Path


def build(archive,output):
    output.mkdir(exist_ok=True);mapping=[]
    with zipfile.ZipFile(archive) as z:
        for bits in [160,224]:
            name=f'Pair_Spectrum{bits}.json';raw=z.read(name);data=json.loads(raw)
            assert data['status']=='passed' and data['top']==20
            for code,label in [('S1','A'),('S2','B')]:
                # No candidate names, subfield, character, factor or coefficient data.
                record={'degree':4,'discriminant':576,'real_places':0,'complex_places':2,
                        'top':20,'positive_root_intervals':data['aggregate'][label]['unlabelled_ordinate_intervals']}
                path=output/f'{code}_{bits}.json';path.write_text(json.dumps(record,indent=2)+'\n')
                mapping.append({'input_file':path.name,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                'source_entry':name,'source_entry_sha256':hashlib.sha256(raw).hexdigest(),'held_out_field':label})
    manifest={'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'mapping':mapping,
              'scope':'Provenance and field identities are retained outside decoder inputs. The decoder receives only common degree/discriminant/signature and a complete aggregate finite spectrum. This is an audited data boundary, not a blinded study.'}
    (output/'Input_Provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=build(a.archive,a.output);print(json.dumps({'status':r['status'],'inputs':len(r['mapping'])}))
