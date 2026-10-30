# Protected Highway Formation and Scattering in Langton's Ant

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23819753)

## Results

- Four is the sharp initial-black threshold for a one-sided highway port; three cells have exact worst first exit 918. Four exterior additions give effective P104 completion.
- For n,m>=10, a four-layer black rectangle frame with white exterior and southwest/north pose shields every interior pattern. The entire trace and exact first P104 entrance depend only on dimensions and their parity.
- All solid rectangles from the southwest/north pose satisfy the sharp bound `tau(n,m)<=242(n+m)+29325`; centered odd squares have a separate complete entrance classification.
- Arbitrary finite guarded scattering trains and unbounded return excursions retain the complete old wake. Nested protected regions justify composition.

## Reproduce

```sh
python3 four_cell_port/reproduce.py
python3 four_cell_port/reproduce.py --frames-only --jobs 3
make -C four_cell_port/paper
```

Python 3.10+, C++17, ISL/GMP and XeLaTeX with DejaVu fonts. Run without Python `-O`.

The full replay checks the original port and scattering modules plus all 42 rectangle parameter certificates and 3538 finite complement inputs. `--jobs 3` sets rectangle concurrency. The rectangle module’s own `--quick` mode covers only four frame schemas and controls.

The scoped second command checks only the corresponding added theorem. Each
entrypoint preserves retained evidence and uses disposable working copies.
`sources.json` binds the article, proof and verifier files.

## Scope

Four cells and four layers minimize different quantities under different contracts. Rectangle theorems require their specified initial pose and white exterior. Scattering composition applies to its verified interfaces; frame shielding alone does not assert such an interface.
