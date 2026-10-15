# Repository method

This repository owns three Langton-ant results: one-black highways, rational clocks
with exponential square-escape bounds, and sharp four-cell outgoing ports.

## Ownership

- `one_black/`, `clock_escape/` and `four_cell_port/` each own their paper, proof, evidence and release.
- Each uses `paper/`, `evidence/`, `release/` and `reproduce.py`. Formalized
  projects also have `lean/`; do not imply a Lean proof for the four-cell result.
- Project-specific code stays with its consumer: one-black dynamics in
  `one_black/langtons_ant/`, clock and port checkers in their respective `verification/` directories.
- `research/` owns further deductions and the open HC program. Its Python
  modules depend on `one_black/`; the clock project is self-contained.
- `docs/` owns the interactive one-black guide and its image/animation exporters.

## Evidence and changes

- A changed theorem lands with its proof narrative and verifier in one commit.
- Every executable check names the proof step it witnesses. Independent
  implementations used for cross-checking remain independent.
- The complete one-black theorem is Lean-checked; the full escape theorem is
  analytic, with local algebra and telescoping formalized in Lean. The four-cell
  result combines analytic reductions with exact computational certificates.
- Preserve published PDFs and source manifests. Rebuilt PDFs go to ignored
  `paper/build/` directories; release manifests describe historical snapshots.
- Keep current navigation in project READMEs. Completed editorial process is
  recoverable from Git history rather than duplicated in live status documents.

## Verification

```sh
python3 one_black/reproduce.py
python3 clock_escape/reproduce.py
python3 four_cell_port/reproduce.py
python3 research/check.py
make -C one_black/paper
make -C clock_escape/paper
make -C four_cell_port/paper
```

Run the checks affected by the change. The one-black reproduction uses a clean
Lean 4.30.0 build and audits both theorem axiom lists; the clock reproduction
runs bundled exact checkers and local Lean lemmas.
