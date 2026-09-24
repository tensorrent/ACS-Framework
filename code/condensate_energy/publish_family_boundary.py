#!/usr/bin/env python3
"""Publish the family/alignment witnesses and verify their evidence chain."""
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
OUT=ROOT/'docs/condensate_energy/family_boundary'


def render_family_boundary():
    data=json.loads((OUT/'results.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(11.8,5),layout='constrained')
    theta=np.linspace(0,np.pi/2,450)
    colors=['#286785','#b56745','#487d63']
    for row,col in zip(data['neutral_vacua'],colors):
        beta=row['beta'];A=row['quadratic_coefficients'][1]*.3**2/2;B=-.02*.3**2/2
        potential=A*np.sin(2*theta)+B*np.cos(2*theta)
        minimum=A*np.sin(2*beta)+B*np.cos(2*beta)
        axes[0].plot(np.rad2deg(theta),(potential-minimum)/(.3**2),color=col,
                     label='κ₂/κ₁ = '+format(row['tan_beta'],'.3f'),lw=2)
        axes[0].scatter([np.rad2deg(beta)],[0],color=col,s=30,zorder=5)
    axes[0].set(title='Quadratic inputs move the angular minimum',xlabel='Neutral angle β (degrees)',
                ylabel='[V(β) − V(β₀)] / (v² d²)',xticks=[0,15,30,45,60,75,90])
    axes[0].legend(frameon=False,fontsize=9)
    ratios=[r['tan_beta'] for r in data['neutral_vacua']]
    masses=[r['minimum_physical_mass_squared'] for r in data['neutral_vacua']]
    axes[1].bar([format(x,'.3f') for x in ratios],masses,color=colors,width=.6)
    for i,m in enumerate(masses):axes[1].text(i,m+.001,'56 / 56 positive',ha='center',fontsize=9)
    axes[1].set(title='All three are strict local minima',xlabel='Chosen neutral VEV ratio κ₂/κ₁',
                ylabel='Smallest physical scalar mass² (d² units)',ylim=(0,.049))
    for ax in axes:
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.suptitle('ACS complete-action witnesses: alignment is not selected by symmetry alone',fontsize=14)
    fig.supxlabel('Same quartics and kinetic action, different quadratic boundary coefficients. All 68 scalar coordinates are retained.\n'
                  'These are chosen, bounded witness actions—not physical fits or proofs of global minima. Source: family_boundary/results.json, 24 September 2026.',fontsize=8.2)
    for ext in ['png','svg']:fig.savefig(OUT/('family-alignment.'+ext),dpi=180)
    plt.close(fig)
    print('Rendered family-alignment.png and .svg')


def seal_family_boundary():
    results=[json.loads((OUT/n).read_text()) for n in ['results.json','verification.json']]
    assert all(x['checks_total']==x['checks_passed'] for x in results)
    assert all(c['passed'] for x in results for c in x['checks'])
    total=sum(x['checks_total'] for x in results)
    last=ROOT/'docs/condensate_energy/selection_energy/receipt.json'
    prior=dict(json.loads(last.read_text())['prior_receipts_verified'])
    prior[str(last.relative_to(ROOT))]=sha256(last.read_bytes()).hexdigest()
    prior_artifacts={}
    for path,h in prior.items():
        p=ROOT/path;assert sha256(p.read_bytes()).hexdigest()==h,path
        for artifact,digest in json.loads(p.read_text())['artifact_sha256'].items():
            assert sha256((ROOT/artifact).read_bytes()).hexdigest()==digest,artifact
            prior_artifacts[artifact]=digest
    for row in json.loads((OUT/'provenance.json').read_text()):
        assert sha256((ROOT/row['snapshot']).read_bytes()).hexdigest()==row['sha256']
    for name in ['acs-family-alignment-boundary.log','acs-verify-family-boundary.log']:
        (OUT/'attempts'/name).write_bytes((Path('/private/tmp')/name).read_bytes())
    review=json.loads((OUT/'visual-review.json').read_text())
    assert review['reviewed'] and review['legible']
    assessment=dict(status='Family and alignment stage complete; original ACS goal active',
        checks_passed=total,
        retained=['Exact cubic adjoint theorem','Equal-real-VEV mass obstruction',
                  'Complete-action conditional stable local vacua'],
        failed_inferences=['Cubic degree fixes physical family count',
            'Archived proportional CKM scan predicts nondegenerate mixing',
            'Inserted masses become a QFP prediction',
            'Isolated determinant-portal minimization classifies the complete scalar action'],
        underdetermined=['Family multiplicity and independent Yukawa matrices',
            'Quadratic/quartic boundary values and physical vacuum alignment'],
        remaining=['Source-inventory reconciliation','Original-scope completion audit including microscopic carrier identification'],
        limits=['No global-minimum proof or measured flavor fit','No arbitrary-coupling finite CW minimization'])
    (OUT/'assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    scripts=['family_alignment_boundary.py','verify_family_boundary.py','publish_family_boundary.py']
    artifacts=[ROOT/'code/condensate_energy'/p for p in scripts]
    artifacts.extend(p for p in OUT.rglob('*') if p.is_file() and p.name!='receipt.json' and '__pycache__' not in p.parts)
    receipt=dict(status=assessment['status'],checks_passed=total,prior_receipts_verified=prior,
        prior_artifacts_verified=prior_artifacts,
        artifact_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(checks_passed=total,artifacts=len(receipt['artifact_sha256']),
                         prior_receipts=len(prior),prior_artifacts=len(prior_artifacts))))


if __name__=='__main__':
    parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--render-only',action='store_true');mode.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    if args.render_only:render_family_boundary()
    else:seal_family_boundary()
