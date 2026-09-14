"""Certify an open interval of cutoffs with the same two 22-root source prefixes."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(report,parents,spectra):
    assert report['status']=='passed' and [c['precision_bits'] for c in report['cases']]==[160,224]
    checked=0
    for c in report['cases']:
        bits=c['precision_bits'];lo,hi=F(c['cutoff_lower']),F(c['cutoff_upper']);assert lo<F(39,2)<hi<20
        a,b=[parents['S'+str(i)+'_'+str(bits)+'.json']['positive_root_intervals'] for i in [1,2]]
        assert [len(a),len(b)]==[23,22]
        assert lo==max(F(a[21]['hi']),F(b[21]['hi'])) and hi==F(a[22]['lo'])
        assert F(c['width'])==hi-lo>0 and c['endpoint_convention']=='open; endpoints are not asserted certified cutoffs'
        for index,roots in enumerate([a,b]):
            assert roots==spectra[bits]['aggregate'][['A','B'][index]]['unlabelled_ordinate_intervals']
            assert all(F(x['hi'])<=lo for x in roots[:22])
            assert all(F(x['lo'])>=hi for x in roots[22:]);checked+=len(roots)
        assert len(c['controls'])==9
        for j,q in enumerate(c['controls'],1):
            t=F(q['cutoff']);assert t==lo+(hi-lo)*F(j,10)
            counts=[[sum(F(x['hi'])<t for x in roots),sum(F(x['lo'])<t for x in roots)] for roots in [a,b]]
            assert counts==q['certain_possible_populations']==[[22,22],[22,22]];checked+=4
    return checked
def run(parent_archive,spectrum_archive):
    with zipfile.ZipFile(parent_archive) as z:parents={n:json.loads(z.read(n)) for n in z.namelist() if n.endswith('.json')}
    with zipfile.ZipFile(spectrum_archive) as z:spectra={b:json.loads(z.read('Pair_Spectrum'+str(b)+'.json')) for b in [160,224]}
    cases=[]
    for bits in [160,224]:
        roots=[parents['S'+str(i)+'_'+str(bits)+'.json']['positive_root_intervals'] for i in [1,2]]
        lo=max(F(x[21]['hi']) for x in roots);hi=F(roots[0][22]['lo'])
        cases.append({'precision_bits':bits,'cutoff_lower':str(lo),'cutoff_upper':str(hi),'width':str(hi-lo),
            'endpoint_convention':'open; endpoints are not asserted certified cutoffs',
            'controls':[{'cutoff':str(lo+(hi-lo)*F(j,10)),'certain_possible_populations':[[22,22],[22,22]]} for j in range(1,10)]})
    report={'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [parent_archive,spectrum_archive]},'cases':cases,
            'scope':'Every cutoff strictly inside the stored interval selects the identical complete 22-entry prefix from both fields, hence the same fixed-population count-gate and ambiguity theorem applies. This is a continuum statement proved by endpoint inequalities; nine cutoffs per precision are additional controls. It does not transfer post-noise censoring or Gaussian tail budgets.'}
    checked=verify(report,parents,spectra);mutations=[]
    import copy
    for name,change in [('overextended lower cutoff',lambda c:c.update(cutoff_lower='18')),('overextended upper cutoff',lambda c:c.update(cutoff_upper='20')),('closed endpoint claim',lambda c:c.update(endpoint_convention='closed')),('false control count',lambda c:c['controls'][0]['certain_possible_populations'][0].__setitem__(0,23))]:
        changed=copy.deepcopy(report);change(changed['cases'][0])
        try:verify(changed,parents,spectra)
        except (AssertionError,ValueError):mutations.append({'name':name,'rejected':True})
        else:raise AssertionError(name)
    report['independent_exact_checks']=checked;report['mutations']=mutations;return report
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['parent','spectra','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.parent,a.spectra);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','cutoff_interval_approx_display':[float(F(r['cases'][0][k])) for k in ['cutoff_lower','cutoff_upper']],'exact_checks':r['independent_exact_checks'],'mutations':len(r['mutations'])}))
