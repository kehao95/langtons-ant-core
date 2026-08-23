# Repository Contract

This repository is rebuilt from first principles.  Preserve a small number of
named concepts and do not import predecessor code or documents wholesale.

Before adding a result:

1. Put its mathematical role in `theory/`.
2. State its assumptions and non-claims.
3. Add a certificate and verifier only when they are part of the result.
4. Keep exploratory programs in `research/` until promotion is justified.

Do not run broad replay suites merely because another result changes.  Verify
the narrow dependency cone affected by a change.

For the initial state-model cone, run `python3 scripts/check.py`. It invokes
only the repository's focused standard-library unit tests.
