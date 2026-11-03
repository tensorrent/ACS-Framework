"""Independent local catalogues, exact exclusion replay and assumption counterexamples."""
import argparse,ast,itertools,json,time,warnings
from fractions import Fraction as F
from pathlib import Path
from flint import ctx
from sympy import Poly,symbols,discriminant,prod,simplify,diff
import dedekind_coupled_recovery as core
from dedekind_coupled_audit import integers,gap
from dedekind_recovery_audit import ordered_models
import dedekind_local_noise as producer

def exact(x):
    m,e=map(int,x.man_exp());return F(m)*F(2)**e
def dyadic(x):return tuple(map(int,x.man_exp()))
def signed_sum(terms):
    terms=[(m,e) for m,e in terms if m]
    if not terms:return 0,0
    exponent=min(e for m,e in terms)
    return sum(m<<(e-exponent) for m,e in terms),exponent
def at_least_grid(n,e,lower):
    return (n<<(e+192))>=lower if e+192>=0 else n>=(lower<<(-e-192))
def key(c):return c['label'],c['delta'],c['top'],c['profile']
def read(p):return json.loads(p.read_text())

def run(directory,prior):
    start=time.monotonic();names=['Local_Noise160.json','Local_Noise224.json'];raws={n:(directory/n).read_bytes() for n in names}
    results={n:json.loads(raw) for n,raw in raws.items()};truth=read(prior.parent/'2026-09-13-coupled-delta/Exact_Audit.json')['relaxation_ambiguity']['baseline_coefficients']
    models=sorted(ordered_models(False)|ordered_models(True))
    homogeneous={tuple([(e,f)]*g) for e,f,g in itertools.product(range(1,5),repeat=3) if e*f*g==4}
    assert len(models)==11 and {m for m in models if len(set(m))==1}==homogeneous
    def coef(model,k):return sum(f for e,f in model if k%f==0)
    x=symbols('x');identities=[]
    for i,model in enumerate(models):
        polynomial=prod(1-x**f for e,f in model)
        right=sum(f*x**f/(1-x**f) for e,f in model)
        assert simplify(-x*diff(polynomial,x)/polynomial-right)==0
        identities.append({'model_id':i,'euler_denominator':str(polynomial),'logarithmic_derivative_identity':True,
            'first_twelve_coefficients':[coef(model,k) for k in range(1,13)]})
    def eligible(p,profile):
        selected=homogeneous if profile.startswith('galois') else set(models)
        if profile.endswith('discriminant'):selected={m for m in selected if any(e!=1 for e,f in m)==(125%p==0)}
        return [i for i,m in enumerate(models) if m in selected]
    records=[];local_total=0;spectral_total=0;minimal_total=0;missing=None;largest_denominator_bits=0
    for bits in [160,224]:
        name='Local_Noise'+str(bits)+'.json';result=results[name]
        assert result['status']=='passed' and result['source_sha256']==core.sha(Path(producer.__file__).read_bytes())
        assert result['profiles_source_sha256']==core.sha(Path(producer.local.__file__).read_bytes())
        assert result['catalogue']==[list(map(list,m)) for m in models]
        assert result['assumption_profiles']=={p:{'degree':4,'galois_extension':p.startswith('galois'),
            'use_discriminant_to_label_ramified_primes':p.endswith('discriminant')} for p in ['degree','degree_discriminant','galois','galois_discriminant']}
        data,powers,source_cases,inputs,measurement_hash=producer.load_inputs(directory,prior,bits)
        assert result['inputs']==inputs and result['measurement_input_sha256']==measurement_hash
        by={(c['label'],c['delta'],c['top']):c for c in source_cases}
        groups={p:[j for j,(_,q,_) in enumerate(powers) if q==p] for p in sorted({p for n,p,k in powers})}
        for case in result['cases']:
            source=by[case['label'],case['delta'],case['top']];seeds=[r['candidates'] for r in source['seed_domains']];domains=[list(d) for d in seeds]
            assert case['seed_domains']==source['seed_domains'] and case['source_sha256']==source['source_sha256']
            assert case['seed_domain_hash']==core.sha(core.canonical(source['seed_domains']))
            rows=source['rows'];ir=integers(rows);profile=case['profile']
            assert case['integer_rows_sha256']==core.sha(core.canonical(ir))
            assert case['measurements_sha256']==core.sha(core.canonical([r['metadata'] for r in rows])) and case['measurement_count']==len(rows)
            lc=sc=0;observed_minima=[]
            for step in case['rounds']:
                old=[list(d) for d in domains];assert step['prior_domains_sha256']==core.sha(core.canonical(old))
                expected=[list(d) for d in old];all_kept={}
                for p,columns in groups.items():
                    kept=[i for i in eligible(p,profile) if all(coef(models[i],powers[j][2]) in old[j] for j in columns)]
                    assert kept;all_kept[p]=kept
                    for j in columns:expected[j]=sorted({coef(models[i],powers[j][2]) for i in kept})
                middle=[list(d) for d in old];seen=set()
                for check in step['local_checks']:
                    p=check['prime'];assert p not in seen;seen.add(p);columns=groups[p];initial=eligible(p,profile);kept=all_kept[p]
                    assert check['eligible_model_ids']==initial and check['retained_model_ids']==kept
                    rejected={r['model_id']:r['witness_column'] for r in check['rejected_models']}
                    assert set(rejected)==set(initial)-set(kept)
                    for i,j in rejected.items():assert j in columns and coef(models[i],powers[j][2]) not in old[j]
                    for change in check['changes']:
                        j=change['column'];assert powers[j][1]==p and powers[j][0]==change['n']
                        assert change['before']==old[j] and change['after']==expected[j]
                        assert truth[j] in change['after'];lc+=len(old[j])-len(expected[j]);middle[j]=expected[j]
                assert middle==expected and step['after_local_domains_sha256']==core.sha(core.canonical(middle))
                if step['round']==1:
                    assert case['local_only_domains_sha256']==core.sha(core.canonical(middle))
                    assert case['local_only_unique_targets']==sum(len(d)==1 for (n,p,k),d in zip(powers,middle) if n<=361)
                domains=[list(d) for d in middle];rational_cache={}
                for witness in step['spectral_checks']:
                    i,c,j=witness['column'],witness['candidate'],witness['measurement_index'];side=witness['side']
                    assert c in domains[i] and powers[i][0]==witness['n'] and c!=truth[i]
                    integer_gap=gap(ir[j],middle,i,c,side);assert integer_gap==int(witness['strict_gap_scaled_integer'])>0
                    if j not in rational_cache:
                        row=rows[j];lo=[dyadic(w.lower()) for w in row['weights']];hi=[dyadic(w.upper()) for w in row['weights']]
                        rational_cache[j]=(lo,hi,dyadic(row['R'].lower()),dyadic(row['R'].upper()),dyadic(row['B'].upper()))
                    lo,hi,rlo,rhi,tail=rational_cache[j]
                    if side=='candidate_minimum_above_observation':
                        terms=[(m*(c if k==i else d[0]),e) for k,((m,e),d) in enumerate(zip(lo,middle))]+[(-rhi[0],rhi[1])]
                    else:
                        terms=[(-m*(c if k==i else d[-1]),e) for k,((m,e),d) in enumerate(zip(hi,middle))]+[rlo,(-tail[0],tail[1])]
                    numerator,exponent=signed_sum(terms)
                    assert numerator>0 and at_least_grid(numerator,exponent,integer_gap)
                    largest_denominator_bits=max(largest_denominator_bits,-exponent)
                    if missing is None:
                        reset=gap(ir[j],[list(range(5)) for _ in middle],i,c,side)
                        if reset<=0:missing={'case':list(key(case)),'precision_bits':bits,'round':step['round'],'witness':witness,
                            'certified_gap_lower_bound':str(F(integer_gap,1<<192)),
                            'full_exact_dyadic_gap_at_least_lower_bound':True,'exact_common_exponent':exponent,
                            'exact_numerator_bits':numerator.bit_length(),'missing_prerequisite_gap_scaled_integer':str(reset)}
                    domains[i].remove(c);sc+=1
                assert step['remaining_domains_sha256']==core.sha(core.canonical(domains))
                assert all(t in d for t,d in zip(truth,domains))
            assert domains==[r['candidates'] for r in case['domains']]
            assert case['rounds'][-1]['prior_domains_sha256']==case['rounds'][-1]['remaining_domains_sha256']
            assert case['unique_target_coefficients']==sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361)
            assert case['unique_support_coefficients']==sum(len(d)==1 for d in domains)
            final_models=[]
            for p,columns in groups.items():
                kept=[i for i in eligible(p,profile) if all(coef(models[i],powers[j][2]) in domains[j] for j in columns)]
                final_models.append({'prime':p,'retained_model_ids':kept})
            assert case['local_models']==final_models
            assert case['unique_target_prime_local_models']==sum(len(m['retained_model_ids'])==1 for m in final_models if m['prime']<=361)
            for certificate in case['minimal_quadratic_seed_observations']:
                column=certificate['column'];n,p,k=powers[column];columns=groups[p];initial=eligible(p,profile);answer=certificate['answer']
                bad={i for i in initial if coef(models[i],k)!=answer}
                ruled_out={j:{i for i in initial if coef(models[i],powers[j][2]) not in seeds[j]} for j in columns}
                examined=0;matches=None
                for size in range(len(columns)+1):
                    sufficient=[]
                    for subset in itertools.combinations(columns,size):
                        examined+=1;removed=set().union(*(ruled_out[j] for j in subset))
                        survivors=set(initial)-removed
                        if survivors and bad<=removed:sufficient.append(subset)
                    if sufficient:matches=sufficient;break
                assert size==certificate['minimum_observation_count'] and len(matches)==certificate['minimum_size_witness_sets']
                assert examined==certificate['subsets_checked_through_minimum_size'] and list(matches[0])==certificate['witness_columns']
                assert [powers[j][0] for j in matches[0]]==certificate['witness_prime_powers']
                minimal_total+=1;observed_minima.append({'n':n,'minimum_observation_count':size,'witness_prime_powers':certificate['witness_prime_powers'],
                    'alternative_minimum_sets':len(matches),'subsets_checked':examined})
            local_total+=lc;spectral_total+=sc
            records.append({'case':list(key(case)),'precision_bits':bits,'local_candidates_removed':lc,'spectral_candidates_removed':sc,
                'domains_sha256':core.sha(core.canonical(domains)),'all_604_arithmetic_coefficients_retained':True,'minimum_observation_checks':observed_minima})
        print(json.dumps({'event':'local_profile_replay','bits':bits,'local_exclusions':local_total,'spectral_exclusions':spectral_total}),flush=True)
    low={key(c):c for c in results['Local_Noise160.json']['cases']};high={key(c):c for c in results['Local_Noise224.json']['cases']}
    assert low.keys()==high.keys() and all(low[k]['domains']==high[k]['domains'] and low[k]['local_models']==high[k]['local_models'] for k in low)
    inclusions=0
    for cases in [low,high]:
        for label,delta,top,_ in cases:
            def contained(a,b):
                nonlocal inclusions
                assert all(set(x['candidates'])<=set(y['candidates']) for x,y in zip(cases[label,delta,top,a]['domains'],cases[label,delta,top,b]['domains']));inclusions+=1
            if _!='degree':continue
            for a,b in [('degree_discriminant','degree'),('galois','degree'),('galois_discriminant','degree_discriminant'),('galois_discriminant','galois')]:contained(a,b)
    # A concrete non-Galois quartic has local type (1,3), which must remain
    # eligible until the Galois premise is explicitly introduced.
    polynomial=Poly(x**4-x-1,x);assert Poly(polynomial,x,modulus=2).is_irreducible
    disc=int(discriminant(polynomial.as_expr(),x));assert disc==-283 and disc%7
    with warnings.catch_warnings():
        warnings.simplefilter('ignore');unit,factors=Poly(polynomial,x,modulus=7).factor_list()
    rebuilt=Poly(unit,x,modulus=7)
    for f,e in factors:rebuilt*=f**e
    assert rebuilt==Poly(polynomial,x,modulus=7)
    counter_model=tuple(sorted((int(e),int(f.degree())) for f,e in factors));assert counter_model==((1,1),(1,3))
    assert counter_model in models and counter_model not in homogeneous and coef(counter_model,1)==1
    # The ramification exponent does not multiply the logarithmic derivative
    # coefficient. The ramified profile e=4,f=1 has every coefficient equal to 1.
    ramified=((4,1),);assert ramified in models and coef(ramified,1)==1
    wrong=sum(e*f for e,f in ramified if 1%f==0);assert wrong==4
    assert missing
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),
        'producer_sha256':core.sha(Path(producer.__file__).read_bytes()),'profiles_source_sha256':core.sha(Path(producer.local.__file__).read_bytes()),
        'results_sha256':{n:core.sha(raw) for n,raw in raws.items()},'independent_catalogue':[list(map(list,m)) for m in models],
        'galois_models_from_integer_triples':[list(map(list,m)) for m in sorted(homogeneous)],'symbolic_euler_identities':identities,
        'replays':records,'local_candidate_exclusions':local_total,'spectral_candidate_exclusions':spectral_total,
        'exact_dyadic_sum_method':'Align nonzero mantissas at the least exponent and add shifted signed integers. No term is discarded or rounded.',
        'largest_exact_common_denominator_bits':largest_denominator_bits,
        'minimal_observation_certificates':minimal_total,'precision_domain_comparisons':len(low),'assumption_inclusion_comparisons':inclusions,
        'adversarial_controls':{'unsupported_galois_premise':{'polynomial':str(polynomial.as_expr()),'irreducible_modulus':2,
            'polynomial_discriminant':disc,'unramified_prime':7,'factors':[{'polynomial':str(f.as_expr()),'multiplicity':int(e),'degree':int(f.degree())} for f,e in factors],
            'local_model':list(map(list,counter_model)),'first_coefficient':1,'rejected_by_unsupported_galois_condition':True,
            'scope':'Irreducibility modulo 2 proves a quartic field; 7 does not divide its polynomial discriminant, so the squarefree mod-7 pattern gives residue degrees 1 and 3. This excludes normality of the degree-four field.'},
            'ramification_exponent_in_coefficient':{'model':[[4,1]],'correct_coefficient':1,'incorrect_multiplicity_weighted_coefficient':4},
            'missing_domain_prerequisites':missing},'elapsed_seconds':time.monotonic()-start,
        'scope':'Independent ordered-composition catalogue and Galois integer triples, symbolic rational-function identities, exact dyadic spectral inequalities, held-out arithmetic and exhaustive minimum-observation hitting sets. Analytic row reconstruction shares the pinned loader; the separate wide-range audit checks its new scalar ranges.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--prior',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.directory,a.prior);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':len(r['replays']),'local_exclusions':r['local_candidate_exclusions'],'spectral_exclusions':r['spectral_candidate_exclusions']}))
