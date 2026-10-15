# Repository changes

## 2026-10-15 — Standard-wake uniqueness version 0.2.0 published

Following the owner's approval, published *Uniqueness of the Classical Langton
Ant Highway Under Its Standard Wake* as
[Zenodo 23405441](https://doi.org/10.5281/zenodo.23405441), a new version of
23402422 in the existing concept 23402421. The release delivers the reviewed
14-page PDF and standalone source archive. Version 0.1.0 and the preparation
snapshots remain unchanged. [Release records](wake_synthesis/release/README.md)
identify the exact artifacts and version chain.

## 2026-10-15 — Standard-wake uniqueness update prepared

Prepared wake version 0.2.0 under the revised title *Uniqueness of the Classical
Langton Ant Highway Under Its Standard Wake*, updating the existing concept
23402421. The complete standard wake and drift `(2,-2)` now have a unique
periodic realization: the standard P104 word. General period bounds and inverse
synthesis from version 0.1.0 remain with their proofs.

Imported the source-pinned exact enumerator and infinite-trace verifier. Further
pruning removes transient upper-graph vertices and separates disjoint fixed
chains in chronological constraints. The source archive reconstructs both the
integer period certificate and completed classification; previous enumerators
remain available as controls. The manuscript derives its checker sector from
the extremal singleton visits. Published 0.1.0 artifacts remain unchanged.
This entry records preparation, not a new Zenodo publication.

## 2026-10-15 — Integer clock update and two new preprints published

Added a fourth publication project, `wake_synthesis/`, with a standalone inverse
problem paper, exact period bounds, original evidence and new symbolic audits.
The clock review manuscript now uses the integer clock and the stronger square
bound with leading coefficient 13/6. The four-cell completion budget is updated
to E(n)+182. Following the owner's approval, published clock 0.4.0 as
[23402379](https://doi.org/10.5281/zenodo.23402379) in the original concept,
four-cell port 0.1.0 as [23402414](https://doi.org/10.5281/zenodo.23402414), and
wake synthesis 0.1.0 as [23402422](https://doi.org/10.5281/zenodo.23402422).
The two new papers cite the exact clock version. Public attachment downloads
match local SHA256 hashes. The one-black and previous clock PDFs are unchanged.
Two-round Gemini editorial discussion informed the final exposition.
See [the publication portfolio](PREPRINTS.md).

## 2026-10-15 — Clock preprint version 0.3.0 published

Published the critical square and rectangle strengthening as
[Zenodo 23401306](https://doi.org/10.5281/zenodo.23401306), updating the existing
clock preprint under concept DOI 23341603. The PDF, source archive and manifest
passed download/hash verification; full reproduction from the uploaded source
archive passed. Version 0.2.0 and its PDF remain preserved. Release receipts,
source hashes and the version chain are recorded under `clock_escape/release/`.


## 2026-10-15 — Critical clock strengthening

Imported the new critical-potential proof into `clock_escape/`: square first
exit is O(3^n), and fixed-height rectangles have degree floor(H/2)+1.
Added independent exact Laurent-polynomial checks, an isolated reproduction
option, an integrated eight-page review manuscript and current source hashes.
The source repository receives the localized-potential clarification and
independent audit. The original published PDFs, DOI records and Lean proofs
are unchanged; no additional publication project is introduced.


## 2026-10-15 — Sharp four-cell outgoing ports

Added `four_cell_port/` as a third independent project: sharp three-black
half-plane escape by 918, a four-black standard P104 port from update 182,
and effective four-cell exterior completion of arbitrary finite observed histories.
The project includes a six-page review manuscript, exact certificates, three
checker implementations, a completion constructor and a reproducible audit.

Imported original evidence from research commit
`f8f593ae5d87929bbcd7dd2ddbd2593afe60c28a`; source-proof corrections clarify
observed-prefix equality versus complete-field difference, absolute phase
coordinates, and uniform first-contact coverage. The original repository receives
the same corrections and new audit. Provenance is pinned in the project manifest.
Existing published PDFs, Lean sources and Zenodo releases are unchanged.


## Symmetric project layout — 2026-10-13

Both results now own `paper/`, `lean/`, `evidence/`, `release/` and one
`reproduce.py` entrypoint. Research and browser-export tooling have their own
homes. Manuscript text, Lean proof sources, scientific checkers and original
figure bytes are preserved. Checked-in PDFs are the exact Zenodo delivery files;
new builds write to ignored `paper/build/` directories.

| Previous path or command | Current location |
|---|---|
| `preprint/paper.md`, figures and PDF | `one_black/paper/` |
| `preprint/verification/` | `one_black/evidence/` |
| `preprint/verify.py`, `one_black/check.py` | `one_black/reproduce.py` (clean build and axiom audit) |
| `clock_escape/main.tex`, PDF and Makefile | `clock_escape/paper/` |
| Project-root release files | Each project's `release/` |
| `PROOF.md`, `RESEARCH.md` | `research/PROOF.md`, `research/README.md` |
| `media/x/` | `one_black/media/` |
| Root and preprint figure exporters | `docs/scripts/` |

Completed editorial drafts, raw Gemini conversations, obsolete draft receipts
and duplicate JSON/log outputs are removed from the current tree. Their full
history remains in [the previous snapshot](https://github.com/kehao95/langtons-ant-core/tree/09acf26205e9f602957fc83216eef38c12307eaa).
The published source manifests retain original archive paths; they are historical
provenance, not inventories of the reorganized working tree. Commands printed
inside the published manuscripts refer to that original layout.

Independent scientific checkers remain separate: their different implementations
provide evidence rather than duplicate administrative state. The browser site's
`docs/` URL and its runtime assets are unchanged.

Validation after migration: the one-black clean build and both axiom audits
passed; the clock reproduction and research checks passed. Both rebuilt PDFs
have exactly the published text. Original manuscript, Lean and independent
checker bytes, original figure bytes, and published PDF hashes were checked.
Local links, exporter paths, the static-site checks and the research repository's
packaging inputs also pass. No Zenodo artifact was modified.

## Published preprints — 2026-10-13

Version 0.2.0 of the [one-black paper](one_black/release/README.md) updates the
original Zenodo version chain. The [clock paper](clock_escape/release/README.md)
has a separate record. Both projects retain publication receipts and exact
published-source hashes. The original public integration verified all 85
one-black scientific files and the clock's standalone replay, numerical reports,
Lean axioms and rebuilt PDF text; its report is retained in
[`clock_escape/evidence/public-integration.json`](clock_escape/evidence/public-integration.json).
