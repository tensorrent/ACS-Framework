"""Verify the shared-invariant field benchmark; optionally replay all contours."""
import argparse, hashlib, json, re, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
from flint import arb, acb, ctx, dirichlet_char
import dedekind_biquadratic_pair as producer
import dedekind_biquadratic_arithmetic_audit as arithmetic
import dedekind_biquadratic_class as classification
import dedekind_biquadratic_decoding as decoding
import dedekind_biquadratic_adversary as adversary
import dedekind_biquadratic_replay as replay
import lfunction_zero_certificate as core

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
PRIOR=ROOT/'docs/frontier/2026-09-13-invariant-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def same(a,b):assert canonical(a)==canonical(b)
def ball(row):return arb(arb(tuple(row['mid'])),arb(tuple(row['rad'])))


def main(recompute):
    previous=subprocess.run([sys.executable,str(CODE/'verify_invariant_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    a=OUT/'Pair_Arithmetic.json';c=OUT/'Pair_Candidate_Class.json';d=OUT/'Pair_Decoding.json'
    same(read(a),producer.run());same(read(OUT/'Pair_Arithmetic_Audit.json'),arithmetic.run(a));same(read(c),classification.run(a))
    endpoint_checks=0
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        with zipfile.ZipFile(OUT/'Pair_Spectra.zip') as z:
            assert set(z.namelist())=={'Pair_Spectrum160.json','Pair_Spectrum224.json','Pair_Spectral_Audit.json'}
            for name in z.namelist():(tmp/name).write_bytes(z.read(name))
        paths=[tmp/'Pair_Spectrum160.json',tmp/'Pair_Spectrum224.json'];spectra=[read(p) for p in paths]
        same(read(d),decoding.run(a,c,paths));same(read(OUT/'Pair_Adversary.json'),adversary.run(a,paths,d))
        ctx.prec=256
        for data in spectra:
            replay.validate(data)
            assert data['source_sha256']==sha((CODE/'dedekind_biquadratic_spectrum.py').read_bytes())
            for name,digest in data['dependencies_sha256'].items():assert digest==sha((CODE/name).read_bytes())
            roots=[]
            for factor in data['factors'].values():
                assert int(ball(factor['contour']['winding']).unique_fmpz())==len(factor['root_intervals'])
                chi=dirichlet_char(factor['modulus'],factor['conrey_number'])
                for r in factor['root_intervals']:
                    for end in ['lo','hi']:
                        assert core.sign(core.hardy(chi,F(r[end])))==r[end+'_sign'];endpoint_checks+=1
                roots+=factor['root_intervals']
            roots+=data['zeta']['root_intervals'];roots.sort(key=lambda r:F(r['lo']))
            assert len(roots)==40 and all(F(x['hi'])<F(y['lo']) for x,y in zip(roots,roots[1:]))
            z1,z2=list(acb.zeta_zeros(1,2));zr=data['zeta']['root_intervals'][0]
            assert int(arb(20).zeta_nzeros().unique_fmpz())==1 and z2.imag>20
            assert z1.imag>arb(zr['lo']) and z1.imag<arb(zr['hi'])
        assert endpoint_checks==156
        direct_path=tmp/'Pair_Spectral_Audit.json';direct=read(direct_path)
        assert direct['source_sha256']==sha((CODE/'dedekind_biquadratic_spectral_audit.py').read_bytes())
        assert direct['core_sha256']==sha((CODE/'lfunction_zero_certificate.py').read_bytes())
        assert direct['endpoint_sign_replays']==156 and len(direct['independent_roots'])==16
        assert sum(len(r['contour']['segments']) for r in direct['direct_L_contours'])==63405
        for r in direct['independent_roots']:
            assert F(r['residual'])<F(1,10**74)
            for data in spectra:
                roots=data['zeta']['root_intervals'] if r['D']=='zeta' else data['factors'][str(r['D'])]['root_intervals']
                bracket=roots[r['index']-1];assert F(bracket['lo'])<F(r['root'])<F(bracket['hi'])
        fresh=read(OUT/'Pair_Fresh_Replay.json')
        assert fresh['source_sha256']==sha((CODE/'dedekind_biquadratic_replay.py').read_bytes())
        assert fresh['stored_segments_replayed']==63405 and fresh['fresh_certified_leaves']==77735
        for r in fresh['direct_paths']:
            assert r['fresh_leaves']==r['stored_segments']+r['subdivisions']
            assert int(ball(r['winding']).unique_fmpz())==r['contour_count']==r['positive_count']+int(r['D']>0)
            assert r['positive_count']==len(spectra[0]['factors'][str(r['D'])]['root_intervals'])
        for output in [direct,fresh,read(d),read(OUT/'Pair_Adversary.json')]:
            for name,digest in output['inputs_sha256'].items():
                path=tmp/name if (tmp/name).exists() else OUT/name
                assert digest==sha(path.read_bytes())
        if recompute:same(fresh,replay.run(paths,direct_path))
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==11 and sum(r['returncode']==0 for r in receipts.values())==10
    assert receipts['pair-fresh-path-replay']['returncode']==1 and receipts['pair-refined-path-replay']['returncode']==0
    assert receipts['pair-arithmetic']['started_utc']<receipts['pair-spectrum160']['started_utc']
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert read_json_bytes(z.read(name+'/receipt.json'))==r
            assert set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
        assert 'AssertionError' in z.read('pair-fresh-path-replay/stderr.txt').decode()
    sources=read(OUT/'Source_Acquisition.json');assert sources['status']=='passed' and len(sources['sources'])==3
    assert all(r['curl_returncode']==0 and r['bytes']>0 and len(r['sha256'])==64 for r in sources['sources'])
    old=read(PRIOR/'Research_Queue.json');queue=read(OUT/'Research_Queue.json')
    before={b['id']:b for b in old['branches']};after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==117 and queue['new_branches']==[]
    assert queue['advanced_existing_branches']==ADVANCED and queue['global_exhaustion_claimed'] is False
    assert queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        n=after[bid];assert n['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:
            assert n['latest_scoped_result']==b['latest_scoped_result'] and n['continuation_condition']==b['continuation_condition']
            assert n['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in n['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes()
    assert len(prefix.splitlines())==378 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256')
        assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==383
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'BIQUADRATIC_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Recursive checkpoint integrity and fresh exact arithmetic, class, count, mutation and endpoint audits. Full direct contours were replayed in the retained execution; default mode checks their transcript hashes. --recompute-contours reruns all direct paths. Classical premises remain unformalized.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','candidate_fields':2,
        'maximal_order_cosets':190,'local_factorizations':144,'finite_factor_roots':40,'fresh_endpoint_signs':endpoint_checks,
        'recorded_direct_segments':63405,'recorded_refined_leaves':77735,'contours_recomputed_this_invocation':recompute,
        'independent_backend_roots':16,'grid_count_replays':80,'actual_mutations_rejected':11,'recorded_commands':11,'failed_commands':1,
        'research_branches':117,'ledger_events':383,'preserved_event_prefix':378,'ledger_head_sha256':last,'local_links':links},indent=2))


def read_json_bytes(raw):return json.loads(raw)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--recompute-contours',action='store_true');main(p.parse_args().recompute_contours)
