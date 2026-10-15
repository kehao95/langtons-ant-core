# Published preprints

Four preprints are published. The latest release is the owner-approved wake
0.2.0 update, which adds standard-wake uniqueness within its existing Zenodo
version chain.

| Project | Current publication | Exact delivery PDF |
|---|---|---|
| One-black highways | [0.2.0 · 23341609](https://doi.org/10.5281/zenodo.23341609) — retained | [PDF](one_black/paper/paper.pdf) |
| An Ant on the Clock | [0.4.0 · 23402379](https://doi.org/10.5281/zenodo.23402379) — existing concept 23341603 | [PDF](clock_escape/release/v0.4.0/paper.pdf) |
| Four Black Cells Force an Outgoing Highway | [0.1.0 · 23402414](https://doi.org/10.5281/zenodo.23402414) — first release | [PDF](four_cell_port/release/v0.1.0/paper.pdf) |
| Uniqueness of the Classical Langton Ant Highway Under Its Standard Wake | [0.2.0 · 23405441](https://doi.org/10.5281/zenodo.23405441) — existing concept 23402421 | [PDF](wake_synthesis/release/v0.2.0/paper.pdf) |

The clock owns the integer clock, the square bound
`E(n)=(13*3^(n-1)-2*n^2-4*n-5)/2`, rectangular escape and complete-state
algorithms. The wake paper owns standard-wake uniqueness, period budgets and
period-unknown inverse synthesis. The four-cell completion time is `E(n)+182`.
The wake and port papers cite the exact clock 0.4.0 DOI.

## Wake version history

Version 0.2.0, *Uniqueness of the Classical Langton Ant Highway Under Its Standard
Wake*, closes the standard-wake classification left open in 0.1.0; the general
period bounds and inverse-synthesis theorem remain. Record **23405441** updates
**23402422** in concept **23402421**. The original 0.1.0 title was *Reading the
Wake: Period Bounds and Inverse Synthesis for Langton's Ant*.
[Current manuscript and proof](wake_synthesis/) ·
[Release records](wake_synthesis/release/README.md).

## Published artifacts and verification

Each release provides a PDF and a self-contained source archive, with delivery
hashes and verification recorded in its versioned release directory. Wake 0.2.0
ships the reviewed 14-page PDF and source ZIP; its standalone replay and PDF text
comparison passed before publication.

The wake 0.2.0 PDF, source ZIP and SHA256 manifest were downloaded anonymously
after publication and matched the local delivery hashes. The previous version
was preserved and the concept's latest version resolves to 0.2.0; see the
[publication receipt](wake_synthesis/release/v0.2.0/publication-receipt.json).

The earlier clock 0.4.0, port 0.1.0 and wake 0.1.0 batch also included SHA256
manifests. All nine attachments in that batch were downloaded anonymously and
matched local SHA256 hashes. Their source ZIPs were independently extracted and
rebuilt, with PDF text matching the delivery PDFs (8, 6 and 6 pages).

Each project's versioned `release/` directory owns the publication receipt,
public record, metadata, exact PDF, source manifest, delivery manifest and
standalone archive checks. Source snapshots identify working-tree content by
per-file hashes and record their base commit; they do not claim an unmade commit.

The existing one-black PDF and clock 0.3.0 PDF were also downloaded and verified
against their earlier publication receipts. No one-black record was created or
modified. Clock 0.4.0 was created with `new-version` from 23401306 and remains
in concept 23341603. Port and wake concepts are 23402413 and 23402421.

[Verification and editorial review](PREPRINT_REVIEW.md) records proof ownership,
checks and the two-round Gemini discussion. `candidate-manifest.json` and
`review-checks.json` retain prepublication snapshots; the versioned release
records are authoritative for published content. The local preparation command
`python3 tools/prepare_preprints.py` performs no network or publication action.

## Open

External mathematical peer review and journal preparation.
No journal submission has been made.
