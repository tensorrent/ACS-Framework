# Independent weak-breaking radiation calculation

Registered during the nonlinear batch, after the first four outcomes and
before solving this response problem. Those outcomes show charge oscillation
and small nonzero outward energy at epsilon/b=.01 and .05. Do not treat
charge nonconservation alone as instability. Derive the outgoing response to
predict leading radiation independently of a fitted decay curve.

Background q=f exp(i omega t), chi=c. Set Omega=4omega and
delta q/epsilon = exp(i omega t)[u exp(-i Omega t)+conj(v) exp(i Omega t)],
delta chi/epsilon = h exp(-i Omega t)+conj(h) exp(i Omega t).
Let U=ru, V=rv, H=sqrt(2)rh. The radial linear equations are

[-d_r^2+c^2+2bf^2-9omega^2]U + bf^2 V + sqrt(2)cf H = -rf^3;
[-d_r^2+c^2+2bf^2-25omega^2]V + bf^2 U + sqrt(2)cf H = 0;
[-d_r^2+3c^2-1+f^2-16omega^2]H + sqrt(2)cf(U+V) = 0.

Regular center U=V=H=0. Outgoing conditions at large radius are
U'=ik3 U, V'=ik5 V, H'=ikc H, where
k3=sqrt(9omega^2-1), k5=sqrt(25omega^2-1), kc=sqrt(16omega^2-2).
All are real for the qualified reference. The signs incorporate the complex
conjugate in the +5omega channel. No fitted radiation amplitude is an input.

Power divided by epsilon^2 is
4pi[3omega k3|U|^2+5omega k5|V|^2+4omega kc|H|^2].
Outgoing charge flux divided by epsilon^2 is 4pi[-k3|U|^2+k5|V|^2].
Average charge source divided by epsilon^2 is 16pi integral rf^3 Im(U)dr.
Check the independent identity S = -P/omega + J_charge.

Use a complex continuum boundary-value solve and independently assembled
second-order finite differences at h=.05,.025,.0125. Compare radius30 and40.
The background is a cubic interpolation of the saved continuum profile, set
to vacuum beyond its domain. Require boundary-value residual<1e-6, power
agreement between BVP and finest FD <.005 relative, successive FD errors
decreasing, radius effect <.001 relative, and source/flux identity <.001
relative to max(1,|S|). Preserve any failure before amending.

Compare weak nonlinear runs with this epsilon^2 prediction using late-time
outgoing flux at radius40 and probe frequencies, accounting for propagation
delay. Agreement is measured, not guaranteed by a pass condition. Any inferred
initial E/P timescale is a local weak-breaking scale, not an established
half-life or physical lifetime in seconds. The background evolves, other
channels exist, and no ACS physical scale or epsilon has been selected.
