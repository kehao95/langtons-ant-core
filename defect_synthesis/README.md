# Counting Defects: Semilinear Reachability and Resource Bounds for Langton's Ant

This paper owns fixed-defect all-coordinate synthesis, complete endpoint arithmetic,
resource spectra for supplied finite schema collections, and small positive witnesses.
It is independent of the factor paper's attraction and mass inequality, while using
its bounded-fold coverage theorem as an attributed input.

[Manuscript](paper/main.tex) · [Review PDF](release/v0.1.0/paper.pdf) ·
[Proof map](PROOF.md) · [Replay](evidence/consolidation-replay.json) ·
[Release preparation](release/README.md)

## Results

- For each supplied mass/event budget, the complete input-coordinate relation is
  effectively semilinear. Event times, poses and endpoint black membership remain exact.
- Minimum first-black cost and contained-defect count of a bounded-power schema
  are piecewise rational-affine. A finite collection admits either a fixed-cost
  unbounded-defect ray or a computable affine supply budget.
- `B[9:] A^a B A^b P^r` is feasible exactly for `a>=1, 0<=b<a, 0<=r<=b+2`.
  Its exact resource image gives the sharp bound `10D<=9C-309`.
- Positive witnesses have polynomial bit length in unary mass and event budgets;
  the existence problem is in NP. The global minimum cost μ(N) has the analytic
  deterministic upper bound `2^O(N^2 log(N+2))`.

The budget counts forward ten-windows wholly contained in the word. The first
nine inverse-history J10 tests belong to a different finite-count convention.
Neither the fixed-budget construction nor a fixed finite schema collection
bounds the number of events on every finite input.

## Quantifier-free backend — 20 October 2026

A restricted supplied-schema backend constructs a polynomial-size QF_LIA circuit
for exact physical execution, factor counts and endpoint-colour queries. Shared
suffix registers avoid Cartesian zero-power case expansion. Unary budgets with
binary linear side conditions admit polynomial-bit positive witnesses; the
minimum cost mu(N) has an FP^NP upper bound. These refine the existing small-witness
result rather than establish NP membership a second time.

Powered words must restore heading with diagonal stride 2 or axis stride 2/4;
source terms are finite XOR segments of those strides or singletons. The older
compiler still owns arbitrary quantified source predicates, complete target
field equality and explicit semilinear projection. The new solver is not a
polynomial-time global synthesis algorithm.
[Proof](proof/quantifier-free-defect-complexity.md) ·
[Fresh backend replay](evidence/replay-2026-10-20.json).

## Reproduce

```sh
python3 defect_synthesis/reproduce.py
make -C defect_synthesis/paper
```

Use Python 3.10+ without `-O`, C++17, the system Z3 and ISL/GMP shared libraries (the retained
reports use ISL 0.27), and pdfLaTeX. The entrypoint verifies the import hashes and
runs the four retained modules and six new backend sections in a disposable copy, including independent finite controls
and finite-cover reconstruction. Source snapshots retain their original research
README paths; the commands above are the portable public entrypoints.

The full all-coordinate nonzero-budget disjunction is a constructive theorem,
not an executed enumeration. The small-witness result has a complete analytic
proof in the paper; its original optional implementation archive is not available
in this checkout and its reported controls are not counted as replayed here.
The supplied-schema, supply-spectrum and optimization implementations are included.

Use `--new-results-only` for the QF backend alone. The restored QF implementation
is distinct from the still-missing original small-witness archive.

## Open

Author review of the first 0.1.0 candidate; restore the original small-witness
implementation if available as supplementary controls. Publication requires the
owner's approval. Independent mathematical review and journal preparation remain open.
