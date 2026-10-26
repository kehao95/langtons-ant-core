# Supplementary complete-history tools

These modules provide exact dynamics and proof interfaces related to the
publication projects. Their inputs retain the complete finite black field.

| Material | Contents |
|---|---|
| [Proof](PROOF.md) | Clean-envelope entry, first interaction and complete-history renewal |
| [Renewal kernel](renewal.py) | Explicit renewal steps and terminal certificates |
| [Executable checks](check.py) | Clean-envelope, interaction-index and renewal controls |
| [Contour and distance results](renewal/) | Rooted contour surgery, noninterlaced first exit and an immediate-target distance obstruction |

The clean-envelope and renewal modules use the exact dynamics in
[`one_black/langtons_ant/`](../one_black/langtons_ant/). The contour modules
have separate proof notes and self-contained checks.

```sh
python3 research/check.py
python3 research/renewal/reproduce.py
```

The first command uses Python 3.10+. The second also requires C++17 and Boost
multiprecision headers. Each module documents its hypotheses and the exact
scope of its certificates.
