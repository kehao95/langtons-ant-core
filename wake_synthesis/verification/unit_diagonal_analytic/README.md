# Analytic unit-diagonal exclusion

A standalone analytic proof of the project's no-unit-diagonal-highway theorem:
no finite-support periodic trace has FULL displacement `(1,-1)` or a quarter-turn
rotation, at any period, width or growth. This is not an exclusion of the
primitive direction: standard P104 has FULL displacement `(2,-2)`.

The theorem and its global `g>=8` corollary already appeared in parallel main
revision `2067bb5`. The new contribution is removing the finite enumeration
premise. Two forced layer words and a binary interleaving contradiction give
a human-checkable proof. Existing signed-residue and other small-drift results
retain their attribution; the growth corollary is not claimed again as new.

- [Analytic proof and provenance](PROOF.md)
- [Standalone manuscript source](../../paper/main.tex)
- [Fresh independent regressions](evidence/full_replay.json)
- [Source manifest](evidence/source_manifest.json)

Run from the repository root:

```sh
python3 wake_synthesis/verification/unit_diagonal_analytic/reproduce.py --output /tmp/unit-diagonal-replay.json
```

The mathematical proof requires no program. The optional regressions require
Python 3.10+ without `-O` and g++ with C++17/undefined-behavior sanitizer. They
build in a disposable directory and refuse to overwrite an existing report.
Any interruption or failed check is not accepted as verification.

The complete-row Python and independent vector-geometry C++ implementations
agree on 4/124/12,756 candidates and 2/2/0 survivors. All 12,880 rejection witnesses
are checked, alongside literal port/count controls and 936 genuine P104 prefixes.
`analytic_audit.py` checks the five displayed return paths, the forced second
layer, and the binary interleaving implication. These checks are not theorem
premises. Detailed witnesses can be regenerated:

```sh
python3 wake_synthesis/verification/unit_diagonal_analytic/local_obstruction.py --certificates /tmp/unit-diagonal-certificates.json.gz
```

The analytic proof appears in the accompanying article.
