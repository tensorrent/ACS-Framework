"""Independent third derivatives and displaced finite sums for quadratic recovery."""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sp
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_quadratic_ordinate as quad


def mp_exact(x):
    m,e=map(int,x.man_exp());return mp.mpf(m)*mp.power(2,e)
def fraction_exact(x):
    m,e=map(int,x.man_exp());return F(m)*F(2)**e
def inside(value,box):return mp_exact(box.lower())<=value<=mp_exact(box.upper())


def run(prior,result_path):
    start=time.monotonic();raw=result_path.read_bytes();result=json.loads(raw)
    assert result['status']=='passed' and result['precision_bits']==160
    data,powers,rows,seeds,previous,provenance=quad.load(prior,160)
    assert result['provenance']==provenance
    basis,metadata=quad.prepare(data,rows,160);assert metadata==result['basis']
    selected=[r for r in data['roots'] if F(r['hi'])<2000];radius=arb('5e-3')
    boxes=[arb(r['lo']).union(arb(r['hi']))+arb(0,radius.upper()) for r in selected]
    assert core.sha(core.canonical([core.encode(b) for b in boxes]))==metadata['root_boxes_sha256']
    t,a,u=sp.symbols('t a u',real=True);h=sp.exp(-a*t*t)*sp.cos(u*t)
    third=sp.exp(-a*t*t)*((-8*a**3*t**3+12*a*a*t+6*a*u*u*t)*sp.cos(u*t)+(-12*a*a*u*t*t+6*a*u+u**3)*sp.sin(u*t))
    assert sp.simplify(sp.diff(h,t,3)-third)==0
    mp.mp.dps=80;ctx.prec=256;points=[];finite_checks=[]
    for index,(row,b) in enumerate(zip(rows,basis)):
        m=row['metadata']
        if m['n'] not in [2,128,361]:continue
        active=[j for j,s in enumerate(selected) if F(s['hi'])<m['height']]
        samples=sorted({active[0],active[1],active[len(active)//3],active[len(active)//2],active[-1]})
        aa=mp.mpf(1)/m['denominator'];uu=mp.log(m['n']);AA=2*mp.sqrt(mp.pi*aa)*mp.sqrt(m['n'])/mp.log(m['prime'])
        af=arb(1)/m['denominator'];uf=arb(m['n']).log();Af=core.decode(m['scale'])
        def mh(z):return mp.exp(-aa*z*z)*mp.cos(uu*z)
        def ah(z):return (-af*z*z).exp()*(uf*z).cos()
        for j in samples:
            box=boxes[j];tt=mp_exact(box.mid());rr=mp_exact(box.rad())
            curvature=AA*rr*rr*mp.diff(mh,tt,2);assert inside(curvature,b['K'][j])
            third_values=[mp.diff(mh,z,3) for z in [mp_exact(box.lower()),tt,mp_exact(box.upper())]]
            bound=quad.third(af,uf,box).abs_upper()
            assert all(abs(v)<=mp_exact(bound.upper()) for v in third_values)
            points.append({'measurement_index':index,'target':m['n'],'height':m['height'],'root_index':j,
                'normalized_curvature':mp.nstr(curvature,72),'third_derivatives':[mp.nstr(v,60) for v in third_values],
                'curvature_enclosed':True,'third_derivatives_bounded':True})
        if m['height']==2000 and m['n'] in [128,361]:
            mp_actual=mp.mpf(0);mp_polynomial=mp.mpf(0);actual=arb(0);polynomial=arb(0);directions=[]
            for j in active:
                box=boxes[j];t0,r=box.mid(),box.rad();tt,rr=mp_exact(t0),mp_exact(r)
                third_at_center=mp.diff(mh,tt,3);direction=-1 if third_at_center>=0 else 1
                directions.append(direction)
                mp_actual+=2*AA*(mh(tt)-mh(tt+rr*direction))
                mp_polynomial+=-2*AA*rr*mp.diff(mh,tt)*direction-AA*rr*rr*mp.diff(mh,tt,2)
                actual+=2*Af*(ah(t0)-ah(t0+r*direction))
                polynomial+=-b['J'][j]*direction-b['K'][j]
            residual=actual-polynomial;mp_residual=mp_actual-mp_polynomial
            assert inside(mp_actual,actual) and inside(mp_polynomial,polynomial) and inside(mp_residual,residual)
            assert residual>0 and residual.abs_upper()<b['cubic'].upper()
            finite_checks.append({'target':m['n'],'height':2000,'roots':len(active),'directions':directions,
                'direction_rule':'Opposite sign of independently computed center third derivative; every direction is an allowed endpoint displacement.',
                'mp_actual_observation_change':mp.nstr(mp_actual,72),'mp_quadratic_prediction':mp.nstr(mp_polynomial,72),
                'mp_residual':mp.nstr(mp_residual,72),'actual_change':core.encode(actual),'quadratic_prediction':core.encode(polynomial),
                'strictly_positive_cubic_residual':core.encode(residual),'certified_cubic_allowance':core.encode(b['cubic']),
                'scope':'An allowed vector of ordinate displacements checks the Taylor model; it is not asserted to be a number-field spectrum.'})
        print(json.dumps({'event':'independent_cubic_checks','height':m['height'],'target':m['n'],'samples':len(samples)}),flush=True)
    assert len(points)==75 and len(finite_checks)==2
    # Use a retained nonzero signed combination to show why endpoints alone
    # do not give the maximum of a concave scalar quadratic.
    proposals=result['proposals'] if 'proposals' in result else [c for step in result['rounds'] for check in step['checks'] for c in check['certificates']]
    witness=None;visited=set();scalar_checks=[]
    for p in proposals:
        key=p['combination_sha256']
        if key in visited or not p['multipliers']:continue
        visited.add(key);alpha=[F(0)]*len(rows)
        for i,v in p['multipliers']:alpha[i]=F(v)
        combo=quad.combine(rows,basis,alpha)
        for j,(d,e) in enumerate(zip(combo['noise'],combo['curve'])):
            support,independent,kind=quad.scalar_support(d,e)
            if kind!='interior_vertex' or not e>0:continue
            vertex=-d/(2*e)
            if not(vertex.lower()>-1 and vertex.upper()<1):continue
            value=-d*vertex-e*vertex*vertex
            endpoint=max(arb(0),(-d-e).upper(),(d-e).upper());excess=value-endpoint
            if excess>0:
                witness={'source_combination_sha256':key,'root_index':j,'linear_coefficient':core.encode(d),'quadratic_coefficient':core.encode(e),
                    'interior_vertex':core.encode(vertex),'vertex_value':core.encode(value),'endpoint_and_zero_upper':core.encode(endpoint),
                    'strict_excess_over_endpoints':core.encode(excess),'certified_support_upper':core.encode(support.upper())}
                assert value.upper()<=support.upper() or value.overlaps(support)
                # Independent scalar maximization uses interval midpoint
                # coefficients; its precision check is explicitly scalar.
                dd,ee=mp_exact(d.mid()),mp_exact(e.mid());vv=-dd/(2*ee)
                maximum=max(mp.mpf(0),-dd-ee,dd-ee,-dd*vv-ee*vv*vv)
                exact_d,exact_e=fraction_exact(d.mid()),fraction_exact(e.mid())
                exact_maximum=exact_d*exact_d/(4*exact_e)
                assert exact_maximum<=fraction_exact(support.upper())
                reference=mp.mpf(exact_maximum.numerator)/exact_maximum.denominator
                assert abs(maximum-reference)<abs(reference)*mp.mpf('1e-70')
                assert maximum<=mp_exact(support.upper())
                scalar_checks.append({'root_index':j,'mp_vertex':mp.nstr(vv,60),'mp_maximum':mp.nstr(maximum,60),
                    'exact_midpoint_maximum':str(exact_maximum),'certified_upper':core.encode(support.upper())})
                break
        if witness:break
    assert witness and scalar_checks
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'basis_source_sha256':core.sha(Path(quad.__file__).read_bytes()),
        'input_result_sha256':core.sha(raw),'input_result_name':result_path.name,'symbolic_third_derivative_identity':True,
        'mpmath_digits':80,'derivative_cases':points,'displaced_finite_sums':finite_checks,'scalar_maximum_checks':scalar_checks,
        'adversarial_controls':{'omitted_cubic_remainder':'Both full displaced finite sums have a strictly positive, certified residual beyond the quadratic prediction.',
            'omitted_interior_vertex':witness},'elapsed_seconds':time.monotonic()-start,
        'scope':'Independent symbolic third derivative and mpmath curvature/third-derivative calculations, plus two full nonlinear displaced sums. Arb enclosures share the input basis. The scalar vertex counterexample concerns the quadratic support lemma, not alternate number fields.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--result',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.prior,a.result);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'derivative_cases':len(r['derivative_cases']),'full_displaced_sums':len(r['displaced_finite_sums'])}))
