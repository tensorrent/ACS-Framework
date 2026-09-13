"""Enclose the shared finite-root and known-moment change before maximizing."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_coupled_dual import inequalities,bound
from dedekind_aggregate_shared import combine,derivative_range
from dedekind_aggregate_noise_certificate import H

BITS=224;PARTITIONS=48
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def moment(t):return 3/(arb('9/4')+t*t)
def moment_prime(t):
    q=arb('9/4')+t*t;return -6*t/(q*q)

def certify(data,source,certificate):
    ctx.prec=BITS;a=arb(1)/25;delta=F(certificate['radius']);obs=certificate['observation_index'];roots=source['positive_root_intervals']
    lambdas,alpha,sigma,description=combine(data,certificate)
    terms=[(arb(str(v))*decode(row['scale']),arb(row['center']).log()) for row,v in zip(data['rows'],alpha) if v]
    rows=[{'weights':[decode(w) for w in row['weights']],'R':decode(row['observations'][obs]['unwidened']),'B':decode(row['prime_tail'])} for row in data['rows']]
    matrix,rhs=inequalities(rows);nominal=bound(matrix,rhs,certificate['column'],certificate['sign'],lambdas)
    kappa=sum((arb(str(v))*decode(row['scale'])*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh() for row,v in zip(data['rows'],sigma)),arb(0))
    originals=[arb(r['lo']).union(arb(r['hi'])) for r in roots]
    wide=[arb(str(F(r['lo'])-delta)).union(arb(str(F(r['hi'])+delta))) for r in roots];assert all(t>0 and t<20 for t in wide)
    U0=decode(data['constant_moment_upper'])-sum((moment(t) for t in originals),arb(0))
    Uwide=decode(data['constant_moment_upper'])-sum((moment(t) for t in wide),arb(0));assert U0>0 and Uwide>0
    root_bounds=[];finite_error=joint_error=arb(0)
    active=any(sigma)
    for index,(root,original) in enumerate(zip(roots,originals)):
        base_H=H(original,a,terms);base_m=moment(original);lo,hi=F(root['lo'])-delta,F(root['hi'])+delta
        leaves=[];finite_upper=joint_upper=arb(0)
        if delta and active:
            for j in range(PARTITIONS):
                left=lo+(hi-lo)*F(j,PARTITIONS);right=lo+(hi-lo)*F(j+1,PARTITIONS);middle=(left+right)/2
                t=arb(str(left)).union(arb(str(right)));mid=arb(str(middle));offset=arb(0,arb(str((right-left)/2)))
                hp,_=derivative_range(t,a,terms);finite_derivative=-2*hp;joint_derivative=finite_derivative-kappa*moment_prime(t)
                finite_center=-2*(H(mid,a,terms)-base_H);joint_center=finite_center-kappa*(moment(mid)-base_m)
                finite_change=finite_center+finite_derivative*offset;joint_change=joint_center+joint_derivative*offset
                leaves.append({'lo':str(left),'hi':str(right),'finite_change':encode(finite_change),'joint_change':encode(joint_change),
                               'finite_derivative':encode(finite_derivative),'joint_derivative':encode(joint_derivative)})
                finite_upper=max(finite_upper,finite_change.upper());joint_upper=max(joint_upper,joint_change.upper())
        finite_error+=finite_upper;joint_error+=joint_upper
        root_bounds.append({'root_index':index,'lo':str(lo),'hi':str(hi),'base_H':encode(base_H),'base_moment':encode(base_m),'leaves':leaves,
                            'finite_increment_upper':encode(finite_upper),'joint_increment_upper':encode(joint_upper)})
    separate=kappa*Uwide+finite_error;joint=kappa*U0+joint_error;coupled=min(separate.upper(),joint.upper())
    methods={}
    for name,budget in [('separate',separate),('coupled',coupled)]:
        upper=decode(nominal['objective_upper_bound'])+budget
        candidates=[v for v in range(5) if not arb(certificate['sign']*v)>upper.upper()];assert candidates
        methods[name]={'total_zero_and_input_budget':encode(budget),'objective_upper_bound':encode(upper),'candidates':candidates}
    assert set(methods['coupled']['candidates'])<=set(methods['separate']['candidates'])
    return {**{k:certificate[k] for k in ['observation_index','radius','column','n','sign','multipliers']},'terms':description,
            'nominal_bound':nominal,'kappa':encode(kappa),'baseline_unknown_moment':encode(U0),'widened_unknown_moment':encode(Uwide),
            'uncapped_joint_budget':encode(joint),'joint_selected':bool(joint.upper()<separate.upper()),'root_bounds':root_bounds,'methods':methods}

def run(measurements,proposals,previous_proposals,inputs):
    data=json.loads(measurements.read_text());p=json.loads(proposals.read_text());old=json.loads(previous_proposals.read_text());sources=[json.loads(x.read_text()) for x in inputs]
    expected={x.name:sha(x) for x in [measurements]+inputs};assert p['inputs_sha256']==old['inputs_sha256']==expected
    cases=[]
    work=[('joint_adapted',c) for c in p['cases']]+[('previous_noise_adapted',{**c,'n':7}) for c in old['cases'] if c['radius'] in p['radii']]
    for name,c in work:
        result=certify(data,sources[c['observation_index']],c);result['multiplier_source']=name;cases.append(result)
        if c['sign']==1 and (c['n']==31 or name=='previous_noise_adapted'):
            print(json.dumps({'event':'moment_certificate','observation':c['observation_index'],'radius':c['radius'],'source':name}),flush=True)
    results=[]
    for obs in range(2):
        for radius in p['radii']:
            targets=[]
            for column,c in enumerate(data['columns']):
                if c['n']>31:continue
                selected=[x for x in cases if x['observation_index']==obs and x['radius']==radius and x['column']==column]
                assert len(selected)==(4 if c['n']==7 else 2)
                methods={name:sorted(set.intersection(*(set(x['methods'][name]['candidates']) for x in selected))) for name in ['separate','coupled']}
                targets.append({'column':column,'n':c['n'],'methods':methods})
            results.append({'observation_index':obs,'radius':radius,'targets':targets,'unique_targets':{name:sum(len(t['methods'][name])==1 for t in targets) for name in ['separate','coupled']}})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [measurements,proposals,previous_proposals]+inputs},
            'precision_bits':BITS,'partitions_per_active_root':PARTITIONS,'global_inputs':data['global_inputs'],'columns':data['columns'],'radii':p['radii'],
            'cases':cases,'results':results,
            'scope':'All seventeen targets under four uncertainty radii, with coefficient-seven legacy multipliers replayed on the common grid. Shared finite and known-moment increments are combined before maximizing; the minimum with the independently valid separated budget prevents a wider numerical enclosure from weakening the certificate. Generic boxes only; local relations and held-out arithmetic are absent.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','proposals','previous-proposals','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.measurements,a.proposals,a.previous_proposals,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'results':[{k:r[k] for k in ['observation_index','radius','unique_targets']} for r in r['results']]}))
