# Pinned upstream material and attribution

Author: **Atharva Jillhewar**.

Source: *Finite-Support Periodic Highways of Langton's Ant: Necessary Conditions,
Transverse Exclusions, and Exact Search* (2026).

Repository: https://github.com/Atharva12456/langtons-ant-highway

Commit: `76a7e234e577d992d086c204c3dea00ae72cf10a`.

The paper source inspected was `paper/main.tex`, Git blob
`12cd05962e071c08f3e900c624cd6438452fa847`, especially the signed mod-four residue
theorem, axis lifted-rank proof and even-diagonal two-lane proof. The paper/prose
is CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . The integrated proof
rewrites the relevant arguments and identifies the modifications. Authorship of
those prior arguments is not transferred to this project.

The two Python scripts and LICENSE here are copied unchanged from upstream:

| File | Original location | Git blob |
|---|---|---|
| axis_rank_parity_audit.py | code/python/axis_rank_parity_audit.py | 82b2d53a995f0c42145c7e3b34225e623dfbb2b7 |
| even_diagonal_rank_parity_audit.py | code/python/even_diagonal_rank_parity_audit.py | 26dad5e68b096dc7cadc4875007201ce62ae60c8 |
| LICENSE | LICENSE | 6261fc7e6e5416be28d6efaa046291cf92a646c0 |

They are MIT-licensed and the original copyright and license are retained. Their
output deliberately calls itself bounded evidence. Rerunning it is not a proof
of the unbounded lemmas. Those lemmas have complete written arguments in the
integrated proof; `code/audit.py` supplies additional independent checks.

The separate source note `research-notes/growth8_checker_pure_exclusion_2026-08-20.md`
(Git blob `c5ad7e4e3cfbdd342b5b5f50282c25543213455d`) explicitly applies the
cardinality-independent two-lane lemma at growth eight. The present note extends
that application to all growth values and does not claim its key lemma as new.
