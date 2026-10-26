# Standard-profile classification

This module removes the longitudinal-residue hypotheses from standard-wake
uniqueness, while retaining drift `(2,-2)` and the layer-count vector
`(2,1,1,1,1,1,1,0,1,1,2)`.

See the [theorem and coverage proof](../../PROFILE_CLASSIFICATION.md) and
[retained evidence](../../evidence/profile_classification/README.md).

```sh
python3 wake_synthesis/verification/profile_classification/reproduce.py
```

The full replay regenerates the integer period-168 witness, the 256 count
relaxations, the 216 all-period modular exclusions, all 40 exact remaining
searches, independent infinite-tail checks, and 40 cap-104 sanitized comparisons
against the inherited baseline. Resource-limited searches fail as INCONCLUSIVE.
Replay uses a disposable directory and preserves the supplied evidence.

`counts_profile.py` owns the parameterized count relaxation;
`audit_profile.py` independently checks local strings and modular necessities;
`generate.py` produces the hash-pinned C++ parameterization;
`verify_word.py` checks accepted words independently of the enumeration graph;
`reproduce.py` assembles the proof checks. The inherited supplied-word criterion
is credited in the main proof; it is not claimed as new here.
