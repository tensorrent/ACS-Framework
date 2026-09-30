"""Extract measurement terms, without importing prior inferred coefficients."""
import argparse,hashlib,json,zipfile
from pathlib import Path


def extract(path):
    with zipfile.ZipFile(path) as z:
        data=json.loads(z.read('Recovery_160.json'));inputs=json.loads(z.read('Recovery_Inputs.json'))
    evals={(r['n'],r['denominator']):r for r in data['evaluations']}
    result={'scope':'Measurement-only boundary: no inferred candidates, local models or validation coefficients.',
            'extractor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'prior_archive_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256':data['source_sha256'],'zero_input_sha256':data['input_sha256'],
            'degree':4,'discriminant':125,'real_places':0,'complex_places':2,'prime_cutoff':4096,
            'roots':inputs['positive_root_intervals'],'measurements':[]}
    for row in data['cases']:
        e=evals[row['n'],row['denominator']]
        result['measurements'].append({key:row[key] for key in ['n','prime','power','height','denominator']}|
              {'pole':e['pole'],'discriminant_term':e['discriminant'],'gamma':e['gamma']['enclosure'],
               'finite_zero_sum':e['finite_sums'][str(row['height'])]})
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=extract(a.prior)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','measurements':len(r['measurements']),'roots':len(r['roots'])}))
