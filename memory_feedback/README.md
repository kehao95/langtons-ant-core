# Memory and Spatial Constraints on Eventual Translation in Langton's Ant

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23844677)

## Results

- Exact next-event prediction for fixed finite memory, with complete finite XOR-field continuation and quadratic finite-event time budgets.
- Total remote and birth-filtered feedback queries, and simultaneous remote, late-born, long-lived readback requirements for non-eventually-translating orbits.
- A twenty-cell family with exactly 31 intervening S_128 events and arbitrarily long feedback lifetimes, exhibiting the role of spatial scale.
- Incoming-request reconstruction, the capacity `q^(j+1)-(q-1)^(j+1)`, finite profile deadlines and speed/spread exponent `4v/(1-2v)` for nontranslating orbits with positive horizontal asymptotic speed v along a time sequence. Every non-eventually-translating orbit satisfies `liminf w(T)/log(log(T))>=1/log(2)` for whole-prefix width along non-axis normals normalized by `min(|alpha|,|beta|)=1`.

## Reproduce

```sh
python3 memory_feedback/reproduce.py
python3 memory_feedback/reproduce.py --crossing-only
make -C memory_feedback/paper
```

Python 3.10+, C++17 and XeLaTeX with DejaVu fonts. Run without Python `-O`.

The full replay covers memory prediction, symbolic continuation, geometry, remote feedback, the twenty-cell construction, birth filtering, crossing information and request reconstruction. `--extensions-only` runs birth-filtered feedback and both crossing modules.

The scoped second command checks only the corresponding added theorem. Each
entrypoint preserves retained evidence and uses disposable working copies.
`sources.json` binds the article, proof and verifier files.

## Scope

Translation certificates allow any nonzero drift, not only P104. S_D, J10 and crossing records are distinct objects. The geometric width bound uses the full head prefix and its stated non-axis normalization. Fixed-D complexity is not a uniform polynomial claim in binary D.
