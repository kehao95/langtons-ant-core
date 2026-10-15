# Four-cell outgoing highways

Four black cells give a sharp one-sided interface for the classical ant:

- Every colouring with at most three black cells in `x >= 0`, started at the
  origin facing east, exits that half-plane within **918** updates, sharply.
- The seed `{(0,-1), (1,1), (1,3), (2,2)}` stays in the half-plane forever and
  follows the standard period-104 highway from update **182**.
- Any finite initial state can be extended by exactly four remote black cells,
  preserving any prescribed finite position/heading/read-colour prefix and
  forcing a standard highway. For a protected square of side `n`, entry occurs
  by **8 n 3ⁿ + 183** updates.

The matching four-cell minimum concerns one-sided ports from the fixed boundary
pose. The completion theorem applies to the augmented initial colouring.

Read the [proof](PROOF.md), [manuscript source](paper/main.tex),
[review PDF](paper/paper.pdf), [verification audit](evidence/README.md),
[literature assessment](paper/LITERATURE.md), or [release state](release/README.md).
The proof combines analytic coverage and coupling with exact finite certificates
and algebraic infinite-tail verification. This project has no Lean proof.

## Reproduce

```sh
python3 four_cell_port/reproduce.py
make -C four_cell_port/paper
```

Run from the repository root with Python 3.10+ (standard library, without `-O`).
The runner works in a temporary directory, compares regenerated certificates
byte for byte, and checks the retained independent audit. The PDF build uses
pdfLaTeX and writes to `paper/build/`.

`paper/` owns the draft and bibliography; `verification/` owns three checker
implementations and the constructive completion algorithm; `evidence/` owns
certificates and audit results; `release/` records provenance and draft hashes.
The original research package and corrected manuscript are also retained in
the source research repository, with provenance recorded in the release manifest.

## Open

External mathematical review of the first-contact and infinite-tail reductions,
followed by a final literature/priority check and a deliberate preprint release.
The current PDF is the locally prepared review version; no Zenodo record has
been created for this project.
