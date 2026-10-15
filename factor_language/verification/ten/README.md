# Ten-factor attraction: source integration

This is the verified source core of the previously supplied ten-factor package. Read [the original complete proof](PROOF.md). Its bytes are unchanged (SHA256 fac0f5761bd10cd91ec2b8b878b7c52465096360434b547558dc8ac879f73e27). The original literature review is preserved as a dated record, not a claim of a fresh exhaustive priority search.

The theorem assumes ALL future length-ten turn factors are among the standard P104 factors. It proves the three eventual physical modes; finite initial black support excludes the two infinite-background modes. Conditional standard entrance is at most 12m+212, with optimal slope 12, not a universal HC entrance bound. The all-input J10 algorithm decides whether another violation exists; it does not prove the event chain terminates.

## Reproduce

From this directory:

```sh
python restore_certificates.py
python reproduce.py
```

The first command reconstructs the large windows10.txt and quotient.tsv, checks their frozen ORIGINAL SHA256 values and refuses to replace a different existing file. Regeneration is not proof. The second command makes a disposable copy, independently re-enumerates all 6,605 words in Python and C++17, verifies every quotient edge, performs damaged-certificate controls, and checks the complete-field local-target algorithm. Python's standard library and a C++17 compiler are sufficient. Do not use Python -O.

The two small JSON certificates are retained byte-for-byte. The large finite certificates are retained by exact reproducible recipes and immutable original hashes, not replaced by sampled simulations. All original Python proof/checking sources are unchanged; independent.cpp differs only in whitespace normalization, and that exact normalized file was freshly compiled and replayed. reports/import-summary.json records the actual successful import-layout replay and the uploaded Git blob identities.

The older 21-letter waiting and 21/14/13 immediate-rigidity packages remain separately supplied artifacts; their theorems are registered in the research import note. This directory does not pretend to contain all their original files. The derived PDF and LaTeX manuscript have not been uploaded by this source-core import. No Zenodo action or external publication is performed here.
