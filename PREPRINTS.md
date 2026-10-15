# Preprints and prepared updates

The owner approved Zenodo publication on 15 October 2026 after review of the
prepared manuscripts and the Gemini editorial discussion. Three releases are
now public; the existing one-black publication is unchanged.

| Project | Current publication | Exact delivery PDF |
|---|---|---|
| One-black highways | [0.2.0 · 23341609](https://doi.org/10.5281/zenodo.23341609) — retained | [PDF](one_black/paper/paper.pdf) |
| An Ant on the Clock | [0.4.0 · 23402379](https://doi.org/10.5281/zenodo.23402379) — existing concept 23341603 | [PDF](clock_escape/release/v0.4.0/paper.pdf) |
| Four Black Cells Force an Outgoing Highway | [0.1.0 · 23402414](https://doi.org/10.5281/zenodo.23402414) — first release | [PDF](four_cell_port/release/v0.1.0/paper.pdf) |
| Reading the Wake | [0.1.0 · 23402422](https://doi.org/10.5281/zenodo.23402422) — first release | [PDF](wake_synthesis/release/v0.1.0/paper.pdf) |

The clock owns the integer clock, the square bound
`E(n)=(13*3^(n-1)-2*n^2-4*n-5)/2`, rectangular escape and complete-state
algorithms. The wake paper owns period budgets and period-unknown inverse
synthesis. The four-cell completion time is `E(n)+182`. Both new preprints
cite the exact clock 0.4.0 DOI.

## Wake 0.2.0 update in preparation

The revised title is *Uniqueness of the Classical Langton Ant Highway Under Its
Standard Wake*. Its main theorem closes the standard-wake classification left
open in 0.1.0; the general period bounds and inverse-synthesis theorem remain.
The update belongs to existing concept **23402421**, whose current published
record is **23402422**. [Current manuscript and proof](wake_synthesis/) ·
[Local update package](wake_synthesis/release/README.md).

## Published artifacts and verification

Each new record has a PDF, a self-contained source ZIP and a SHA256 manifest.
All nine attachments were downloaded anonymously through the public API and
matched byte-for-byte by SHA256 against the local delivery files. Source ZIPs
were independently extracted and rebuilt before publication; their PDF text
matches the delivery PDFs (8, 6 and 6 pages).

Each project's versioned `release/` directory owns the publication receipt,
public record, metadata, exact PDF, source manifest, delivery manifest and
standalone archive checks. Source snapshots identify working-tree content by
per-file hashes and record their base commit; they do not claim an unmade commit.
The previously reproduced mathematical sources are unchanged by the final
editorial and citation edits; retained mathematical checks are identified separately.

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

External mathematical peer review and journal preparation. The owner also
authorized README cleanup and Git submission of this publication batch.
No journal submission has been made.
