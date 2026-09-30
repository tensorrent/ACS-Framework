"""Enumerate joint target assignments and certify conditional local-model separation."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from dedekind_aggregate_primal_models import groups_for,numeric_system,group_bound,witness,digest,DUAL_GRID

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def separation(cuts,selected,groups,system,count):
    C,rhs,equality,target,offsets,size,exponents=system
    result=linprog(np.r_[np.zeros(size),-1],A_ub=sparse.hstack([sparse.csr_matrix(C),np.ones((len(selected),1))],format='csr'),b_ub=rhs,
                   A_eq=sparse.hstack([equality,sparse.csr_matrix((len(groups),1))],format='csr'),b_eq=np.ones(len(groups)),
                   bounds=[(0,None)]*size+[(None,None)],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    multipliers=[]
    if result.success:
        for index,value in zip(selected,result.ineqlin.marginals):
            n=round(max(0.,-float(value))*DUAL_GRID);shift=cuts[index]['normalization_exponent']-exponents[index];assert shift>=0
            if n:multipliers.append([index,str(F(n*(1<<shift),DUAL_GRID))])
    upper,stream=group_bound(cuts,multipliers,groups,0,0,count)
    return {'solver_status':int(result.status),'solver_message':result.message,'floating_maximum_minimum_slack':float(-result.fun) if result.success else None,
            'multipliers':multipliers,'constant_objective_upper':str(upper),'strict_infeasibility_gap':str(-upper) if upper<0 else None,
            'integer_combination_sha256':stream,'refuted_by_exact_separation':upper<0}

def run(models_path,model_audit_path,cut_audit_path):
    data=json.loads(models_path.read_text());checked=json.loads(model_audit_path.read_text());audit=json.loads(cut_audit_path.read_text())
    assert data['status']==checked['status']==audit['status']=='passed' and checked['inputs_sha256'][models_path.name]==sha(models_path)
    assert checked['inputs_sha256'][cut_audit_path.name]==sha(cut_audit_path)
    columns=data['columns'];cases=[]
    for case_index,source in enumerate(data['cases']):
        if source['mode']!='all_directions_from_common_seed':continue
        obs=source['observation_index'];cuts=audit['observations'][obs]['cuts'];selected=list(range(len(cuts)))
        varying=[i for i,c in enumerate(columns) if c['n']<=31 and len(source['final_domains'][i])>1];branches=[]
        for values in itertools.product(*(source['final_domains'][i] for i in varying)):
            assignment=[{'column':i,'n':columns[i]['n'],'candidate':v} for i,v in zip(varying,values)]
            forced=[list(d) for d in source['final_domains']]
            for i,v in zip(varying,values):forced[i]=[v]
            groups,projected,removed=groups_for(columns,forced,source['profile']);system=numeric_system(cuts,selected,groups,len(columns))
            proof=separation(cuts,selected,groups,system,len(columns));point=None
            if proof['refuted_by_exact_separation']:status='refuted'
            else:
                point=witness(cuts,selected,groups,system,projected,None,None)
                status='feasible_integer_witness' if point['verified_full_pool_feasible'] else 'unresolved'
            branches.append({'assignment':assignment,'forced_domains_sha256':digest(forced),'conditional_domains_sha256':digest(projected),
                             'conditional_groups_sha256':digest(groups),'conditional_local_removals':removed,'separation':proof,'witness':point,'status':status})
            print(json.dumps({'event':'joint_target_branch','observation':obs,'profile':source['profile'],'assignment':{str(x['n']):x['candidate'] for x in assignment},'status':status}),flush=True)
        feasible=[b for b in branches if b['status']=='feasible_integer_witness'];complete=all(b['status']!='unresolved' for b in branches)
        projections=[]
        for i in varying:
            projections.append({'column':i,'n':columns[i]['n'],'parent_candidates':source['final_domains'][i],
                                'witnessed_candidates':sorted({b['witness']['coefficients'][i] for b in feasible}),
                                'nonrefuted_candidates':sorted({next(x['candidate'] for x in b['assignment'] if x['column']==i) for b in branches if b['status']!='refuted'})})
        cases.append({'source_case_index':case_index,'observation_index':obs,'radius':source['radius'],'profile':source['profile'],
                      'varying_columns':varying,'branches':branches,'projection_complete_for_retained_relaxation':complete,
                      'target_projections':projections,'refuted_branches':sum(b['status']=='refuted' for b in branches),
                      'feasible_branches':len(feasible),'unresolved_branches':sum(b['status']=='unresolved' for b in branches)})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [models_path,model_audit_path,cut_audit_path]},
            'cases':cases,'joint_assignments':sum(len(c['branches']) for c in cases),'refuted_branches':sum(c['refuted_branches'] for c in cases),
            'feasible_branches':sum(c['feasible_branches'] for c in cases),'unresolved_branches':sum(c['unresolved_branches'] for c in cases),
            'scope':'The Cartesian product of remaining target domains is enumerated for each full-pool/profile case. Every tuple fixes complete local patterns before a conditional LP proposes a nonnegative cut combination. A negative exact upper bound on the constant zero refutes the whole tuple. Otherwise a complete integer/local-model point must satisfy every cut to witness feasibility; failure remains unresolved. Any complete projection characterizes only this finite necessary-inequality relaxation, not alternate spectra or number fields.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['models','model-audit','cut-audit','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.models,a.model_audit,a.cut_audit);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','joint_assignments','refuted_branches','feasible_branches','unresolved_branches']}))
