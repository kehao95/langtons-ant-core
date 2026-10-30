# Wake Parity and Highway Rigidity in Langton's Ant

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23675970)

## Results

- Full drift `(2,-2)`, growth twelve, transverse width ten and at most one odd class per interior layer force the standard P104 turn word and wake.
- For every full non-axis drift and explicit odd-class wake, a computable period bound gives terminating inverse synthesis.
- Non-axis quadratic wake characters and an analytic unit-diagonal exclusion constrain possible periodic traces.
- For full axis displacement `(a,0)`, the strict inversion count of odd classes in `0<=x<a` is even. This gives all-period excluded families and an `O(g log(g+1))` integer-operation sparse test.

## Reproduce

```sh
python3 wake_synthesis/reproduce.py
python3 wake_synthesis/reproduce.py --axis-only
make -C wake_synthesis/paper
```

Python 3.10+, C++17 and pdfLaTeX. Run without Python `-O`.

Default replay includes axis parity, periodic arithmetic and the complete 76-case/83-job thin-wake classification. `--extensions-only` runs the arithmetic modules including axis parity. `--quick` skips the large thin-wake exhaustion while retaining its upper graph and controls. `--jobs 4` sets native concurrency.

The scoped second command checks only the corresponding added theorem. Each
entrypoint preserves retained evidence and uses disposable working copies.
`sources.json` binds the article, proof and verifier files.

## Scope

Parity conditions are necessary screens. The inverse-synthesis termination theorem assumes non-axis drift. The uniqueness theorem retains its drift, growth, width and interior-thinness hypotheses; the standard layer profile follows from them.
