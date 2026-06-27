#!/usr/bin/env bash
# Single-command full reproduction of all verifiable claims.
# Runs every paper section as a script, then runs the test suite.
set -e

cd "$(dirname "$0")"

echo "================================================================"
echo "ACS Framework — Full Reproduction"
echo "================================================================"
echo ""
echo "Random seed: 20260423 (canonical)"
echo "Expected runtime: under 60 seconds"
echo ""

echo "================================================================"
echo "Paper C — Foundation theorems"
echo "================================================================"
python3 -m src.paper_c.theorem_c
echo ""
python3 -m src.paper_c.killing_orthogonality
echo ""
python3 -m src.paper_c.orthogonal_complement_probe
echo ""
python3 -m src.paper_c.spectral_taxonomy
echo ""
python3 -m src.paper_c.er_epr_algebraic

echo ""
echo "================================================================"
echo "Paper A — Phenomenology and parameter pruning"
echo "================================================================"
python3 -m src.paper_a.branch_a_parameters
echo ""
python3 -m src.paper_a.branch_a_vacuum
echo ""
python3 -m src.paper_a.betac_tan_beta
echo ""
python3 -m src.paper_a.yukawa_no_go
echo ""
python3 -m src.paper_a.theta13_obstruction
echo ""
python3 -m src.paper_a.tm1_pmns

echo ""
echo "================================================================"
echo "Paper B — Spectral / resolvent reinterpretation"
echo "================================================================"
python3 -m src.paper_b.explicit_formula_resolvent
echo ""
python3 -m src.paper_b.wronskian_leibniz
echo ""
python3 -m src.paper_b.renormalized_stability
echo ""
python3 -m src.paper_b.berry_keating_counting

echo ""
echo "================================================================"
echo "Test suite"
echo "================================================================"
python3 -m pytest tests/ -v

echo ""
echo "================================================================"
echo "All verifications complete."
echo "================================================================"
