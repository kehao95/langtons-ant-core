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

## Reproduce

```sh
python3 defect_synthesis/reproduce.py
make -C defect_synthesis/paper
```

Use Python 3.10+ without `-O`, C++17, the system ISL/GMP shared library (the retained
reports use ISL 0.27), and pdfLaTeX. The entrypoint verifies the import hashes and
runs four exact modules in a disposable copy, including independent finite controls
and finite-cover reconstruction. Source snapshots retain their original research
README paths; the commands above are the portable public entrypoints.

The full all-coordinate nonzero-budget disjunction is a constructive theorem,
not an executed enumeration. The small-witness result has a complete analytic
proof in the paper; its original optional implementation archive is not available
in this checkout and its reported controls are not counted as replayed here.
The supplied-schema, supply-spectrum and optimization implementations are included.

## Open

Author review of the first 0.1.0 candidate; restore the original small-witness
implementation if available as supplementary controls. Publication requires the
owner's approval. Independent mathematical review and journal preparation remain open.
