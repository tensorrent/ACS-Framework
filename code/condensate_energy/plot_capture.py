#!/usr/bin/env python3
"""Render the incoming and initially confined preparations without rescaling data."""
import json
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[2]
out=root/'docs/condensate_energy'
incoming=json.loads((out/'capture-results.json').read_text())['cases']
confined=json.loads((out/'results.json').read_text())['dynamics']['cases']
fig,axes=plt.subplots(1,2,figsize=(11.5,4.7),layout='constrained')
for key,label,color in [('h0','U₀=0','#9dabae'),('h4','U₀=4','#365c70'),('h9','U₀=9','#172d3a')]:
    rows=incoming[key]['history']
    axes[0].plot([r['t'] for r in rows],[r['trapped'] for r in rows],label=label,color=color)
axes[0].set(title='Incoming pulse: energy enters and later leaves',xlabel='Time (c=1 units)',
            ylabel='Energy inside [0,5] / initial total energy',ylim=(-.025,1.025))
axes[0].legend(title='Barrier width b=1',fontsize=8)
for case,label,color in [(confined['h4-b1'],'Initially confined standing wave','#365c70'),
                          (incoming['h4'],'Initially exterior incoming pulse','#a65e38')]:
    rows=case['history']
    axes[1].plot([r['t'] for r in rows],[r['trapped'] for r in rows],label=label,color=color)
axes[1].set(title='Same barrier, different preparations · U₀=4, b=1',xlabel='Time (c=1 units)',
            ylabel='Energy inside [0,5] / initial total energy',ylim=(-.025,1.025))
axes[1].legend(fontsize=8)
fig.suptitle('Linear wave completion · cavity [0,4] + barrier [4,5]; each preparation has total energy 1',fontsize=12)
fig.savefig(out/'capture-comparison.png',dpi=170)
fig.savefig(out/'capture-comparison.svg')
