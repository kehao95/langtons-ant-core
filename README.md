# Langton's Ant: proof and research core

This repository hosts the proof sources and reproducible artifacts for two
preprints by Hao Ke:

| Preprint | Published version | Sources and verification |
|---|---|---|
| *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway: A Lean-Checked Proof* | [0.2.0 — Zenodo](https://doi.org/10.5281/zenodo.23341609) | [Manuscript](preprint/README.md) · [Lean proof](one_black/README.md) |
| *An Ant on the Clock: Exponential Escape Bounds for Langton’s Ant* | [0.2.0 — Zenodo](https://doi.org/10.5281/zenodo.23341604) | [Manuscript, proof and checks](clock_escape/README.md) |

## Clock and exponential escape

For every square of n cells per side, every colouring and every initial pose,
the classical ant exits within **8 n 3ⁿ + 1 updates**. A rational clock gives
the bound and, for complete finite-support states, algorithms for reachability,
orbit equivalence and canonical orbit representatives.

The [clock directory](clock_escape/README.md) contains the published PDF,
LaTeX source, Lean local lemmas, exact checkers and numerical certificates.
Its reproduction workflow is self-contained:

```sh
python3 clock_escape/reproduce.py
make -C clock_escape
```

The full escape theorem has an analytic proof; Lean checks the local algebra
and telescoping lemmas. [Verification details](clock_escape/VERIFICATION.md)
connect each claim to its evidence.

## One-black theorem

This repository contains a complete Lean-checked proof that every classical
Langton-ant state with exactly one black cell, at any ant position and heading,
eventually reaches the standard translating period-104 highway:

```lean
theorem OneBlack.universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s
```

[![Global one-black proof map](./preprint/figures/stages/stage-06-global-map.png)](https://kehao95.github.io/langtons-ant-core/)

*Global proof map: every visible black-cell placement is assigned to one of
the five proof stages. The colored rays represent affine classes that the Lean
proof extends to every depth. Click the image for the interactive guide.*

- [Read the published preprint](https://doi.org/10.5281/zenodo.23341609)
- [Read the proof](./one_black/PROOF.md)
- [Inspect and rebuild the proof artifact](./one_black/README.md)
- [Explore the interactive proof guide](https://kehao95.github.io/langtons-ant-core/)
- [Download X-ready proof animations](./media/x/README.md)

> Hao Ke, *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway:
> A Lean-Checked Proof*, Zenodo, 2026.
> [doi:10.5281/zenodo.23341609](https://doi.org/10.5281/zenodo.23341609)

The browser guide is explanatory. The theorem in
[`one_black/lean/OneBlack.lean`](./one_black/lean/OneBlack.lean) and its closed
Lean proof cone are authoritative. This result does not prove the general
finite-support Highway Conjecture.


## Published revision 0.2.0 — 2026-10-13

The published revision explicitly binds the standard blank read word and exports
[`universal_one_black_standard_trace`](one_black/lean/StandardTrace.lean).
The [revised manuscript](preprint/paper.md), [review report](preprint/JOURNAL_REVIEW.md)
and [clean-build workflow](preprint/verify.py) document the published proof artifact.
[Zenodo 23341609](https://doi.org/10.5281/zenodo.23341609) is the new version
of record 22086968, with shared concept ID 22086967 and the original PDF retained.
The clock paper has its own [publication record](clock_escape/RELEASE.md).
[Public-repository verification](PUBLICATION_SYNC.md) records this integration.

## Open

External mathematical review and venue-specific journal preparation:
Journal of Automated Reasoning for the one-black paper and Natural Computing
for the clock paper are candidates. Subsequent editorial
work should accumulate locally before the next deliberate versioned release.
