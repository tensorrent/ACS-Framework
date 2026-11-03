"""Reject missing corner-proof premises and check exact counterexamples to shortcuts."""
import argparse, copy, hashlib, json
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from flint import fmpq, fmpq_mat
from dedekind_signed_corner_audit import validate_exact, read, ROOT, ANCHOR, REGION, UPPER

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(data,path,value):
    for k in path[:-1]:data=data[k]
    data[path[-1]]=value

def controls():
    I=fmpq_mat([[1,0],[0,1]]);A=fmpq_mat([[2,0],[1,1]]);B=I;X=A.inv();Y=B.inv();D=A-B
    v=fmpq_mat([[1],[1]]);d=fmpq_mat([[1],[1]])
    actual=(X*v-Y*v)[0,0];correct=-(X*d)[0,0]*(Y*v)[0,0];wrong=-(X*d)[0,0]*(X*v)[0,0]
    assert X-Y==-X*D*Y and actual==correct and actual!=wrong
    def replace(M,j,z):return fmpq_mat([[z[i] if k==j else M[i,k] for k in range(2)] for i in range(2)])
    rhs=[-1,1];assert replace(A,0,rhs).det()==replace(B,0,rhs).det()==-1
    assert (X*fmpq_mat([[x] for x in rhs]))[0,0]<0 and (Y*fmpq_mat([[x] for x in rhs]))[0,0]<0
    assert replace(A,1,rhs).det()!=replace(B,1,rhs).det()
    neg=-I;assert I.det()==neg.det()==1 and (I+neg).det()==0
    q=F(-1,4);base=F(1);delta=abs(q-base);penalty=2*max(F(0),delta-abs(base))
    assert abs(q)==q+penalty and abs(q)>q
    assert F(1,3)-1<0 and F(-2)<F(1,2)  # B=-2 violates nonnegativity despite a small signed row sum.
    eta=F(1,100);actual_curvature=56*eta**6;correct_remainder=F(factorial(8),factorial(6))*eta**6
    assert actual_curvature==correct_remainder>F(factorial(8),factorial(7))*eta**6
    # g'(t)=1+t^2 on [-1,1] has endpoint inverse 1/2 but center inverse 1.
    assert F(1,1)>F(1,2)
    # A linear functional bound extends to convex weights, not arbitrary affine weights.
    assert 2*1+(-1)*0>1 and F(1,3)*1+F(2,3)*0<=1
    # A fixed numerator can change quotient sign if determinant orientation changes.
    assert F(-1)/1<0<F(-1)/(-1)
    return [
        {'name':'finite_inverse_step_uses_old_direction_factor','actual':str(actual),'correct':str(correct),'wrong_new_direction':str(wrong)},
        {'name':'Cramer_numerator_independent_of_replaced_column_only','fixed_numerator':'-1','wrong_column_numerator_changes':True},
        {'name':'same_sign_nonsingular_endpoints_do_not_prove_nonsingular_hull','endpoint_determinants':['1','1'],'midpoint_determinant':'0'},
        {'name':'signed_row_bound_requires_flip_penalty','row_value':str(q),'absolute_value':str(abs(q)),'necessary_penalty':str(penalty)},
        {'name':'negative_B_invalidates_positive_resolvent_logic','B':'-2','resolvent_minus_identity':'-2/3'},
        {'name':'eighth_derivative_remainder_needs_six_factorial','polynomial':'t^8','exact_curvature':str(actual_curvature),'underestimate_with_7_factorial':str(correct_remainder/7)},
        {'name':'endpoint_inverse_values_without_monotonicity_miss_interior_maximum','derivative':'1+t^2','endpoint_inverse':'1/2','center_inverse':'1'},
        {'name':'negative_affine_weights_do_not_preserve_endpoint_bounds','weights':['2','-1'],'values':['1','0'],'combination':'2','endpoint_upper':'1'},
        {'name':'quotient_sign_transfer_requires_denominator_orientation','numerator':'-1','denominators':['1','-1'],'quotients':['-1','1']},
    ]

def run(certificate,root=ROOT):
    paths=[root/p for p in [ANCHOR,REGION,UPPER]];a,reg,upper=map(read,paths);cert=read(certificate)
    validate_exact(cert,a,reg,upper)
    mutations=[
        ('pointwise_family_substitution',['matrix_family'],'pointwise_Jacobians_only'),
        ('omitted_secant_bridge',['secants_in_family'],False),
        ('overstated_formalization',['entire_bridge_Lean_formalized'],True),
        ('unsupported_threshold_sharpness',['optimal_source_feasible_threshold_proved'],True),
        ('changed_coordinate_region',['contract','observed_root_region_radius'],'3/100'),
        ('raw_roots_added',['contract','raw_roots_or_counts_released'],True),
        ('feature_order_swapped',['contract','features',0,'center'],3),
        ('critical_index_changed',['critical_index'],12),
        ('inverse_row_sign_flipped',['critical_sign_vector',0],-cert['critical_sign_vector'][0]),
        ('negative_resolvent_row',['signed_regions',0,'resolvent_minus_identity_row',0],'-1'),
        ('broken_exact_residual',['signed_regions',0,'positive_resolvent_critical_row',1],'1'),
        ('undersized_direction_supersolution',['signed_regions',0,'signed_vector_supersolution',1],'1'),
        ('omitted_large_region_flip_penalty',['signed_regions',1,'sign_flip_penalty'],'0'),
        ('wrong_Taylor_orders',['curvature_Taylor_orders'],list(range(1,7))),
        ('missing_eighth_derivative',['curvature_remainder_derivative_order'],7),
        ('wrong_remainder_power',['curvature_remainder_power'],7),
        ('wrong_remainder_factorial',['curvature_remainder_factorial'],5040),
        ('curvature_sign_flipped',['uniform_curvature_checks',0,'columns',0,'curvature_sign'],-cert['uniform_curvature_checks'][0]['columns'][0]['curvature_sign']),
        ('uncertified_global_direction_12',['uniform_curvature_checks',0,'columns',12,'inverse_direction_sign'],-1),
        ('opposite_endpoint',['uniform_curvature_checks',0,'columns',0,'endpoint_direction'],-cert['uniform_curvature_checks'][0]['columns'][0]['endpoint_direction']),
        ('coordinate_12_replaced_too_early',['first_replacement_order'],list(range(21))),
        ('face_sign_claimed_globally',['last_direction_scope'],'entire_matrix_family'),
        ('wrong_last_endpoint',['last_replacement_direction'],1),
        ('nonnegative_face_reference',['corner_checks',0,'reference_direction_12'],{'mid':[1,0],'rad':[0,0]}),
        ('determinant_enclosure_contains_zero',['corner_checks',0,'reference_determinant'],{'mid':[0,0],'rad':[1,0]}),
        ('corner_norm_understated',['corner_uniform_inverse_bound'],'55'),
        ('guarantee_overstated',['uniform_identification_strictly_below'],'2e-10'),
        ('upper_endpoint_changed',['inherited_ambiguity_upper_endpoint'],'2e-10'),
    ]
    results=[]
    for name,path,value in mutations:
        changed=copy.deepcopy(cert);put(changed,path,value)
        try:validate_exact(changed,a,reg,upper)
        except (AssertionError,ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):results.append({'mutation':name,'rejected':True})
        else:raise AssertionError('accepted invalid premise: '+name)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in paths+[certificate]},
        'mutations_rejected':len(results),'mutations':results,'exact_counterexample_controls':controls(),
        'scope':'Twenty-eight premise mutations and nine exact algebraic controls. These exercise the proof conditions; they are not an exhaustive audit or a replacement for the analytic closed-hull/secant proof. The polar map (exp(x)cos(y),exp(x)sin(y)) on [0,1] x [0,2*pi] additionally illustrates in the written audit why everywhere nonsingular pointwise derivatives do not imply a global inverse bound.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.certificate);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations_rejected':r['mutations_rejected'],'exact_controls':len(r['exact_counterexample_controls'])}))
