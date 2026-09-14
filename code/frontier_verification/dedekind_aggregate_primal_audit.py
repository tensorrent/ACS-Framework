"""Audit global cut budgets and retain exact integer linear inequalities."""
import argparse,copy,gc,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from dedekind_aggregate_adaptive_audit import audit_budget,canonical
from dedekind_aggregate_integer_audit import integer_rows,GRID,DUAL_GRID
from dedekind_aggregate_moment_local_audit import integer_dual

UNIT=GRID*GRID*DUAL_GRID
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def make_cut(rows,certificate,budget,count):
    beta,residual,unit=integer_dual(rows,certificate,count);assert unit==GRID*DUAL_GRID
    a=[((certificate['sign']*unit if k==certificate['column'] else 0)-r)*GRID for k,r in enumerate(residual)]
    error=F(budget)*UNIT;assert error.denominator==1 and error>=0
    rhs=beta*GRID+error.numerator
    exponent=max([UNIT,abs(rhs)]+[abs(v) for v in a]).bit_length()
    return {'coefficients':a,'rhs':rhs,'normalization_exponent':exponent}

def run(pool_paths,measurements,inputs,truth_path):
    m=json.loads(measurements.read_text());sources=[json.loads(p.read_text()) for p in inputs];truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    altered=copy.deepcopy(m)
    for row in altered['rows']:
        for obs in [0,1]:row['observations'][obs]['R']=row['observations'][obs]['unwidened']
    integers=[integer_rows(altered,obs) for obs in [0,1]];observations=[]
    for obs,path in enumerate(pool_paths):
        data=json.loads(path.read_text());assert data['status']=='passed' and data['observation_index']==obs and data['radius']==['1/10','3/50'][obs]
        assert data['columns']==m['columns'] and data['inputs_sha256'][measurements.name]==sha(measurements)
        for p in inputs:assert data['inputs_sha256'][p.name]==sha(p)
        cuts=[];budgets=[];seen=set();unit_rows=[]
        for index,entry in enumerate(data['cases']):
            c=entry['certificate'];key=hashlib.sha256(canonical(c['multipliers'])).hexdigest()
            assert key==entry['direction_sha256'] and key not in seen;seen.add(key)
            assert c['observation_index']==obs and c['radius']==data['radius'] and c['column']==0 and c['sign']==1
            b=audit_budget(m,sources[obs],c);budgets.append(b);cut=make_cut(integers[obs],c,b['budget_upper'],len(m['columns']))
            if entry['is_unit_row']:
                assert len(c['multipliers'])==1 and c['multipliers'][0][1]=='1';unit_rows.append(c['multipliers'][0][0])
            slack=cut['rhs']-sum(a*v for a,v in zip(cut['coefficients'],truth[['A','B'][obs]]));assert slack>0
            cuts.append({'pool_case_index':index,'direction_sha256':key,'multipliers':c['multipliers'],'is_unit_row':entry['is_unit_row'],
                         'analytic_budget_upper':b['budget_upper'],**cut,'heldout_true_vector_strictly_satisfies':True})
            if (index+1)%20==0:print(json.dumps({'event':'independent_global_cut_audit','observation':obs,'cuts':index+1}),flush=True)
        assert sorted(unit_rows)==list(range(34))
        observations.append({'observation_index':obs,'radius':data['radius'],'cuts':cuts,'budget_replays':budgets,
                             'strict_true_vector_checks':len(cuts)})
        del data;gc.collect()
    flat=[b for o in observations for b in o['budget_replays']]
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in pool_paths+[measurements,truth_path]+inputs},
            'columns':m['columns'],'global_inputs':m['global_inputs'],'common_integer_unit':UNIT,'observations':observations,
            'stored_midpoints_checked':sum(b['stored_midpoints_checked'] for b in flat),'fresh_quadratic_interval_leaves':sum(b['fresh_quadratic_interval_leaves'] for b in flat),
            'independent_displaced_controls':sum(len(b['independent_displaced_controls']) for b in flat),'exact_global_cuts':len(flat),
            'scope':'Every direction receives a fresh complex quadratic/rational moment budget. Outward integer rows retain the complete inequality A_lambda*c <= b_lambda+E_lambda, before any residual support projection. Dyadic normalization is exact and used only for solver proposals. Both observations have all 34 signed unit rows. Held-out arithmetic strictly satisfies every retained cut; no alternative-field existence follows from relaxed feasibility.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--pools',type=Path,nargs=2,required=True);p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.pools,a.measurements,a.inputs,a.truth)
    a.output.write_text(json.dumps(r,separators=(',',':'))+'\n');print(json.dumps({k:r[k] for k in ['status','stored_midpoints_checked','fresh_quadratic_interval_leaves','independent_displaced_controls','exact_global_cuts']}))
