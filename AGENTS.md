# Repository contract

This repository is a minimal proof and research artifact.

- One-black proof code and prose must discharge an obligation in
  `one_black/PROOF.md`; general deductions belong in root `PROOF.md`.
- A research addition must sharpen one edge in `RESEARCH.md`; exploratory
  detail belongs in commit history until it changes that graph.
- Do not add a test, checker, or proof abstraction without naming the proof
  step that consumes it. Do not split `RESEARCH.md` into status documents.
- When a claim changes, update its owning proof document and finite verifier
  together.
- Distinguish local proof, predecessor evidence, finite experiment, and open
  conjecture. Never promote a predecessor result without reconstructing its
  proof object locally.
- Verify the closed theorem with `python3 one_black/check.py`. Verify only the
  separate consequences with `python3 research/check.py`; do not invoke
  unrelated closure suites.
- `one_black/` must remain standalone: no import or runtime read may escape its
  directory. Research may depend on it, never the reverse.
- Do not import predecessor implementations or documents.
