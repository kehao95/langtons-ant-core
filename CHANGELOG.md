# Repository changes

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
