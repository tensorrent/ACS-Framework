#!/usr/bin/env python3
"""Local truth vs global correctness: what averaging deletes.

The claim being tested: consensus formed by averaging deletes minority
information, and the deleted information is exactly what predicts failure.
Local perspectives are each TRUE; the invariant is CORRECT; and you do not
reach the second by averaging the first.

    C1  does the mean delete the information that predicts failure?
    C2  how often, in general?  (not one anecdote)
    C3  does iterative "cleaning" make the record look safer while the risk
        is unchanged?
    C4  an invariant is NOT an average -- the Tw/Wr case
    C5  true vs correct, stated as two different predicates
    C6  the boundary: what this does and does not establish

SCOPE, stated up front because it bounds everything below: this is a result
about INFORMATION AGGREGATION -- what an averaging operator does to a
distribution.  Whether that explains any human institution is a reading, not a
result, and C6 marks the line rather than blurring it.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78
rng = np.random.default_rng(20260901)


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def c1_the_mean_deletes_the_failure():
    head("C1", "Does the mean delete the information that predicts failure?")
    print("""  A worked case already in this corpus: the latency fixture from the eval
  runs.  Four releases, a 125 ms threshold, and a report that concluded "no
  regression" from the mean.\n""")
    data = {"v1.0": 120.0, "v1.1": 118.5, "v1.2": 131.2, "v1.3": 129.9}
    thr = 125.0
    mean = float(np.mean(list(data.values())))
    over = {k: v for k, v in data.items() if v > thr}
    print(f"     {'release':>8}  {'p95':>7}  {'vs 125ms':>9}")
    for k, v in data.items():
        print(f"     {k:>8}  {v:>7.1f}  {'OVER' if v > thr else 'ok':>9}")
    print(f"\n     mean          = {mean:.2f} ms   -> {'PASS' if mean < thr else 'FAIL'} (margin {thr-mean:.2f} ms)")
    print(f"     worst member  = {max(data.values()):.1f} ms   -> exceeds by {max(data.values())-thr:.1f} ms")
    print(f"     members over threshold: {len(over)} of {len(data)}  ({', '.join(over)})")
    ratio = (max(data.values()) - thr) / (thr - mean)
    print(f"\n     the mean's margin understates the worst case by {ratio:.0f}x")
    print("""
     Both statements are TRUE: the mean is under threshold, and half the
     releases are over it.  Only one of them predicts the outage.  The
     averaging operator is what removed the other.""")
    return {"data": data, "threshold": thr, "mean": mean,
            "members_over": list(over), "understatement_factor": float(ratio)}


def c2_how_often_in_general():
    head("C2", "How often, in general?  (one case is an anecdote)")
    print("""  Draw many populations and count how often the mean passes a threshold
  while at least one member fails it.  Sweep the spread, since that is the
  parameter the mean is blind to.\n""")
    n_pop, n_members, thr = 20000, 8, 100.0
    print(f"     {'spread (sd)':>12}  {'mean passes':>12}  {'a member fails':>15}  {'mean passes AND member fails':>29}")
    rows = []
    for sd in (2, 5, 10, 20, 40):
        vals = rng.normal(95.0, sd, size=(n_pop, n_members))
        mean_ok = vals.mean(axis=1) < thr
        any_bad = vals.max(axis=1) > thr
        both = np.mean(mean_ok & any_bad)
        rows.append({"sd": sd, "mean_passes": float(mean_ok.mean()),
                     "member_fails": float(any_bad.mean()), "masked": float(both)})
        print(f"     {sd:>12}  {mean_ok.mean():>12.3f}  {any_bad.mean():>15.3f}  {both:>29.3f}")
    peak = max(rows, key=lambda r: r["masked"])
    print(f"""
     The masked fraction is NOT monotonic -- it peaks at sd = {peak['sd']} ({peak['masked']*100:.0f}% of
     draws) and falls to {rows[-1]['masked']*100:.0f}% by sd = {rows[-1]['sd']}.  That shape is the finding, and it
     is sharper than "more spread is worse":

        sd small ...... everyone agrees and nobody is over.  Nothing to mask.
        sd MODERATE ... the mean still looks comfortable while the tail is
                        already out.  Maximum masking.
        sd large ...... the outliers drag the mean over too, so the average
                        FAILS as well ({rows[-1]['mean_passes']*100:.0f}% pass vs {rows[0]['mean_passes']*100:.0f}% at sd={rows[0]['sd']}) and the
                        disagreement becomes visible in the summary statistic.

     So the dangerous regime is MODERATE heterogeneity, not extreme.  Loud
     disagreement is self-reporting; it is quiet disagreement -- large enough
     to breach, small enough not to move the mean -- that the average deletes.

     This is not a flaw in any particular average.  It is what an average IS:
     a statistic that discards the distribution and keeps one moment.""")
    return {"rows": rows, "threshold": thr, "members": n_members,
            "peak_masking_sd": peak["sd"], "peak_masking": peak["masked"],
            "monotonic": False}


def c3_iterative_cleaning():
    head("C3", "Does 'cleaning' the outliers make it look safer?")
    print("""  Consensus procedures usually do not just average once -- they iterate,
  dropping the readings that disagree most, then re-averaging.  Run that.\n""")
    vals = np.concatenate([rng.normal(95, 4, 40), rng.normal(140, 8, 6)])  # a real minority
    thr = 100.0
    print(f"     {'round':>6}  {'n':>4}  {'mean':>7}  {'reported':>9}  {'true max':>9}  {'true risk':>10}")
    rows, cur = [], vals.copy()
    true_max = float(vals.max())
    for rnd in range(6):
        m = float(cur.mean())
        rows.append({"round": rnd, "n": int(cur.size), "mean": m,
                     "reported": "PASS" if m < thr else "FAIL",
                     "true_max": true_max})
        print(f"     {rnd:>6}  {cur.size:>4}  {m:>7.2f}  {'PASS' if m < thr else 'FAIL':>9}"
              f"  {true_max:>9.2f}  {'UNCHANGED':>10}")
        if cur.size < 8:
            break
        keep = np.abs(cur - cur.mean()) <= 2.0 * cur.std()      # drop the dissenters
        cur = cur[keep] if keep.sum() < cur.size else cur[:-1]
    print(f"""
     The reported mean falls every round and the true maximum never moves.
     Each individual round is defensible -- outlier rejection is a standard,
     well-founded procedure. The composition is what fails: the readings being
     dropped are the only ones carrying the tail, so the process converges to a
     number that describes a population it has itself constructed.

     The record gets cleaner and the system does not get safer.""")
    return {"rounds": rows, "true_max": true_max, "threshold": thr}


def c4_invariant_is_not_an_average():
    head("C4", "An invariant is NOT an average of the local readings")
    print("""  The tempting repair is: if one frame is partial, average over frames.
  Test it on a case where the invariant is known -- the Tw/Wr family at
  Sl = 2, where every split is a TRUE reading from some framing.\n""")
    fam = [(2.0, 0.0), (1.5, 0.5), (1.0, 1.0), (0.5, 1.5), (0.0, 2.0)]
    tw = np.array([a for a, _ in fam]); wr = np.array([b for _, b in fam])
    sl = tw + wr
    print(f"     {'Tw':>5}  {'Wr':>5}  {'Sl':>5}")
    for a, b in fam:
        print(f"     {a:>5}  {b:>5}  {a+b:>5}")
    print(f"\n     mean Tw = {tw.mean():.2f}   mean Wr = {wr.mean():.2f}   -> the 'consensus' framing")
    print(f"     Sl for every member       = {sorted(set(sl))}")
    print(f"     Sl is constant across frames?  {len(set(sl)) == 1}")
    print(f"""
     The averaged reading (Tw={tw.mean():.1f}, Wr={wr.mean():.1f}) is a legitimate member here --
     but it is not privileged, and it is not where the invariant lives.  Sl is
     obtained by finding what is PRESERVED across frames, not by averaging
     them.  Averaging happens to land inside this family; in general it lands
     on no frame at all (the mean of two valid rotations is not a rotation).

     The general point: invariance is a property of the GROUP ACTION, and the
     way to find it is to ask what commutes with the action -- not to take a
     mean over its orbit.""")
    return {"family": fam, "mean_Tw": float(tw.mean()), "mean_Wr": float(wr.mean()),
            "Sl_values": sorted(set(map(float, sl))), "Sl_invariant": len(set(sl)) == 1}


def c5_true_vs_correct():
    head("C5", "True and correct are different predicates")
    print("""     TRUE     a local reading is true if it is what that frame actually
              observes.  Every frame in C4 reports truly.  A false reading is
              one the frame does not in fact produce.

     CORRECT  a statement is correct if it holds across frames.  Sl = 2 is
              correct.  "Tw = 1.5" is TRUE in one framing and NOT CORRECT,
              because another framing reports 2.0 and neither is privileged.

  The two failure modes are opposite, and confusing them is the error:

     mistaking TRUE for CORRECT   -> "my measurement says 118.5 ms, so we are
                                     fine" -- true locally, wrong globally
     mistaking CORRECT for TRUE   -> "the invariant is 2, so every observer
                                     must measure 2" -- correct globally,
                                     false as a prediction of any local reading

  C1-C3 are the first error at scale.  Averaging produces a number that is
  true of nothing -- no release had 124.90 ms -- and treats it as the global
  fact.  The invariant it should have reported (the maximum, for a threshold
  question) was available the whole time and was discarded by the operator.

  So the corrective is not "listen to minorities" as a value.  It is
  structural: FOR A THRESHOLD QUESTION THE INVARIANT IS THE EXTREMUM, NOT THE
  MEAN, and using the wrong statistic deletes the answer before anyone
  deliberates.""")
    return {"true": "holds in a given frame", "correct": "holds across frames",
            "error_1": "treating a local truth as global",
            "error_2": "treating a global invariant as a local prediction",
            "corrective": "for a threshold question the invariant is the extremum"}


def c6_boundary():
    head("C6", "What this establishes, and what it does not")
    print("""  ESTABLISHED, computed above:
     * an averaging operator discards the distribution and keeps one moment,
       so it cannot answer a threshold question (C1);
     * the failure is systematic rather than anecdotal, and PEAKS AT MODERATE
       heterogeneity (C2) -- loud disagreement moves the mean and so reports
       itself; quiet disagreement does not and is deleted;
     * iterated outlier rejection lowers the reported number while leaving the
       true extremum untouched (C3);
     * an invariant is found by what is preserved under the group action, not
       by averaging over its orbit (C4).

  NOT ESTABLISHED, and worth being plain about:
     * that any human institution behaves this way.  These are properties of
       operators on distributions.  Applying them to governance is a READING
       -- it may be a good one, and it is not something this instrument tests.
       An institution has feedback, incentives and memory that no statistic
       here models.
     * that minority readings are more accurate.  C3's minority carried the
       tail by construction.  A minority reading can equally be an error, and
       nothing computed here distinguishes those cases -- that is exactly what
       an evidence chain is for.

  The transferable part is narrow and solid: CHOOSE THE STATISTIC THAT MATCHES
  THE QUESTION.  For "will anything breach?", that is the extremum.  A mean
  answers a different question, truly, and its answer is not correct.""")
    return {"established": ["averaging cannot answer threshold questions",
                            "failure grows with heterogeneity",
                            "iterated trimming lowers the report, not the risk",
                            "invariants come from preservation, not averaging"],
            "not_established": ["that institutions behave this way",
                                "that minority readings are more accurate"]}


def main():
    print(RULE)
    print("LOCAL TRUTH vs GLOBAL CORRECTNESS: WHAT AVERAGING DELETES")
    print(RULE)
    res = {"C1_mean_deletes_failure": c1_the_mean_deletes_the_failure(),
           "C2_how_often": c2_how_often_in_general(),
           "C3_iterative_cleaning": c3_iterative_cleaning(),
           "C4_invariant_not_average": c4_invariant_is_not_an_average(),
           "C5_true_vs_correct": c5_true_vs_correct(),
           "C6_boundary": c6_boundary()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  "All true, but global is correct" is two predicates, and the gap between
  them is where the failure lives.

    C1  mean 124.90 < 125 (PASS) while half the releases are over -- both
        statements true, one predicts the outage, the operator deleted it.
        The mean's margin understates the worst case {res['C1_mean_deletes_failure']['understatement_factor']:.0f}x.
    C2  and it is systematic, with a shape: masking PEAKS at moderate spread
        ({res['C2_how_often']['peak_masking']*100:.0f}% of draws at sd={res['C2_how_often']['peak_masking_sd']}) and falls at extreme spread, because
        loud disagreement drags the mean over too and so reports itself.  It
        is QUIET disagreement that gets deleted.
    C3  iterated outlier rejection lowers the reported mean every round while
        the true maximum never moves.  Cleaner record, same risk.
    C4  and averaging frames does not recover the invariant.  Sl is what is
        PRESERVED across framings, not the mean of them.
    C5  so: true = holds in a frame; correct = holds across frames.  For a
        threshold question the invariant is the EXTREMUM, and using the mean
        deletes the answer before anyone deliberates.

  C6 marks the boundary honestly: these are results about operators on
  distributions.  That institutions behave this way is a reading, not
  something computed here.""")
    print(RULE)
    out = ROOT / "docs" / "consensus_and_invariants.json"
    out.write_text(json.dumps({
        "description": "Local truth vs global correctness; what averaging deletes",
        "source": "code/constraint_projection/consensus_and_invariants.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
