# Repository method

This repository owns four publication projects: one-black highways, integer/rational
clocks and escape, sharp four-cell outgoing ports, and wake-period inverse synthesis.

## Ownership

- `one_black/`, `clock_escape/`, `four_cell_port/` and `wake_synthesis/` each own their paper, proof, evidence and release.
- Each uses `paper/`, `evidence/`, `release/` and `reproduce.py`. Formalized
  projects also have `lean/`; do not imply a Lean proof for the four-cell result.
- Project-specific code stays with its consumer: one-black dynamics in
  `one_black/langtons_ant/`, clock, port and wake checkers in their respective `verification/` directories.
- `research/` owns further deductions and the open HC program. Its Python
  modules depend on `one_black/`; the clock project is self-contained.
- `docs/` owns the interactive one-black guide and its image/animation exporters.

## Evidence and changes

- A changed theorem lands with its proof narrative and verifier in one commit.
- Every executable check names the proof step it witnesses. Independent
  implementations used for cross-checking remain independent.
- The complete one-black theorem is Lean-checked; the full escape theorem is
  analytic, with supercritical local algebra and telescoping formalized in Lean.
  The critical O(3^n) square and fixed-height rectangle bounds have analytic
  proofs and exact Laurent-polynomial checks; those new proofs are not in Lean. The integer-clock square bound and wake-period
  synthesis also have analytic proofs and exact checks. The four-cell
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
