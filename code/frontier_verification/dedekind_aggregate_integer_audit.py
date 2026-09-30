"""Replay every exclusion and dual with integers, then compare held-out fields."""
import argparse,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

BITS=192;GRID=1<<BITS;DUAL_GRID=10**9
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def endpoint(encoded,upper):
    m,e=encoded['mid'];r,f=encoded['rad'];assert r>=0
    exponent=min(e,f);value=(m<<(e-exponent))+(r<<(f-exponent))*(1 if upper else -1)
    shift=exponent+BITS
    if shift>=0:return value<<shift
    divisor=1<<(-shift)
    return -((-value)//divisor) if upper else value//divisor


def integer_rows(data,observation):
    return [{'lo':[max(0,endpoint(w,False)) for w in r['weights']],
             'hi':[endpoint(w,True) for w in r['weights']],
             'rlo':endpoint(r['observations'][observation]['R'],False),
             'rhi':endpoint(r['observations'][observation]['R'],True),
             'tail':endpoint(r['prime_tail'],True)} for r in data['rows']]


def exclusion_gap(row,domains,column,value,side):
    old=domains[column]
    low=sum(w*d[0] for w,d in zip(row['lo'],domains))+row['lo'][column]*(value-old[0])
    high=sum(w*d[-1] for w,d in zip(row['hi'],domains))+row['hi'][column]*(value-old[-1])+row['tail']
    assert side in ['candidate_minimum_above_observation','candidate_maximum_below_observation']
    return low-row['rhi'] if side=='candidate_minimum_above_observation' else row['rlo']-high


def objective_bound(rows,column,certificate,count):
    sign=certificate['sign'];assert sign in [-1,1]
    vector=[0]*count;rhs=0;seen=set()
    for index,value in certificate['multipliers']:
        assert type(index) is int and 0<=index<2*len(rows) and index not in seen;seen.add(index)
        scalar=F(value)*DUAL_GRID;assert scalar.denominator==1 and scalar>=0;scalar=scalar.numerator
        row=rows[index//2]
        coefficients=row['lo'] if index%2==0 else [-v for v in row['hi']]
        b=row['rhi'] if index%2==0 else -row['rlo']+row['tail']
        rhs+=scalar*b;vector=[v+scalar*a for v,a in zip(vector,coefficients)]
    unit=GRID*DUAL_GRID
    residual=[(sign*unit if j==column else 0)-v for j,v in enumerate(vector)]
    correction=4*sum(max(v,0) for v in residual)
    return rhs+correction,unit


def arithmetic_vectors(path,columns):
    data=json.loads(path.read_text());x=sp.symbols('x');vectors={};factorizations=[]
    for label,a in [('A',2),('B',-2)]:
        given=data['fields'][label];assert given['field_discriminant']==576
        models={}
        for p in sorted({c['prime'] for c in columns}):
            c=2 if p==given['power_basis_index'] else 1
            poly=sp.Poly((x*x-x+1+c*c*a)**2-c*c*a*(1-2*x)**2,x)
            index_square=int(sp.discriminant(poly))//576;index=math.isqrt(index_square)
            assert index*index==index_square and index%p
            reduced=sp.Poly(poly,modulus=p);unit,fs=reduced.factor_list();product=sp.Poly(unit,x,modulus=p);model=[]
            for factor,e in fs:
                assert factor.is_irreducible;product*=factor**e;model.append([int(e),int(factor.degree())])
            assert product==reduced;models[p]=model
            factorizations.append({'field':label,'prime':p,'beta_multiplier':c,'index':index,'model':model})
        vector=[sum(f for e,f in models[c['prime']] if c['power']%f==0) for c in columns]
        assert all(0<=v<=4 for v in vector);vectors[label]=vector
        for old in given['prime_power_coefficients']:
            found=[i for i,c in enumerate(columns) if c['n']==old['n']]
            if found:assert vector[found[0]]==old['coefficient']
    assert len(factorizations)==1128
    return vectors,factorizations


def run(measurements,recoveries,arithmetic):
    ds=[json.loads(p.read_text()) for p in measurements];rs=[json.loads(p.read_text()) for p in recoveries]
    columns=ds[0]['columns'];assert len(columns)==604 and all(d['columns']==columns for d in ds)
    truth,factorizations=arithmetic_vectors(arithmetic,columns);results=[];total_exclusions=total_duals=0
    for path,d,r in zip(measurements,ds,rs):
        assert r['measurement_sha256']==sha(path)
        for result in r['results']:
            obs=result['observation_index'];label=['A','B'][obs];rows=integer_rows(d,obs);domains=[list(range(5)) for _ in columns];exclusions=0
            for step in result['monotone_exclusion']['rounds']:
                assert step['prior_domains_sha256']==hashlib.sha256(canonical(domains)).hexdigest();old=[list(x) for x in domains]
                for w in step['removals']:
                    i,c,j=w['column'],w['candidate'],w['measurement_index'];assert columns[i]['n']==w['n'] and c in old[i]
                    assert exclusion_gap(rows[j],old,i,c,w['side'])>0
                    assert c!=truth[label][i];domains[i].remove(c);exclusions+=1
                assert step['remaining_domains_sha256']==hashlib.sha256(canonical(domains)).hexdigest()
            assert domains==[r['candidates'] for r in result['monotone_exclusion']['domains']]
            assert all(v in domain for v,domain in zip(truth[label],domains))
            bounds=[]
            for target in result['dual_targets']:
                column=target['column'];exact=[objective_bound(rows,column,c,len(columns)) for c in target['certificates']]
                candidates=[v for v in range(5) if all(c['sign']*v*unit<=num for c,(num,unit) in zip(target['certificates'],exact))]
                assert candidates==target['candidates'] and truth[label][column] in candidates
                bounds.append({'n':target['n'],'candidates':candidates,'objective_upper_rationals':[str(F(n,u)) for n,u in exact]});total_duals+=2
            # Independent outward-rounded row inequalities retain the full held-out arithmetic.
            for row in rows:
                lower=sum(w*v for w,v in zip(row['lo'],truth[label]));upper=sum(w*v for w,v in zip(row['hi'],truth[label]))
                assert lower<=row['rhi'] and upper+row['tail']>=row['rlo']
            results.append({'measurement_file':path.name,'observation_index':obs,'held_out_field':label,'exclusions':exclusions,
                            'all_604_arithmetic_values_retained':True,'dual_bounds':bounds,
                            'monotone_domains_sha256':hashlib.sha256(canonical(domains)).hexdigest()});total_exclusions+=exclusions
    for a,b in zip(rs[0]['results'],rs[1]['results']):
        assert a['monotone_exclusion']['domains']==b['monotone_exclusion']['domains']
        assert [(r['n'],r['candidates']) for r in a['dual_targets']]==[(r['n'],r['candidates']) for r in b['dual_targets']]
    assert total_exclusions==184 and total_duals==136
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in measurements+recoveries+[arithmetic]},
            'fixed_grid_bits':BITS,'exact_exclusions':total_exclusions,'exact_dual_bounds':total_duals,'independent_polynomial_factorizations':len(factorizations),
            'field_factorizations':factorizations,'arithmetic_vectors':truth,'results':results,
            'scope':'Exact Python integers replay all coefficient deductions after outward conversion of exact dyadic measurements; no interval backend or solver is used for the deductions. Held-out field arithmetic is read only by this auditor, after producer outputs were frozen, and is checked via polynomial factors away from the selected order index. Analytic measurements still depend on their separately audited enclosures.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--measurements',type=Path,nargs=2,required=True);p.add_argument('--recoveries',type=Path,nargs=2,required=True)
    p.add_argument('--arithmetic',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.measurements,a.recoveries,a.arithmetic)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'exclusions':r['exact_exclusions'],'duals':r['exact_dual_bounds'],'factorizations':r['independent_polynomial_factorizations']}))
