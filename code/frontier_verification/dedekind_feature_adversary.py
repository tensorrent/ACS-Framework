"""Exercise source, contract, numerical-certificate and fixed-point failure modes."""
import argparse,copy,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
import dedekind_feature_audit as audit
import dedekind_feature_certificate as certifier

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(proposal_path,certificate_path,input_archive,source_path,original_audit_path,corrected_audit_path):
    read=lambda p:json.loads(p.read_text());p=read(proposal_path);c=read(certificate_path);source=read(source_path)
    with zipfile.ZipFile(input_archive) as z:inputs={n:json.loads(z.read(n)) for n in z.namelist()}
    mutations=[]
    def reject(name,call):
        try:call()
        except (AssertionError,ValueError,KeyError,IndexError,TypeError,StopIteration,ZeroDivisionError) as e:mutations.append({'name':name,'rejected':True,'exception':type(e).__name__})
        else:raise AssertionError('Mutation accepted: '+name)
    def changed(name,change):
        pp,cc,ii=copy.deepcopy(p),copy.deepcopy(c),copy.deepcopy(inputs);change(pp,cc,ii)
        reject(name,lambda:audit.audit_data(pp,cc,ii))
    changed('missing Gaussian feature',lambda p,c,i:p['centers'].pop())
    changed('wrong Gaussian width',lambda p,c,i:p.update(gaussian_a='1/24'))
    changed('wrong critical coordinate',lambda p,c,i:p.update(critical_index=0))
    changed('wrong critical displacement',lambda p,c,i:p.update(critical_split_epsilon='-1/1000000'))
    changed('wrong radius',lambda p,c,i:p.update(radius='0'))
    changed('corrupted common coordinate',lambda p,c,i:p['common_rational_coordinates'].__setitem__(0,'100'))
    changed('critical coordinate admitted as free variable',lambda p,c,i:p['selected_A_variable_indices'].__setitem__(0,1))
    changed('duplicated variable index',lambda p,c,i:p['selected_A_variable_indices'].__setitem__(0,p['selected_A_variable_indices'][1]))
    changed('missing correction variable',lambda p,c,i:p['corrections'].pop())
    changed('singular zero preconditioner',lambda p,c,i:p.update(preconditioner=[['0']*17 for _ in range(17)]))
    changed('inadequate identity preconditioner',lambda p,c,i:p.update(preconditioner=[[str(int(x==y)) for y in range(17)] for x in range(17)]))
    changed('preconditioner perturbed by one',lambda p,c,i:p['preconditioner'][0].__setitem__(0,str(F(p['preconditioner'][0][0])+1)))
    for key,value in [('included_unknown_tail',True),('released_moment',True),('released_cumulative_counts',True),('released_raw_coordinates',True),('post_noise_window_censoring',True),('source_population',23),('normalization',1),('source_selection','post_noise_window')]:
        changed('changed observable contract '+key,lambda p,c,i,k=key,v=value:c['contract'].__setitem__(k,v))
    changed('fixed B coordinate changed',lambda p,c,i:c['B_fixed_observed_coordinates'].__setitem__(1,p['common_rational_coordinates'][1]))
    changed('false strict radius improvement',lambda p,c,i:c.update(strict_improvement_below_lower='0'))
    changed('coordinate margin inflated',lambda p,c,i:c['coordinate_audit'][0].update(error_margin='1'))
    changed('coordinate witness truncated',lambda p,c,i:c['coordinate_audit'].pop())
    changed('common feature vector corrupted',lambda p,c,i:c['contraction_checks'][0]['fixed_common_feature_vector'].__setitem__(0,{'mid':[1000000,0],'rad':[0,0]}))
    changed('negative self-map margin',lambda p,c,i:c['contraction_checks'][0]['rows'][0].update(strict_self_map_margin={'mid':[-1,0],'rad':[0,0]}))
    changed('derivative row omitted',lambda p,c,i:c['contraction_checks'][0]['rows'].pop())
    changed('precision certificate omitted',lambda p,c,i:c['contraction_checks'].pop())
    changed('source root omitted',lambda p,c,i:i['E1_224.json']['positive_root_intervals'].pop())
    changed('wrong field discriminant',lambda p,c,i:i['E1_224.json'].update(discriminant=125))
    changed('field label leaked into anonymous input',lambda p,c,i:i['E1_224.json'].update(field='A'))
    changed('root multiplicity corrupted',lambda p,c,i:i['E1_224.json']['positive_root_intervals'].__setitem__(1,i['E1_224.json']['positive_root_intervals'][0]))
    def primary(name,change,rho=None):
        pp=copy.deepcopy(p);change(pp)
        def attempt():
            par=certifier.parameters(pp,source,rho or c['correction_box_radius'])
            assert all(x['within_radius'] for x in certifier.coordinate_audit(par,source,input_archive))
            certifier.contraction(par,512)
        reject(name,attempt)
    primary('uncorrected midpoint fails feature self-map',lambda p:p.update(corrections=['0']*17))
    primary('off-root center fails strict self-map',lambda p:p['corrections'].__setitem__(0,str(F(p['corrections'][0])+F(1,10**10))))
    primary('oversized correction box',lambda p:None,'1')
    original=read(original_audit_path);corrected=read(corrected_audit_path)
    assert original['status']=='failed' and not original['residual_report_consistent_with_exported_center'] and not original['preconditioner_consistent_with_exported_center']
    assert corrected['status']=='passed' and corrected['residual_report_consistent_with_exported_center'] and corrected['preconditioner_consistent_with_exported_center']
    small=F(1,10**100);left=F(-1);image=left-small;assert image<left and small!=0
    zero_margin_controls=[]
    for x in c['coordinate_audit']:
        if F(x['error_margin'])==0:
            slo,shi=map(float,map(F,x['source_interval']));olo,ohi=map(float,map(F,x['observed_interval']))
            floating=float(F(c['radius']))-max(abs(a-b) for a in [slo,shi] for b in [olo,ohi])
            zero_margin_controls.append({'input_member':x['input_member'],'source_index':x['source_index'],'exact_margin':'0','binary64_recomputed_margin':floating})
    assert len(zero_margin_controls)==4
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [proposal_path,certificate_path,input_archive,source_path,original_audit_path,corrected_audit_path]},
            'mutations':mutations,'mutations_rejected':len(mutations),'original_export_reporting_bug_independently_rejected':True,'corrected_export_independently_accepted':True,
            'exact_zero_margin_controls':zero_margin_controls,
            'tiny_residual_counterexample':{'function':'F(x)=1e-100 for every real x','preconditioner':'1','domain':'[-1,1]','residual_everywhere':str(small),'has_root':False,'T_at_left_endpoint':str(image),'self_map_fails':True},
            'singular_preconditioner_counterexample':{'function':'F(x)=1','preconditioner':'0','T':'identity','all_points_fixed':True,'F_has_root':False,'lesson':'A fixed point of x-RF(x) alone does not imply F(x)=0 without an injective R; the actual certificates prove nonsingularity.'},
            'scope':'Semantic mutations target actual producer/auditor functions. Independent sufficient conditions certify existence; solver success or tiny residual alone does not. Rejected certificates and local Newton failures do not prove nonexistence outside the tested slice.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['proposal','certificate','inputs','source','original-audit','corrected-audit','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.proposal,a.certificate,a.inputs,a.source,a.original_audit,a.corrected_audit);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','mutations_rejected':r['mutations_rejected'],'exact_zero_margin_controls':r['exact_zero_margin_controls'],'reporting_bug_rejected':True}))
