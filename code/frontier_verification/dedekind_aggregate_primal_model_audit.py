"""Independently replay local-model bounds and complete integer cut witnesses."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import decode,encode
from dedekind_coupled_dual import inequalities
from dedekind_aggregate_local_audit import catalog,coefficient
from dedekind_aggregate_moment_local_audit import project,digest

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def independent_groups(columns,domains,profile):
    models=catalog();groups=[]
    for prime in sorted({c['prime'] for c in columns}):
        indices=[i for i,c in enumerate(columns) if c['prime']==prime];by_values={}
        for index,model in enumerate(models):
            if profile=='degree_discriminant' and any(e>1 for e,f in model)!=(576%prime==0):continue
            values=tuple(coefficient(model,columns[i]['power']) for i in indices)
            if all(v in domains[i] for i,v in zip(indices,values)):by_values.setdefault(values,[]).append(index)
        assert by_values
        groups.append({'prime':prime,'columns':indices,'patterns':[{'coefficients':list(v),'model_ids':ids} for v,ids in sorted(by_values.items())]})
    return groups

def fractional_bound(cuts,multipliers,groups,column,sign,count):
    combined=[F(0)]*count;rhs=F(0);seen=set()
    for index,value in multipliers:
        assert type(index) is int and index not in seen and 0<=index<len(cuts);seen.add(index)
        scalar=F(value);assert scalar>=0 and (scalar*10**9).denominator==1
        weight=scalar/F(1<<cuts[index]['normalization_exponent']);rhs+=weight*cuts[index]['rhs']
        combined=[x+weight*y for x,y in zip(combined,cuts[index]['coefficients'])]
    total=rhs
    for g in groups:
        scores=[]
        for pattern in g['patterns']:
            local=sum(((F(sign) if i==column else F(0))-combined[i])*v for i,v in zip(g['columns'],pattern['coefficients']))
            scores.append(local)
        total+=max(scores)
    return total

def real_cuts(m,observation):
    ctx.prec=384;obs=observation['observation_index']
    matrix,rhs=inequalities([{'weights':[decode(w) for w in r['weights']],'R':decode(r['observations'][obs]['unwidened']),'B':decode(r['prime_tail'])} for r in m['rows']])
    result=[]
    for cut in observation['cuts']:
        vector=[arb(0) for _ in m['columns']];bound=arb(cut['analytic_budget_upper'])
        for index,value in cut['multipliers']:
            v=arb(value);bound+=v*rhs[index];vector=[x+v*y for x,y in zip(vector,matrix[index])]
        result.append((vector,bound))
    return result

def run(models_path,cut_audit_path,seed_path,measurements,truth_path):
    data=json.loads(models_path.read_text());audit=json.loads(cut_audit_path.read_text());seed=json.loads(seed_path.read_text());m=json.loads(measurements.read_text());truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    assert data['status']==audit['status']==seed['status']=='passed' and data['witness_search_performed'] is True
    assert data['inputs_sha256'][cut_audit_path.name]==sha(cut_audit_path) and data['inputs_sha256'][seed_path.name]==sha(seed_path)
    assert audit['inputs_sha256'][measurements.name]==sha(measurements) and data['columns']==audit['columns']==m['columns']
    assert canonical(data['catalog'])==canonical(catalog())
    keys=[(obs,profile,mode) for obs in [0,1] for profile in ['degree_only','degree_discriminant'] for mode in ['unit_rows_from_common_seed','all_directions_from_common_seed']]
    assert [(c['observation_index'],c['profile'],c['mode']) for c in data['cases']]==keys
    columns=m['columns'];models=catalog();reals=[real_cuts(m,o) for o in audit['observations']];replays=[]
    for case in data['cases']:
        obs=case['observation_index'];observation=audit['observations'][obs];cuts=observation['cuts'];source=seed['cases'][case['seed_case_index']]
        assert all(source[k]==case[k] for k in ['observation_index','radius','profile']) and case['radius']==observation['radius']
        selected=[i for i,c in enumerate(cuts) if case['mode'].startswith('all_') or c['is_unit_row']];assert selected==case['selected_cut_indices']
        exponents={str(i):max([1,abs(cuts[i]['rhs'])]+[abs(v) for v in cuts[i]['coefficients']]).bit_length() for i in selected};assert exponents==case['solver_normalization_exponents']
        domains=[list(d) for d in source['final_domains']];assert domains==case['input_domains'];proofs=[];lc=dc=0
        for iteration,step in enumerate(case['rounds'],1):
            assert step['iteration']==iteration and digest(domains)==step['before_domains_sha256']
            groups=independent_groups(columns,domains,case['profile']);after,retained,removed=project(columns,domains,case['profile'])
            assert groups==step['groups'] and removed==step['local_removals'] and digest(after)==step['after_local_sha256'];lc+=len(removed)
            expected=[(i,s) for i,c in enumerate(columns) if c['n']<=31 and len(after[i])>1 for s in [-1,1]]
            assert [(p['column'],p['sign']) for p in step['model_hull_proofs']]==expected
            bounds=[]
            for p in step['model_hull_proofs']:
                assert p['n']==columns[p['column']]['n'] and all(i in selected for i,v in p['multipliers'])
                upper=fractional_bound(cuts,p['multipliers'],groups,p['column'],p['sign'],len(columns));assert upper==F(p['exact_upper'])
                assert p['sign']*truth[['A','B'][obs]][p['column']]<=upper
                bounds.append(upper);proofs.append({'iteration':iteration,'column':p['column'],'sign':p['sign'],'exact_upper':str(upper)})
            domains=[list(d) for d in after];seen=set()
            for excluded in step['dual_removals']:
                i=excluded['column'];v=excluded['candidate'];j=excluded['proof_index'];p=step['model_hull_proofs'][j]
                assert p['column']==i and excluded['n']==columns[i]['n'] and v in after[i] and (i,v) not in seen;seen.add((i,v))
                gap=p['sign']*v-bounds[j];assert gap>0 and gap==F(excluded['strict_gap']) and v!=truth[['A','B'][obs]][i]
                domains[i].remove(v)
            dc+=len(seen);assert all(domains) and digest(domains)==step['after_domains_sha256'] and all(v in d for v,d in zip(truth[['A','B'][obs]],domains))
        assert domains==case['final_domains'] and not case['rounds'][-1]['local_removals'] and not case['rounds'][-1]['dual_removals']
        groups=independent_groups(columns,domains,case['profile']);assert groups==case['final_groups']
        expected_assignments=[None]+[{'column':i,'candidate':v} for i,c in enumerate(columns) if c['n']<=31 and len(domains[i])>1 for v in domains[i]]
        assert [w['assignment'] for w in case['witness_proposals']]==expected_assignments
        witnesses=[];feasible_points=[]
        for index,w in enumerate(case['witness_proposals']):
            record={'proposal_index':index,'assignment':w['assignment'],'solver_status':w['solver_status'],'integer_proposal_available':w['integer_proposal_available'],
                    'verified_selected_feasible':False,'verified_full_pool_feasible':False}
            if w['integer_proposal_available']:
                values=w['coefficients'];assert len(values)==len(columns) and all(type(v) is int and v in d for v,d in zip(values,domains))
                if w['assignment']:assert values[w['assignment']['column']]==w['assignment']['candidate']
                assert len(w['local_choices'])==len(groups)
                for g,choice in zip(groups,w['local_choices']):
                    assert choice['prime']==g['prime'];pattern=g['patterns'][choice['pattern_index']];assert choice['model_id'] in pattern['model_ids']
                    model=models[choice['model_id']];assert all(coefficient(model,columns[i]['power'])==values[i] for i in g['columns'])
                slacks=[c['rhs']-sum(a*v for a,v in zip(c['coefficients'],values)) for c in cuts]
                selected_ok=all(slacks[i]>=0 for i in selected);full_ok=all(s>=0 for s in slacks)
                assert selected_ok==w['verified_selected_feasible'] and full_ok==w['verified_full_pool_feasible']
                assert min(slacks[i] for i in selected)==w['selected_minimum_integer_slack'] and min(slacks)==w['full_pool_minimum_integer_slack']
                assert [i for i,s in enumerate(slacks) if s<0]==w['violated_full_pool_cut_indices']
                record.update(verified_selected_feasible=selected_ok,verified_full_pool_feasible=full_ok,coefficient_vector_sha256=digest(values),
                              selected_minimum_slack=str(F(min(slacks[i] for i in selected),audit['common_integer_unit'])),
                              full_pool_minimum_slack=str(F(min(slacks),audit['common_integer_unit'])),violated_full_pool_cut_indices=[i for i,s in enumerate(slacks) if s<0])
                if selected_ok:
                    margins=[]
                    for i in selected:
                        vector,bound=reals[obs][i];margin=bound-sum((a*v for a,v in zip(vector,values)),arb(0));margins.append(margin)
                    strict=all(g>0 for g in margins)
                    record.update(unrounded_real_cut_checks=len(margins),all_unrounded_real_cuts_strictly_satisfied=strict,
                                  smallest_unrounded_real_margin=encode(min((g.lower() for g in margins))))
                    if full_ok:feasible_points.append(values)
            else:assert not w['verified_selected_feasible'] and not w['verified_full_pool_feasible']
            witnesses.append(record)
        unique=lambda ds:sum(len(d)==1 for c,d in zip(columns,ds) if c['n']<=31)
        assert unique(domains)==case['final_unique_targets'] and unique(case['input_domains'])==case['initial_unique_targets'] and sum(len(d)==1 for d in domains)==case['final_unique_support']
        replays.append({**{k:case[k] for k in ['observation_index','radius','profile','mode','initial_unique_targets','final_unique_targets','final_unique_support']},
                        'iterations':len(case['rounds']),'model_hull_objectives':len(proofs),'local_removals':lc,'dual_removals':dc,'objective_replays':proofs,'witness_replays':witnesses,
                        'full_pool_witnessed_target_values':[{'n':c['n'],'values':sorted({v[i] for v in feasible_points})} for i,c in enumerate(columns) if c['n']<=31],
                        'all_604_true_coefficients_retained_each_round':True})
        print(json.dumps({'event':'independent_model_audit','observation':obs,'profile':case['profile'],'mode':case['mode'],'local_removals':lc,'dual_removals':dc,
                          'verified_selected_witnesses':sum(w['verified_selected_feasible'] for w in witnesses),'verified_full_pool_witnesses':sum(w['verified_full_pool_feasible'] for w in witnesses)}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [models_path,cut_audit_path,seed_path,measurements,truth_path]},
            'cases':replays,'exact_model_hull_objectives':sum(c['model_hull_objectives'] for c in replays),'local_removals':sum(c['local_removals'] for c in replays),'dual_removals':sum(c['dual_removals'] for c in replays),
            'verified_selected_witnesses':sum(w['verified_selected_feasible'] for c in replays for w in c['witness_replays']),
            'verified_full_pool_witnesses':sum(w['verified_full_pool_feasible'] for c in replays for w in c['witness_replays']),
            'scope':'Independent local catalogue enumeration and direct Fraction arithmetic replay every model-hull bound and exclusion. Every returned integer point is reconstructed from an actual allowed local model for each prime and checked against all selected/full-pool integer cuts. Feasible selected points also receive fresh 384-bit checks against the unrounded measurement combinations. This establishes only feasibility or exclusions in the declared necessary-inequality/local-model relaxation, not alternate spectra or number fields.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['models','cut-audit','seed','measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.models,a.cut_audit,a.seed,a.measurements,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['status','exact_model_hull_objectives','local_removals','dual_removals','verified_selected_witnesses','verified_full_pool_witnesses']}))
