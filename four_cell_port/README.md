# Four-Cell Ports and Composable Highway Scattering for Langton’s Ant

Sharp four-cell ports and exterior completion, arbitrary finite guarded scattering trains, and composable unbounded return packets with genuine old-wake consumption.

## Manuscript and status

Version **0.2.0** is [published on Zenodo](https://doi.org/10.5281/zenodo.23665526). [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [Fresh verification](evidence/review-2026-10-15.json) ·
[Release and artifacts](release/README.md).

Record [23665526](https://doi.org/10.5281/zenodo.23665526) updates
[23402414](https://doi.org/10.5281/zenodo.23402414) in the existing concept
**23402413**. Earlier published files are preserved.

## Exact scope

The four-cell minimum concerns the fixed inward boundary pose. Both train theorems cover specified, arbitrarily long finite descriptions with preinstalled markers and full history. Their output times are certificate boundaries, whereas the separate twenty-cell paper proves a first-entry time.

## Reproduce

```sh
python3 four_cell_port/reproduce.py --output-report /tmp/four_cell_port-review.json
make -C four_cell_port/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.

## Open

Independent mathematical peer review and journal preparation remain open.
