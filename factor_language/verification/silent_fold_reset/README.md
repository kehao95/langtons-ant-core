# Silent fold / autonomous reset audit

A complete one-parameter finite-support family, its six natural post-return
scans, exact standard-entry time, and a linearly growing repair cost. This is
not a global HC theorem or an infinite autonomous counterexample.

`grammar.json` lists every finite word and affine exponent. `check.py` derives
the complete initial field, chronological affine read records and field updates.
The all-parameter finite reduction is in [silent-fold-reset.md](../../proof/silent-fold-reset.md):
all breakpoint orders are fixed for n>=2, so n=0,1,2 are complete order cases,
not three sampled seeds. Full literal simulations are independent controls.

`derived_masks.json` is regenerated data: complete top/bottom caps, bulk colour
requirements and all reset comparisons. Its SHA256 and the source hashes are
in `report.json`. The root runner compares both generated files byte-for-byte.

```sh
python3 factor_language/reproduce.py --extensions-only
```

Initial intrinsic J10 events at times 0..8 are retained in the count. Spatial
endpoint bounds fail for J10 here, not for the previously proved S_D predicate.
