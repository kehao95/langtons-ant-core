# Complete-history renewal: contour tools and rank obstructions

Exact contour operations, first-contour exit bounds and a distance obstruction
for complete finite-support Langton-ant states.

| Result | Established scope | Missing global step |
|---|---|---|
| [Rooted contour surgery](proof/contour-surgery-pivot.md) | Exact frozen-routing permutation and physical split/merge controls | Detached contours can rejoin; no permanent retirement or transience |
| [Noninterlaced first exit](proof/noninterlaced-contour-exit.md) | Exact first-contour transfer; `T<=L+1` under noninterlacing; sharp physical family | Interlaced contacts and chains of exits; `L=100,T=220` disproves unrestricted `2L` |
| [Immediate-target distance obstruction](proof/immediate-highway-distance-obstruction.md) | A physical three-step PG move raises distance from 1 to `n+10`, although first P104 time stays 12,440 | This particular edit distance is not a descending rank; other full-history ranks remain open |

The contour representation is attributed to earlier Truchet/rotator work in
the imported note. Frozen cycles are not periodic orbits of the flipping ant.
The literal kernel retains every unread black cell. The distance obstruction
concerns edits to an immediate standard future at fixed pose, not basin distance
or deletion of physically irrelevant history.

## Verification

```sh
python3 research/renewal/reproduce.py
```

Python 3.10+ without `-O`, C++17 and Boost multiprecision headers are required.
[Import hashes](evidence/import-2026-10-20.json) preserve all original sources.
[Fresh replay](evidence/replay-2026-10-20.json) checks all three modules in
disposable copies. The C++ checks require Boost multiprecision headers.
