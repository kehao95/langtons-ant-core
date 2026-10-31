# Maximal Separated Phase Clocks and Spatial Charges for Cyclic Langton Ants

For a cyclic n-color ant, all-state observables separating the complete coloring from the head pose admit a constant-rate phase clock of maximal order 8n when both turn counts are odd, and 4n otherwise. One common coloring function for both checkerboard sectors has maximal order 4n. The article gives the full mixed-rule face equations, an explicit classical modulo-16 clock and the complete compact-charge basis over abelian groups.

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof map](PROOF.md) · [Evidence](evidence/README.md)

## Reproduce

```sh
python3 phase_cocycle/reproduce.py
make -C phase_cocycle/paper
```

Python 3.10+ without `-O`, a C++17 compiler and pdfLaTeX. The exact matrix audit requires SymPy 1.14.0.
Checks run in a disposable copy and compare frozen evidence without replacing it.
The package has no dependency on a separate research checkout.

`sources.json` fixes all article and certificate inputs by SHA-256.
