"""Per-ordinate derivative and stationary-point ranges for Gaussian measurements.

Critical points are isolated through the strictly increasing phase
theta(t)=u*t+atan(2*a*t/u). There are no field-specific arithmetic seeds.
"""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
import dedekind_coupled_recovery as core

HEIGHTS=[220,600,1000,1500,2000]


def h(a,u,t):return (-a*t*t).exp()*(u*t).cos()
def hp(a,u,t):return (-a*t*t).exp()*(-2*a*t*(u*t).cos()-u*(u*t).sin())
def phase(a,u,t):return u*t+(2*a*t/u).atan()


def root_boxes(data,top,delta):
    radius=arb(delta)
    rows=[r for r in data['roots'] if F(r['hi'])<top]
    boxes=[arb(r['lo']).union(arb(r['hi']))+arb(0,radius.upper()) for r in rows]
    assert all(b.lower()>0 and b.upper()<top for b in boxes)
    return boxes


def critical(a,u,k,cache):
    if k in cache:return cache[k]
    assert k>=1 and 2*a/(u*u)<1
    # The phase has exactly one positive root at k*pi. atan is between
    # zero and pi/2, so this initial interval contains it.
    t=((k-arb('1/2'))*arb.pi()/u).union(k*arb.pi()/u)
    for iteration in range(50):
        t=(k*arb.pi()-(2*a*t/u).atan())/u
        assert t.lower()>0
        if t.rad()<arb('1e-34'):break
    else:raise AssertionError('Critical-point contraction needs more iterations')
    # At the phase root, cos(u*t)=(-1)^k/sqrt(1+(2*a*t/u)^2).
    ratio=2*a*t/u
    transformed=((-1)**k)*(-a*t*t).exp()/(1+ratio*ratio).sqrt()
    direct=h(a,u,t);assert direct.overlaps(transformed)
    value=direct.intersection(transformed)
    result={'point':t,'value':value,'iterations':iteration+1}
    cache[k]=result;return result


def finite_ranges(boxes,a,u):
    derivative_sum=arb(0);direct_sum=arb(0);lower_sum=arb(0);upper_sum=arb(0)
    cache={};critical_boxes=0;edge_boxes=0;hash_rows=[]
    for box in boxes:
        lo,hi=box.lower(),box.upper()
        derivative=hp(a,u,box).abs_upper();derivative_sum+=derivative
        direct_sum+=2*h(a,u,box)
        candidates=[h(a,u,lo),h(a,u,hi)]
        kmin=int((phase(a,u,lo)/arb.pi()).lower().ceil().unique_fmpz())
        kmax=int((phase(a,u,hi)/arb.pi()).upper().floor().unique_fmpz())
        assert kmax-kmin<=1
        included=[]
        for k in range(max(1,kmin),kmax+1):
            result=critical(a,u,k,cache)
            if result['point'].overlaps(box):
                candidates.append(result['value']);included.append(k)
                if not box.contains(result['point']):edge_boxes+=1
        critical_boxes+=bool(included)
        lower=min(v.lower() for v in candidates);upper=max(v.upper() for v in candidates)
        lower_sum+=2*lower;upper_sum+=2*upper
        hash_rows.append({'box':core.encode(box),'derivative_upper':core.encode(derivative),
                          'lower':core.encode(lower),'upper':core.encode(upper),'critical_indices':included})
    # Each sum endpoint is kept separately before constructing a display/solver
    # ball; Arb radius rounding must not define the precision of the endpoints.
    sharp=lower_sum.lower().union(upper_sum.upper())
    assert sharp.overlaps(direct_sum)
    return {'derivative_sum':derivative_sum,'direct_sum':direct_sum,'sharp_sum':sharp,
            'lower_sum':lower_sum,'upper_sum':upper_sum,
            'critical_boxes':critical_boxes,'critical_edge_boxes':edge_boxes,
            'per_root_ranges_sha256':core.sha(core.canonical(hash_rows)),
            'critical_points':[{'k':k,'point':core.encode(v['point']),'value':core.encode(v['value']),
                                'iterations':v['iterations']} for k,v in sorted(cache.items())]}


def prepare(data,top,bits,delta):
    powers,base_rows,settings=core.prepare(data,top,bits,delta)
    boxes=root_boxes(data,top,delta);radius=arb(delta)
    rowsets={name:[] for name in ['global','derivative','direct','stationary']};diagnostics=[]
    for row in base_rows:
        item=row['metadata'];a=arb(1)/item['denominator'];u=arb(item['n']).log();A=core.decode(item['scale'])
        ranges=finite_ranges(boxes,a,u)
        derivative_error=2*A*radius*ranges['derivative_sum']
        global_error=core.decode(item['input_error'])
        # Both are valid; preserve the old bound if interval dependency makes
        # the per-root derivative expression less useful in an extreme case.
        chosen=min(derivative_error.upper(),global_error.upper())
        zero_error=core.decode(item['zero_error']);background=arb(item['pole'])+arb(item['discriminant_term'])+arb(item['gamma'])
        R0=core.decode(item['R0'])
        observations={'global':row['R'],'derivative':R0+arb(0,(chosen+zero_error).upper()),
                      'direct':A*(background-ranges['direct_sum'])+arb(0,zero_error.upper()),
                      'stationary':A*(background-ranges['sharp_sum'])+arb(0,zero_error.upper())}
        # The independent expressions enclose the same finite value. Their
        # intersection is safe, but each method is retained separately here.
        assert all(observations['global'].overlaps(R) for R in observations.values())
        for method,R in observations.items():
            metadata={**item,'R':core.encode(R),'range_method':method}
            rowsets[method].append({'weights':row['weights'],'R':R,'B':row['B'],'metadata':metadata})
        diagnostics.append({'target':item['n'],'height':top,'denominator':item['denominator'],
                            'global_input_error':core.encode(global_error),'derivative_input_error':core.encode(derivative_error),
                            'chosen_derivative_error':core.encode(chosen),'direct_zero_sum':core.encode(ranges['direct_sum']),
                            'stationary_zero_sum':core.encode(ranges['sharp_sum']),
                            'stationary_lower_sum':core.encode(ranges['lower_sum']),
                            'stationary_upper_sum':core.encode(ranges['upper_sum']),
                            'critical_boxes':ranges['critical_boxes'],'critical_edge_boxes':ranges['critical_edge_boxes'],
                            'critical_points':ranges['critical_points'],'per_root_ranges_sha256':ranges['per_root_ranges_sha256']})
    return powers,rowsets,settings,diagnostics


def run(path,bits,deltas,methods):
    raw=path.read_bytes();data=json.loads(raw);results=[];bounds=[]
    for delta in deltas:
        available={m:[] for m in methods}
        for top in HEIGHTS:
            start=time.monotonic();powers,rowsets,settings,diagnostics=prepare(data,top,bits,delta)
            bounds.append({'settings':settings,'additional_radius':delta,'diagnostics':diagnostics,
                           'measurements_by_method':{m:[r['metadata'] for r in rowsets[m]] for m in methods}})
            for method in methods:
                available[method]+=rowsets[method]
                for policy,rows in [('single_cutoff',rowsets[method]),('retained_prefix',available[method])]:
                    result=core.eliminate(powers,rows);assert result['status']=='passed',result
                    results.append({'settings':settings,'additional_radius':delta,'method':method,'policy':policy,
                                    'measurement_count':len(rows),'measurements_sha256':core.sha(core.canonical([r['metadata'] for r in rows])),**result})
            print(json.dumps({'delta':delta,'height':top,'counts':{m:{p:next(r['unique_target_coefficients'] for r in reversed(results) if r['method']==m and r['policy']==p) for p in ['single_cutoff','retained_prefix']} for m in methods},
                              'elapsed_seconds':time.monotonic()-start}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'core_sha256':core.sha(Path(core.__file__).read_bytes()),
            'input_sha256':core.sha(raw),'precision_bits':bits,'methods':methods,'bounds':bounds,'cases':results,
            'scope':'Additional independent ordinate-box uncertainty with fixed certified membership. Finite Gaussian sums are enclosed by global/individual derivative and endpoint/critical-point routes. Shared zero/prime tail bounds remain unconditional; no local arithmetic seeds.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--deltas',nargs='+',default=['5e-6','5e-5','5e-4','5e-3'])
    p.add_argument('--methods',nargs='+',choices=['global','derivative','direct','stationary'],default=['global','derivative','stationary'])
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.input,a.precision,a.deltas,a.methods)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
