# General non-axis quadratic wake obstruction

A period-free necessary screen for every full drift `(a,b)` with `a*b != 0`.
The complete odd-class wake determines all odd-used edges. Their ordered-port
sign gives a quadratic character `q_d(O)` and the necessary conditions

```
Omega_d(O) = 1,    q_d(O) = 1+a  (mod 2),    after normalizing a>0.
```

The evaluator works in polynomial bit time in the explicit wake input. It uses
at most `g(a+1)` arithmetic edge runs, never expands huge gaps, and never reports
realizability: its answers are `EXCLUDED` or `NOT_EXCLUDED`. Axis drift is
unsupported, not excluded. No heading assumption is required.

The application excludes an explicit growth-eight, drift-`(3,1)` family at
arbitrarily large transverse span. Its 32-run symbolic identity holds for every
integer parameter `n>=1`, not just sampled sizes.

[Full proof and attribution](PROOF.md) · [Independent manuscript](paper.tex) ·
[Exact replay](evidence/full_replay.json). Jillhewar's stable-order criterion,
signed residues and rank-factorization method, and the project's earlier
`(2,-2)` mixed-wake formula retain their attribution. The contribution is the
general non-axis wake-only reduction and compressed algorithm, not a claim to
have invented permutation signs. Independent peer review remains pending.

## Reproduce

```sh
python3 wake_synthesis/verification/general_wake_parity/reproduce.py \
  --output /tmp/general-wake-parity.json
```

Python 3.10+ and a C++17 compiler with undefined-behavior sanitizer are required.
The full suite runs in a temporary directory, checks hashes, reconstructs all
reports, and compares deterministic results with retained evidence. It does not
write over evidence or releases. No network, solver, or external Python package
is needed. The manuscript can be compiled with pdfLaTeX.

To screen an input JSON object with `drift` and `wake` fields:

```sh
python3 wake_synthesis/verification/general_wake_parity/screen.py input.json
```

`screen.py` owns compressed arithmetic. `audit.py` builds literal individual
edges and checks them independently. `independent.cpp` starts from geometric turn
words and audits the port factorization. `family.py` derives affine runs and
certifies all minimum/maximum branches over `n>=1` symbolically.

This concerns HC's periodic-classification side, not the entry/convergence
problem. It proves neither HC nor existence or impossibility of every growth-eight
highway. This draft is not an authorization to post a preprint or submit a journal.
