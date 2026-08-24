# Draft self-review

This is an internal reviewer-facing audit of `paper.md`, not part of the
typeset preprint.

## Contribution

- **Pass:** the theorem covers an unbounded natural family, not a coordinate
  window. The main statement is identical to the exported Lean theorem.
- **Pass:** the paper identifies two independently useful structural results:
  the 22-channel frontier decomposition and the exceptional affine reverse-hit
  normal form.
- **Boundary:** the literature audit does not establish priority. The title,
  abstract, and contribution list therefore avoid “first”.

## Clarity and reproducibility

- **Pass:** dynamics, time convention, P104 semantics, channel orientation,
  finite leaves, and the reproduction command are stated explicitly.
- **Pass:** the finite witness totals are identified as certificate work, not
  a uniform transient bound.
- **Pass:** the website is identified as exposition rather than proof evidence.
- **Pass:** the 22-panel scattering figure is exported from the app's exact
  replay canvas, contains every certified phase exactly once, and explicitly
  identifies independent panel fitting. Its light paper palette remains
  separable in a grayscale print preview.
- **Pass:** the exceptional-channel figure is an exact Stage 05 replay at the
  physical induction anchor (phase 72, depth 15), rather than a schematic. Its
  caption separates the finite history, reverse segment, fixed collision, and
  final forward highway, while treating the image as exposition rather than
  proof evidence.
- **Pass:** Stages 01/02 visualize the exhaustive first-contact split, Stage 04
  motivates the channel-specific historical cutoff, and Stage 06 summarizes
  the universal spatial partition. Every caption distinguishes its finite
  display window from the checked all-depth argument.
- **Pass:** the title page identifies Hao Ke and provides the author's contact
  address; the abstract and reproduction section link the public source-code
  and Lean-proof repository explicitly.
- **Needs pre-submission revision:** add the final affiliation, freeze a tagged
  artifact revision or DOI, and cite exact source locations from the final
  released commit.

## Evidence completeness

- **Pass:** `python3 one_black/check.py` rebuilds the final theorem from the
  checked-in proof cone.
- **Pass:** the PDF builds without missing citations, missing glyphs, undefined
  references, or typesetting warnings.
- **Not applicable:** baseline accuracy, ablations, and statistical metrics are
  not suitable evaluation criteria for an exact theorem. The relevant checks
  are exhaustive case coverage, certificate soundness, and reproducibility.

## Method and trust boundary

- **Pass:** the manuscript distinguishes analytic all-depth induction from
  finite native evaluation.
- **Pass:** `native_decide` is not described as kernel-only or axiom-free.
- **Scope limitation:** the theorem is exactly-one-black and observation-level
  P104. It does not settle arbitrary finite support, two black cells, or
  generalized ant rules.

## Submission blockers

1. Confirm affiliation and acknowledgements.
2. Freeze and tag the Lean artifact; record its commit hash in the paper.
3. Complete a broader citation-chain/database audit before considering any
   explicit priority claim.
4. Choose the target venue and adapt bibliography/style metadata accordingly.
