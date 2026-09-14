"""Certify which omitted observables distinguish the constructed feature-collision witness."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def av(x):q=F(x);return arb(q.numerator)/arb(q.denominator)
def run(certificate_path,source_path):
    c=json.loads(certificate_path.read_text());source=json.loads(source_path.read_text());assert c['status']==source['status']=='passed'
    a=[tuple(map(F,x)) for x in c['A_observed_coordinate_boxes']];b=list(map(F,c['B_fixed_observed_coordinates']));assert len(a)==len(b)==22
    h=F(next(m for m in source['matching_cases'] if m['precision_bits']==224)['rational_height'])
    acount=[sum(hi<h for lo,hi in a),sum(lo<h for lo,hi in a)];bcount=sum(x<h for x in b)
    assert acount==[1,1] and bcount==2
    cases=[]
    for bits in [512,768]:
        ctx.prec=bits;A=[av(lo).union(av(hi)) for lo,hi in a];B=list(map(av,b))
        specs=[('finite_rational_moment',lambda x:3/(arb(9)/4+x*x)),
               ('extra_center_37_same_width',lambda x:2*(-x*x/25).exp()*(arb(37).log()*x).cos()),
               ('center_2_width_1_over_24',lambda x:2*(-x*x/24).exp()*(arb(2).log()*x).cos())]
        rows=[]
        for name,fun in specs:
            value_a=sum((fun(x) for x in A),arb(0));value_b=sum((fun(x) for x in B),arb(0));difference=value_a-value_b
            assert difference>0 or difference<0
            rows.append({'observable':name,'A_enclosure':enc(value_a),'B_enclosure':enc(value_b),'difference_enclosure':enc(difference),'difference_sign':'positive' if difference>0 else 'negative','approx_difference_display':float(difference.mid())})
        cases.append({'precision_bits':bits,'omitted_observables':rows})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [certificate_path,source_path]},
            'interior_count':{'height':str(h),'A_count_envelope':acount,'B_count':bcount,'distinct':True},'cases':cases,
            'scope':'These additional statistics uniformly distinguish this particular certified feature-collision box from its fixed B observation. They were not in the released17-feature vector. This does not prove general identifiability after adding a statistic: a different collision satisfying more equations may still exist. The finite rational moment is not an equality claim about unrecorded-tail terms.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['certificate','source','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.certificate,a.source);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','interior_counts':[1,2],'additional_observables':[{'name':x['observable'],'difference_approx':x['approx_difference_display']} for x in r['cases'][0]['omitted_observables']]}))
