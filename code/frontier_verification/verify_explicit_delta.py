"""Verify retained Gaussian explicit-formula evidence and prior checkpoint history.

This recombines reported interval quantities and checks identities. It does not
rerun root certification, quadrature, or the analytic proof of the formula.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from flint import arb, ctx
from dedekind_inputs import load_factors, at_height
from dedekind_explicit_crosscheck import independent_powers

CODE=Path(__file__).absolute().parent
ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-explicit-delta'
PRIOR=ROOT/'docs/frontier/2026-09-13-dedekind-delta'
ADVANCED=['P05','R12','R13','K04']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    ctx.prec=256
    previous=subprocess.run([sys.executable,str(CODE/'verify_dedekind_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for p,item in manifest['files'].items():
        raw=(ROOT/p).read_bytes()
        assert len(raw)==item['bytes'] and sha(raw)==item['sha256'],p
    sources=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        for kind in ['instruments','dependencies']:
            for p,digest in sources[kind].items():
                assert sha(z.read(kind+'/'+p))==digest==sha((ROOT/p).read_bytes())
    factors,identity=load_factors(PRIOR/'Factor_Certificates.zip',ROOT/'docs/frontier/2026-09-13-lfunction-delta/Certificates.zip')
    powers=independent_powers(100000)
    assert len(powers)==2436
    audits={}
    with zipfile.ZipFile(OUT/'Gaussian_Audits.zip') as z:
        for bits in [160,224]:
            raw=z.read(f'Gaussian_{bits}.json')
            data=json.loads(raw)
            assert data['status']=='passed' and data['precision_bits']==bits
            assert data['source_sha256']==sha((CODE/'dedekind_explicit_formula.py').read_bytes())
            assert data['input_identity']==identity and len(data['configurations'])==30
            audits[bits]=(raw,data)
    max_radius=arb(0)
    config_keys=set()
    for bits,(_,data) in audits.items():
        m=data['moment_bounds']
        constant=arb(3)/2+arb(125).log()/2-2*(2*arb.pi()).log()+2*arb(2).digamma()
        assert constant.overlaps(arb(m['constant_upper']))
        prime_moment=sum((coeff*arb(p).log()/(n*n) for n,p,k,coeff in powers),arb(0))
        assert prime_moment.overlaps(arb(m['prime_partial_at_2']))
        for c in data['configurations']:
            a,u=arb(c['a']),arb(c['frequency'])
            key=(c['a'],c['frequency_label'])
            config_keys.add(key)
            expected_u=arb(c['frequency_rational']) if c['frequency_rational'] else arb(c['frequency_log_integer']).log()
            assert u.overlaps(expected_u)
            assert 0<a and 0<=u
            g0=(-u*u/(4*a)).exp()/(2*(arb.pi()*a).sqrt())
            assert (arb(125).log()*g0).overlaps(arb(c['conductor']))
            assert (2*(a/4).exp()*(u/2).cosh()).overlaps(arb(c['pole']))
            rows=c['prime_terms']
            assert [(r['n'],r['prime'],r['power'],r['coefficient_divided_by_log_prime']) for r in rows]==powers
            assert all(arb(r['contribution'])>=0 for r in rows)
            for X in [1000,10000,100000]:
                q=c['prime_cutoffs'][str(X)]
                partial=sum((arb(r['contribution']) for r in rows if r['n']<=X),arb(0))
                assert partial.overlaps(arb(q['partial']))
                y=arb(X).log()-u-a
                assert y>0 and arb(X).log()>2
                tail=8*(a/arb.pi()).sqrt()*(u/2+a/4-y*y/(4*a)).exp()*(1+(u+a)/y)
                assert tail.overlaps(arb(q['tail_bound']))
                assert (partial+arb(0,tail.upper())).overlaps(arb(q['enclosure']))
            gamma=c['gamma']
            last=F('1e-20')
            total=arb(0)
            for segment in gamma['segments']:
                assert F(segment['lo'])==last and F(segment['hi'])>last
                assert arb(segment['integral_imag']).contains(0)
                total+=arb(segment['integral_real'])
                last=F(segment['hi'])
            assert last==180
            gamma_constant=-4*(arb.const_euler()+(8*arb.pi()).log())*g0
            assert gamma_constant.overlaps(arb(gamma['constant']))
            assert (gamma_constant+4*total).overlaps(arb(gamma['finite_value']))
            lower=3/(4*a*(arb.pi()*a).sqrt())*arb('1e-40')
            upper=8*(g0+1/(2*(arb.pi()*a).sqrt()))*arb(-90).exp()/(1-arb(-180).exp())
            assert lower.overlaps(arb(gamma['lower_tail_bound'])) and upper.overlaps(arb(gamma['upper_tail_bound']))
            arithmetic=arb(c['pole'])+arb(c['conductor'])+arb(gamma['enclosure'])-arb(c['prime_cutoffs']['100000']['enclosure'])
            assert arithmetic.overlaps(arb(c['arithmetic_enclosure']))
            for top in [60,100,220]:
                z=c['zero_cutoffs'][str(top)]
                selected=at_height(factors,top)
                assert z['counts']=={k:len(v) for k,v in selected.items()}
                finite=sum((arb(v) for v in z['factor_sums'].values()),arb(0))
                assert finite.overlaps(arb(z['finite_sum']))
                known=sum((3/(arb('9/4')+(arb(r['lo']).union(arb(r['hi'])))**2)
                           for values in selected.values() for r in values),arb(0))
                assert known.overlaps(arb(m['cutoffs'][str(top)]['known_zero_moment']))
                U=constant-prime_moment-known
                assert U>0 and U.overlaps(arb(m['cutoffs'][str(top)]['unknown_zero_moment_upper']))
                assert a*(4+top*top)>=1
                tail=U*(4+top*top)*(-a*top*top+a/4).exp()*(u/2).cosh()
                assert tail.overlaps(arb(z['tail_bound']))
                expected=finite+arb(0,tail.upper())-arithmetic
                assert expected.contains(0) and arb(z['residual']).contains(0)
                assert expected.overlaps(arb(z['residual']))
                if top==220:
                    radius=arb(z['residual']).abs_upper()
                    assert radius<arb('7e-24')
                    max_radius=max_radius.union(radius)
    assert len(config_keys)==30
    a160={ (c['a'],c['frequency_label']):c for c in audits[160][1]['configurations']}
    a224={ (c['a'],c['frequency_label']):c for c in audits[224][1]['configurations']}
    for k in config_keys:
        assert arb(a160[k]['arithmetic_enclosure']).overlaps(arb(a224[k]['arithmetic_enclosure']))
        assert a160[k]['gamma']['segments']!=a224[k]['gamma']['segments']
    cross=read(OUT/'Cross_Method.json')
    assert cross['status']=='passed' and cross['producer_result_sha256']==sha(audits[224][0])
    assert cross['source_sha256']==sha((CODE/'dedekind_explicit_crosscheck.py').read_bytes())
    assert len(cross['independent_configurations'])==30 and len(cross['digamma_routes'])==9
    for row in cross['independent_configurations']:
        c=a224[row['a'],row['frequency_label']]
        for expected,actual in [(c['zero_cutoffs']['220']['finite_sum'],row['zero_sum']),
                                (c['prime_cutoffs']['100000']['partial'],row['prime_sum']),
                                (c['gamma']['enclosure'],row['gamma']),(c['arithmetic_enclosure'],row['arithmetic'])]:
            assert arb(expected).contains(arb(actual))
    for row in cross['digamma_routes']:
        c=a224[row['a'],row['frequency_label']]
        assert arb(row['enclosure']).overlaps(arb(c['gamma']['enclosure']))
        assert (arb(row['digamma_integral'])+arb(row['gamma_normalization'])).overlaps(arb(row['finite_value']))
    counts={name:0 for name in cross['mutation_rejection_counts']}
    assert len(counts)==10 and len(cross['mutation_results'])==30
    for row in cross['mutation_results']:
        for name,value in row['variants'].items():
            assert value['rejected']==(not arb(value['residual']).contains(0))
            counts[name]+=value['rejected']
    assert counts==cross['mutation_rejection_counts'] and all(n>0 for n in counts.values())
    algebra=read(OUT/'Algebra_Audit.json')
    assert algebra['status']=='passed' and algebra['discriminant']==125
    assert algebra['source_sha256']==sha((CODE/'dedekind_explicit_algebra.py').read_bytes())
    assert len(algebra['symbolic_identities'])==6 and len(algebra['gamma_duplication_controls'])==6
    receipts=read(OUT/'Execution_Receipts.json')
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:
                assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
    assert len(receipts)==9 and sum(r['returncode']==0 for r in receipts.values())==5
    assert receipts['cross-method-tail-aware']['returncode']==0 and receipts['cross-method']['returncode']!=0
    ledger=(OUT/'Branch_Events.jsonl').read_bytes()
    old=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines())==346
    previous='0'*64
    for i,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line)
        digest=event.pop('event_sha256')
        assert event['sequence']==i and event['previous_event_sha256']==previous
        assert sha(json.dumps(event,sort_keys=True,separators=(',',':')).encode())==digest
        previous=digest
    assert i==350
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json')
    after={b['id']:b for b in queue['branches']}
    assert len(after)==len(queue['branches'])==115 and set(after)==set(before)
    assert queue['global_exhaustion_claimed'] is False and queue['new_branches']==[]
    for bid,b in after.items():
        old_b=before[bid]
        assert b['prior_delta_evidence']==old_b.get('prior_delta_evidence',[])+old_b['new_evidence']
        if bid not in ADVANCED:
            assert b['latest_scoped_result']==old_b['latest_scoped_result']
            assert b['continuation_condition']==old_b['continuation_condition']
            assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for evidence in b['new_evidence']:
            assert (ROOT/evidence).exists()
    links=0
    for p in [OUT/'README.md',OUT.parent/'README.md',CODE/'EXPLICIT_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (p.parent/link.split('#')[0]).exists(),(p,link)
                links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Retained identity and reported-computation consistency; quadrature, roots and analytic proofs are not rerun.',
        'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
        'configurations_per_precision':30,'precisions_bits':[160,224],
        'zero_cutoffs_per_configuration':3,'prime_cutoffs_per_configuration':3,
        'eligible_prime_powers':2436,'independent_configurations':30,'alternate_gamma_integrals':9,
        'distinct_mutations':10,'mutation_cases':300,'rejected_mutation_cases':sum(counts.values()),
        'all_final_residuals_below':'7e-24','receipts':len(receipts),'research_branches':115,
        'ledger_events':350,'preserved_event_prefix':346,'ledger_head_sha256':previous,'local_links':links},indent=2))


if __name__=='__main__':
    main()
