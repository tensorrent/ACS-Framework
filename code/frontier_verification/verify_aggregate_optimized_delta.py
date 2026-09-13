"""Verify noise-adapted aggregate certificates and their immutable research history."""
import contextlib,hashlib,io,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_aggregate_noise_proposals as proposals
import dedekind_aggregate_noise_certificate as certificate
import dedekind_aggregate_noise_audit as audit
import dedekind_aggregate_noise_adversary as adversary
from dedekind_aggregate_local_audit import catalog,coefficient

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-aggregate-optimized-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-aggregate-shared-delta';BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def same(a,b):assert canonical(a)==canonical(b)
def quiet(fn,*args):
    with contextlib.redirect_stdout(io.StringIO()):return fn(*args)
def unpack(path,tmp,names):
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist())==set(names)
        for name in names:(tmp/name).write_bytes(z.read(name))

def summarize(coarse,fine,independent):
    audited=[];supported=[];improvements=[]
    for row in fine['results']:
        obs=row['observation_index'];radius=row['radius'];methods={}
        for source in ['frozen','noise_adapted']:
            selected=[c for c in independent['objective_replays'] if c['observation_index']==obs and c['radius']==radius and c['multiplier_source']==source];assert len(selected)==2
            for name in ['direct_one_sided','symmetric_derivative']:
                methods[source+'_'+name]=sorted(set(selected[0]['methods'][name]['c7_candidates'])&set(selected[1]['methods'][name]['c7_candidates']))
        audited.append({'observation_index':obs,'radius':radius,'methods':methods})
        other=next(r for r in coarse['results'] if r['observation_index']==obs and r['radius']==radius)
        supported.append({'observation_index':obs,'radius':radius,'methods':{name:sorted(set(values)&set(row['methods'][name])&set(other['methods'][name])) for name,values in methods.items()}})
    for c,r in zip(fine['cases'],independent['objective_replays']):
        assert all(c[k]==r[k] for k in ['observation_index','radius','sign','multiplier_source'])
        for name in c['methods']:
            old,new=c['methods'][name]['c7_candidates'],r['methods'][name]['c7_candidates']
            if old!=new:improvements.append({**{k:c[k] for k in ['observation_index','radius','sign','multiplier_source']},'method':name,'producer_candidates':old,'independent_candidates':new})
    maxima={name:[str(max((F(r['radius']) for r in supported if r['observation_index']==obs and len(r['methods'][name])==1),default=F(0))) for obs in range(2)] for name in supported[0]['methods']}
    models=catalog();allowed=sorted({coefficient(model,1) for model in models if all(e==1 for e,f in model)});assert allowed==[0,1,2,4] and 576%7
    supplement=[{'observation_index':r['observation_index'],'radius':r['radius'],'c7_candidates':sorted(set(r['methods']['noise_adapted_direct_one_sided'])&set(allowed))} for r in supported]
    local_max=[str(max(F(r['radius']) for r in supplement if r['observation_index']==obs and len(r['c7_candidates'])==1)) for obs in range(2)]
    return {'producer_radius_results':{'224':coarse['results'],'320':fine['results']},'independently_audited_radius_results':audited,'supported_radius_results':supported,
            'largest_successful_tested_radii':maxima,'precision_subdivision_differences':independent['precision_subdivision_differences'],
            'independent_candidate_improvements':improvements,'generic_unramified_values':allowed,'generic_unramified_supplement':supplement,'largest_tested_unramified_supplement_radii':local_max}

def main():
    prior=subprocess.run([sys.executable,str(CODE/'verify_aggregate_shared_delta.py')],capture_output=True,text=True)
    assert prior.returncode==0,prior.stdout+prior.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        unpack(BASELINE/'Aggregate_Inputs.zip',tmp,['S1_160.json','S2_160.json','S1_224.json','S2_224.json'])
        unpack(BASELINE/'Measurements_Recovery.zip',tmp,['Measurements160.json','Measurements224.json','Recovery160.json','Recovery224.json'])
        unpack(OUT/'Noise_Certificates.zip',tmp,['Certificate224.json','Certificate320.json'])
        m=tmp/'Measurements224.json';r=tmp/'Recovery224.json';inputs=[tmp/'S1_224.json',tmp/'S2_224.json'];pp=OUT/'Proposals.json';cp=[tmp/'Certificate224.json',tmp/'Certificate320.json']
        proposed=read(pp);same(proposed,quiet(proposals.run,m,inputs));assert len(proposed['cases'])==48 and all(c['solver_status']==0 for c in proposed['cases'])
        for bits,path in zip([224,320],cp):same(read(path),quiet(certificate.run,m,r,pp,inputs,bits))
        independent=read(OUT/'Noise_Audit.json');mutations=read(OUT/'Adversary_Audit.json')
        same(independent,quiet(audit.run,cp,m,r,pp,inputs,BASELINE/'Integer_Audit.json'))
        same(mutations,quiet(adversary.run,cp[1],OUT/'Noise_Audit.json',m,inputs))
        for data in [proposed,read(cp[0]),read(cp[1]),independent,mutations]:
            for name,digest in data['inputs_sha256'].items():
                path=next(p for p in [tmp/name,OUT/name,BASELINE/name] if p.exists());assert sha(path.read_bytes())==digest
        summary=summarize(read(cp[0]),read(cp[1]),independent)
        same(summary,read(OUT/'Noise_Summary.json')['derived_results'])
        assert summary['largest_successful_tested_radii']=={'frozen_direct_one_sided':['1/500','7/100'],'frozen_symmetric_derivative':['1/500','7/100'],
            'noise_adapted_direct_one_sided':['3/50','13/100'],'noise_adapted_symmetric_derivative':['1/50','1/10']}
        assert summary['largest_tested_unramified_supplement_radii']==['7/50','13/100']
        assert len(summary['precision_subdivision_differences'])==1 and len(summary['independent_candidate_improvements'])==2
        assert independent['stored_midpoints_checked']==158400 and independent['fresh_quadratic_interval_leaves']==126720 and independent['exact_objective_bounds']==192
        assert len(independent['independent_displaced_controls'])==192 and len(independent['certified_off_grid_counterexamples'])==2
        assert mutations['actual_component_mutations_rejected']==8
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==6 and all(r['returncode']==0 and not r['timed_out'] for r in receipts.values())
    assert receipts['noise-proposals']['started_utc']<min(receipts[n]['started_utc'] for n in ['noise-certificate224','noise-certificate320'])
    assert max(receipts[n]['started_utc'] for n in ['noise-certificate224','noise-certificate320'])<receipts['independent-noise-audit']['started_utc']
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r and set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
    probe=read(OUT/'Exploratory_Probe.json');assert len(probe['cases'])==36 and all(c['status']==0 for c in probe['cases'])
    for path,digest in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    sources=read(OUT/'Primary_Sources.json');assert sources['new_downloads']==0 and sources['inherited_record_sha256']==sha((BASELINE/'Primary_Sources.json').read_bytes())
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==117 and queue['new_branches']==[] and queue['advanced_existing_branches']==ADVANCED
    assert queue['global_exhaustion_claimed'] is False and queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:
            assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition']
            assert a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==393 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==398
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_OPTIMIZED_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Fresh sampled proposals, exact-rational continuum certificates, independent complex quadratic covers, integer objective replay, displaced sums, off-grid counterexamples and semantic mutations. Prior checkpoint verified recursively. Interval routes share FLINT; no optimal noise threshold or full formal proof is claimed.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','coefficient_target':7,'measurement_rows':17,'generic_coefficients':604,
        'largest_tested_noise_adapted_direct_radii':['3/50','13/100'],'largest_tested_frozen_direct_radii':['1/500','7/100'],
        'largest_tested_noise_adapted_symmetric_radii':['1/50','1/10'],'largest_tested_unramified_supplement_radii':['7/50','13/100'],
        'proposal_count':48,'exploratory_proposal_count':36,'stored_midpoints_checked':158400,'fresh_quadratic_interval_leaves':126720,
        'exact_objective_bounds':192,'independent_displaced_controls':192,'certified_off_grid_counterexamples':2,'actual_component_mutations_rejected':8,
        'producer_subdivision_differences':1,'independent_candidate_improvements':2,'recorded_commands':6,'failed_commands':0,
        'research_branches':117,'ledger_events':398,'preserved_event_prefix':393,'ledger_head_sha256':last,'local_links':links},indent=2))

if __name__=='__main__':main()
