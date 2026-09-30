"""Freshly certify earlier multiplier directions as simultaneous global linear cuts."""
import argparse,gc,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_moment_certificate import certify

RADII=['1/10','3/50']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def collect(measurements,inputs,recovery,noise,moment,adaptive,nested):
    m=json.loads(measurements.read_text());pools=[{},{}];zero_counts={}
    assert [sha(p) for p in inputs]==m['input_sha256']
    def add(obs,values,origin):
        normalized=sorted([[int(j),str(F(v))] for j,v in values if F(v)])
        assert len({j for j,v in normalized})==len(normalized)
        assert all(0<=j<34 and F(v)>0 and (F(v)*10**9).denominator==1 for j,v in normalized)
        if not normalized:
            zero_counts[origin['source']]=zero_counts.get(origin['source'],0)+1;return
        key=hashlib.sha256(canonical(normalized)).hexdigest()
        if key not in pools[obs]:pools[obs][key]={'multipliers':normalized,'origins':[]}
        pools[obs][key]['origins'].append(origin)
    r=json.loads(recovery.read_text());assert r['measurement_sha256']==sha(measurements)
    for obs,result in enumerate(r['results']):
        for i,target in enumerate(result['dual_targets']):
            for j,c in enumerate(target['certificates']):add(obs,c['multipliers'],{'source':recovery.name,'position':[obs,i,j]})
    del r;gc.collect()
    for path,key in [(noise,'cases'),(moment,'cases'),(adaptive,'certificates'),(nested,'certificates')]:
        d=json.loads(path.read_text());assert d['inputs_sha256'][measurements.name]==sha(measurements)
        for p in inputs:assert d['inputs_sha256'][p.name]==sha(p)
        for i,c in enumerate(d[key]):add(c['observation_index'],c['multipliers'],{'source':path.name,'position':[i]})
        del d;gc.collect()
    for obs in [0,1]:
        for j in range(34):add(obs,[[j,'1']],{'source':'unit','position':[j]})
    return pools,zero_counts

def run(measurements,inputs,recovery,noise,moment,adaptive,nested):
    m=json.loads(measurements.read_text());sources=[json.loads(p.read_text()) for p in inputs]
    assert m['global_inputs']=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2,'top':20}
    pools,zero_counts=collect(measurements,inputs,recovery,noise,moment,adaptive,nested);results=[]
    paths=[measurements,recovery,noise,moment,adaptive,nested]+inputs
    for obs,pool in enumerate(pools):
        cases=[]
        for key,entry in sorted(pool.items()):
            # The target label is bookkeeping; the new use retains A_lambda*c <= b_lambda+E_lambda.
            request={'observation_index':obs,'radius':RADII[obs],'column':0,'n':m['columns'][0]['n'],'sign':1,'multipliers':entry['multipliers']}
            proof=certify(m,sources[obs],request)
            cases.append({'direction_sha256':key,'origins':entry['origins'],'is_unit_row':any(o['source']=='unit' for o in entry['origins']),'certificate':proof})
            if len(cases)%20==0:print(json.dumps({'event':'global_cut_certificate','observation':obs,'directions':len(cases)}),flush=True)
        assert sum(c['is_unit_row'] for c in cases)==34
        results.append({'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in paths},
                        'observation_index':obs,'radius':RADII[obs],'global_inputs':m['global_inputs'],'columns':m['columns'],'cases':cases,
                        'skipped_zero_vectors_by_source':zero_counts,
                        'scope':'All distinct nonzero directions from the listed earlier proposal/certificate records, plus 34 unit signed rows, receive fresh shared finite/moment certificates at this observation-specific radius. Original selection radii/profiles do not become assumptions: every analytic budget is recomputed. The subsequent use retains global linear inequalities rather than only signed target bounds. No arithmetic coefficients enter this stage.'})
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','recovery','noise','moment','adaptive','nested','output-a','output-b']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.measurements,a.inputs,a.recovery,a.noise,a.moment,a.adaptive,a.nested)
    for path,data in zip([a.output_a,a.output_b],r):path.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps({'status':'passed','directions':[len(d['cases']) for d in r],'unit_rows':[sum(c['is_unit_row'] for c in d['cases']) for d in r]}))
