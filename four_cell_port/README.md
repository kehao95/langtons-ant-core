# Four-Cell Ports and Composable Highway Scattering for Langton’s Ant

Sharp four-cell ports and exterior completion, arbitrary finite guarded scattering trains, and composable unbounded return packets with genuine old-wake consumption.

## Article

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Reproduction details](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23675974)

## Exact scope

The four-cell minimum concerns the fixed inward boundary pose. Both train theorems cover specified, arbitrarily long finite descriptions with preinstalled markers and full history. Their output times are certificate boundaries, whereas the separate twenty-cell paper proves a first-entry time.

## Reproduce

```sh
python3 four_cell_port/reproduce.py --output-report /tmp/four_cell_port-checks.json
make -C four_cell_port/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.
