# Release history and prepared update

## Version 0.2.0 — local preparation

Hao Ke, *Uniqueness of the Classical Langton Ant Highway Under Its Standard Wake*.
The revision adds all-period standard-wake uniqueness, reduced exact
certificates, and complete reproducible enumeration. The general wake-period
bounds and inverse-synthesis theorem from 0.1.0 are retained.

Build and package with:

```sh
make -C wake_synthesis/paper
python3 tools/prepare_preprints.py --project wake_synthesis
```

The [prepared PDF](v0.2.0/paper.pdf) and versioned preparation records
identify the revision being reviewed. The [full replay](v0.2.0/review-checks.json)
and [standalone archive check](v0.2.0/standalone-reproduction.json) record actual
verification. The local [candidate manifest](candidate-manifest.json) identifies source and
PDF hashes; `candidate/` holds the delivery PDF and standalone source ZIP.
The intended Zenodo action is a **new version of record 23402422 in concept
23402421**. No new DOI version has been created or published for this update.

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
The top-level candidate manifest describes the current local update.

The mathematical source originates in research commit `9c50691`, with
publication allocation reviewed at `c56a76b`. Retained research reports are
byte-identical; the new coefficient and complete-seed audits accompany them.
