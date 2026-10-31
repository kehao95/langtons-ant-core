# Sparse Initial Conditions and the Trace Space of Langton's Ant

With the initial pose fixed and at most m black cells at unrestricted coordinates, the number of length-n turn prefixes is Θ_m(n^m). The compact countable trace spaces satisfy `T_m' = T_(m-1)` and have Cantor–Bendixson rank m+1. A protected family of positive highway instances attains both the prefix exponent and the derived-set hierarchy; the optimal passive prediction mistake budget is m.

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof map](PROOF.md) · [Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23838433)

## Reproduce

```sh
python3 sparse_trace_space/reproduce.py
make -C sparse_trace_space/paper
```

Python 3.10+ without `-O`, a C++17 compiler and pdfLaTeX.
Checks run in a disposable copy and compare frozen evidence without replacing it.
The package has no dependency on a separate research checkout.

`sources.json` fixes all article and certificate inputs by SHA-256.
