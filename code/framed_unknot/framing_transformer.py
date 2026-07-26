#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
The framing transformer of the Mobius-screw centerline.

Companion computation to papers/notes/Mobius_Screw_Electron.tex.

The note defines the model electron as the framed unknot

    gamma(phi) = ( (R + a cos(phi/2)) cos phi,
                   (R + a cos(phi/2)) sin phi,
                    a sin(phi/2) ),          phi in [0, 4 pi),

a (2,1) curve on the torus of radii (R, a), and asserts the self-linking
number Sl = p q = 2 under the torus framing.

This script computes the chain that turns that geometry into a statement
about spin, and evaluates each stage numerically:

    gamma            centerline (embedded closed curve, unknotted)
      |  torus surface normal
    U(phi)           framing vector field along gamma
      |  Calugareanu-White-Fuller
    Sl = Tw + Wr     self-linking splits into twist and writhe
      |  adapted frame  F = [T, U, T x U]
    F : S^1 -> SO(3) loop of frames
      |  lift through the double cover SU(2) -> SO(3)
    q : S^1 -> SU(2) (closes iff [F] = 0 in pi_1(SO(3)) = Z/2)

The last stage is the only place spin can enter, and it is a parity
question, not a magnitude question. The quantity that decides it is the
sign

    sigma = q(4 pi) / q(0) = +1  (frame lift closes; non-spinorial)
                           = -1  (frame lift does not close; spinorial)

which this script evaluates for the model curve and for a control family
of circles carrying n framing twists, so the map n -> sigma is measured
rather than assumed.

Run:  python3 code/framed_unknot/framing_transformer.py
"""

import json
import pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# geometry: centerline, torus framing, and their analytic derivatives
# --------------------------------------------------------------------------


def mobius_screw(phi, R=1.0, a=0.3):
    """Centerline gamma(phi) and dgamma/dphi for the (2,1) torus curve.

    Longitude angle is phi, meridian angle is phi/2, so the curve winds
    p = 2 times longitudinally and q = 1 time meridionally and closes at
    phi = 4 pi.
    """
    c2, s2 = np.cos(phi / 2), np.sin(phi / 2)
    c, s = np.cos(phi), np.sin(phi)
    rho = R + a * c2
    drho = -0.5 * a * s2

    gamma = np.stack([rho * c, rho * s, a * s2], axis=-1)
    dgamma = np.stack(
        [drho * c - rho * s, drho * s + rho * c, 0.5 * a * c2], axis=-1
    )
    return gamma, dgamma


def torus_framing(phi):
    """Outward torus normal U(phi) along the curve, and dU/dphi.

    U is the unit normal of the torus surface at meridian angle phi/2,
    longitude phi. Because gamma lies in that surface, U is automatically
    orthogonal to the tangent -- this is the natural (surface) framing
    whose self-linking number is p*q.
    """
    c2, s2 = np.cos(phi / 2), np.sin(phi / 2)
    c, s = np.cos(phi), np.sin(phi)

    U = np.stack([c2 * c, c2 * s, s2], axis=-1)
    dU = np.stack(
        [-0.5 * s2 * c - c2 * s, -0.5 * s2 * s + c2 * c, 0.5 * c2], axis=-1
    )
    return U, dU


def twisted_circle(phi, n_twist, R=1.0):
    """Control family: round circle of radius R with n_twist framing turns.

    Closed over phi in [0, 2 pi). The framing rotates n_twist times about
    the tangent as the circle is traversed, so Wr = 0 and Tw = Sl = n_twist.
    """
    c, s = np.cos(phi), np.sin(phi)
    gamma = np.stack([R * c, R * s, np.zeros_like(phi)], axis=-1)
    dgamma = np.stack([-R * s, R * c, np.zeros_like(phi)], axis=-1)

    # radial and vertical directions are both normal to the tangent
    er = np.stack([c, s, np.zeros_like(phi)], axis=-1)
    ez = np.stack([np.zeros_like(phi)] * 2 + [np.ones_like(phi)], axis=-1)
    th = n_twist * phi
    ct, st = np.cos(th)[..., None], np.sin(th)[..., None]
    U = ct * er + st * ez
    dU = n_twist * (-st * er + ct * ez) + ct * np.stack(
        [-s, c, np.zeros_like(phi)], axis=-1
    )
    return gamma, dgamma, U, dU


# --------------------------------------------------------------------------
# stage 1: Calugareanu-White-Fuller  Sl = Tw + Wr
# --------------------------------------------------------------------------


def unit(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def twist_uniform(dgamma, U, dU, dphi):
    """Tw on a uniform periodic grid (trapezoid = Riemann sum here)."""
    T = unit(dgamma)
    integrand = np.einsum("ij,ij->i", np.cross(T, U), dU)
    return integrand.sum() * dphi / (2 * np.pi)


def writhe(gamma, dgamma, dphi):
    """Gauss double integral for the writhe of a closed curve.

    Wr = (1/4 pi) int int  [ (g(s)-g(t)) . (g'(s) x g'(t)) ] / |g(s)-g(t)|^3

    The integrand extends continuously by zero on the diagonal, so the
    diagonal samples are set to zero.
    """
    diff = gamma[:, None, :] - gamma[None, :, :]
    cross = np.cross(dgamma[:, None, :], dgamma[None, :, :])
    num = np.einsum("ijk,ijk->ij", diff, cross)
    d3 = np.linalg.norm(diff, axis=-1) ** 3
    with np.errstate(divide="ignore", invalid="ignore"):
        integrand = np.where(d3 > 1e-14, num / d3, 0.0)
    return integrand.sum() * dphi * dphi / (4 * np.pi)


def linking_number(g1, dg1, g2, dg2, dphi1, dphi2):
    """Gauss linking integral between two disjoint closed curves."""
    diff = g1[:, None, :] - g2[None, :, :]
    cross = np.cross(dg1[:, None, :], dg2[None, :, :])
    num = np.einsum("ijk,ijk->ij", diff, cross)
    d3 = np.linalg.norm(diff, axis=-1) ** 3
    return (num / d3).sum() * dphi1 * dphi2 / (4 * np.pi)


# --------------------------------------------------------------------------
# stage 2: the frame loop F : S^1 -> SO(3) and its SU(2) lift
# --------------------------------------------------------------------------


def adapted_frames(dgamma, U):
    """Rotation matrices F(phi) with columns [T, U, T x U].

    Orthonormal because U is a surface normal and T is tangent to that
    same surface, hence T . U = 0 by construction.
    """
    T = unit(dgamma)
    Uh = unit(U)
    V = np.cross(T, Uh)
    return np.stack([T, Uh, V], axis=-1)  # columns


def matrix_to_quaternion(M):
    """Quaternion (w, x, y, z) of a proper rotation matrix, Shepperd's method.

    Sign is arbitrary at this stage; continuity is imposed afterwards.
    """
    m = M
    tr = m[0, 0] + m[1, 1] + m[2, 2]
    if tr > 0:
        S = np.sqrt(tr + 1.0) * 2
        w = 0.25 * S
        x = (m[2, 1] - m[1, 2]) / S
        y = (m[0, 2] - m[2, 0]) / S
        z = (m[1, 0] - m[0, 1]) / S
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        S = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        w = (m[2, 1] - m[1, 2]) / S
        x = 0.25 * S
        y = (m[0, 1] + m[1, 0]) / S
        z = (m[0, 2] + m[2, 0]) / S
    elif m[1, 1] > m[2, 2]:
        S = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        w = (m[0, 2] - m[2, 0]) / S
        x = (m[0, 1] + m[1, 0]) / S
        y = 0.25 * S
        z = (m[1, 2] + m[2, 1]) / S
    else:
        S = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        w = (m[1, 0] - m[0, 1]) / S
        x = (m[0, 2] + m[2, 0]) / S
        y = (m[1, 2] + m[2, 1]) / S
        z = 0.25 * S
    return np.array([w, x, y, z])


def continuous_lift(frames):
    """Lift a path of rotations to SU(2), choosing signs for continuity.

    Returns the array of quaternions and the holonomy sigma = q_end / q_0
    obtained by closing the loop (the last frame is the first frame again).
    """
    qs = [matrix_to_quaternion(frames[0])]
    for M in frames[1:]:
        q = matrix_to_quaternion(M)
        if np.dot(q, qs[-1]) < 0:      # pick the lift on the same sheet
            q = -q
        qs.append(q)
    qs = np.array(qs)
    sigma = float(np.dot(qs[-1], qs[0]))   # +1 closes, -1 flips sheet
    return qs, sigma


# --------------------------------------------------------------------------
# drivers
# --------------------------------------------------------------------------


def analyse_mobius_screw(N=2000, R=1.0, a=0.3, eps_frac=0.05):
    """Full transformer chain for the (2,1) Mobius-screw centerline."""
    # open grid for integrals (periodic, so a plain sum is spectrally accurate)
    phi = np.linspace(0.0, 4 * np.pi, N, endpoint=False)
    dphi = 4 * np.pi / N
    gamma, dgamma = mobius_screw(phi, R, a)
    U, dU = torus_framing(phi)

    orth = np.abs(np.einsum("ij,ij->i", unit(dgamma), U)).max()

    Tw = twist_uniform(dgamma, U, dU, dphi)
    Wr = writhe(gamma, dgamma, dphi)

    # self-linking as the linking number of the centerline with the
    # framing pushoff, evaluated at two offsets to show eps-independence
    Sl = {}
    for f in (2 * eps_frac, eps_frac):
        eps = f * a
        g2 = gamma + eps * U
        dg2 = dgamma + eps * dU
        Sl[f] = linking_number(gamma, dgamma, g2, dg2, dphi, dphi)

    # closed grid for the frame loop (endpoint repeats the start)
    phi_c = np.linspace(0.0, 4 * np.pi, N + 1)
    _, dg_c = mobius_screw(phi_c, R, a)
    U_c, _ = torus_framing(phi_c)
    frames = adapted_frames(dg_c, U_c)
    _, sigma = continuous_lift(frames)

    # the framing field alone, U = A(phi) e_x with A = Rz(phi) Ry(-phi/2)
    A = np.einsum("ijk,ikl->ijl", _Rz(phi_c), _Ry(-phi_c / 2))
    _, sigma_A = continuous_lift(A)

    return dict(
        orthogonality_max=orth,
        Tw=Tw,
        Wr=Wr,
        Sl=Sl,
        Sl_check=Tw + Wr,
        sigma_frame=sigma,
        sigma_framing_field=sigma_A,
    )


def quaternion_holonomy_closed_form():
    """Closed-form SU(2) holonomy of the framing field, as a cross-check.

    The torus normal is U(phi) = A(phi) e_x with

        A(phi) = Rz(phi) Ry(-phi/2),

    since (phi, phi/2) are exactly the longitude and meridian angles of the
    sphere parameterisation. Lifting each factor to unit quaternions,

        Rz(t) -> cos(t/2) + k sin(t/2)
        Ry(t) -> cos(t/2) + j sin(t/2)

    gives the lift

        q(phi) = [cos(phi/2) + k sin(phi/2)] [cos(phi/4) - j sin(phi/4)],

    which is continuous with q(0) = 1. Closing the curve at phi = 4 pi,

        q(4 pi) = [cos 2pi + k sin 2pi] [cos pi - j sin pi] = (1)(-1) = -1.

    The half-angle of the MERIDIAN factor is what does it: the meridian
    angle advances by 2 pi over the closed curve, so its quaternion factor
    advances by only pi and lands on -1. Returns the exact holonomy -1 and
    the quaternion path evaluated numerically from the same formula.
    """
    def qmul(p, q):
        w1, x1, y1, z1 = p
        w2, x2, y2, z2 = q
        return np.array([
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ])

    phi = np.linspace(0.0, 4 * np.pi, 4001)
    qs = []
    for p in phi:
        qz = np.array([np.cos(p / 2), 0.0, 0.0, np.sin(p / 2)])      # about k
        qy = np.array([np.cos(p / 4), 0.0, -np.sin(p / 4), 0.0])     # about j
        qs.append(qmul(qz, qy))
    qs = np.array(qs)
    # verify the path is continuous (no sign jumps) and read off the holonomy
    jumps = np.abs(np.einsum("ij,ij->i", qs[1:], qs[:-1]))
    return float(np.dot(qs[-1], qs[0])), float(jumps.min())


def _Rz(t):
    c, s, z, o = np.cos(t), np.sin(t), np.zeros_like(t), np.ones_like(t)
    return np.stack(
        [np.stack([c, -s, z], -1), np.stack([s, c, z], -1), np.stack([z, z, o], -1)],
        axis=-2,
    )


def _Ry(t):
    c, s, z, o = np.cos(t), np.sin(t), np.zeros_like(t), np.ones_like(t)
    return np.stack(
        [np.stack([c, z, s], -1), np.stack([z, o, z], -1), np.stack([-s, z, c], -1)],
        axis=-2,
    )


def analyse_control(n_twist, N=1200, R=1.0):
    """Round circle with n_twist framing turns: measures n -> (Sl, sigma)."""
    phi = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    dphi = 2 * np.pi / N
    gamma, dgamma, U, dU = twisted_circle(phi, n_twist, R)
    Tw = twist_uniform(dgamma, U, dU, dphi)
    Wr = writhe(gamma, dgamma, dphi)

    phi_c = np.linspace(0.0, 2 * np.pi, N + 1)
    _, dg_c, U_c, _ = twisted_circle(phi_c, n_twist, R)
    frames = adapted_frames(dg_c, U_c)
    _, sigma = continuous_lift(frames)
    return Tw, Wr, Tw + Wr, sigma


def main():
    print("=" * 74)
    print("FRAMING TRANSFORMER — Mobius-screw centerline (2,1) torus curve")
    print("=" * 74)

    res = analyse_mobius_screw()
    print(f"\nframing orthogonality  max|T.U| = {res['orthogonality_max']:.3e}"
          "   (0 => U is a genuine framing)")
    print("\nCalugareanu-White-Fuller decomposition")
    print(f"  Tw (twist)          = {res['Tw']:+.6f}")
    print(f"  Wr (writhe)         = {res['Wr']:+.6f}")
    print(f"  Tw + Wr             = {res['Sl_check']:+.6f}")
    for f, v in res["Sl"].items():
        print(f"  Sl = Lk(g, g+{f:.3f}a U) = {v:+.6f}")
    print("  expected |Sl| = p*q = 2          (torus framing, p=2, q=1)")
    print("  the overall sign is the handedness convention of the embedding;")
    print("  as parameterised the (2,1) screw is left-handed, so Sl = -2.")

    print("\nSU(2) lift of the frame loop  (sigma = q(4pi)/q(0))")
    print(f"  adapted frame [T,U,TxU] : sigma = {res['sigma_frame']:+.6f}")
    print(f"  framing field Rz(f)Ry(-f/2): sigma = {res['sigma_framing_field']:+.6f}")
    sigma_exact, cont = quaternion_holonomy_closed_form()
    print(f"  closed form  q(4pi)/q(0)   : sigma = {sigma_exact:+.6f}"
          f"   (path continuity {cont:.4f})")
    verdict = ("SPINORIAL — lift does not close; the frame returns only after "
               "two circuits")
    if res["sigma_frame"] > 0:
        verdict = ("NON-SPINORIAL — lift closes; the frame returns after one "
                   "circuit")
    print(f"  verdict: {verdict}")

    print("\n" + "-" * 74)
    print("CONTROL: round circle with n framing twists (Wr = 0, Sl = n)")
    print("-" * 74)
    print(f"{'n':>3} | {'Tw':>9} | {'Wr':>9} | {'Sl':>7} | {'sigma':>7} | class")
    parities = {}
    for n in range(-2, 5):
        Tw, Wr, Sl, sigma = analyse_control(n)
        cls = "trivial" if sigma > 0 else "spinorial"
        parities[n] = sigma
        print(f"{n:>3} | {Tw:>+9.5f} | {Wr:>+9.5f} | {Sl:>+7.3f} | "
              f"{sigma:>+7.3f} | {cls}")

    odd_sigma = {n: s for n, s in parities.items() if n % 2}
    even_sigma = {n: s for n, s in parities.items() if not n % 2}
    print("\n  measured rule:")
    print(f"    Sl even -> sigma = {np.sign(list(even_sigma.values())[0]):+.0f}")
    print(f"    Sl odd  -> sigma = {np.sign(list(odd_sigma.values())[0]):+.0f}")
    print("\n  So the pi_1(SO(3)) = Z/2 class of the frame loop is set by the")
    print("  PARITY of Sl, not its magnitude. Sl = 2 and Sl = 0 lie in the")
    print("  same class; Sl = 2 and Sl = 1 do not.")
    print("=" * 74)

    artifact = ROOT / "docs" / "framed_unknot_results.json"
    payload = {
        "description": "Framing transformer of the Mobius-screw centerline",
        "source": "code/framed_unknot/framing_transformer.py",
        "companion_note": "papers/notes/Framing_Transformer_Spin_Parity.tex",
        "parameters": {"R": 1.0, "a": 0.3, "N_curve": 2000, "N_control": 1200},
        "mobius_screw": {
            "orthogonality_max_abs_T_dot_U": res["orthogonality_max"],
            "twist": res["Tw"],
            "writhe": res["Wr"],
            "twist_plus_writhe": res["Sl_check"],
            "self_linking_by_gauss_linking": {str(k): v for k, v in res["Sl"].items()},
            "self_linking_magnitude_expected_pq": 2,
            "sigma_adapted_frame": res["sigma_frame"],
            "sigma_framing_field": res["sigma_framing_field"],
            "sigma_closed_form": sigma_exact,
            "pi1_SO3_class": "nontrivial (spinorial)" if res["sigma_frame"] < 0
                             else "trivial",
        },
        "control_twisted_circles": {
            str(n): {"Sl": analyse_control(n)[2], "sigma": parities[n]}
            for n in sorted(parities)
        },
        "measured_rule": "sigma = (-1)^(Sl+1); equivalently (-1)^(p+q) for "
                         "torus curves. Spin content is the parity of Sl, "
                         "not its magnitude.",
    }
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\nartifact written: {artifact.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
