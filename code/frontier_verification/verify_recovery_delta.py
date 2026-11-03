"""Check retained recovery evidence; no fresh root certification or quadrature."""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from flint import acb,arb,ctx
from dedekind_recovery_audit import powers,ordered_models

CODE=Path(__file__).absolute().parent
ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-recovery-delta'
PRIOR=ROOT/'docs/frontier/2026-09-13-explicit-delta'
ADVANCED=['P05','R12','R13','K04']


def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def decode(x):return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def complex_decode(x):return acb(decode(x['real']),decode(x['imag']))


def folded(contour):
    assert decode(contour['euler_disk_radius'])<1
    total=decode(contour['right_argument_change'])+decode(contour['left_argument_change'])
    for p in contour['horizontal_pieces']:
        a=tuple(map(F,p['a']));b=tuple(map(F,p['b']));last=a;change=arb(0)
        for s in p['segments']:
            lo,hi=tuple(map(F,s['a'])),tuple(map(F,s['b']))
            assert lo==last and lo[1]==hi[1]==a[1] and (hi[0]-lo[0])*(b[0]-a[0])>0
            assert not complex_decode(s['image']).contains(0)
            ratio=complex_decode(s['ratio']);assert ratio.real>0
            assert ratio.arg().overlaps(decode(s['angle']))
            change+=decode(s['angle']);last=hi
        assert last==b and change.overlaps(decode(p['L_argument_change']))
        assert (change+decode(p['gamma_argument_change'])).overlaps(decode(p['completed_argument_change']))
        total+=decode(p['completed_argument_change'])
    winding=total/(2*arb.pi())
    assert winding.overlaps(decode(contour['winding']))
    assert int(winding.unique_fmpz())==contour['zero_count']


def main():
    ctx.prec=256
    prior=subprocess.run([sys.executable,str(CODE/'verify_explicit_delta.py')],capture_output=True,text=True)
    assert prior.returncode==0,prior.stdout+prior.stderr
    manifest=read(OUT/'Manifest.json')
    for path,v in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==v['bytes'] and sha(raw)==v['sha256'],path
    inventory=read(OUT/'Source_Inventory.json');source_hashes=set()
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():
                assert sha(z.read(kind+'/'+path))==digest==sha((ROOT/path).read_bytes())
        source_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.py')}
    with zipfile.ZipFile(OUT/'Certificates.zip') as z:
        certificates={name:json.loads(z.read(name)) for name in z.namelist()}
    with zipfile.ZipFile(OUT/'Replays.zip') as z:
        replays={name:json.loads(z.read(name)) for name in z.namelist()}
    counts=[]
    for c,expected in [(2,2028),(3,2029),(4,2028)]:
        data=certificates[f'character-{c}.json'];replay=replays[f'replay-{c}.json']
        assert data['status']==replay['status']=='passed'
        assert data['source_sha256']==sha((CODE/'dirichlet_extended_certificate.py').read_bytes())
        for name,digest in data['dependencies_sha256'].items():assert digest==sha((CODE/name).read_bytes())
        for contour in [data['contour'],replay['contour']]:folded(contour)
        assert data['contour']['zero_count']==replay['contour']['zero_count']==len(data['root_intervals'])==expected
        assert len(replay['root_endpoint_checks'])==expected and len(replay['independent_roots'])==7
        for row,check in zip(data['root_intervals'],replay['root_endpoint_checks']):
            assert row['index']==check['index'] and check['opposite_signs']
            for prefix in ['lo','hi']:
                value=arb(check[prefix+'_Z']);sign=1 if value>0 else -1 if value<0 else 0
                assert sign==row[prefix+'_sign']!=0
            assert row['lo_sign']*row['hi_sign']==-1 and F(row['hi'])-F(row['lo'])<=F(2,10**30)
        for row in replay['independent_roots']:
            bracket=data['root_intervals'][row['index']-1]
            assert F(bracket['lo'])<F(row['mpmath_ordinate'])<F(bracket['hi']) and F(row['L_residual'])<F('1e-50')
        counts.append(expected)
    zeta=certificates['riemann-160.json'];zr=replays['riemann-224.json']
    assert zeta['count']==zr['count']==len(zeta['root_intervals'])==1517
    assert len(zr['root_intervals'])==1517 and len(zr['independent_checks'])==3
    for a,b in zip(zeta['root_intervals'],zr['root_intervals']):
        assert arb(a['lo']).union(arb(a['hi'])).overlaps(arb(b['lo']).union(arb(b['hi'])))
    with zipfile.ZipFile(OUT/'Recovery_Audits.zip') as z:
        raw_input=z.read('Recovery_Inputs.json');input_data=json.loads(raw_input)
        audit_raw={bits:z.read(f'Recovery_{bits}.json') for bits in [160,224]}
    audits={bits:json.loads(raw) for bits,raw in audit_raw.items()}
    rows=input_data['positive_root_intervals'];assert len(rows)==sum(counts)+1517==7602
    assert sum(r['count'] for r in input_data['prefix_checks'])==528
    assert all(F(a['hi'])<F(b['lo']) for a,b in zip(rows,rows[1:]))
    roots=[(F(r['hi']),arb(r['lo']).union(arb(r['hi']))) for r in rows]
    C=arb(3)/2+arb(125).log()/2-2*(2*arb.pi()).log()+2*arb(2).digamma()
    for bits,data in audits.items():
        assert data['status']=='passed' and data['source_sha256']==sha((CODE/'dedekind_coefficient_recovery.py').read_bytes())
        assert data['input_sha256']==sha(raw_input) and data['target_count']==91
        assert data['generic_prime_power_count']==len(powers(4096))==604
        evals={(e['n'],e['denominator']):e for e in data['evaluations']}
        for T in data['heights']:
            known=sum((3/(arb('9/4')+r*r) for hi,r in roots if hi<T),arb(0))
            assert known.overlaps(arb(data['moments'][str(T)]['known']))
            assert (C-known).overlaps(arb(data['moments'][str(T)]['unknown_upper']))
        for e in evals.values():
            a,u=arb(1)/e['denominator'],arb(e['n']).log()
            g0=(-u*u/(4*a)).exp()/(2*(arb.pi()*a).sqrt())
            assert (2*(a/4).exp()*(u/2).cosh()).overlaps(arb(e['pole']))
            assert (arb(125).log()*g0).overlaps(arb(e['discriminant']))
            gamma=e['gamma'];integral=arb(0);last=F('1e-20')
            for s in gamma['segments']:
                assert F(s['lo'])==last<F(s['hi']) and arb(s['imag']).contains(0)
                last=F(s['hi']);integral+=arb(s['real'])
            assert last==180
            constant=-4*(arb.const_euler()+(8*arb.pi()).log())*g0
            lower=3/(4*a*(arb.pi()*a).sqrt())*arb('1e-40')
            upper=8*(g0+1/(2*(arb.pi()*a).sqrt()))*arb(-90).exp()/(1-arb(-180).exp())
            assert constant.overlaps(arb(gamma['constant'])) and lower.overlaps(arb(gamma['lower_tail'])) and upper.overlaps(arb(gamma['upper_tail']))
            assert (constant+4*integral+arb(0,(lower+upper).upper())).overlaps(arb(gamma['enclosure']))
        for row in data['cases']:
            m,p,T=row['n'],row['prime'],row['height'];a=arb(1)/row['denominator'];u=arb(m).log()
            e=evals[m,row['denominator']];scale=2*(arb.pi()*a*m).sqrt()/arb(p).log()
            assert scale.overlaps(arb(row['scale']))
            assert len(row['all_width_budgets'])==27
            budget=row['selected_budget'];assert budget in row['all_width_budgets']
            U=arb(data['moments'][str(T)]['unknown_upper'])
            phi=(4+T*T)*(-a*T*T).exp() if a*(4+T*T)>=1 else (4*a-1).exp()/a
            E=scale*U*phi*(a/4).exp()*(u/2).cosh()
            assert E.overlaps(arb(budget['scaled_zero_tail']))
            R0=scale*(arb(e['pole'])+arb(e['discriminant'])+arb(e['gamma']['enclosure'])-arb(e['finite_sums'][str(T)]))
            assert R0.overlaps(arb(row['unwidened_estimate']))
            assert (R0+arb(0,E.upper())).overlaps(arb(row['estimate']))
            D=1+(-u*u/a).exp();assert D.overlaps(arb(row['diagonal_multiplier']))
            # Arb's human-readable string rounds a broad ball outward, and
            # can retain extra candidates. Reconstruct the tighter enclosure
            # from the recorded component terms and explicit error allowance.
            L=arb(budget['leakage_upper']);R=R0+arb(0,E.upper())
            candidates=[c for c in range(5) if R.overlaps(c*D+arb(L/2,L.upper()/2))]
            assert candidates==row['candidates']
        for T,v in data['inferences_by_height'].items():
            assert v['direct_unique']==sum(len(r['candidates'])==1 for r in data['cases'] if str(r['height'])==T)
            assert v['local_unique']==sum(len(r['candidates'])==1 for p in v['models'] for r in p['powers'])
    assert [(v['direct_unique'],v['local_unique']) for v in audits[160]['inferences_by_height'].values()]==[(46,56),(69,75),(79,84),(86,90),(89,91)]
    cross=read(OUT/'Cross_Method.json');assert cross['status']=='passed'
    assert cross['inputs_sha256']=={'zero_input':sha(raw_input),'160':sha(audit_raw[160]),'224':sha(audit_raw[224])}
    assert len(cross['holdout_comparisons'])==455 and len(cross['independent_final_targets'])==91
    hcases={r['n']:r for r in audits[224]['cases']}
    hevals={(r['n'],r['denominator']):r for r in audits[224]['evaluations']}
    for r in cross['independent_final_targets']:
        case=hcases[r['n']];e=hevals[r['n'],r['denominator']]
        for a,b in [(e['finite_sums']['2000'],r['zero_sum']),(e['gamma']['enclosure'],r['gamma']),
                    (case['selected_budget']['finite_leakage'],r['finite_leakage']),
                    (case['unwidened_estimate'],r['unwidened_estimate'])]:assert arb(a).contains(arb(b))
    for r in cross['holdout_comparisons']:assert r['expected'] in r['candidates'] and r['retained']
    mutation_counts={name:0 for name in cross['mutation_exclusion_counts']}
    for r in cross['mutations']:
        for name,v in r['variants'].items():
            assert v['true_coefficient_excluded']==(r['expected'] not in v['candidates'])
            mutation_counts[name]+=v['true_coefficient_excluded']
    assert mutation_counts==cross['mutation_exclusion_counts'] and sum(mutation_counts.values())==1647
    local=read(OUT/'Local_Identifiability.json')
    assert local['recovery_sha256']==sha(audit_raw[160]) and local['unresolved_count']==48
    assert local['range_of_next_powers']==[529,128881]
    for r in local['unresolved_local_factors']:
        assert r['first_distinguishing_exponent']==2 and r['next_prime_power']==r['prime']**2>361
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==23 and sum(r['returncode']==0 for r in receipts.values())==18
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
            assert set(r['input_sources_sha256'].values())<=source_hashes
    ledger=(OUT/'Branch_Events.jsonl').read_bytes();old=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines())==350
    previous='0'*64
    for i,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256')
        assert event['sequence']==i and event['previous_event_sha256']==previous
        assert sha(json.dumps(event,sort_keys=True,separators=(',',':')).encode())==digest
        previous=digest
    assert i==355
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert len(after)==len(queue['branches'])==116 and set(after)-set(before)=={'R14'}
    assert queue['global_exhaustion_claimed'] is False and queue['new_branches']==['R14']
    for bid,b in after.items():
        if bid in before:
            old_b=before[bid]
            assert b['prior_delta_evidence']==old_b.get('prior_delta_evidence',[])+old_b['new_evidence']
            if bid not in ADVANCED:
                assert b['latest_scoped_result']==old_b['latest_scoped_result'] and b['continuation_condition']==old_b['continuation_condition']
                assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for p in b['new_evidence']:assert (ROOT/p).exists()
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'RECOVERY_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link)
                links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Retained identities and recombination of reported enclosures; no fresh quadrature or root certification.',
        'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
        'positive_roots':7602,'preserved_prefix_roots':528,'recovery_cases_160':455,'recovery_cases_224':91,
        'direct_final_coefficients':89,'local_final_coefficients':91,'independent_final_targets':91,
        'mutation_cases':3185,'mutation_exclusions':1647,'unresolved_local_factors':48,
        'receipts':23,'research_branches':116,'ledger_events':355,'preserved_event_prefix':350,
        'ledger_head_sha256':previous,'local_links':links},indent=2))


if __name__=='__main__':main()
