# Complete profile-classification evidence

The associated [proof](../../PROFILE_CLASSIFICATION.md) covers all 256 residue
assignments, with no period bound in the theorem hypotheses. The full replay is
`python3 wake_synthesis/verification/profile_classification/reproduce.py`.

`summary.json` records the final classification; `upper_certificate.json`
regenerates the inherited untrimmed integer witness. `audits.json` contains the
216 modular exclusions and local-string audits. `count_relaxations.json`
records all 256 capped count relaxations. `searches.json` records all 40 complete
cap-168 searches, not time-limited samples. `accepted_words.json` gives both
words, full finite seeds, and all-future checks. `differential.json` records
all 40 cap-104 UBSan comparisons against the inherited baseline.

`manifest.json` binds source and evidence hashes. This is computationally
assisted evidence, not a Lean proof or independent peer-review report.
