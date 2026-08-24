# Preprint

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22086968.svg)](https://doi.org/10.5281/zenodo.22086968)

This directory contains the source and generated PDF for the universal
one-black theorem preprint:

> Hao Ke, *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway:
> A Lean-Checked Proof*, Zenodo, 2026.
> [doi:10.5281/zenodo.22086968](https://doi.org/10.5281/zenodo.22086968)

The published record is available on
[Zenodo](https://zenodo.org/records/22086968). This directory remains the
reproducible manuscript source for subsequent revisions.

## Canonical evidence

- [`../one_black/PROOF.md`](../one_black/PROOF.md): mathematical proof narrative.
- [`../one_black/lean/`](../one_black/lean/): definitions, analytic lemmas,
  finite checked data, and the final Lean theorem.
- [`../one_black/README.md`](../one_black/README.md): artifact entry point and
  reproduction command.
- [`../docs/`](../docs/): explanatory visualization only; not proof evidence.

The older `kehao95/langtons-ant` repository may supply research history,
candidate references, and useful exposition. No theorem, artifact claim, or
numerical constant is imported from it without checking against this
repository's current Lean proof cone.

## Manuscript files

- [`OUTLINE.md`](./OUTLINE.md): the locked three-part narrative covering the
  proof architecture, literature positioning, and section-by-section preprint
  plan, with only audited claim and trust-boundary corrections.
- [`LITERATURE.md`](./LITERATURE.md): primary-source claim audit and priority
  boundary.
- [`references.bib`](./references.bib): bibliography used by the Pandoc draft.
- [`REVIEW.md`](./REVIEW.md): adversarial self-review and submission blockers.
- [`paper.md`](./paper.md): complete Markdown manuscript source.
- [`Makefile`](./Makefile): reproducible Pandoc/XeLaTeX build.
- [`Every-One-Black-Cell-Langton-Ant-Reaches-the-Period-104-Highway-A-Lean-Checked-Proof.pdf`](./Every-One-Black-Cell-Langton-Ant-Reaches-the-Period-104-Highway-A-Lean-Checked-Proof.pdf):
  generated preprint PDF after a successful build.
- [`figures/scattering/`](./figures/scattering/): 22 terminal canvases exported
  directly from Stage 03 of the interactive proof app.
- [`figures/exceptional/`](./figures/exceptional/): the phase-72 depth-15
  physical-history replay exported from Stage 05.
- [`figures/stages/`](./figures/stages/): overview canvases exported from
  Stages 01, 02, 04, and 06 for the proof narrative.
- [`scripts/export_scattering_panels.mjs`](./scripts/export_scattering_panels.mjs):
  Playwright exporter for regenerating those canvases from a local `docs/`
  server.

Build the PDF from this directory with `make`. Mathematical claims track the
current Lean proof cone; the Zenodo record preserves the published preprint.
