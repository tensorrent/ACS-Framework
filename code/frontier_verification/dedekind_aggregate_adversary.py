"""Reject leaking inputs and corrupted proofs; replay widened-radius bounds."""
import argparse,ast,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from dedekind_aggregate_measurements import validate
from dedekind_aggregate_integer_audit import integer_rows,objective_bound,exclusion_gap


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def number(s):
    q=F(s);return mp.mpf(q.numerator)/q.denominator


def run(measurements,recovery,radius,inputs):
    d=json.loads(measurements.read_text());r=json.loads(recovery.read_text());noise=json.loads(radius.read_text())
    original=json.loads(inputs[0].read_text());controls=[];noise_replay=[];displaced_checks=0;mp.mp.dps=80
    for name,change in [
        ('field_identity',lambda x:x.update(field='A')),
        ('galois_group',lambda x:x.update(galois_group='V4')),
        ('quadratic_subfields',lambda x:x.update(quadratic_discriminants=[8,-3,-24])),
        ('arithmetic_seed',lambda x:x.update(coefficients={'7':4})),
        ('duplicate_root',lambda x:x['positive_root_intervals'].insert(0,copy.deepcopy(x['positive_root_intervals'][0]))),
        ('reversed_bracket',lambda x:x['positive_root_intervals'][0].update(lo=x['positive_root_intervals'][0]['hi'])),
        ('invalid_cutoff',lambda x:x.update(top=18))]:
        changed=copy.deepcopy(original);change(changed)
        try:validate(changed)
        except (ValueError,AssertionError):controls.append({'mutation':name,'rejected_by':'aggregate input validator','mutated_json_sha256':hashlib.sha256(canonical(changed)).hexdigest()})
        else:raise AssertionError('Accepted '+name)
    target=next(t for t in r['results'][0]['dual_targets'] if t['n']==7);cert=copy.deepcopy(target['certificates'][0]);rows=integer_rows(d,0)
    for name,change in [('negative_multiplier',lambda x:x['multipliers'][0].__setitem__(1,'-1')),
                        ('out_of_range_row',lambda x:x['multipliers'][0].__setitem__(0,2*len(rows))),
                        ('duplicate_multiplier_row',lambda x:x['multipliers'].append(copy.deepcopy(x['multipliers'][0])))]:
        changed=copy.deepcopy(cert);change(changed)
        try:objective_bound(rows,target['column'],changed,len(d['columns']))
        except AssertionError:controls.append({'mutation':name,'rejected_by':'exact integer dual validator','mutated_certificate':changed})
        else:raise AssertionError('Accepted '+name)
    changed=copy.deepcopy(target);changed['candidates']=[3]
    bounds=[objective_bound(rows,target['column'],c,len(d['columns'])) for c in changed['certificates']]
    computed=[v for v in range(5) if all(c['sign']*v*u<=n for c,(n,u) in zip(changed['certificates'],bounds))]
    assert computed!=changed['candidates'] and computed==[4]
    controls.append({'mutation':'false_candidate_list','rejected_by':'independent integer candidate recomputation','claimed':[3],'computed':computed})
    domains=[list(range(5)) for _ in d['columns']];prerequisite=None
    for step in r['results'][0]['monotone_exclusion']['rounds']:
        old=copy.deepcopy(domains)
        for w in step['removals']:
            row=rows[w['measurement_index']];i,c=w['column'],w['candidate']
            actual=exclusion_gap(row,old,i,c,w['side'])
            reset=exclusion_gap(row,[list(range(5)) for _ in domains],i,c,w['side'])
            if actual>0 and reset<=0 and prerequisite is None:
                prerequisite={'mutation':'omit_exclusion_prerequisites','rejected_by':'exact gap after resetting required domains','round':step['round'],'n':w['n'],'candidate':c,'valid_gap':str(actual),'reset_gap':str(reset)}
            domains[i].remove(c)
    assert prerequisite is not None;controls.append(prerequisite)
    for case in noise['results']:
        obs=case['observation_index'];target=next(t for t in r['results'][obs]['dual_targets'] if t['n']==7)
        changed=copy.deepcopy(d)
        for row,wide in zip(changed['rows'],case['measurements']):row['observations'][obs]['R']=wide['R']
        ir=integer_rows(changed,obs);exact=[objective_bound(ir,target['column'],c,len(d['columns'])) for c in target['certificates']]
        candidates=[v for v in range(5) if all(c['sign']*v*u<=n for c,(n,u) in zip(target['certificates'],exact))]
        assert candidates==case['c7_candidates']
        noise_replay.append({'observation_index':obs,'radius':case['radius'],'candidates':candidates,'objective_upper_rationals':[str(F(n,u)) for n,u in exact]})
        rs=json.loads(inputs[obs].read_text())['positive_root_intervals'];centers=[(number(x['lo'])+number(x['hi']))/2 for x in rs];delta=number(case['radius'])
        for row,wide in zip(d['rows'],case['measurements']):
            a=mp.mpf(1)/row['denominator'];u=mp.log(row['center']);p=next(c['prime'] for c in d['columns'] if c['n']==row['center'])
            scale=2*mp.sqrt(mp.pi*a)*mp.sqrt(row['center'])/mp.log(p)
            def h(t):return mp.exp(-a*t*t)*mp.cos(u*t)
            original_sum=2*mp.fsum(h(t) for t in centers)
            for direction in [-1,1]:
                shifted=2*mp.fsum(h(t+direction*delta) for t in centers)
                error=2*scale*len(rs)*delta*(mp.sqrt(2*a/mp.e)+u)
                assert abs(scale*(shifted-original_sum))<=error+mp.mpf('1e-70');displaced_checks+=1
    assert len(controls)==12 and len(noise_replay)==12 and displaced_checks==408
    # Audit the actual function boundary and imports used by the decoder.
    code=Path(__file__).absolute().parent
    tree=ast.parse((code/'dedekind_aggregate_measurements.py').read_text())
    imports=[(n.module,[a.name for a in n.names]) for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
    assert ('dedekind_coefficient_recovery',['gamma','kernel','prime_powers']) in imports
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements,recovery,radius]+inputs},
            'actual_mutations_rejected':len(controls),'controls':controls,'exact_radius_dual_bounds':24,'radius_replays':noise_replay,
            'independent_displaced_sum_controls':displaced_checks,'import_boundary':imports,
            'scope':'Actual input, multiplier and candidate mutations exercise the validators; exact integer replay checks all widened-radius c7 bounds. Uniform displaced sums are numerical controls, while the global derivative inequality supplies the all-displacements bound. Static imports and strict schemas support the data boundary, not a formal information-flow proof.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','recovery','radius','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.measurements,a.recovery,a.radius,a.inputs)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations':r['actual_mutations_rejected'],'radius_duals':r['exact_radius_dual_bounds'],'displaced_sums':r['independent_displaced_sum_controls']}))
