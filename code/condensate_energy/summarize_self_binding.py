#!/usr/bin/env python3
"""Render qualified binding evidence without promoting an ACS identification."""
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR','/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from self_binding import ROOT,OUT


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def series(row,key):
    return np.array([v[key] for v in row['history']])


def main():
    stationary=json.loads((OUT/'results.json').read_text())
    dynamics=json.loads((OUT/'dynamic-results.json').read_text())
    formation=json.loads((OUT/'formation-results.json').read_text())
    contract=json.loads((OUT/'source-contract.json').read_text())
    for data in [stationary,dynamics,formation]:
        assert data['all_checks_passed'] and all(v['passed'] for v in data['checks'])
    assert all(contract['checks'].values())
    assert dynamics['stationary_sha256']==digest(OUT/'results.json')
    for data in [stationary,dynamics,formation,contract]:
        for label in ['source_sha256','supplement_sha256']:
            for name,sha in data.get(label,{}).items():
                assert digest(ROOT/name)==sha,name
    for prior in [OUT.parent/'receipt.json',OUT.parent/'capture_stability/receipt.json',
                  OUT.parent/'autonomous_gate/receipt.json']:
        for name,sha in json.loads(prior.read_text())['artifact_sha256'].items():
            assert digest(ROOT/name)==sha,name
    continuum=stationary['reference']['continuum']
    x=np.array(continuum['profile']['r'])
    chi=np.array(continuum['profile']['chi'])
    f=np.array(continuum['profile']['f'])
    omega=continuum['omega']
    b=stationary['reference']['fine']['b']
    tail=(x>15)&(x<20)
    exponent=float(-np.polyfit(x[tail],np.log(x[tail]*f[tail]),1)[0])
    predicted=float(np.sqrt(1-omega**2))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'axes.titleweight':'bold','axes.grid':True,'grid.alpha':.18,
                         'figure.facecolor':'white','savefig.facecolor':'white'})
    fig,axes=plt.subplots(2,2,figsize=(12.7,8.6),layout='constrained')
    ax=axes[0,0]
    ax.plot(x,chi,color='#237d86',label='Condensate chi')
    ax.plot(x,f,color='#b16e31',label='Charged-field amplitude f')
    ax.set(title='A  Both fields form the localized state',xlabel='Radius',ylabel='Field amplitude',xlim=(0,18))
    ax.legend()
    ax=axes[0,1]
    ax.plot(x,chi*chi,label='Condensate contribution chi²',color='#237d86')
    ax.plot(x,chi*chi+b*f*f,label='Full profile-dependent coefficient',color='#b16e31')
    ax.axhline(omega*omega,color='#6f568e',ls='--',label='Squared mode frequency')
    ax.axhline(1,color='gray',ls=':',label='Exterior threshold')
    ax.set(title='B  The condensate generates the well',xlabel='Radius',ylabel='Squared-frequency scale',xlim=(0,18))
    ax.legend(fontsize=8,loc='lower right')
    ax=axes[1,0]
    for label,name,color in [('zero','b = 0','#70819d'),('source','b = 0.1283','#237d86'),
                              ('half','b = 0.5','#b16e31'),('control','b = 1.2','#a13f49')]:
        rows=[stationary['optimizations'][stationary['selected'][f'{label}-Q{q}']] for q in [100,300,1000,3000]]
        ax.semilogx([v['charge'] for v in rows],[v['energy_per_charge'] for v in rows],'o-',label=name,color=color)
    ax.axhline(1,color='black',ls='--',lw=1,label='Free-wave threshold')
    ax.set(title='C  Binding includes condensate energy',xlabel='Conserved charge Q',ylabel='Total energy / charge')
    ax.legend(fontsize=8)
    ax=axes[1,1]
    take=(x>=8)&(x<=24)
    ax.semilogy(x[take],x[take]*f[take],color='#b16e31',label='Continuum boundary-value solution')
    match=16.
    amplitude=np.interp(match,x,x*f)
    ax.semilogy(x[take],amplitude*np.exp(-predicted*(x[take]-match)),'k--',label='Predicted exterior decay')
    ax.set(title='D  An exponential tail below the continuum',xlabel='Radius',ylabel='r f(r)')
    ax.legend(fontsize=8)
    fig.suptitle('A three-dimensional self-binding candidate: Q = 1000 reference',fontsize=16)
    for ext in ['png','svg']:
        fig.savefig(OUT/f'binding-evidence.{ext}',dpi=170)
    plt.close(fig)

    fig,axes=plt.subplots(2,2,figsize=(12.7,8.6),layout='constrained')
    ax=axes[0,0]
    for name,label,color in [('unperturbed','Stationary profile','#237d86'),
                              ('perturb2','2% shape disturbance','#b16e31'),
                              ('perturb5','5% shape disturbance','#6f568e')]:
        row=dynamics['cases'][name]
        ax.plot(series(row,'t'),100*series(row,'local_energy')/row['initial_energy'],label=label,color=color)
    ax.set(title='A  Perturbed states remain localized',xlabel='Time',ylabel='Energy inside radius 15 (% of initial)')
    ax.legend(fontsize=8)
    ax=axes[0,1]
    for name,label,color in [('sigma6','Condensate responds','#237d86'),
                             ('frozen-sigma6','Condensate held at vacuum','#777777')]:
        row=formation['cases'][name]
        ax.plot(series(row,'t'),100*series(row,'local_energy')/row['initial_energy'],label=label,color=color)
    ax.set(title='B  Identical initial packet, different response',xlabel='Time',ylabel='Energy inside radius 15 (% of initial)')
    ax.legend(fontsize=8)
    ax=axes[1,0]
    for name,label,color in [('sigma3','Width 3','#b16e31'),('sigma6','Width 6','#237d86'),('sigma9','Width 9','#6f568e')]:
        row=formation['cases'][name]
        ax.plot(series(row,'t'),series(row,'chi0'),label=label,color=color,lw=1)
    ax.axhline(1,color='gray',ls=':',lw=1)
    ax.set(title='C  The initially uniform condensate is displaced',xlabel='Time',ylabel='Central condensate value')
    ax.legend(fontsize=8)
    ax=axes[1,1]
    for name,label,color in [('sigma3','Width 3','#b16e31'),('sigma6','Width 6','#237d86'),
                             ('sigma9','Width 9','#6f568e'),('frozen-sigma6','Frozen, width 6','#777777')]:
        row=formation['cases'][name]
        ax.plot(series(row,'t'),100*series(row,'local_charge')/row['initial_charge'],label=label,color=color)
    ax.set(title='D  Local charge remains while energy radiates',xlabel='Time',ylabel='Charge inside radius 15 (% of total)')
    ax.legend(fontsize=8)
    fig.suptitle('Dynamical condensate response, compared with a frozen control',fontsize=16)
    for ext in ['png','svg']:
        fig.savefig(OUT/f'dynamic-evidence.{ext}',dpi=170)
    plt.close(fig)

    report=dict(status='qualified_reduced_model_binding_mechanism',
                stationary_survey_starts=32,dynamic_runs=len(dynamics['cases'])+len(formation['cases']),
                numerical_checks=len(stationary['checks'])+len(dynamics['checks'])+len(formation['checks']),
                symbolic_checks=len(contract['checks']),original_failures=stationary['original_failures'],
                numerical_correction=stationary['qualification'],
                reference=dict(charge=1000.,energy=continuum['energy'],omega=omega,
                               free_wave_energy_threshold=1000.,binding_margin_fraction=1-continuum['energy_per_charge'],
                               predicted_tail_exponent=predicted,fitted_tail_exponent=exponent),
                dynamics={name:{k:row[k] for k in ['initial_energy','initial_charge','final_local_energy_fraction','final_local_charge_fraction']}
                          for name,row in dynamics['cases'].items()},
                formation={name:{k:row[k] for k in ['initial_energy','initial_charge','final_local_energy_fraction','final_local_charge_fraction']}
                           for name,row in formation['cases'].items()},
                conclusions=dict(
                    mechanism='Condensate deformation creates exterior gap and interior well; conserved charge supports a localized rotating field',
                    known_theory='Friedberg-Lee-Sirlin-type scalar soliton with an added positive complex-field quartic',
                    binding='Reference energy lies below free waves of the same conserved charge; all field energies included',
                    stability='No negative modes found in tested amplitude/phase sectors; small radial perturbations remain localized through t80',
                    formation='Charged Gaussian packets displace an initially uniform condensate and retain localized charge through t80',
                    not_established=['asymptotic formation from arbitrary input','nonlinear stability against all finite perturbations',
                                     'quantum stability or elementary-particle mass','complete ACS field/gauge/charge embedding']),
                ACS_embedding=contract['ACS_embedding'],source_and_parent_hashes_verified=True)
    (OUT/'assessment.json').write_text(json.dumps(report,indent=2)+'\n')
    paths=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='receipt.json')
    paths+=sorted((ROOT/'code/condensate_energy').glob('self_binding*.py'))
    paths.append(Path(__file__).resolve())
    receipt=dict(status=report['status'],numerical_checks=report['numerical_checks'],symbolic_checks=report['symbolic_checks'],
                  artifact_sha256={str(p.relative_to(ROOT)):digest(p) for p in paths})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['dynamics','formation']},indent=2))


if __name__=='__main__':
    main()
