# One-black standard-trace proof artifact, 0.2.0-review

This standalone archive contains the sources matching the accompanying revised
preprint and its clean-build report. It strengthens the original preprint's
terminal predicate to a fixed standard read word and exports complete future
standard-trace equality. No external two-black theorem is imported.

With Lean 4.30.0 installed:

```sh
python3 one_black/check.py
python3 preprint/verify.py       # optional new-directory/no-cache rebuild
```

The second command checks the actual axiom list. Both final theorems use the
same three native computation leaves, plus propext, Classical.choice and
Quot.sound. Native compiler/runtime trust is required. No Mathlib or network
dependency is needed after the pinned Lean toolchain is installed.

To typeset the manuscript, install Pandoc, XeLaTeX and the listed TeX packages,
then run `make -C preprint`. The browser visualization is not required.
`artifact-manifest.json` binds the exact source bytes, and the separate release
manifest binds the supplied PDF and ZIP. See `preprint/JOURNAL_REVIEW.md` for
the claim/evidence audit and `preprint/verification/` for actual build evidence.
This is an unpublished revision of DOI 10.5281/zenodo.22086968.
