#!/usr/bin/env python3
"""Render the complete scalar audit and seal its current evidence receipt."""
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR','/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from canonical_scalar_action import ROOT,OUT


def canonical_summary():
    result=json.loads((OUT/'qualified-results.json').read_text())
    exact=json.loads((OUT/'exact-witness.json').read_text())
    assert result['all_checks_passed'] and exact['all_checks_passed']
    for data in [result,exact]:
        for key in ['source_sha256','qualification_sha256']:
            for name,digest in data.get(key,{}).items():
                assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    prior={}
    for name in ['self_binding','charge_audit','charge_leakage','gauge_completion']:
        path=OUT.parent/name/'receipt.json'
        receipt=json.loads(path.read_text())
        for file,digest in receipt['artifact_sha256'].items():
            assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,file
        prior[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    fig,axes=plt.subplots(1,2,figsize=(12.2,5.6),layout='constrained')
    series=[('angular-positive',.2,'#246B8E'),('angular-zero',0.,'#7B8188'),('angular-negative',-.2,'#A44A3F')]
    t=np.linspace(-.58,.58,501)
    for name,k,color in series:
        row=result['cases'][name]
        spectrum=np.array(row['mass_squared'])
        spectrum[abs(spectrum)<row['zero_band']]=0.
        axes[0].plot(np.arange(1,57),spectrum,'o-',ms=3,lw=1,color=color,label=f'k={k:+g}: {row["positive"]} positive, {row["zero"]} flat, {row["negative"]} negative')
        potential=(1+k/3)*t**4+(5*k/3+4/5625)*t**2
        axes[1].plot(t,potential,color=color,label=f'k={k:+g}',lw=1.8)
    axes[0].set_yscale('symlog',linthresh=.01)
    axes[0].set_xlabel('Eigenvalue index (sorted within each action)')
    axes[0].set_ylabel('Canonical mass squared (chosen model units)')
    axes[0].set_title('A  Full physical scalar spectrum',loc='left',fontsize=12)
    axes[0].legend(frameon=False,fontsize=8,loc='upper left')
    axes[1].set_xlabel('t = Re(D3_00), a charged field amplitude (model units)')
    axes[1].set_ylabel('V(t) - V(0) (potential-density model units)')
    axes[1].set_title('B  Exact transverse instability at the same vacuum',loc='left',fontsize=12)
    axes[1].legend(frameon=False,fontsize=9)
    for ax in axes:
        ax.axhline(0.,color='.3',ls='--',lw=.8)
        ax.grid(alpha=.16)
    fig.suptitle('Identical neutral potential and masses; different full-field stability',fontsize=14)
    fig.supxlabel('Source: exact inherited 17-quartic action and 68-coordinate Hessian, 2026-09-24. VEV inputs a=1/3, b=1/5, d=1.\nTwelve gauge directions removed; 56 real physical modes. Only neutral-invisible quartics change. No physical ACS coefficient selection is asserted.',fontsize=9)
    fig.savefig(OUT/'canonical-evidence.png',dpi=175)
    fig.savefig(OUT/'canonical-evidence.svg')
    plt.close(fig)
    assessment=dict(status='complete canonical scalar calculator and qualified counterexample; ACS coefficient selection remains open',
        checks_passed=len(result['checks'])+len(exact['checks']),
        fields_real=68,quartics=17,quadratics=4,neutral_quartic_rank=11,
        neutral_invisible_quartics=6,physical_modes=56,gauge_directions=12,
        witness_spectra={name:{k:row[k] for k in ['positive','negative','zero','minimum_mass_squared','tadpole_infinity_norm','phase_derivative']} for name,row in result['cases'].items()},
        exact_transverse_mass=exact['mass_squared'],
        neutral_mass_squared=result['cases']['angular-positive']['sectors'][0]['mass_squared'],
        original_verification_failure=result['original_failure'],
        scope='Chosen bounded witness potentials; not a physical spectrum prediction, global minimum theorem or quantum stability proof.',
        prior_receipts_verified=prior)
    (OUT/'assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    paths=[p for p in OUT.rglob('*') if p.is_file() and p.name!='receipt.json']
    paths += [ROOT/'code/condensate_energy'/f'{name}.py' for name in ['canonical_scalar_action','canonical_vacuum_audit','canonical_vacuum_qualify','canonical_exact_witness','summarize_canonical_vacuum']]
    receipt=dict(status=assessment['status'],checks_passed=assessment['checks_passed'],
        prior_receipts_verified=prior,
        artifact_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(checks_passed=assessment['checks_passed'],artifacts=len(receipt['artifact_sha256']),prior_receipts_verified=len(prior)),indent=2))


if __name__=='__main__':
    canonical_summary()
