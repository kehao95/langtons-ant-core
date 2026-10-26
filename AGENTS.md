# Publication repository

This repository contains complete articles, mathematical proofs, reproducible
certificates and interactive explanations for the classical Langton ant.

- Keep each article, proof and verifier together in its existing project directory.
- Present complete definitions, hypotheses, proofs and accurate primary citations.
  Lead with positive results; collect broader limitations in a dedicated section.
- Keep theorem scope and the computational trust boundary explicit. A finite
  experiment establishes a universal claim only with its coverage argument.
- Keep article text free of editorial history and publication-process notes.
- Present current articles and results in repository navigation. Zenodo and Git
  own version history; do not maintain previous-version lists or release-history
  indexes here. Retain precise version identifiers where needed for citation
  and reproducibility.
- Preserve third-party attribution and licenses.
- `publications.json` identifies the current articles and their published DOIs.
  Each project's `sources.json` is the explicit source-package file list.
- Run the affected reproduction entrypoints and `python3 tools/check_publication.py`.
  Site changes also require the checks in `docs/README.md`.
