#!/usr/bin/env python3
"""Publish the remaining source tests with bounded coverage and chained receipts."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/source_endpoint'


def render_source_endpoint():
    data=json.loads((OUT/'running.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    theta=np.linspace(0,np.pi/2,400)
    axes[0].plot(np.degrees(theta),np.sqrt(2)*np.cos(theta),color='#276786',lw=2)
    axes[0].axhline(1/3,color='#a45a37',ls='--',label='Proposed fixed value: 1/3')
    axes[0].set(title='A normalized projection ratio is still free',xlabel='Generator direction θ (degrees)',
                ylabel='Absolute ratio of lepton components',xlim=(0,90),ylim=(0,1.5),xticks=[0,15,30,45,60,75,90])
    axes[0].legend(frameon=False,fontsize=9)
    rows=data['trajectories'];scales=[r['scale_GeV'] for r in rows];initial=data['initial']['theta_degrees']
    for field,label,color in [('historical_angle','Original equations; exact angle','#9c7854'),
                              ('corrected_angle','Corrected equations; exact angle','#276786')]:
        axes[1].semilogx(scales,[1e3*(r[field]-initial) for r in rows],color=color,lw=2,label=label)
    axes[1].set(title='Only a tiny differential running effect',xlabel='Assumed running scale μ (GeV)',
                ylabel='Upward angle change (millidegrees)')
    axes[1].legend(frameon=False,fontsize=8.5,loc='lower left')
    for ax in axes:
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.17)
    fig.suptitle('Source endpoint: geometry and running do not supply a flavor selector',fontsize=14)
    fig.supxlabel('Left: exact unit-Frobenius counterfamily. Right: historical mixed-scheme inputs, top-only quark Yukawa truncation, no thresholds.\n'
                  'Separate candidate run downward: +0.000223° against a 1.168° gap (0.0191%). These are conditional diagnostics, not precision fits.',fontsize=8.5)
    for ext in ['png','svg']:fig.savefig(OUT/('source-endpoint.'+ext),dpi=180)
    plt.close(fig)
    print('Rendered source-endpoint.png and .svg')


def seal_source_endpoint():
    datasets=[json.loads((OUT/n).read_text()) for n in ['algebra.json','running.json']]
    assert all(d['checks_total']==d['checks_passed'] and all(c['passed'] for c in d['checks']) for d in datasets)
    provenance=json.loads((OUT/'provenance.json').read_text())
    additional={r['source']:r for r in provenance}
    for r in provenance:
        assert sha256((ROOT/r['snapshot']).read_bytes()).hexdigest()==r['sha256']
        assert sha256(Path(r['source']).read_bytes()).hexdigest()==r['sha256']
    previous=json.loads((ROOT/'docs/condensate_energy/source-reconciliation-20260924.json').read_text())
    rows=[]
    for r in previous['rows']:
        q=dict(r)
        if q['source'] in additional:
            new=additional[q['source']]
            assert q['sha256']==new['sha256']
            q['snapshots']=[new['snapshot']]
        assert q['snapshots'],q['source']
        for p in q['snapshots']:assert sha256((ROOT/p).read_bytes()).hexdigest()==q['sha256']
        q['evidence_reports']=sorted({str(Path(p).parents[1]/'README.md') for p in q['snapshots']})
        assert all((ROOT/p).is_file() for p in q['evidence_reports'])
        q['status']='Preserved source matched to scoped scientific audit; not every printed assertion is validated'
        rows.append(q)
    inventory=dict(status='Targeted 36-entry source inventory reconciled; broader coverage remains qualified',
        inventory_count=len(rows),snapshot_matches=len(rows),pending_count=0,rows=rows,
        exclusions=previous['qualifications'],original_goal_complete=False)
    (OUT/'inventory-reconciliation.json').write_text(json.dumps(inventory,indent=2)+'\n')
    last=ROOT/'docs/condensate_energy/family_boundary/receipt.json'
    prior=dict(json.loads(last.read_text())['prior_receipts_verified'])
    prior[str(last.relative_to(ROOT))]=sha256(last.read_bytes()).hexdigest()
    prior_artifacts={}
    for path,h in prior.items():
        p=ROOT/path;assert sha256(p.read_bytes()).hexdigest()==h,path
        for artifact,digest in json.loads(p.read_text())['artifact_sha256'].items():
            assert sha256((ROOT/artifact).read_bytes()).hexdigest()==digest,artifact
            prior_artifacts[artifact]=digest
    for name in ['acs-source-endpoint-algebra.log','acs-source-endpoint-running.log']:
        (OUT/'attempts'/name).write_bytes((Path('/private/tmp')/name).read_bytes())
    review=json.loads((OUT/'visual-review.json').read_text())
    assert review['reviewed'] and review['legible']
    assert review['png_sha256']==sha256((OUT/'source-endpoint.png').read_bytes()).hexdigest()
    assessment=dict(status='Source endpoint stage complete; original ACS goal active',
        checks_passed=sum(d['checks_passed'] for d in datasets),
        source_entries_reconciled=12,targeted_inventory_reconciled=36,
        full_replays=10,executable_duplicates=2,
        retained=['Matrix norm and bracket-parity identities','Koide common-scale invariance',
                  'Conditional flavor-differential one-loop running'],
        failed=['Fixed normalized neutrino suppression','Displayed neutrino unit conversions',
                'Running closes the historical angle gap','Unnormalized proxy selects Higgs scale'],
        remaining=['Integrated original-scope action-to-carrier completion audit',
                   'Broader relevant source coverage reconciliation'],
        limits=datasets[1]['limitations'])
    (OUT/'assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    scripts=['source_endpoint_algebra.py','source_endpoint_running.py','publish_source_endpoint.py']
    artifacts=[ROOT/'code/condensate_energy'/p for p in scripts]
    artifacts.extend(p for p in OUT.rglob('*') if p.is_file() and p.name!='receipt.json' and '__pycache__' not in p.parts)
    receipt=dict(status=assessment['status'],checks_passed=assessment['checks_passed'],prior_receipts_verified=prior,
        prior_artifacts_verified=prior_artifacts,
        artifact_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(checks_passed=assessment['checks_passed'],artifacts=len(receipt['artifact_sha256']),
                         prior_receipts=len(prior),prior_artifacts=len(prior_artifacts))))


if __name__=='__main__':
    parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--render-only',action='store_true');mode.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    if args.render_only:render_source_endpoint()
    else:seal_source_endpoint()
