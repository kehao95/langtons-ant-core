# Preprint

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23341609.svg)](https://doi.org/10.5281/zenodo.23341609)

This directory contains the source and generated PDF for the universal
one-black theorem preprint:

> Hao Ke, *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway:
> A Lean-Checked Proof*, Zenodo, 2026.
> [doi:10.5281/zenodo.23341609](https://doi.org/10.5281/zenodo.23341609)

The published record is available on
[Zenodo](https://zenodo.org/records/23341609). This directory remains the
reproducible manuscript source for subsequent revisions. The earlier
[version 22086968](https://doi.org/10.5281/zenodo.22086968) remains available
in the same version chain (concept ID 22086967).

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


## Published revision 0.2.0

The 2026-10-13 published revision strengthens the final predicate to the fixed
blank-highway word and proves complete standard-trace equality. See
[JOURNAL_REVIEW.md](JOURNAL_REVIEW.md), [verify.py](verify.py), and the
[clean-build evidence](verification/). The existing public record is preserved;
[RELEASE.md](RELEASE.md) records the published Zenodo version and artifact checksums.
[Published source manifest](published-source-manifest.json) preserves the exact
0.2.0 source and figure hashes; later repository documentation is tracked in Git.
The manuscript presents the theorem, scattering construction and reproducibility
in contribution-focused prose; internal review tasks remain in the review files.

## Editorial review — 2026-10-13

[Gemini 全文结构反馈与核对](reviews/gemini-2026-10-13/ASSESSMENT.md)记录了
通过 agy 进行的通读。作者决定保持原公开标题。建议保留证明章节顺序，
优先补充纯净态和历史隔离的动机，精简摘要常量并集中 Lean 实现说明。
这些建议已落实，见 [修改与核验记录](EDITORIAL_REVISION.md)。作者随后明确要求
发布；已使用原记录 22086968 的新版本 23341609 发布，concept ID 同为 22086967。
