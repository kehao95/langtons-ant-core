# Repository method

This repository owns six publication projects: one-black highways, clocks and escape,
ports and composable scattering, wake rigidity and inverse synthesis, factor
language and mass defects, and finite-memory prediction and remote feedback.

## Ownership

- `one_black/`, `clock_escape/`, `four_cell_port/`, `wake_synthesis/`,
  `factor_language/` and `memory_feedback/` each own their paper, proof, evidence and release.
- Each uses `paper/`, `evidence/`, `release/` and `reproduce.py`. Formalized
  projects also have `lean/`; do not imply a Lean proof for the four-cell result.
- Project-specific code stays with its consumer: one-black dynamics in
  `one_black/langtons_ant/`, clock, port and wake checkers in their respective `verification/` directories.
- `research/` owns further deductions and the open HC program. Its Python
  modules depend on `one_black/`; the clock project is self-contained.
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
- Keep current navigation in project READMEs. Completed editorial process is
  recoverable from Git history rather than duplicated in live status documents.

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

## Current release approval boundary

On 2026-10-15, after reviewing the prepared manuscripts and Gemini editorial
discussion, the owner explicitly requested submission of the new Zenodo releases.
This authorizes the clock 0.4.0 update in its existing concept and the first
0.1.0 releases of port and wake. The existing one-black publication is retained.
Record exact delivery hashes, publication receipts and download verification.
The owner subsequently authorized README cleanup and Git commit/push of this
publication batch. Journal submission remains a separate approval step.

## Current wake release

The owner approved publication of the prepared 0.2.0 update with
“好的更新一下zenodo吧”, superseding the prior preparation-only boundary.
Version 0.2.0 is published as record 23405441 in the existing concept 23402421,
following record 23402422. It retains the general inverse-synthesis theorem and
uses the revised standard-wake uniqueness title. Preserve all versioned
published artifacts and the prepublication snapshots; publication receipts
record the delivered content. Journal submission remains a separate approval step.

## Six-paper preparation (2026-10-15)

The owner requested this portfolio consolidation after wake 0.2.0 publication.
Prepare wake 0.3.0 and port 0.2.0 in their existing concepts, plus first factor
and memory preprints. Retain one-black 0.2.0 and clock 0.4.0. This request
prepares reviewable local manuscripts and archives; it does not authorize
publishing these four new candidates. The earlier Zenodo approval was exercised
for the already published wake 0.2.0 package. Record fresh full/quick scope
separately and preserve every published versioned artifact.

For wake, thin-wake rigidity subsumes standard-layer-profile and complete-wake
uniqueness; use the strongest proved theorem while retaining its exact drift,
growth, width and thinness assumptions. Factor's finite-word mass proof is
independent of its infinite attraction proof. Memory owns the twenty-cell
lifetime obstruction; port owns finite scattering composition, including returns.
Older immediate 21/14/13 thresholds and PG-budget/rank-obstruction notes remain
research material until their required proof closure is assembled.

## Review revision (2026-10-16)

Continue the six-paper preparation from research `2f6010a`: wake owns mixed-wake
parity and its attributed periodic-growth dependencies; factor owns silent
legal-memory production and folded recovery/reset costs; memory owns the exact
birth-filtered query and growing-scale necessity. Port, clock and one-black
are unchanged. Retain pending version numbers and preserve earlier draft
snapshots. No new Zenodo authorization is implied. New-module replay and
hash-matched inheritance of an earlier full replay must be distinguished.
