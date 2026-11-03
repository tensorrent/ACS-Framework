"""Source-critical strip bootstrap under the unchanged local observation contract."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,arb_mat,ctx
from dedekind_augmented_feature_audit import SPECS,jets,input_geometry
from dedekind_weighted_region_certificate import av,enc,dyadic_upper
from dedekind_signed_corner_audit import validate_exact

ROOT=Path(__file__).absolute().parents[2]
PREVIOUS='docs/frontier/2026-09-14-aggregate-signed-corner-delta/Signed_Corner_Certificate.json'
ANCHOR='docs/frontier/2026-09-14-aggregate-augmented-feature-delta/Augmented_Proposals_Local.json'
REGION='docs/frontier/2026-09-14-aggregate-weighted-feature-delta/Weighted_Region_Certificate.json'
UPPER='docs/frontier/2026-09-14-aggregate-variable-noise-delta/Variable_Noise_Certificate.json'
INPUTS='docs/frontier/2026-09-14-aggregate-equal-population-delta/Equal_Population_Inputs.zip'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def run(root=ROOT):
    paths=[root/p for p in [PREVIOUS,ANCHOR,REGION,UPPER,INPUTS]];prior,a,reg,upper=map(read,paths[:4])
    c,R,v=validate_exact(prior,a,reg,upper)
    with zipfile.ZipFile(paths[4]) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    cc,L,U=input_geometry(data);assert c==cc
    r=U-F('1e-8');gap=L-r;assert gap>0 and F(prior['contract']['root_coordinate_error_radius'])==r
    T=F(upper['best_certified_tau_upper']);Kold=F(prior['corner_uniform_inverse_bound']);assert T==F(prior['inherited_ambiguity_upper_endpoint']) and Kold>0
    aroot=data['E1_224.json']['positive_root_intervals'][1];broot=data['E2_224.json']['positive_root_intervals'][1]
    amin=F(aroot['lo'])-r;bmax=F(broot['hi'])+r;assert amin-bmax==2*gap>0
    cap=2*T*Kold;A=(amin,bmax+cap);B=(amin-cap,bmax);lo,hi=B[0],A[1]
    assert A[0]<=A[1] and B[0]<=B[1] and c[1]-F(1,100)<lo<hi<c[1]+F(1,100)
    directions=[x['endpoint_direction'] for x in prior['uniform_curvature_checks'][0]['columns']]
    assert directions[1]==1 and directions[12]==0 and [i for i,s in enumerate(directions) if s==0]==[12]
    ref=[x+F(1,100)*s for x,s in zip(c,directions)];ref[1]=hi;corner=list(ref);corner[12]=c[12]-F(1,100)
    checks=[]
    for bits in [1024,1536]:
        ctx.prec=bits
        def inverse(y):
            J=arb_mat([[jets(spec,av(x))[1] for x in y] for spec in SPECS]);det=J.det();assert det>0 or det<0
            return J.inv(),det
        Y,det=inverse(ref);u12=sum((Y[12,k]*v[k] for k in range(22)),arb(0));assert u12<0
        Z,cornerdet=inverse(corner);assert (det>0 and cornerdet>0) or (det<0 and cornerdet<0)
        assert all((Z[1,k]>0 if v[k]>0 else Z[1,k]<0) for k in range(22))
        norm=sum((abs(Z[1,k]) for k in range(22)),arb(0));ku=dyadic_upper(norm,100);assert 0<norm<av(ku)
        checks.append({'precision_bits':bits,'face_reference_determinant':enc(det),'face_direction_12':enc(u12),'corner_determinant':enc(cornerdet),
            'corner_critical_inverse_row':[enc(Z[1,k]) for k in range(22)],'corner_norm':enc(norm),'corner_norm_upper':str(ku),'corner_norm_display':float(norm.mid())})
    K=max(F(x['corner_norm_upper']) for x in checks);lower=gap/K
    assert 0<K<Kold and F(prior['uniform_identification_strictly_below'])<lower<T
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in paths},'contract':prior['contract'],
        'critical_index':1,'common_root_center':list(map(str,c)),'source_threshold_lower':str(L),'source_threshold_upper':str(U),'critical_source_gap_lower':str(2*gap),
        'source_A_critical_interval':[aroot['lo'],aroot['hi']],'source_B_critical_interval':[broot['lo'],broot['hi']],
        'necessary_A_critical_lower':str(amin),'necessary_B_critical_upper':str(bmax),
        'bootstrap_feature_budget_cap':str(T),'inherited_uniform_critical_inverse_bound':str(Kold),'critical_difference_cap':str(cap),
        'conditional_A_critical_interval':list(map(str,A)),'conditional_B_critical_interval':list(map(str,B)),
        'critical_column_curve_interval':[str(lo),str(hi)],'critical_strip_half_width_display':float((hi-lo)/2),
        'family':'product_of_closed_column_hulls_with_only_coordinate_1_interval_restricted',
        'family_scope':'all_common_report_pairs_with_feature_budget_at_most_bootstrap_cap',
        'other_coordinate_radius':'1/100','first_replacement_order':[i for i in range(22) if i!=12],
        'face_reference_coordinates':list(map(str,ref)),'corner_coordinates':list(map(str,corner)),
        'last_replacement_coordinate':12,'last_replacement_direction':-1,'checks':checks,'dyadic_rounding_bits':100,
        'conditional_secant_inverse_bound':str(K),'inverse_bound_display':float(K),
        'uniform_identification_strictly_below':str(lower),'guarantee_display':float(lower),'previous_uniform_guarantee':prior['uniform_identification_strictly_below'],
        'new_lower_is_below_bootstrap_cap':True,'original_observation_contract_preserved':True,'entire_bridge_Lean_formalized':False,
        'scope':'The written source-strip bootstrap narrows the critical secant family only for candidate common reports within the inherited budget cap. The new strict lower guarantee lies below that cap, so it applies under the original observation contract without assuming an externally restricted root strip. Inherited family signs plus the new face Cramer sign give the conditional secant constant. Source-feasible sharpness and global recovery remain open.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run();a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['status','critical_strip_half_width_display','inverse_bound_display','guarantee_display']}))
