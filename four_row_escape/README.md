# From Four Rows to Five: Escape Times and Persistent Memory in Langton's Ant

Four rows have exact maximal first-exit time `34n-150` for `n>=13`, with all smaller values determined. Five rows admit an explicit width-`4k+9` source with exact exit time `8k²+60k+16` and infinitely many persistent boundary responses. The complete two-counter family has an exact earliest P104 entrance formula and polynomial-bit-time random access to its full evolving state.

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof map](PROOF.md) · [Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23844660)

## Reproduce

```sh
python3 four_row_escape/reproduce.py
make -C four_row_escape/paper
```

Python 3.10+ without `-O`, a C++17 compiler and pdfLaTeX.
Checks run in a disposable copy and compare frozen evidence without replacing it.
The package has no dependency on a separate research checkout.

Use `--component four`, `five`, `basin`, or `access` for a theorem-local replay.
The default checks all four components.

`sources.json` fixes all article and certificate inputs by SHA-256.
