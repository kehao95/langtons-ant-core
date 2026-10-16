# Release history

## Version 0.3.0 — review package

[Review PDF](v0.3.0/paper.pdf) · [Source snapshot](v0.3.0/prepared-source-manifest.json) · [Standalone check](v0.3.0/standalone-check.json)

*Uniqueness of the Classical Langton Ant Highway from Its Layer Profile*. The PDF and standalone source archive are prepared locally; no Zenodo mutation is part of this revision. The intended action is a new version of record 23405441 in concept 23402421. [Candidate hashes](candidate-manifest.json) identify the exact review snapshot.


## Version 0.2.0 — published

Hao Ke, *Uniqueness of the Classical Langton Ant Highway Under Its Standard Wake*.
The revision adds all-period standard-wake uniqueness, reduced exact
certificates, and complete reproducible enumeration. The general wake-period
bounds and inverse-synthesis theorem from 0.1.0 are retained.

Version **0.2.0**, published 15 October 2026:
[doi:10.5281/zenodo.23405441](https://doi.org/10.5281/zenodo.23405441).
It updates record **23402422** within the existing concept
[10.5281/zenodo.23402421](https://doi.org/10.5281/zenodo.23402421).

- [Exact published PDF](v0.2.0/paper.pdf).
- [Publication receipt](v0.2.0/publication-receipt.json) and
  [public API record](v0.2.0/public-record.json).
- [Reviewed source manifest](v0.2.0/prepared-source-manifest.json),
  [delivery hashes](v0.2.0/delivery-manifest.json), and
  [metadata](v0.2.0/metadata.json): preserved preparation snapshots.
- [Full replay](v0.2.0/review-checks.json) and
  [standalone archive check](v0.2.0/standalone-reproduction.json): the complete
  uniqueness search, exact upper certificate, and matching 14-page PDF.

All three published attachments—the PDF, standalone source ZIP and
[SHA256 manifest](v0.2.0/release-manifest.json)—were downloaded anonymously and
matched the local delivery hashes. The previous record is unchanged, and the
concept's latest version resolves to 0.2.0.

Build and package locally with:

```sh
make -C wake_synthesis/paper
python3 tools/prepare_preprints.py --project wake_synthesis
```

## Version 0.1.0 — published

Hao Ke, *Reading the Wake: Period Bounds and Inverse Synthesis for Langton’s Ant*.

Version **0.1.0**, published 15 October 2026:
[doi:10.5281/zenodo.23402422](https://doi.org/10.5281/zenodo.23402422).
Concept DOI: [10.5281/zenodo.23402421](https://doi.org/10.5281/zenodo.23402421).
The manuscript cites the exact companion clock version 0.4.0, record 23402379.

- [Exact published PDF](v0.1.0/paper.pdf).
- [Publication receipt](v0.1.0/publication-receipt.json): all public attachments downloaded and SHA256-verified.
- [Source manifest](v0.1.0/published-source-manifest.json) and [delivery manifest](v0.1.0/release-manifest.json): exact sources, working-tree provenance and attachment hashes.
- [Standalone archive checks](v0.1.0/standalone-reproduction.json): extracted sources build to matching PDF text; prior mathematical checks apply to unchanged proof/verifier sources.
- [Metadata](v0.1.0/zenodo-metadata.json) and [public API record](v0.1.0/public-record.json).

Published files and receipts are immutable. Versioned release records identify the actual published contents.
The candidate and preparation manifests retain the reviewed prepublication
snapshot. Publication receipts identify the published records.

The mathematical source originates in research commit `9c50691`, with
publication allocation reviewed at `c56a76b`. Retained research reports are
byte-identical; the new coefficient and complete-seed audits accompany them.

## Review revision — 16 October 2026

The candidate version number is retained until publication. The current PDF,
metadata and exact source hashes include the new results from research
`2f6010a`. The previous 15 October review files are retained under the version's
`revisions/2026-10-15/` directory. No Zenodo draft or publication was changed.

The current standalone report separates a fresh new-module replay and PDF
rebuild from hash-matched inheritance of the previous full classification.
The complete default replay remains available; the independent profile replay
has its own command in `PROFILE_REPLAY.md`.
