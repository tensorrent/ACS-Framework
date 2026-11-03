"""Check retained quadratic certificates, failed attempts and append-only history."""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from flint import arb,ctx

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-quadratic-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-shared-delta'
ADVANCED=['R12','R13','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(p.read_text())
def ball(v):return arb(arb(tuple(v['mid'])),arb(tuple(v['rad'])))
def exact(v):
    m,e=map(int,v.man_exp());return F(m)*F(2)**e


def main():
    ctx.prec=256
    earlier=subprocess.run([sys.executable,str(CODE/'verify_shared_delta.py')],capture_output=True,text=True)
    assert earlier.returncode==0,earlier.stdout+earlier.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        source_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.py')}
        lean_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.lean')}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert sha(z.read(kind+'/'+path))==digest==sha((ROOT/path).read_bytes())
    with zipfile.ZipFile(OUT/'Quadratic_Audits.zip') as z:raws={n:z.read(n) for n in z.namelist()}
    expected={'Quadratic_Frozen160.json':'dedekind_quadratic_ordinate.py',
        'Quadratic_160.json':'dedekind_quadratic_recovery.py',
        'Conic_Probe160.json':'dedekind_quadratic_conic.py','Conic_Extended160.json':'dedekind_quadratic_conic.py',
        'Quadratic_Union160.json':'dedekind_quadratic_union.py'}
    assert set(raws)==set(expected);data={n:json.loads(raw) for n,raw in raws.items()}
    audit=read(OUT/'Quadratic_Audit.json');numeric=read(OUT/'Quadratic_Numeric2.json')
    assert audit['status']=='passed' and audit['source_sha256']==sha((CODE/'dedekind_quadratic_audit.py').read_bytes())
    assert audit['basis_source_sha256']==sha((CODE/'dedekind_quadratic_ordinate.py').read_bytes())
    assert audit['results_sha256']=={n:sha(raw) for n,raw in raws.items()}
    assert audit['fixed_point_scale_bits']==192 and audit['multiplier_denominator']==10**9
    with zipfile.ZipFile(PRIOR/'Shared_Audits.zip') as z:seed_raw=z.read('Shared_160.json')
    previous=json.loads(seed_raw);seeds=[d['candidates'] for d in previous['domains']]
    truth=read(PRIOR.parent/'2026-09-13-coupled-delta'/'Exact_Audit.json')['relaxation_ambiguity']['baseline_coefficients']
    assert previous['unique_targets']==81 and len(seeds)==len(truth)==604
    for name,result in data.items():
        assert result['status']=='passed' and result['precision_bits']==160
        assert result['source_sha256']==sha((CODE/expected[name]).read_bytes())
        p=result['provenance'];assert p['seed_domains']==previous['domains']
        assert p['shared_result_sha256']==sha(seed_raw) and p['shared_audit_sha256']==sha((PRIOR/'Shared_Audit.json').read_bytes())
        assert p['seed_domains_sha256']==sha(canonical(seeds))
        assert result['basis']['roots']==7602 and len(result['basis']['basis'])==455
        if 'basis_source_sha256' in result:assert result['basis_source_sha256']==audit['basis_source_sha256']
    certificate_count=0;replay_count=0
    def replay(name,stage,bits,mode,steps,expected_domains,grouped=False,conic=False):
        nonlocal certificate_count,replay_count
        matching=[r for r in audit['replays'] if r['file']==name and r['stage']==stage and r['precision_bits']==bits]
        assert len(matching)==1;retained=matching[0];items=iter(retained['certificates']);domains=[list(d) for d in seeds]
        def bound(c,column):
            nonlocal certificate_count
            item=next(items);certificate_count+=1
            assert item['n']==previous['domains'][column]['n'] and item['sign']==c['sign'] and c['sign'] in [-1,1]
            assert item['precision_bits']==bits and item['mode']==mode
            assert item['combination_sha256']==c['combination_sha256']==sha(canonical(c['multipliers']))
            assert len({i for i,v in c['multipliers']})==len(c['multipliers'])
            assert all(0<=i<455 and (F(v)*10**9).denominator==1 for i,v in c['multipliers'])
            value=sum(F(item[k]) for k in ['weighted_center_upper','tail_upper','ordinate_support_upper','residual_support_upper'])
            assert value==F(item['objective_upper_bound']) and c['sign']*truth[column]<=value
            proof=c['bounds'][mode] if 'bounds' in c else c
            return value,ball(proof['objective_upper_bound']).upper()
        for step in steps:
            old=[list(d) for d in domains]
            if not conic:assert step['prior_domains_sha256']==sha(canonical(old))
            for check in step['checks']:
                column=check['column'];before=seeds[column] if conic else old[column] if grouped else domains[column]
                assert check['before']==before
                cs=check['certificates'] if grouped else [check]
                values=[bound(c,column) for c in cs]
                after=[v for v in before if all(c['sign']*v<=value for c,(value,_) in zip(cs,values))]
                assert after==[v for v in before if all(not arb(c['sign']*v)>value for c,(_,value) in zip(cs,values))]
                wanted=check['control_candidates'][mode] if conic else check['after']
                assert after==wanted and after;domains[column]=after
            if not conic:assert step['remaining_domains_sha256']==sha(canonical(domains))
        assert list(items)==[] and retained['domains_sha256']==sha(canonical(domains))
        assert retained['all_604_arithmetic_coefficients_retained'] and all(t in d for t,d in zip(truth,domains))
        if expected_domains is not None:assert domains==[d['candidates'] for d in expected_domains]
        replay_count+=1
    for name,result in data.items():
        for bits in [160,224]:
            if 'cases' in result:
                for case in result['cases']:replay(name,case['mode'],bits,case['mode'],case['rounds'],case['domains'])
            elif 'rounds' in result:
                replay(name,'optimized_main',bits,'quadratic',result['rounds'],result['domains'],grouped=True)
                for case in result['controls']:
                    replay(name,'proposal_control_'+case['mode'],bits,case['mode'],case['rounds'],case['domains'])
            else:
                for mode in ['linear','independent_quadratic','quadratic']:
                    replay(name,'conic_'+mode,bits,mode,[{'checks':result['checks']}],None,grouped=True,conic=True)
    assert certificate_count==audit['certificate_evaluations_across_precisions']==2392 and replay_count==len(audit['replays'])==32
    frozen=data['Quadratic_Frozen160.json'];optimized=data['Quadratic_160.json'];union=data['Quadratic_Union160.json']
    assert [c['unique_targets'] for c in frozen['cases']]==[81,81,81]
    assert optimized['unique_targets']==83 and optimized['stabilized'] and len(optimized['rounds'])==3
    statuses=[c['solver_status'] for s in optimized['rounds'] for k in s['checks'] for c in k['certificates']]
    assert len(statuses)==52 and statuses.count(0)==50 and statuses.count(None)==2
    assert union['input_results_sha256']=={n:sha(raws[n]) for n in expected if n!='Quadratic_Union160.json'}
    assert len(union['proposals'])==100 and len(union['combinations'])==15
    assert [c['unique_targets'] for c in union['cases']]==[81,83,83]
    final=next(c for c in union['cases'] if c['mode']=='quadratic')
    assert final['domains']==optimized['domains']==next(c for c in union['cases'] if c['mode']=='independent_quadratic')['domains']
    changes=[{'n':d['n'],'before':s,'after':d['candidates']} for d,s in zip(final['domains'],seeds) if d['candidates']!=s]
    assert changes==[{'n':128,'before':[0,1,2,3],'after':[0,1,2]},
        {'n':256,'before':[0,1,2,3,4],'after':[1,2,3,4]},
        {'n':289,'before':[0,1],'after':[0]},{'n':359,'before':[0,1],'after':[0]},
        {'n':361,'before':[2,3,4],'after':[3,4]}]
    unresolved=[d for d in final['domains'] if d['n']<=361 and len(d['candidates'])>1]
    assert [d['n'] for d in unresolved]==[64,81,125,128,243,256,343,361]
    conic_statuses=[]
    for name in ['Conic_Probe160.json','Conic_Extended160.json']:
        result=data[name];assert result['unique_targets']==81
        model=result['float_model'];assert model['variables']==15808 and model['rows']==32526 and model['lorentz_cones']==7602
        assert model['nonnegative_cone_dimension']==9720 and result['geometry_check']['solver_status']=='Solved'
        assert result['runtime_additions']=={'clarabel':'0.11.1','cffi':'2.1.1','pycparser':'3.0'}
        conic_statuses += [c['solver_status'] for check in result['checks'] for c in check['certificates']]
    assert conic_statuses.count('MaxTime')==2 and conic_statuses.count('AlmostSolved')==1 and conic_statuses.count('Solved')==5
    assert numeric['status']=='passed' and numeric['source_sha256']==sha((CODE/'dedekind_quadratic_numeric.py').read_bytes())
    assert numeric['basis_source_sha256']==audit['basis_source_sha256'] and numeric['input_result_sha256']==sha(raws['Quadratic_160.json'])
    assert numeric['symbolic_third_derivative_identity'] and numeric['mpmath_digits']==80
    assert len(numeric['derivative_cases'])==75 and all(c['curvature_enclosed'] and c['third_derivatives_bounded'] for c in numeric['derivative_cases'])
    assert len(numeric['displaced_finite_sums'])==2
    for check in numeric['displaced_finite_sums']:
        assert check['roots']==7602 and len(check['directions'])==7602 and set(check['directions'])<={-1,1}
        residual=ball(check['strictly_positive_cubic_residual'])
        assert residual>0 and residual.abs_upper()<ball(check['certified_cubic_allowance']).upper()
        assert residual.overlaps(ball(check['actual_change'])-ball(check['quadratic_prediction']))
        assert exact(residual.lower())<=F(check['mp_residual'])<=exact(residual.upper())
    witness=numeric['adversarial_controls']['omitted_interior_vertex']
    assert ball(witness['strict_excess_over_endpoints'])>0 and ball(witness['interior_vertex']).lower()>-1 and ball(witness['interior_vertex']).upper()<1
    assert len(numeric['scalar_maximum_checks'])==1
    scalar=numeric['scalar_maximum_checks'][0]
    midpoint_max=exact(ball(witness['linear_coefficient']).mid())**2/(4*exact(ball(witness['quadratic_coefficient']).mid()))
    assert midpoint_max==F(scalar['exact_midpoint_maximum'])<=exact(ball(scalar['certified_upper']).upper())
    assert abs(F(scalar['mp_maximum'])-midpoint_max)<abs(midpoint_max)*F(1,10**55)
    dependency=audit['missing_seed_control'];assert F(dependency['without_seed_bounds'])>F(dependency['valid_upper'])
    assert any(F(dependency['valid_upper'])<v<=F(dependency['without_seed_bounds']) for v in dependency['excluded'])
    lean=read(OUT/'Lean_Check.json')
    assert lean['status']=='passed' and lean['returncode']==0 and lean['source_sha256']==sha((CODE/'proofs/QuadraticSupport.lean').read_bytes())
    assert lean['checker_sha256']==sha((CODE/'check_quadratic_lean.py').read_bytes())
    traces=re.findall(r"'QuadraticSupport\.([^']+)' depends on axioms: (\[[^\]]*\])",lean['stdout'])
    assert len(traces)==10 and len({n for n,a in traces})==10
    assert all('sorryAx' not in a for n,a in traces) and 'sorryAx' not in lean['stdout']
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==14 and sum(r['returncode']==0 for r in receipts.values())==10
    assert {n for n,r in receipts.items() if r['returncode']!=0}=={'quadratic-independent-numeric','quadratic-lean2','quadratic-lean3','quadratic-lean4'}
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
            assert set(r['input_sources_sha256'].values())<=source_hashes
        assert sha(z.read('Lean_Check5.olean'))==lean['olean_sha256']
        for version in [2,3,4,5]:
            check=json.loads(z.read('Lean_Check'+str(version)+'.json'))
            assert check['source_sha256'] in lean_hashes and check['checker_sha256'] in source_hashes
            assert check['status']==('passed' if version==5 else 'failed')
        assert json.loads(z.read('Lean_Check5.json'))==lean
        assert 'quadratic-lean1/Launch_Failure.json' in z.namelist()
        packaging=json.loads(z.read('Packaging_Failure.json'))
        assert packaging['status']=='failed' and packaging['exception']=='FileNotFoundError'
        diagnostic=json.loads(z.read('Scalar_Diagnostic.json'))
        assert diagnostic['exact_comparison_passed'] and not diagnostic['mp_comparison_passed']
        assert F(diagnostic['exact_midpoint_maximum'])<=F(diagnostic['exact_support_upper'])
    summary=read(OUT/'Quadratic_Summary.json')
    assert summary['unresolved_targets']==unresolved and summary['all_target_domain_changes']==changes
    assert summary['quadratic_unique_targets']==83 and summary['certificate_evaluations_across_precisions']==2392
    ledger=(OUT/'Branch_Events.jsonl').read_bytes();prefix=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(prefix) and len(prefix.splitlines())==366;last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256')
        assert event['sequence']==index and event['previous_event_sha256']==last and sha(canonical(event))==digest
        last=digest
    assert index==369
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==116 and queue['new_branches']==[] and queue['global_exhaustion_claimed'] is False
    assert queue['advanced_existing_branches']==ADVANCED
    assert queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in after.items():
        old=before[bid];assert b['prior_delta_evidence']==old.get('prior_delta_evidence',[])+old['new_evidence']
        if bid not in ADVANCED:
            assert b['latest_scoped_result']==old['latest_scoped_result'] and b['continuation_condition']==old['continuation_condition']
            assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in b['new_evidence']:assert (ROOT/path).exists()
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'QUADRATIC_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Retained source, transcript and history checks. Recorded numerical and Lean audits are verified by their artifacts; optimizers, analytic bases and kernel compilation are not rerun.',
        'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
        'certificate_evaluations_across_two_precisions':certificate_count,'replay_stages':replay_count,
        'independent_derivative_cases':75,'independent_full_displaced_sums':2,'kernel_checked_scalar_theorems':10,
        'quadratic_unique_targets':83,'unresolved_targets':8,'recorded_commands':14,'unsuccessful_recorded_commands':4,
        'additional_launch_failures':1,'retained_packaging_failures':1,'limited_conic_trials':2,'almost_solved_conic_trials':1,
        'research_branches':116,'ledger_events':369,'preserved_event_prefix':366,'ledger_head_sha256':last,'local_links':links},indent=2))


if __name__=='__main__':main()
