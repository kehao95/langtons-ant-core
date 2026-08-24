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
- **Needs pre-submission revision:** replace the placeholder author metadata,
  add a tagged artifact revision or DOI, and cite exact source locations from
  the final released commit.

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

1. Confirm author name, affiliation, contact address, and acknowledgements.
2. Freeze and tag the Lean artifact; record its commit hash in the paper.
3. Complete a broader citation-chain/database audit before considering any
   explicit priority claim.
4. Choose the target venue and adapt bibliography/style metadata accordingly.
