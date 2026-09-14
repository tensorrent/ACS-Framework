"""Certify source-feasible pairs with one free A or B root per noncritical coordinate."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,arb_mat,ctx
from dedekind_augmented_feature_proposal import FEATURES
from dedekind_augmented_feature_certificate_v2 import kernel
from dedekind_augmented_feature_audit import input_geometry
from dedekind_feature_certificate import coordinate_audit
from dedekind_weighted_region_certificate import av,enc

ROOT=Path(__file__).absolute().parents[2]
PRIOR='docs/frontier/2026-09-14-aggregate-signed-corner-delta/Signed_Corner_Certificate.json'
SOURCE='docs/frontier/2026-09-14-aggregate-equal-population-delta'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def parameters(case,c,epsilon):
    assert case['status']=='feasible_numerical_candidate' and case['numerically_converged'] is True and case['source_centers_pass'] is True
    free=case['free_indices'];sides=case['free_coordinate_sides'];assert free==[i for i in range(22) if i!=1] and all(type(i) is int for i in free)
    assert len(sides)==21 and set(sides)=={'A','B'}
    w=list(map(F,case['variable_center']));fixedA=list(map(F,case['fixed_A_coordinates']));fixedB=list(map(F,case['fixed_B_coordinates']))
    assert len(w)==len(fixedA)==len(fixedB)==22
    A=list(fixedA);B=list(fixedB)
    for k,(i,side) in enumerate(zip(free,sides)):(A if side=='A' else B)[i]=w[k]
    assert list(map(F,case['rational_A_coordinates']))==A and list(map(F,case['rational_B_coordinates']))==B
    assert A[1]==c[1]+epsilon and B[1]==c[1]-epsilon
    scale=F(case['tau_scale']);rho=F('1e-120');assert scale==F('1e-10') and w[21]>rho
    freeA={i for i,side in zip(free,sides) if side=='A'};freeB=set(free)-freeA
    boxesA=[(x-rho,x+rho) if i in freeA else (x,x) for i,x in enumerate(A)]
    boxesB=[(x-rho,x+rho) if i in freeB else (x,x) for i,x in enumerate(B)]
    distance=max(abs(x-z) for boxes in [boxesA,boxesB] for box,z in zip(boxes,c) for x in box)
    assert distance<F(1,100) and all(boxes[0][0]>0 and all(x[1]<y[0] for x,y in zip(boxes,boxes[1:])) for boxes in [boxesA,boxesB])
    R=[list(map(F,row)) for row in case['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R)
    return A,B,free,sides,w,scale,rho,R,boxesA,boxesB,F(1,100)-distance
def contraction(A,B,c,free,sides,w,scale,rho,R,v,bits):
    ctx.prec=bits;RR=arb_mat([[av(x) for x in row] for row in R]);det=RR.det();assert det>0 or det<0
    X=[av((A if side=='A' else B)[i])+arb(0,av(rho).upper()) for i,side in zip(free,sides)]
    signs=[1 if side=='A' else -1 for side in sides]
    J=arb_mat([[s*kernel(spec,x,True) for s,x in zip(signs,X)]+[-2*av(scale)*v[k]] for k,spec in enumerate(FEATURES)])
    E=arb_mat([[int(i==j) for j in range(22)] for i in range(22)])-RR*J
    f=arb_mat([[sum((kernel(spec,av(x)) for x in A),arb(0))-sum((kernel(spec,av(x)) for x in B),arb(0))-2*av(scale)*av(w[21])*v[k]] for k,spec in enumerate(FEATURES)])
    residual=RR*f;rows=[]
    for i in range(22):
        q=sum((abs(E[i,j]) for j in range(22)),arb(0));budget=abs(residual[i,0])+av(rho)*q;assert q<1 and budget<av(rho)
        rows.append({'index':i,'derivative_defect':enc(q),'preconditioned_residual':enc(residual[i,0]),'self_map_bound':enc(budget),'strict_margin':enc(av(rho)-budget)})
    freeA={i for i,s in zip(free,sides) if s=='A'};freeB=set(free)-freeA
    observedA=[av(x)+(arb(0,av(rho).upper()) if i in freeA else arb(0)) for i,x in enumerate(A)]
    observedB=[av(x)+(arb(0,av(rho).upper()) if i in freeB else arb(0)) for i,x in enumerate(B)]
    midpoint=[(sum((kernel(spec,x) for x in observedA),arb(0))+sum((kernel(spec,x) for x in observedB),arb(0)))/2 for spec in FEATURES]
    difference=[midpoint[k]-sum((kernel(spec,av(x)) for x in c),arb(0)) for k,spec in enumerate(FEATURES)];assert difference[0]>0 or difference[0]<0
    return {'precision_bits':bits,'preconditioner_determinant':enc(det),'F_at_center':[enc(f[i,0]) for i in range(22)],'rows':rows,
        'common_midpoint_enclosures':[enc(x) for x in midpoint],'midpoint_minus_Phi_c':[enc(x) for x in difference],
        'midpoint_component_0_difference_display':float(difference[0].mid())}
def run(proposal,root=ROOT):
    paths=[root/PRIOR,root/SOURCE/'Equal_Population_Decoder.json',root/SOURCE/'Equal_Population_Inputs.zip',proposal]
    prior,src,p=map(read,[paths[0],paths[1],proposal])
    with zipfile.ZipFile(paths[2]) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    c,L,U=input_geometry(data);r=U-F('1e-8');epsilon=F('1e-8')+F('1e-24');v=prior['critical_sign_vector']
    assert prior['status']==src['status']=='passed' and prior['contract']['features']==FEATURES and list(map(F,prior['common_root_center']))==c
    assert F(prior['contract']['root_coordinate_error_radius'])==r and r<L and U-L==F('2e-30')
    assert F(p['root_coordinate_error_radius'])==r and F(p['critical_epsilon'])==epsilon and p['feature_direction']==v and all(type(x) is int and abs(x)==1 for x in v)
    for path in paths[:3]:assert p['inputs_sha256'][path.name]==sha(path)
    assert len(p['cases'])==2 and [F(x['margin']) for x in p['cases']]==[F('1e-6'),F('1e-10')]
    cases=[]
    for case in p['cases']:
        A,B,free,sides,w,scale,rho,R,boxesA,boxesB,margin=parameters(case,c,epsilon)
        coordinates=coordinate_audit({'radius':r,'boxes_A':boxesA,'boxes_B':boxesB},src,paths[2]);assert all(x['within_radius'] for x in coordinates)
        checks=[contraction(A,B,c,free,sides,w,scale,rho,R,v,bits) for bits in [768,1024]]
        tau=(scale*(w[21]-rho),scale*(w[21]+rho))
        cases.append({'status':'actual_source_mixed_variable_noise_pair','case_id':case['margin'],'variable_dimension':22,'root_variable_count':21,'root_variable_indices':free,
            'root_variable_sides':sides,'root_jacobian_column_signs':[1 if s=='A' else -1 for s in sides],
            'variable_center':list(map(str,w)),'variable_radius':str(rho),'noise_variable_index':21,'noise_variable_definition':'alpha=tau/scale',
            'tau_scale':str(scale),'noise_jacobian_column':[str(-2*scale*s) for s in v],'noise_column_derivative_variation':'0',
            'A_observation_boxes':[list(map(str,x)) for x in boxesA],'B_observation_boxes':[list(map(str,x)) for x in boxesB],
            'tau_interval':list(map(str,tau)),'tau_upper_display':float(tau[1]),'minimum_cube_margin':str(margin),'critical_root_gap':str(A[1]-B[1]),
            'coordinate_audit':coordinates,'direct_checks':checks,'common_release':'(Phi(A)+Phi(B))/2','component_error_at_exact_solution':'tau',
            'budget_guaranteed_for_pair':str(tau[1]),'signed_feature_difference_coefficients':[2*s for s in v]})
    best=min(F(x['tau_interval'][1]) for x in cases);old=F(prior['inherited_ambiguity_upper_endpoint']);assert F(prior['uniform_identification_strictly_below'])<best<old
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{path.name:sha(path) for path in paths},'contract':prior['contract'],
        'common_root_center':list(map(str,c)),'feature_direction':v,'critical_epsilon':str(epsilon),'cases':cases,'certified_pair_count':2,
        'best_certified_tau_upper':str(best),'best_upper_display':float(best),'previous_upper_endpoint':str(old),
        'scope':'Two exact self-mapping contraction constructions with one free A or B root per noncritical coordinate give common feature midpoint reports. Their positive noise intervals bound the original local ambiguity threshold from above. Root-error, observation region and feature units are unchanged. The smaller fixed critical safety increment is explicitly certified against every source interval. Source-feasible sharpness and arbitrary-report decoding remain open.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--proposal',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.proposal);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'pairs':r['certified_pair_count'],'best_upper_display':r['best_upper_display']}))
