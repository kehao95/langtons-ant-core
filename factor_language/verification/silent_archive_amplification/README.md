# Silent archive / J10 bridge audit

[Full proof and quantifiers](../../proof/silent-archive-amplification.md).
"Silent" means no J10, not no old-memory reads. The complete finite field is
retained at every checkpoint.

For every n>=1, the explicit (10n+41)-black input first reaches J10 at 56n+168,
with fixed input/event poses but a 4n+13-high excursion. Before then every initial
black lifetime is consumed. A legal prelude creates 2(n+1) distinct black
lifetimes later consumed at J10 events, including n+1 of age at least 48n+124.
The twenty-step pulse executes n+1 times and fails at relative offset 20n+22;
it is not infinitely self-renewing.

```sh
python3 factor_language/reproduce.py --extensions-only
```

The witness is declarative. `affine.py` covers every integer n>=1 by the complete
arrangement of affine visit intervals. Its infinite slab is checked by exact
endpoint/slope conditions. `independent.cpp` and a separate Python vector
simulator provide finite implementation controls, not the universal bridge.
`check.py --write <file>` explicitly writes a new report; normal checking never
repairs or overwrites a witness.

The finite-prefix certificate is accompanied by the
[all-parameter construction](../../proof/silent-archive-amplification.md) and
[complete recovery proof](../../proof/silent-archive-recovery.md).
