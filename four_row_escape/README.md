# Exact Escape Times of Langton's Ant in Four Rows

For every coloring and internal starting pose of a four-row, n-column rectangle,
the maximum first-exit time is `S(4,n)=34n-150` for every `n>=13`. All smaller
values are determined. Exterior colors are arbitrary and unread before exit;
the exit-producing update is counted. This resolves Etse's MFCS 2026 four-row
linear-bound conjecture (published Conjecture 11; arXiv v1 Conjecture 13).

Version **0.1.0**, published 26 October 2026:
[doi:10.5281/zenodo.23665471](https://doi.org/10.5281/zenodo.23665471).

[Manuscript](paper/main.tex) · [Published PDF](release/v0.1.0/paper.pdf) ·
[Proof map](PROOF.md) · [Replay](evidence/replay-2026-10-20.json) ·
[Release and artifacts](release/README.md)

## Proof and scope

A persistent same-side interface retains residual color behavior after every
return. Four side/parity catalogs each contain 269 types and are closed under
all 16 new-column masks. A weighted graph with 21,248 states and 527,764 edges
restores durations and covers every initial internal pose. Integer inequalities
and tight-edge attainment prove the formula for all widths by induction.
The sharp per-column update bound is 34 and the vertical-cut crossing bound is 21.

The analytic reductions and finite certificates are computer-assisted and
unformalized. Separate Python and C++ implementations are internal cross-checks,
not external mathematical review. No arbitrary-height linear bound, unrestricted
plane transience or Highway Conjecture conclusion follows.

## Reproduce

```sh
python3 four_row_escape/reproduce.py
make -C four_row_escape/paper
python3 tools/prepare_preprints.py --project four_row_escape
```

Use Python 3.10+ without `-O`, a C++17 compiler and pdfLaTeX for the manuscript.
The checker reconstructs the complete certificate in a disposable directory
and compares the frozen report. There is no research-checkout dependency.
Imported source READMEs retain their historical paths; the commands above are
the portable core entrypoints. `[1,...,12]` maxima are
`[2,18,28,46,64,86,104,146,156,206,224,266]`.

## Open

Independent mathematical review and journal preparation remain open.
