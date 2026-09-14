"""Audit exhaustive target projection by rational separation and integer local-model witnesses."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb
from dedekind_coupled_recovery import encode
from dedekind_aggregate_local_audit import catalog,coefficient
from dedekind_aggregate_moment_local_audit import project,digest
from dedekind_aggregate_primal_model_audit import independent_groups,fractional_bound,real_cuts

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(branches_path,models_path,model_audit_path,cut_audit_path,measurements,truth_path):
    data=json.loads(branches_path.read_text());models_data=json.loads(models_path.read_text());model_check=json.loads(model_audit_path.read_text());audit=json.loads(cut_audit_path.read_text())
    m=json.loads(measurements.read_text());truth=json.loads(truth_path.read_text())['arithmetic_vectors'];columns=m['columns'];catalogue=catalog()
    assert data['status']==models_data['status']==model_check['status']==audit['status']=='passed'
    assert data['inputs_sha256']=={p.name:sha(p) for p in [models_path,model_audit_path,cut_audit_path]}
    assert model_check['inputs_sha256'][models_path.name]==sha(models_path) and audit['inputs_sha256'][measurements.name]==sha(measurements)
    expected_cases=[i for i,c in enumerate(models_data['cases']) if c['mode']=='all_directions_from_common_seed'];assert [c['source_case_index'] for c in data['cases']]==expected_cases
    real=[real_cuts(m,o) for o in audit['observations']];cases=[]
    for case in data['cases']:
        source=models_data['cases'][case['source_case_index']];obs=case['observation_index'];cuts=audit['observations'][obs]['cuts']
        assert all(source[k]==case[k] for k in ['observation_index','radius','profile'])
        varying=[i for i,c in enumerate(columns) if c['n']<=31 and len(source['final_domains'][i])>1];assert varying==case['varying_columns']
        expected=[[{'column':i,'n':columns[i]['n'],'candidate':v} for i,v in zip(varying,values)] for values in itertools.product(*(source['final_domains'][i] for i in varying))]
        assert [b['assignment'] for b in case['branches']]==expected
        replays=[];feasible=[];nonrefuted=[]
        for index,b in enumerate(case['branches']):
            forced=[list(d) for d in source['final_domains']]
            for x in b['assignment']:forced[x['column']]=[x['candidate']]
            groups=independent_groups(columns,forced,case['profile']);projected,retained,removed=project(columns,forced,case['profile'])
            assert digest(forced)==b['forced_domains_sha256'] and digest(projected)==b['conditional_domains_sha256'] and digest(groups)==b['conditional_groups_sha256'] and removed==b['conditional_local_removals']
            proof=b['separation'];upper=fractional_bound(cuts,proof['multipliers'],groups,0,0,len(columns));assert upper==F(proof['constant_objective_upper'])
            assert proof['refuted_by_exact_separation']==(upper<0)
            record={'branch_index':index,'assignment':b['assignment'],'status':b['status'],'constant_objective_upper':str(upper)}
            if upper<0:
                assert b['status']=='refuted' and b['witness'] is None and F(proof['strict_infeasibility_gap'])==-upper
                assert any(x['candidate']!=truth[['A','B'][obs]][x['column']] for x in b['assignment'])
                record['strict_infeasibility_gap']=str(-upper)
            else:
                nonrefuted.append(b);w=b['witness'];assert w is not None
                if b['status']=='feasible_integer_witness':
                    assert w['integer_proposal_available'] and w['verified_selected_feasible'] and w['verified_full_pool_feasible']
                    values=w['coefficients'];assert len(values)==len(columns) and all(type(v) is int and v in d for v,d in zip(values,projected))
                    assert all(values[x['column']]==x['candidate'] for x in b['assignment']) and len(w['local_choices'])==len(groups)
                    for g,choice in zip(groups,w['local_choices']):
                        assert choice['prime']==g['prime'];pattern=g['patterns'][choice['pattern_index']];assert choice['model_id'] in pattern['model_ids']
                        model=catalogue[choice['model_id']];assert all(coefficient(model,columns[i]['power'])==values[i] for i in g['columns'])
                    slacks=[c['rhs']-sum(a*v for a,v in zip(c['coefficients'],values)) for c in cuts];assert all(s>=0 for s in slacks)
                    assert min(slacks)==w['selected_minimum_integer_slack']==w['full_pool_minimum_integer_slack'] and w['violated_full_pool_cut_indices']==[]
                    margins=[bound-sum((a*v for a,v in zip(vector,values)),arb(0)) for vector,bound in real[obs]]
                    record.update(coefficient_vector_sha256=digest(values),minimum_integer_cut_slack=str(F(min(slacks),audit['common_integer_unit'])),
                                  unrounded_real_cut_checks=len(margins),all_unrounded_real_cuts_strictly_satisfied=all(g>0 for g in margins),
                                  smallest_unrounded_real_margin=encode(min(g.lower() for g in margins)))
                    feasible.append(b)
                else:assert b['status']=='unresolved' and not w['verified_full_pool_feasible']
            replays.append(record)
        complete=all(b['status']!='unresolved' for b in case['branches']);assert complete==case['projection_complete_for_retained_relaxation']
        projections=[]
        for i in varying:
            p={'column':i,'n':columns[i]['n'],'parent_candidates':source['final_domains'][i],
               'witnessed_candidates':sorted({b['witness']['coefficients'][i] for b in feasible}),
               'nonrefuted_candidates':sorted({next(x['candidate'] for x in b['assignment'] if x['column']==i) for b in nonrefuted})}
            projections.append(p)
            if complete:assert p['witnessed_candidates']==p['nonrefuted_candidates']
        assert projections==case['target_projections']
        refuted=sum(b['status']=='refuted' for b in case['branches']);unresolved=sum(b['status']=='unresolved' for b in case['branches'])
        assert refuted==case['refuted_branches'] and len(feasible)==case['feasible_branches'] and unresolved==case['unresolved_branches']
        assert any(all(x['candidate']==truth[['A','B'][obs]][x['column']] for x in b['assignment']) for b in nonrefuted)
        remaining=[{'n':p['n'],'candidates':p['nonrefuted_candidates']} for p in projections]
        final_unique=source['final_unique_targets']+sum(len(p['nonrefuted_candidates'])==1 for p in projections)
        cases.append({**{k:case[k] for k in ['source_case_index','observation_index','radius','profile']},'projection_complete_for_retained_relaxation':complete,
                      'joint_assignments':len(replays),'refuted_branches':refuted,'feasible_branches':len(feasible),'unresolved_branches':unresolved,
                      'target_projections':projections,'remaining_domains':remaining,'final_unique_targets_after_branch_refutations':final_unique,
                      'branch_replays':replays,'all_heldout_target_values_retained':True})
        print(json.dumps({'event':'independent_joint_projection','observation':obs,'profile':case['profile'],'assignments':len(replays),'refuted':refuted,'feasible':len(feasible),'unresolved':unresolved}),flush=True)
    assert sum(c['joint_assignments'] for c in cases)==data['joint_assignments']
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [branches_path,models_path,model_audit_path,cut_audit_path,measurements,truth_path]},
            'cases':cases,'joint_assignments':sum(c['joint_assignments'] for c in cases),'refuted_branches':sum(c['refuted_branches'] for c in cases),
            'feasible_branches':sum(c['feasible_branches'] for c in cases),'unresolved_branches':sum(c['unresolved_branches'] for c in cases),
            'scope':'Every Cartesian target tuple is accounted for. Direct Fraction combinations independently refute conditional model convex hulls; exact integer vectors and independently enumerated local models witness surviving tuples, with fresh unrounded interval checks reported separately. Complete coverage proves only the target projection of the declared necessary-cut/local-model relaxation, not existence of alternate zero spectra or number fields.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['branches','models','model-audit','cut-audit','measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.branches,a.models,a.model_audit,a.cut_audit,a.measurements,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['status','joint_assignments','refuted_branches','feasible_branches','unresolved_branches']}))
