# Reproduction and certificate scope

`escapes.json` lists the complete first-read branching tree for at most
three black cells. `witness.json` supplies the four-cell highway port.
The analytic coverage lemma turns the finite tree into the all-coordinate bound.
The runner regenerates the base certificates, compares two independent
implementations and checks guarded scattering and return-scattering interfaces.

```sh
python3 four_cell_port/reproduce.py
```

[Proof dependencies](../PROOF.md) · [Source file hashes](../sources.json)

## Rectangular frames

Full 42-schema certificate replay and the 3538-input finite complement, including all infinite tails.

[Module and retained evidence](../verification/rectangular_frames/). Run
`python3 four_cell_port/reproduce.py --frames-only --jobs 3`. The analytic coverage
argument is in the article and [proof map](../PROOF.md).
