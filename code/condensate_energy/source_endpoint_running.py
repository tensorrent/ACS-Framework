#!/usr/bin/env python3
"""Repair the historical angle-running diagnostic without fitting its target."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/source_endpoint'


def angle_coordinates(y):
    """Exact three-amplitude Fourier angle; no forced Koide-radius fit."""
    x=np.sqrt(np.array(y,float))[[2,0,1]]
    angles=2*np.pi*np.arange(3)/3
    mean=float(np.mean(x));C=float(2/3*x@np.cos(angles));S=float(-2/3*x@np.sin(angles))
    return dict(theta_degrees=float(np.degrees(np.arctan2(S,C))),mean=mean,
                radius_over_mean=float(np.hypot(C,S)/mean),
                Q=float(np.sum(x*x)/np.sum(x)**2))


def corrected_angle_rhs(t,state,gut=False):
    h,g2,g3,ye,ymu,ytau,yt=state
    lepton=np.array([ye,ymu,ytau]);trace=3*yt*yt+float(lepton@lepton)
    b1=41/10 if gut else 41/6
    lepton_h=9/4 if gut else 15/4
    top_h=17/20 if gut else 17/12
    gauge=np.array([b1*h**3,-19/6*g2**3,-7*g3**3])
    leptons=lepton*(trace-lepton_h*h*h-9/4*g2*g2+1.5*lepton*lepton)
    top=yt*(trace+1.5*yt*yt-top_h*h*h-9/4*g2*g2-8*g3*g3)
    return np.r_[gauge,leptons,top]/(16*np.pi**2)


def audit_source_running():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    src=OUT/'source-snapshots/koide_rg_flow.py'
    tree=ast.parse(src.read_text())
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
    env=dict(np=np,minimize=minimize,v=246.22)
    exec(compile(ast.Module(body=functions,type_ignores=[]),str(src),'exec'),env)
    masses=np.array([.51099895e-3,.1056583755,1.77686])
    gauge=np.sqrt(4*np.pi*np.array([.01017,.03382,.1179]))
    y0=np.r_[gauge,np.sqrt(2)*masses/246.22,np.sqrt(2)*173.1/246.22]
    end=np.log(2e16/91.1876)
    times=np.linspace(0,end,101)
    old=solve_ivp(env['rge_system'],[0,end],y0,method='DOP853',rtol=2e-12,atol=2e-15,dense_output=True)
    new=solve_ivp(corrected_angle_rhs,[0,end],y0,method='DOP853',rtol=2e-12,atol=2e-15,dense_output=True)
    independent=solve_ivp(corrected_angle_rhs,[0,end],y0,method='RK45',rtol=1e-10,atol=1e-14,max_step=.08,dense_output=True)
    gut0=y0.copy();gut0[0]*=np.sqrt(5/3)
    gut=solve_ivp(lambda t,y:corrected_angle_rhs(t,y,True),[0,end],gut0,
                  method='DOP853',rtol=2e-12,atol=2e-15,dense_output=True)
    for name,sol in [('historical',old),('corrected',new),('second solver',independent),('GUT convention',gut)]:
        check(name+' reaches declared endpoint',sol.success and abs(sol.t[-1]-end)<1e-12)
    difference=np.max(abs(new.sol(times)-independent.sol(times)))
    check('two independent integrators agree',difference<2e-9,{'max_absolute_state_difference':float(difference)})
    transformed=gut.sol(times);transformed[0]/=np.sqrt(5/3)
    check('properly transformed hypercharge conventions agree',np.max(abs(new.sol(times)-transformed))<1e-10)
    # Closed one-loop gauge solutions supply an independent integrator control.
    exact_gauge=gauge[:,None]/np.sqrt(1-(np.array([41/6,-19/6,-7])[:,None]*gauge[:,None]**2*times)/(8*np.pi**2))
    check('gauge trajectories match their closed form',np.max(abs(new.sol(times)[:3]-exact_gauge))<1e-10)
    back=solve_ivp(corrected_angle_rhs,[end,0],new.y[:,-1],method='DOP853',rtol=2e-12,atol=2e-15)
    check('reverse integration returns the historical inputs',back.success and np.max(abs(back.y[:,-1]-y0))<1e-9)
    # Exact cancellation of flavor-universal running from the Fourier angle.
    xx=s.Matrix(s.symbols('x0:3',positive=True));cc=s.symbols('c',real=True)
    C=s.Rational(2,3)*(xx[0]-(xx[1]+xx[2])/2)
    S=(xx[2]-xx[1])/s.sqrt(3)
    dC=s.Rational(2,3)*(cc*xx[0]-cc*(xx[1]+xx[2])/2);dS=cc*(xx[2]-xx[1])/s.sqrt(3)
    check('universal rescaling contributes exactly zero angular velocity',s.expand(C*dS-S*dC)==0)
    for factor in [.001,7.,1e5]:
        check('angle extraction is scale invariant '+str(factor),
              abs(angle_coordinates(y0[3:6])['theta_degrees']-angle_coordinates(factor*y0[3:6])['theta_degrees'])<1e-12)
    # Direct integration of the exact ratio equation verifies the flavor term.
    integral=quad(lambda t:3/(32*np.pi**2)*(new.sol(t)[5]**2-new.sol(t)[4]**2),0,end,
                  epsabs=1e-13,epsrel=1e-11)[0]
    ratio_change=np.log((new.y[5,-1]/new.y[4,-1])/(y0[5]/y0[4]))
    check('flavor-ratio integral agrees with coupled flow',abs(integral-ratio_change)<1e-11)
    inputs=angle_coordinates(y0[3:6]);old_final=angle_coordinates(old.y[3:6,-1]);new_final=angle_coordinates(new.y[3:6,-1])
    fitted_initial=env['extract_theta0'](*y0[3:6]);fitted_final=env['extract_theta0'](*new.y[3:6,-1])
    bare=np.pi/6-np.arctan(1/3);candidate=np.degrees(bare)
    # Start from the historical candidate at the chosen UV scale with the overall
    # normalization taken from the corrected upward run. This remains an input test.
    amps=np.sqrt(new.y[3:6,-1]*246.22/np.sqrt(2));A=np.sum(amps)/3
    candidate_amps=np.sort(A*(1+np.sqrt(2)*np.cos(bare+2*np.pi*np.arange(3)/3)))
    check('candidate Koide amplitudes stay positive',np.min(candidate_amps)>0)
    c0=new.y[:,-1].copy();c0[3:6]=np.sqrt(2)*candidate_amps**2/246.22
    candidate_down=solve_ivp(corrected_angle_rhs,[end,0],c0,method='DOP853',rtol=2e-12,atol=2e-15)
    check('candidate downward trajectory reaches IR',candidate_down.success and candidate_down.t[-1]==0)
    cfinal=angle_coordinates(candidate_down.y[3:6,-1])
    check('candidate initial angle is reconstructed without fitting',abs(angle_coordinates(c0[3:6])['theta_degrees']-candidate)<1e-12)
    gap=inputs['theta_degrees']-candidate
    shift=cfinal['theta_degrees']-candidate
    check('corrected source diagnostic cannot bridge its claimed angle gap',abs(shift)<.01*abs(gap))
    # The source's analytic angular estimate omitted the coordinate Jacobian.
    # Record it as an estimate, never as an independently verified angle formula.
    source_estimate=np.degrees(3/(32*np.pi**2)*y0[5]**2*end)
    grids=[]
    for t in times:
        o=angle_coordinates(old.sol(t)[3:6]);n=angle_coordinates(new.sol(t)[3:6])
        grids.append(dict(log_mu_over_MZ=float(t),scale_GeV=float(91.1876*np.exp(t)),
                          historical_angle=o['theta_degrees'],corrected_angle=n['theta_degrees'],
                          corrected_radius_ratio=n['radius_over_mean']))
    # Preserve complete replays. Only the hardcoded figure path is changed.
    replay_rows=[]
    for name in ['koide_rg_flow','koide_clebsch_gordan']:
        dest=OUT/'attempts'/name;dest.mkdir(exist_ok=True)
        source=(OUT/'source-snapshots'/(name+'.py')).read_text()
        code=source.replace('/home/claude/figures',str(dest/'figures'))
        path=dest/'replay.py';path.write_text(code)
        try:
            run=subprocess.run([sys.executable,str(path)],cwd=dest,capture_output=True,text=True,timeout=90)
            (dest/'stdout.txt').write_text(run.stdout);(dest/'stderr.txt').write_text(run.stderr)
            row=dict(source=name,returncode=run.returncode,plot_path_replacements=source.count('/home/claude/figures'),
                     replay_sha256=sha256(path.read_bytes()).hexdigest())
            check('source replay '+name,run.returncode==0)
        except subprocess.TimeoutExpired as err:
            (dest/'stdout.txt').write_bytes(err.stdout or b'');(dest/'stderr.txt').write_bytes(err.stderr or b'')
            row=dict(source=name,timeout_seconds=90,completed=False)
            check('source replay '+name,False,row)
        (dest/'execution.json').write_text(json.dumps(row,indent=2)+'\n');replay_rows.append(row)
    data=dict(checks_total=len(checks),checks_passed=sum(x['passed'] for x in checks),checks=checks,
        convention='gY at historical initial value; g1_GUT=sqrt(5/3) gY is a separately integrated control',
        equation_reference='https://arxiv.org/html/hep-ph/0501272v3#A4',
        comparison_inputs=dict(MZ_GeV=91.1876,UV_GeV=2e16,v_GeV=246.22,state=y0.tolist()),
        initial=inputs,historical_final=old_final,corrected_final=new_final,
        forced_radius_fit=dict(initial_degrees=fitted_initial,corrected_final_degrees=fitted_final),
        candidate=dict(initial_degrees=float(candidate),IR_degrees=cfinal['theta_degrees'],
                       shift_degrees=float(shift),gap_to_input_angle_degrees=float(gap),
                       fraction_of_gap=float(abs(shift/gap))),
        source_angular_estimate_degrees=float(source_estimate),flavor_log_ratio_integral=float(integral),
        trajectories=grids,replays=replay_rows,
        limitations=['Diagnostic uses historical mixed-scheme numerical inputs, not a precision SM mass fit',
            'All quark Yukawas except top and all neutrino Yukawas are set to zero',
            'No thresholds or new physics between the stated endpoints are included',
            'RG evolution is conditional on boundary values; no ACS matching scale is derived',
            'The exact Fourier angle does not force the Koide radius ratio to sqrt(2)'])
    (OUT/'running.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=data['checks_passed'],
        failures=[x for x in checks if not x['passed']],initial=inputs,corrected_final=new_final,
        candidate=data['candidate']),indent=2))
    if data['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':audit_source_running()
