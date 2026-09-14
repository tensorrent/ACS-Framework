"""Challenge projection coverage, multiplier constraints, witness claims and parity scope."""
import argparse,copy,hashlib,json,tempfile
from fractions import Fraction as F
from pathlib import Path
import dedekind_aggregate_primal_branch_audit as branch_audit
import dedekind_aggregate_parity_audit_v2 as parity_audit
from dedekind_aggregate_primal_models import group_bound
from dedekind_aggregate_discriminant_parity import metadata,permitted
from verify_aggregate_moment_delta import quiet

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(branches,projection,models,model_audit,cut_audit,parity,measurements,inputs,truth):
    read=lambda p:json.loads(p.read_text());bd=read(branches);pd=read(parity);md=read(models);cuts=read(cut_audit);records=[]
    def rejected(name,call):
        try:call()
        except AssertionError:records.append({'mutation':name,'rejected':True});return
        raise AssertionError('Mutation accepted: '+name)
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        def changed_branch(name,mutate):
            d=copy.deepcopy(bd);mutate(d);p=tmp/branches.name;p.write_text(json.dumps(d))
            rejected(name,lambda:quiet(branch_audit.run,p,models,model_audit,cut_audit,measurements,truth))
        def changed_parity(name,mutate):
            d=copy.deepcopy(pd);mutate(d);p=tmp/parity.name;p.write_text(json.dumps(d))
            rejected(name,lambda:quiet(parity_audit.run,p,branches,projection,models,cut_audit,measurements,inputs,truth))
        changed_branch('drop_one_cartesian_target_tuple',lambda d:d['cases'][0]['branches'].pop())
        changed_branch('change_exact_separation_bound',lambda d:d['cases'][0]['branches'][0]['separation'].__setitem__('constant_objective_upper','-1000000'))
        c=cuts['observations'][0]['cuts'];groups=md['cases'][1]['final_groups']
        rejected('negative_cut_multiplier',lambda:group_bound(c,[[0,'-1']],groups,0,0,604))
        rejected('duplicate_cut_multiplier',lambda:group_bound(c,[[0,'1'],[0,'1']],groups,0,0,604))
        changed_parity('forget_signed_discriminant',lambda d:d['metadata'][0].__setitem__('complex_places',1))
        changed_parity('drop_surviving_relaxed_tuple_before_parity',lambda d:d['cases'][0]['branches'].pop())
        changed_parity('invent_incompatible_prime',lambda d:d['cases'][0]['branches'][0].__setitem__('incompatible_primes',[2]))
        changed_parity('forge_full_parity_witness',lambda d:next(b for b in d['cases'][0]['branches'] if b['retained'])['witness']['coefficients'].__setitem__(0,99))
        changed_parity('wrong_permutation_sign',lambda d:d['permutations'][0].__setitem__('sign',-1))
        changed_parity('assume_V4_and_discard_three_cycles',lambda d:d['allowed_unramified_cycle_types'].remove([1,3]))
    invalid=[]
    for i,case in enumerate(md['cases']):
        for j,w in enumerate(case['witness_proposals']):
            if w['integer_proposal_available'] and not w['verified_selected_feasible']:
                assert w['solver_status']==0 and w['selected_minimum_integer_slack']<0
                invalid.append({'case_index':i,'proposal_index':j,'solver_status':0,'selected_minimum_integer_slack':str(w['selected_minimum_integer_slack']),
                                'scope':'Optimal maximum-slack proposal with negative slack is not a feasible point.'})
    assert len(invalid)==12
    # Actual feasible branch: replacing max residual support by min can falsely refute constant zero.
    bad_support=None
    for case in pd['cases']:
        source=md['cases'][case['source_case_index']];b=next(b for b in case['branches'] if b['retained']);domains=copy.deepcopy(source['final_domains'])
        for x in b['assignment']:domains[x['column']]=[x['candidate']]
        groups,empty=parity_audit.independent_groups(cuts['columns'],domains,pd['metadata'][case['observation_index']]);assert not empty
        for j,c in enumerate(cuts['observations'][case['observation_index']]['cuts']):
            wrong=c['rhs']-sum(max(sum(c['coefficients'][i]*v for i,v in zip(g['columns'],p['coefficients'])) for p in g['patterns']) for g in groups)
            if wrong<0:
                correct,_=group_bound(cuts['observations'][case['observation_index']]['cuts'],[[j,'1']],groups,0,0,604)
                w=b['witness']['coefficients'];slack=c['rhs']-sum(a*v for a,v in zip(c['coefficients'],w));assert correct>=0 and slack>=0
                bad_support={'source_case_index':case['source_case_index'],'cut_index':j,'wrong_min_support_upper':str(F(wrong,1<<c['normalization_exponent'])),
                             'correct_max_support_upper':str(correct),'verified_witness_integer_slack':str(slack)};break
        if bad_support:break
    assert bad_support is not None
    base=metadata(read(inputs[0]));assert permitted([(2,2)],2,base) and permitted([(1,1),(1,3)],5,base) and not permitted([(1,4)],5,base)
    negative=metadata({'degree':4,'discriminant':400,'real_places':2,'complex_places':1});assert not negative['signed_discriminant_is_nonzero_square'] and permitted([(1,4)],3,negative)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [branches,projection,models,model_audit,cut_audit,parity,measurements,truth]+inputs},
            'actual_component_mutations_rejected':len(records),'mutations':records,'optimal_but_infeasible_proposals':invalid,'minimum_instead_of_maximum_support_counterexample':bad_support,
            'ramified_and_signed_discriminant_guard_checks':'passed','scope':'Ten mutations reach semantic component assertions. A real stored feasible point refutes the min-support substitution. Twelve optimal slack-search outputs are preserved as infeasible proposals. These are finite-relaxation controls, not claims of alternate fields or noise impossibility.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['branches','projection','models','model-audit','cut-audit','parity','measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.branches,a.projection,a.models,a.model_audit,a.cut_audit,a.parity,a.measurements,a.inputs,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','mutations':len(r['mutations']),'infeasible_optimal_proposals':len(r['optimal_but_infeasible_proposals'])}))
