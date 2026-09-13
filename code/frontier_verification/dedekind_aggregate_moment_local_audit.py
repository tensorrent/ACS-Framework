"""Independently replay noisy local projections and residual-domain feedback with integers."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_local_audit import catalog,coefficient
from dedekind_aggregate_integer_audit import integer_rows,GRID,DUAL_GRID

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def integer_dual(rows,certificate,count):
    unit=GRID*DUAL_GRID;vector=[0]*count;rhs=0;seen=set();sign=certificate['sign'];assert sign in [-1,1]
    for j,value in certificate['multipliers']:
        assert type(j) is int and 0<=j<2*len(rows) and j not in seen;seen.add(j)
        scalar=F(value)*DUAL_GRID;assert scalar.denominator==1 and scalar>=0;scalar=scalar.numerator
        row=rows[j//2];a=row['lo'] if j%2==0 else [-v for v in row['hi']];b=row['rhi'] if j%2==0 else -row['rlo']+row['tail']
        rhs+=scalar*b;vector=[v+scalar*w for v,w in zip(vector,a)]
    residual=[(sign*unit if j==certificate['column'] else 0)-v for j,v in enumerate(vector)]
    return rhs,residual,unit

def domain_bound(prepared,domains,budget):
    rhs,residual,unit=prepared
    support=sum(r*(d[-1] if r>=0 else d[0]) for r,d in zip(residual,domains))
    return F(rhs+support,unit)+F(budget)

def project(columns,domains,profile):
    models=catalog();groups={p:[i for i,c in enumerate(columns) if c['prime']==p] for p in sorted({c['prime'] for c in columns})}
    result=[list(x) for x in domains];retained=[];removals=[]
    for p,indices in groups.items():
        ids=[j for j,model in enumerate(models) if (profile=='degree_only' or any(e>1 for e,f in model)==(576%p==0)) and all(coefficient(model,columns[i]['power']) in domains[i] for i in indices)]
        assert ids;retained.append({'prime':p,'model_ids':ids})
        for i in indices:
            allowed=sorted({coefficient(models[j],columns[i]['power']) for j in ids})
            for v in sorted(set(domains[i])-set(allowed)):removals.append({'column':i,'n':columns[i]['n'],'candidate':v,'prime':p})
            result[i]=allowed
    removals.sort(key=lambda r:(r['column'],r['candidate']))
    return result,retained,removals

def run(local_path,feedback_path,certificate_path,moment_audit_path,measurements,proposals,previous_proposals,truth_path):
    local=json.loads(local_path.read_text());feedback=json.loads(feedback_path.read_text());certificate=json.loads(certificate_path.read_text());audit=json.loads(moment_audit_path.read_text())
    m=json.loads(measurements.read_text());p=json.loads(proposals.read_text());old=json.loads(previous_proposals.read_text());truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    for data in [local,feedback]:
        assert [tuple(map(tuple,x)) for x in data['catalog']]==catalog()
    columns=m['columns'];assert columns==local['columns']==feedback['columns']==certificate['columns'];single_replays=[];one_pass_removals=0
    for case in local['cases']:
        obs=case['observation_index'];source=next(r for r in certificate['results'] if r['observation_index']==obs and r['radius']==case['radius'])
        initial=[list(range(5)) for _ in columns]
        for row in source['targets']:initial[row['column']]=row['methods'][case['spectral_method']]
        assert initial==case['input_domains'];domains,retained,removals=project(columns,initial,case['profile'])
        assert domains==case['output_domains'] and retained==case['local_models'] and removals==case['removals']
        assert all(v in d for v,d in zip(truth[['A','B'][obs]],domains));one_pass_removals+=len(removals)
        unique=sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31);assert unique==case['local_unique_targets']
        single_replays.append({**{k:case[k] for k in ['observation_index','radius','spectral_method','profile']},'unique_targets':unique,'removals':len(removals),'all_604_true_coefficients_retained':True})
    altered=copy.deepcopy(m)
    for row in altered['rows']:
        for obs in [0,1]:row['observations'][obs]['R']=row['observations'][obs]['unwidened']
    rows=[integer_rows(altered,obs) for obs in [0,1]];prepared=[]
    for row in audit['objective_replays']:
        candidate=next(c for c in (p if row['multiplier_source']=='joint_adapted' else old)['cases'] if all(c[k]==row[k] for k in ['observation_index','radius','column','sign']))
        prepared.append(integer_dual(rows[row['observation_index']],candidate,len(columns)))
    feedback_replays=[];local_removals=dual_removals=0
    for case in feedback['cases']:
        obs=case['observation_index'];initial=[list(range(5)) for _ in columns]
        selected=[(i,r) for i,r in enumerate(audit['objective_replays']) if r['observation_index']==obs and r['radius']==case['radius']]
        for i,r in selected:initial[r['column']]=sorted(set(initial[r['column']])&set(r['methods'][case['method']]['candidates']))
        assert initial==case['input_domains'];domains=[list(x) for x in initial];lc=dc=0;exact_proofs=[]
        for step in case['rounds']:
            assert step['before_domains_sha256']==digest(domains)
            after_local,retained,removed=project(columns,domains,case['profile'])
            assert retained==step['local_models'] and removed==step['local_removals'] and digest(after_local)==step['after_local_sha256']
            if step['iteration']==1:assert after_local==case['first_local_domains']
            domains=[list(x) for x in after_local]
            for witness in step['dual_removals']:
                i=witness['audit_case_index'];row=audit['objective_replays'][i];column=witness['column'];value=witness['candidate']
                assert i in [j for j,r in selected] and row['column']==column and row['n']==witness['n'] and row['sign']==witness['sign'] and value in after_local[column]
                upper=domain_bound(prepared[i],after_local,row['methods'][case['method']]['budget_upper'])
                gap=row['sign']*value-upper;assert gap>0
                assert value!=truth[['A','B'][obs]][column];domains[column].remove(value)
                exact_proofs.append({'iteration':step['iteration'],'audit_case_index':i,'column':column,'candidate':value,'objective_upper':str(upper),'strict_gap':str(gap)})
            assert all(domains) and digest(domains)==step['after_domains_sha256']
            assert all(v in d for v,d in zip(truth[['A','B'][obs]],domains))
            lc+=len(removed);dc+=len(step['dual_removals'])
        assert domains==case['final_domains'] and not case['rounds'][-1]['local_removals'] and not case['rounds'][-1]['dual_removals']
        unique=sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31);support=sum(len(d)==1 for d in domains)
        assert unique==case['feedback_unique_targets'] and support==case['feedback_unique_support']
        feedback_replays.append({**{k:case[k] for k in ['observation_index','radius','method','profile']},'iterations':len(case['rounds']),
            'unique_targets':unique,'unique_support':support,'local_removals':lc,'dual_removals':dc,'exact_dual_proofs':exact_proofs,'all_604_true_coefficients_retained_each_round':True})
        local_removals+=lc;dual_removals+=dc
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{path.name:sha(path) for path in [local_path,feedback_path,certificate_path,moment_audit_path,measurements,proposals,previous_proposals,truth_path]},
            'independent_catalog':catalog(),'one_pass_replays':single_replays,'one_pass_local_removals':one_pass_removals,'feedback_replays':feedback_replays,
            'feedback_local_removals':local_removals,'feedback_dual_removals':dual_removals,
            'scope':'Independent degree-partition enumeration checks every local projection. Exact integer coefficients and rational domain-support bounds replay every feedback exclusion with the unchanged audited analytic budget. No interval backend is used in these deductions. All 604 held-out arithmetic values remain after every round; global realization of survivors is not established.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['local','feedback','certificate','moment-audit','measurements','proposals','previous-proposals','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.local,a.feedback,a.certificate,a.moment_audit,a.measurements,a.proposals,a.previous_proposals,a.truth)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'one_pass_local':r['one_pass_local_removals'],'feedback_local':r['feedback_local_removals'],'feedback_dual':r['feedback_dual_removals']}))
