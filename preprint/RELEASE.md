# Draft revision 0.2.0-review

Zenodo new-version draft **23341609**,
[owner preview](https://zenodo.org/records/23341609?preview=1), based on the
published [record 22086968](https://doi.org/10.5281/zenodo.22086968).
Title: *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway:
A Lean-Checked Proof*. Author: Hao Ke, Independent, ORCID 0009-0001-2818-4986.

This is an unsubmitted new version. The original published version remains
intact. The revised source is committed locally and retained in the draft
artifact; no public GitHub branch update is required to prepare this draft.

Files prepared:

- `One-Black-Standard-Trace-v0.2.0-review.pdf`
- `one-black-0.2.0-review-source.zip`
- `one-black-0.2.0-review-manifest.json`
- `one-black-0.2.0-review-figures-*.zip` (original figure assets)

The source archive records all source SHA256 hashes and includes the exact
Lean proof, native leaf data, clean-build logs, final axiom lists, manuscript,
bibliography, and figure assets. The outer manifest binds the PDF and ZIP.
The later `upload-receipt.json` records the observed remote draft state and
successful download-back identity checks. No release or journal submission
is asserted. Author approval and external mathematical review remain open.


The delivery PDF optimizes embedded images above 350 dpi to 300 dpi at quality
95 using `optimize_pdf.py` and PyMuPDF 1.28.2. Text extraction and page count
are compared exactly before/after. The full-resolution master PDF remains in
this repository and every original figure byte is retained in the source
assets. To rebuild, extract the source ZIP and all figure ZIPs into the same
directory, run `make -C preprint`, then the optimizer if the delivery version
is desired. Large legacy-key uploads timed out/returned HTTP 502; they were
inspected and not retried. Final receipt, not an attempted upload, establishes
the files actually present in the draft.
