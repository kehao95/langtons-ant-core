# Repository contract

This repository is a minimal proof and research artifact.

- Proof code and proof prose must discharge a named obligation in `PROOF.md`.
- A research addition must sharpen one edge in `RESEARCH.md`; exploratory
  detail belongs in commit history until it changes that graph.
- Do not add a test, checker, or proof abstraction without naming the proof
  step that consumes it. Do not split `RESEARCH.md` into status documents.
- When a claim changes, update `PROOF.md` and its finite verifier together.
- Distinguish local proof, predecessor evidence, finite experiment, and open
  conjecture. Never promote a predecessor result without reconstructing its
  proof object locally.
- Verify the current proof cone with `python3 scripts/check.py`; do not invoke
  unrelated closure suites.
- Do not import predecessor implementations or documents.
