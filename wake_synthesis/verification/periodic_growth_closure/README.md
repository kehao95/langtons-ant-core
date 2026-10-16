# Periodic growth: closed proof dependencies and small-drift obstructions

Read `PROOF.md`. This package supplies the signed-residue and rank-permutation
arguments behind the prior external dependencies, together with the complete
unit-diagonal certificate. It proves the necessary global periodic-growth bound
`g >= 8`; it does not prove that growth eight occurs or that HC is true/false.

Further all-period conclusions:

* full axis drift of two cells forces `P = 4 (mod 8)` and `g = 0 (mod 8)`;
* full diagonal drift `(2,-2)` cannot have a checker-pure odd-class wake, for
  any growth; both checker parities occur a positive even number of times;
* at growth eight and that diagonal drift, exactly six residue-count matrices
  remain after these necessary tests. They are not asserted realizable.

The external source is A. Jillhewar (2026), pinned at
`76a7e234e577d992d086c204c3dea00ae72cf10a`; attribution and license are retained.
Two audit scripts are byte-identical to that source, and a separate local
implementation checks the algebra and witnesses. The full general arguments
are written here, not delegated to a library theorem or an external website.

```sh
python reproduce.py --output /tmp/periodic-growth-replay.json
```

Python 3.10+ standard library suffices. All sources and reports are pinned by
SHA256. The 1.7 MB unit certificate is regenerated, hash-matched, and then checked
branch-by-branch by an independent verifier; no optimizer, network or SAT result
is needed. Original unit Python sources are unchanged; proof Sections 1-6 are retained
with an updated integration note. The earlier result is not
claimed as newly discovered in this integration.

Do not use `python -O`. A thrown exception is failure, not a negative mathematical
answer. No public preprint, DOI, Lean claim or peer-review status is changed.
