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
- [`check.py`](./check.py) is the only proof-replay entrypoint.

From any working directory, run:

```sh
python3 /path/to/langtons-ant-core/one_black/check.py
```

The command uses only the Python standard library and files below this
directory. It does not read repository-root modules, research code, generated
certificates, predecessor artifacts, or the network.

## Trust boundary

The executable trust base is CPython plus the three modules listed above.
`check.py` derives its finite witness and cases from exact integer dynamics;
there is no serialized certificate to trust. The recurrence, affine-separation,
induction, case-exhaustion, and symmetry steps are the human-checked arguments
in `PROOF.md`. They are not claimed to be proof-assistant formalizations.

The root research layer may import this artifact. Nothing in this directory
imports that layer, so the proof remains independently reproducible.
