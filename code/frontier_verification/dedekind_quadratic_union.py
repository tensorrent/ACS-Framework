"""Combine all retained rational proposals without importing later coefficient answers."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_quadratic_ordinate as quad


def run(directory,prior,bits,names):
    data,powers,rows,seeds,previous,provenance=quad.load(prior,bits);ctx.prec=bits
    basis,metadata=quad.prepare(data,rows,bits);proposals=[];combos={};sources={}
    for name in names:
        raw=(directory/name).read_bytes();result=json.loads(raw);sources[name]=core.sha(raw)
        assert result['status']=='passed' and result['provenance']==provenance
        if 'proposals' in result:items=result['proposals']
        elif 'checks' in result:items=[{**c,'column':check['column'],'n':check['n']} for check in result['checks'] for c in check['certificates']]
        else:items=[c for step in result['rounds'] for check in step['checks'] for c in check['certificates']]
        for item in items:
            proposal={k:item[k] for k in ['column','n','sign','multipliers','combination_sha256']}
            proposal['source_file']=name;proposals.append(proposal);key=item['combination_sha256']
            if key not in combos:
                alpha=[F(0)]*len(rows)
                for i,v in item['multipliers']:alpha[i]=F(v)
                combos[key]=quad.combine(rows,basis,alpha)
    reports=[]
    for mode in ['linear','independent_quadratic','quadratic']:
        domains=[list(d) for d in seeds];rounds=[]
        for number in range(1,4*91+2):
            old=[list(d) for d in domains];checks=[]
            for p in proposals:
                column=p['column']
                if len(old[column])==1:continue
                proof=quad.objective(combos[p['combination_sha256']],column,p['sign'],old,mode)
                after=[v for v in domains[column] if not arb(p['sign']*v)>core.decode(proof['objective_upper_bound']).upper()]
                assert after
                checks.append({**p,'before':list(domains[column]),'after':after,**proof});domains[column]=after
            changed=sum(a!=b for a,b in zip(old,domains))
            rounds.append({'round':number,'prior_domains_sha256':core.sha(core.canonical(old)),'checks':checks,
                'changed_targets':changed,'remaining_domains_sha256':core.sha(core.canonical(domains))})
            if not changed:break
        else:raise AssertionError('Finite proposal union failed to stabilize')
        reports.append({'mode':mode,'rounds':rounds,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
            'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),'stabilized':True})
        print(json.dumps({'mode':mode,'unique_targets':reports[-1]['unique_targets'],'rounds':len(rounds)}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'basis_source_sha256':core.sha(Path(quad.__file__).read_bytes()),
        'precision_bits':bits,'height':2000,'additional_radius':'5e-3','provenance':provenance,'basis':metadata,
        'input_results_sha256':sources,'proposals':proposals,'combinations':{k:v['metadata'] for k,v in combos.items()},'cases':reports,
        'scope':'All retained proposal sources are revalidated from the same prior 81-domain seed, with independent linear, independent-square and coupled-square controls. No coefficient is imported from the new LP or conic output domains.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--prior',type=Path,required=True);p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--results',nargs='+',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.directory,a.prior,a.precision,a.results);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status']}))
