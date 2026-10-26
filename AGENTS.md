# Repository method

This repository owns eight publication projects: one-black highways, clocks and escape,
ports and composable scattering, wake rigidity and inverse synthesis, factor
language and mass defects, finite-memory prediction and remote feedback, and
bounded-defect arithmetic synthesis, and exact four-row escape.

## Ownership

- `one_black/`, `clock_escape/`, `four_cell_port/`, `wake_synthesis/`,
  `factor_language/`, `memory_feedback/`, `defect_synthesis/` and `four_row_escape/` each own their paper, proof, evidence and release.
- Each uses `paper/`, `evidence/`, `release/` and `reproduce.py`. Formalized
  projects also have `lean/`; do not imply a Lean proof for the four-cell result.
- Project-specific code stays with its consumer: one-black dynamics in
  `one_black/langtons_ant/`, clock, port and wake checkers in their respective `verification/` directories.
- `research/` contains supplementary complete-history and contour tools. Its
  Python modules depend on `one_black/`; `research/renewal/` has a self-contained
  scoped replay. The clock and four-row projects are self-contained.
- `docs/` owns the six interactive proof labs, their source-pinned exports,
  browser checks and the one-black image/animation exporters. See its README
  for the staged Pages build and interaction design.

## Evidence and changes

- A changed theorem lands with its proof narrative and verifier in one commit.
- Every executable check names the proof step it witnesses. Independent
  implementations used for cross-checking remain independent.
- The complete one-black theorem is Lean-checked; the full escape theorem is
  analytic, with supercritical local algebra and telescoping formalized in Lean.
  The critical O(3^n) square and fixed-height rectangle bounds have analytic
  proofs and exact Laurent-polynomial checks; those new proofs are not in Lean. The integer-clock square bound and wake-period
  synthesis also have analytic proofs and exact checks. Standard-wake uniqueness
  combines an all-period integer bound with complete ordered-event enumeration. The four-cell
  result combines analytic reductions with exact computational certificates.
- Preserve published PDFs and source manifests. Rebuilt PDFs go to ignored
  `paper/build/` directories; release manifests describe historical snapshots.
- Keep current navigation in project READMEs. Editorial operations and review history belong in the private
  research workspace, outside this public repository.

## Publication quality standards

Every preprint is a complete research article. Apply all four standards to the
actual source and rendered PDF intended for publication.

1. **External-reader review.** Have Gemini read the entire manuscript through
   `agy`. Ask whether the abstract identifies a concrete question, setup, main
   result and proof idea; whether notation and motivation arrive before use;
   and whether each section advances an argument comprehensible without project
   history. Resolve substantive findings and recheck materially revised prose.
   A model review is editorial evidence, not mathematical certification.
2. **A complete, standalone article.** Supply the definitions, hypotheses,
   statements and proof/dependency chain needed to understand and check the
   results. State external dependencies precisely and cite stable sources.
   Title pages and prose must contain no internal version history, editorial
   status, approval state, review rounds, release plans or change-log narration.
   Bibliographic version identifiers, reproducibility details and appropriate
   assistance disclosures remain valid scientific content. Inspect the PDF,
   including title page, cross-references, figures and bibliography.
3. **Constructive exposition.** Lead with the question, positive result and
   mechanism. Collect broader boundaries, unresolved extensions and non-results
   in a dedicated Limitations section, rather than interrupting the argument
   with repeated defensive disclaimers. Keep every necessary hypothesis in its
   theorem and setup. Preserve logical negations used in proofs, honest evidence
   scope and qualified sharpness claims; never strengthen a theorem by deleting
   a restriction or conceal a material limitation.
4. **Verified references.** Check that each reference exists, its authors,
   title, venue/date and DOI or stable version are correct, and the primary text
   supports the associated claim. Read the relevant passage or theorem; a
   resolving URL or search snippet alone is insufficient. Distinguish prior work
   from this article's contribution and preserve attribution. Record inaccessible
   or unresolved sources as unverified and resolve material citation gaps before
   publication; do not invent bibliographic details or priority claims.

Record manuscript/PDF hashes, review inputs and responses, findings, resolutions,
and verification scope in the private publication workspace. Distinguish pass,
revision required and unverified. When independent agents audit multiple papers,
use a separate reviewer context for each manuscript. Sol audits supplement the
Gemini check; neither substitutes for proof and certificate verification.

## Public repository boundary

This is the publication-facing repository. Keep articles, proofs, reproducible
certificates, scientific reference notes, result navigation, and released
artifacts here. Keep internal progress, owner instructions and quotes, approval
or hold state, reviewer conversations, editorial checklists, candidate histories,
and publication planning in the private research workspace. Do not link public
navigation to private operational records. `AGENTS.md` contains enduring
contributor standards, not session history or publication authorization.

Published PDFs and source archives remain immutable historical artifacts. Record
new scientific versions through the existing publication chains. Public release
notes describe scientific or reproducibility changes, not internal deliberations.
Do not rewrite Git history or alter an existing published archive during cleanup.

## Verification

```sh
python3 one_black/reproduce.py
python3 clock_escape/reproduce.py
python3 clock_escape/reproduce.py --critical-only
python3 four_cell_port/reproduce.py
python3 research/check.py
make -C one_black/paper
make -C clock_escape/paper
make -C four_cell_port/paper
python3 wake_synthesis/reproduce.py --search
make -C wake_synthesis/paper
python3 tools/prepare_preprints.py
```

Run the checks affected by the change. The one-black reproduction uses a clean
Lean 4.30.0 build and audits both theorem axiom lists; the clock reproduction
runs bundled exact checkers and local Lean lemmas.
