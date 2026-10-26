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
