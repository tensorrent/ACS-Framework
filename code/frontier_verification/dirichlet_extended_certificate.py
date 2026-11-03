"""Count with folded contours, then exhaust that finite count with Hardy brackets."""
import argparse,hashlib,json
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
from flint import ctx,dirichlet_char
import flint
import dirichlet_folded_count as counter
import dirichlet_strip_certificate as refinement
import lfunction_zero_certificate as core


def sources():
    return {Path(m.__file__).name:hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()
            for m in [counter,refinement,core]}


def generate(number,top,bits):
    ctx.prec=bits;chi=dirichlet_char(5,number)
    counted=counter.count(number,top,bits)
    print(json.dumps({'event':'count','character':number,'count':counted['zero_count']}),flush=True)
    scans=[]
    for denominator in [10,20,40,80]:
        lo=F(0);slo=core.sign(core.hardy(chi,lo));assert slo
        brackets=[]
        for j in range(1,denominator*top+1):
            hi=F(j,denominator);shi=core.sign(core.hardy(chi,hi));assert shi
            if shi!=slo:brackets.append((lo,hi))
            lo,slo=hi,shi
            if j%(denominator*250)==0:
                print(json.dumps({'event':'scan','character':number,'denominator':denominator,
                                  'height':str(hi),'brackets':len(brackets)}),flush=True)
        scans.append({'denominator':denominator,'brackets':len(brackets)})
        assert len(brackets)<=counted['zero_count']
        if len(brackets)==counted['zero_count']:break
    else:raise AssertionError('Hardy scan does not exhaust the finite count')
    roots=[]
    for j,(lo,hi) in enumerate(brackets,1):
        row=refinement.refine(chi,lo,hi);row['index']=j;roots.append(row)
        if j%100==0:print(json.dumps({'event':'refined','character':number,'roots':j}),flush=True)
    assert all(F(a['hi'])<F(b['lo']) for a,b in zip(roots,roots[1:]))
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dependencies_sha256':sources(),'recorded_utc':datetime.now(timezone.utc).isoformat(),
            'character':number,'modulus':5,'parity':int(chi.parity()),'top':top,'precision_bits':bits,
            'python_flint':flint.__version__,'flint':flint.__FLINT_VERSION__,
            'contour':counted,'scans':scans,'root_intervals':roots,
            'scope':'Completed rectangle [-1,2] x [-1/2,T]; count matching disjoint positive Hardy brackets proves finite completeness and simplicity. No global GRH claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--character',type=int,choices=[2,3,4],required=True)
    p.add_argument('--top',type=int,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert a.top>0
    r=generate(a.character,a.top,a.precision);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'character':a.character,'roots':len(r['root_intervals'])}),flush=True)
