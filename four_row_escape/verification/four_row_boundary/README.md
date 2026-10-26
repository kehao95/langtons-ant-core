# Four-row escape: exact persistent-boundary classification

**Result:** for the classical ant and every initial four-row rectangle coloring
and internal pose, the exact maximum first-exit time is

```
n:       1  2  3  4  5  6   7   8   9  10  11  12
S(4,n):  2 18 28 46 64 86 104 146 156 206 224 266
S(4,n) = 34*n-150 for EVERY n >= 13.
```

This proves Etse's MFCS 2026 Conjecture 11 (`S(4,n)<=34n`) and determines the
whole function, not merely its asymptotic slope. It does **not** solve HC or
assume general plane trajectories are confined to four rows.

Run from the repository root:

```sh
python four_row_escape/reproduce.py
```

Dependencies: Python standard library (3.10+), `g++` with C++17. Typical replay
in the development environment took approximately 11 seconds and 225 MiB;
those are informational measurements, not formal complexity claims.
The default check never overwrites `report.json`. `check.py --generate` is a
separate explicit development action, not called by the replay entrypoint.

## Proof/certificate split

- `core.py` constructs four persistent one-sided response catalogs, their exact
  column-extension operations, and a complete rooted weighted-query recurrence.
- `verify.cpp` independently reconstructs those operations from literal movement,
  checks ALL recurrence edges including both initial-head placements, and checks
  the affine stabilization inequalities and tight attainment edges.
- `check.py` independently recomputes the integer recurrence in Python, replays
  all representative behaviors and additional complete physical inputs, rejects
  altered certificates, and compares a fresh report to frozen evidence.
- `report.json` pins all numeric claims, source hashes, catalog/graph serialization
  and affine-vector hashes. Large tables are regenerated in a temporary directory.

The analytic arguments and exact certificate checker form the trusted base.
The verifier uses the supplied finite response classification and integer
recurrence; this proof is not Lean-formalized.

## Infinite-width coverage

There are 269 exact response types per side/parity. The width-7 and width-8
sets coincide and are closed under adding ANY of the 16 column colorings.
Every child residual is retained, so this is persistent memory, not a reset
oracle. The exact weighted graph has 21,248 vertices, 527,764 edges and 1,078
root goals. A two-phase vector certificate at widths 20 and 21 proves the
formula at ALL future widths. Simulations through width 1001 are controls only.

See [four-row-exact-escape](../../proof/four-row-exact-escape.md) for the full argument and
[main](../../paper/main.tex) for the complete article.

## Maximal examples

The native checker reconstructs maximal seeds for widths 1..23, 40,41,200,201,
1000,1001. Export and independently replay them with:

```sh
python four_row_escape/verification/four_row_boundary/check.py \
  --witnesses /tmp/four-row-maximizers.txt
```

A line is `n x y h time mask0 ... mask(n-1)`, headings N,E,S,W=0,1,2,3;
bit y of mask x is the initial black color at (x,y). The checker also verifies
an autonomous 21-crossing cut witness and an attained 34-update column.
