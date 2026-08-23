# Repository contract

This repository is a proof artifact, not a general research workspace.

- Keep only code or prose that discharges a named obligation in `PROOF.md`.
- Do not add a test, checker, abstraction, or status document without naming
  the proof step that consumes it.
- When a claim changes, update `PROOF.md` and its finite verifier together.
- Verify the current proof cone with `python3 scripts/check.py`; do not invoke
  unrelated closure suites.
- Do not import predecessor implementations or documents.
