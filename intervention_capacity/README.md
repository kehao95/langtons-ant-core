# When to Intervene: Predictive Memory in a Langton Highway

Within one exact passive P104 trace class, predicting a single current-cell toggle at an unspecified time requires Θ(T²) source-dependent bits over horizon T. A menu of q possible times requires Θ(qT), uniformly for `1<=q<=T` and large T. Protected lanes give explicit bounds, exact response counts and an error-tolerant lower bound. Arbitrary toggle words have an exact quotient determined by the free colors in the finite controlled read region.

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof map](PROOF.md) · [Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23844704)

## Reproduce

```sh
python3 intervention_capacity/reproduce.py
make -C intervention_capacity/paper
```

Python 3.10+ without `-O`, a C++17 compiler and pdfLaTeX.
Checks run in a disposable copy and compare frozen evidence without replacing it.
The package has no dependency on a separate research checkout.

`sources.json` fixes all article and certificate inputs by SHA-256.
