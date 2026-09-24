# Preserved verification failure: neutral slice versus coordinate submatrix

The first run's exact polynomial restriction passed, while the numerical
`neutral-hessian-unchanged-by-hidden-coefficients` check failed. The latter
used independent rows/columns26 and47 in its coordinate submatrix. But the
declared neutral slice fixes x26=d/sqrt(2), x47=-d/sqrt(2); the orthogonal
combination is a charged fluctuation. A larger coordinate submatrix therefore
includes a direction that is supposed to change under the hidden couplings.

The correction uses the actual neutral tangent matrix T, with its d-column
(e26-e47)/sqrt(2), and computes T^T H T. It independently compares this
pullback with the exact Hessian obtained from the already recorded neutral
polynomial in (a,u,w,d). It also compares the physical electric-charge-zero
spectrum across the three witness actions. The original script, results and
failure remain unchanged. No physical coefficients, eigenvalues, numerical
thresholds or other gates are changed. This amendment repairs the scope of
the verification test, not a scalar-spectrum failure.
