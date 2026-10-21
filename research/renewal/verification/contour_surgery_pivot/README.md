# Rooted contour-surgery research pilot

Run from the repository root:

```sh
python experiments/hc_global/contour_surgery_pivot/check.py
```

Python standard library only. Default execution checks the frozen report without overwriting it. `--write` is an explicit report-regeneration mode, not normal verification.

This explores a different global HC route: exact ordered reconnection of planar routing contours, without a J10-silent premise or an event budget. It does not establish HC, transience, permanent sealing or a new result of publication-level novelty. Truchet contours and split/merge operations are prior methods; see `proof/research-contour-surgery-pivot-2026-10-20.md` for attribution, analytic identities and targets.

The implementation keeps the complete field via a sparse deviation of a frozen-routing permutation. Frozen cycles must not be confused with cycles of the physically flipping ant. The blank orbit already detaches a 16-arc cycle at update 4 and reattaches it at update 8, refuting the naive permanent-retirement inference.
