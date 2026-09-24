#!/usr/bin/env python3
"""Verify provenance, summarize autonomous experiments, and render audit plots."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from matplotlib.colors import LogNorm

from run import ROOT, plt

OUT=ROOT/'docs/condensate_energy/autonomous_gate'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def values(case,key):
    return np.array([r[key] for r in case['history']])


def symbolic_audit():
    a,g,k,intensity=sp.symbols('a g k I',positive=True)
    potential=(g*intensity*a*a+k*(a-1)**2)/2
    equilibrium=k/(k+g*intensity)
    effective=sp.simplify(potential.subs(a,equilibrium))
    checks=dict(equilibrium_force_vanishes=sp.simplify(sp.diff(potential,a).subs(a,equilibrium))==0,
                effective_potential=sp.simplify(effective-k*g*intensity/(2*(k+g*intensity)))==0,
                effective_field_coupling=sp.simplify(sp.diff(effective,intensity)-g*equilibrium**2/2)==0,
                strict_equilibrium_minimum=sp.diff(potential,a,2).is_positive is True)
    assert all(checks.values())
    result=dict(sympy=sp.__version__,checks=checks,equilibrium=str(equilibrium),effective_potential=str(effective))
    (OUT/'symbolic-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    data=json.loads((OUT/'results.json').read_text())
    refined=json.loads((OUT/'refinement-results.json').read_text())
    assert data['all_checks_passed'] and all(r['passed'] for r in data['checks'])
    assert refined['all_checks_passed'] and all(r['passed'] for r in refined['checks'])
    assert refined['parent_results_sha256']==digest(OUT/'results.json')
    for payload in [data,refined]:
        for name,sha in payload['source_sha256'].items():
            assert digest(ROOT/name)==sha,name
    for filename in [OUT.parent/'receipt.json',OUT.parent/'capture_stability/receipt.json']:
        prior=json.loads(filename.read_text())
        for name,sha in prior['artifact_sha256'].items():
            assert digest(ROOT/name)==sha,name
    symbolic=symbolic_audit()
    cases=data['cases']
    labels=['low','middle','high']
    notation=['pi/8','pi/4','pi/2']
    colors=['#237b9a','#bd6630','#7357aa']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'axes.titleweight':'bold','axes.grid':True,'grid.alpha':.17,
                         'figure.facecolor':'white','savefig.facecolor':'white'})
    fig,axes=plt.subplots(2,3,figsize=(13,8),layout='constrained')
    for row,g in enumerate([4,16]):
        for col,label in enumerate(labels):
            ax=axes[row,col]
            matrix=np.array([[100*cases[f'{label}-g{g}-M{m:g}-K{k:g}']['summary']['final']['trapped']
                              for m in [.1,1.,10.]] for k in [.1,1.,10.]])
            im=ax.imshow(np.maximum(matrix,1e-12),origin='lower',cmap='viridis',
                         norm=LogNorm(vmin=.001,vmax=10.),aspect='equal')
            for (y,x),v in np.ndenumerate(matrix):
                ax.text(x,y,f'{v:.2g}%',ha='center',va='center',
                        color='black' if v>1 else 'white',fontsize=10)
            ax.set(title=f'Carrier {notation[col]} | g = {g}',xticks=[0,1,2],yticks=[0,1,2],
                   xticklabels=['0.1','1','10'],yticklabels=['0.1','1','10'],
                   xlabel='Gate inertia M',ylabel='Restoring strength K')
            ax.grid(False)
    fig.colorbar(im,ax=axes.ravel().tolist(),shrink=.8,label='Trapped field energy / initial energy (%)',extend='min')
    fig.suptitle('All 54 coupled parameter cases: field retained at t = 160',fontsize=16)
    for ext in ['png','svg']:
        fig.savefig(OUT/f'parameter-sweep.{ext}',dpi=170)
    plt.close(fig)

    fig,axes=plt.subplots(2,2,figsize=(13,8.7),layout='constrained')
    ax=axes[0,0]
    for label,note,color in zip(labels,notation,colors):
        c=refined['cases'][f'long-refined-{label}']
        old=cases[f'selected-long-{label}']
        ax.semilogy(values(c,'t'),values(c,'trapped'),color=color,label=f'Carrier {note}')
        ax.semilogy(values(old,'t'),values(old,'trapped'),'--',color=color,alpha=.4)
    ax.set(title='A  Selected cases keep leaking',xlabel='Time (model units)',
           ylabel='Trapped field energy / initial energy',xlim=(20,480),ylim=(1e-5,1))
    ax.legend(fontsize=9)
    ax.text(.98,.96,'Solid: refined grid\nDashed: original grid',transform=ax.transAxes,
            ha='right',va='top',fontsize=8)
    ax=axes[0,1]
    for name,label,color in [('middle-g4-M1-K1','Autonomous gate','#237b9a'),
                            ('middle-fixed-g4','Fixed barrier, same initial height','#777777')]:
        c=cases[name]
        ax.plot(values(c,'t'),values(c,'trapped'),color=color,label=label)
    ax.set(title='B  Autonomous response improves finite-time residence',xlabel='Time (model units)',
           ylabel='Trapped field energy / initial energy',xlim=(0,160))
    ax.legend(fontsize=8)
    ax=axes[1,0]
    c=cases['middle-g4-M1-K1']
    ax.plot(values(c,'t'),values(c,'height'),color='#237b9a')
    ax.axhline(4,ls=':',color='gray',label='Initial height')
    ax.set(title='C  The wave changes the barrier',xlabel='Time (model units)',
           ylabel='Barrier height g a²',xlim=(0,80))
    ax.legend(fontsize=8)
    ax=axes[1,1]
    c=cases['middle-g4-M10-K0.1']
    ax.plot(values(c,'t'),values(c,'trapped'),color='#237b9a',label='Trapped field energy')
    ax.plot(values(c,'t'),values(c,'gate'),color='#bd6630',label='Mechanical gate energy')
    ax.plot(values(c,'t'),-values(c,'work_on_field'),'k--',lw=1,label='Negative integrated work on field')
    ax.set(title='D  Gate motion stores energy separately',xlabel='Time (model units)',
           ylabel='Energy / initial energy',xlim=(0,160))
    ax.legend(fontsize=8)
    fig.suptitle('Conservative field–gate exchange: added candidate model',fontsize=16)
    for ext in ['png','svg']:
        fig.savefig(OUT/f'autonomous-dynamics.{ext}',dpi=170)
    plt.close(fig)

    selected={}
    for label in labels:
        base=data['selected_by_field_retention'][label]
        selected[label]=dict(parameters=cases[base]['parameters'],
                             coarse_at160=cases[base]['summary']['final'],
                             refined_at160=cases[f'selected-refined-{label}']['summary']['final'],
                             fixed_same_g_at160=cases[f'{label}-fixed-g4']['summary']['final'],
                             coarse_at480=cases[f'selected-long-{label}']['summary'],
                             refined_at480=refined['cases'][f'long-refined-{label}']['summary'])
    assessment=dict(status='all_registered_and_targeted_numerical_checks_passed',
                     original_variants=len(cases),targeted_variants=len(refined['cases']),
                     additional_short_calibration_trajectories=3,
                     original_checks=len(data['checks']),targeted_checks=len(refined['checks']),
                     symbolic_checks=len(symbolic['checks']),source_and_parent_hashes_verified=True,
                     selected=selected,
                     conclusions=dict(
                         autonomous_field_gate_exchange='demonstrated for this candidate Hamiltonian',
                         finite_time_residence='can improve or worsen; all 54 parameter cases reported',
                         permanent_field_capture='not established; selected long trajectories continue leaking',
                         stationary_gate_localized_harmonic_field='analytically excluded for all positive g,M,K under stated half-line assumptions',
                         general_time_dependent_bound_solution='not settled by the stationary exclusion or finite simulations',
                         physical_gate_and_coupling='supplied model inputs; not derived from source foam',
                         particle_mass='not derived'))
    (OUT/'assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    sources=[Path(__file__).resolve(),ROOT/'code/condensate_energy/autonomous_gate.py',
             ROOT/'code/condensate_energy/autonomous_refinement.py']
    paths=sources+sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='receipt.json')
    receipt=dict(status=assessment['status'],original_variants=len(cases),targeted_variants=len(refined['cases']),
                  numerical_checks=len(data['checks'])+len(refined['checks']),symbolic_checks=len(symbolic['checks']),
                  artifact_sha256={str(p.relative_to(ROOT)):digest(p) for p in paths})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in assessment.items() if k!='selected'},indent=2))


if __name__=='__main__':
    main()
