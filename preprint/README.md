# Preprint draft

This directory is the working manuscript area for the universal one-black
theorem. The current phase fixes the paper's story and its claim--evidence
boundary before prose or typesetting is expanded.

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

## Draft files

- [`OUTLINE.md`](./OUTLINE.md): the locked three-part narrative covering the
  proof architecture, literature positioning, and section-by-section preprint
  plan, with only audited claim and trust-boundary corrections.
- [`LITERATURE.md`](./LITERATURE.md): primary-source claim audit and priority
  boundary.
- [`references.bib`](./references.bib): bibliography used by the Pandoc draft.
- [`REVIEW.md`](./REVIEW.md): adversarial self-review and submission blockers.
- [`paper.md`](./paper.md): complete Markdown manuscript source.
- [`Makefile`](./Makefile): reproducible Pandoc/XeLaTeX build.
- [`paper.pdf`](./paper.pdf): generated preprint PDF after a successful build.

Build the PDF from this directory with `make`. The manuscript is a draft:
mathematical claims track the current Lean proof cone, while venue selection,
author metadata, and final copy-editing remain pre-submission work.
