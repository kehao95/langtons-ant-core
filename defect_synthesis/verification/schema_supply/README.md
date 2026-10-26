# Flat-schema initial supply and defect budgets

This isolated module computes complete same-cell feasibility, the minimum
INITIAL black supply, and contained ten-factor defect counts for supplied
bounded-power word expressions. No geometric bounding box or exponent cap is
used in the symbolic statements. It is not an all-input HC classifier.

The completed three-variable family `B[9:] A^a B A^b P^r` is feasible exactly
when `a>=1, 0<=b<a, 0<=r<=b+2`. Its minimum supply is `46+5a+5b`; its defects
are zero for r=0 and `9r-3` otherwise. Exact image decomposition gives the sharp
bound `10D<=9C-309` and maximum `15+9*floor((m-51)/10)` at input mass m>=51.
Only its original one-parameter subfamily has the separate existing full-recovery
proof. No all-future claim is made for every new asymmetric seed.

Full proof: [supply dichotomy](../../proof/flat-schema-supply-dichotomy.md).

```
python3 defect_synthesis/verification/schema_supply/reproduce.py
```

Requirements: Python 3.10+, system libisl (frozen report: isl-0.27-GMP), g++
with C++17. No network, Python package installation, solver service, or changed
shared runtime is required. `--write` explicitly writes a new report;
`--compare` never repairs the immutable witness or saved report.

`unary_count` is a certified interval/residue fast path. It first proves exact
progression coverage, rather than assuming convexity or extrapolating a count.
Unsupported fibres raise `Unsupported` (UNKNOWN), never NO. The general analytic
counting theorem uses the explicitly cited published unary-counting result;
this package is not a complete implementation of that general QE algorithm.

The general ray classifier requires a supplied COMPLETE semilinear decomposition
and proves equality with the computed relation before applying it. The synthetic
vertical-ray control is arithmetic-only, not a discovered ant counterexample.
Native ISL/GMP and this Python compiler are trusted for universal symbolic checks.
The C++ literal implementation is an independent finite control, not an outside
mathematical review. No Lean or priority claim is made.
