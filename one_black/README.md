# Universal one-black proof

This directory is the complete local artifact for the theorem:

> For the classical two-colour Langton ant on the integer lattice, every
> initial state with exactly one black cell reaches the translating P104
> highway, for every ant position and heading.

## Contents

- [`PROOF.md`](./PROOF.md) states the theorem and connects every finite check
  to the recurrence, separation, induction, and symmetry arguments.
- [`langtons_ant/model.py`](./langtons_ant/model.py) is the literal update rule.
- [`langtons_ant/highway.py`](./langtons_ant/highway.py) constructs and checks
  the blank P104 witness, its recurrence predicate, and all prefix cases.
- [`langtons_ant/one_black.py`](./langtons_ant/one_black.py) checks the pristine,
  historical-wake, and exceptional phase-72 obligations.
- [`check.py`](./check.py) replays the finite proof obligations.

From any working directory, run:

```sh
python3 /path/to/langtons-ant-core/one_black/check.py
```

`check.py` derives every finite witness and case from exact integer dynamics.
`PROOF.md` supplies the recurrence, affine separation, induction, exhaustive
partition, and symmetry arguments that connect those computations to the
universal theorem.
