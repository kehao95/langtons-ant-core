# Literature and venue audit — 2026-10-13

## Primary sources read

- Kossi Roland Etse, *How Long Can The Escaping Ant Be Confined?*,
  MFCS 2026, LIPIcs 386, 49:1–49:17.
  [Official record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2026.49)
  and [formal-version PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol386-mfcs2026/LIPIcs.MFCS.2026.49/LIPIcs.MFCS.2026.49.pdf).
  Page 49:9, Theorem 5: square bound `(n+1)!`. Page 49:4 describes the
  white-right/black-left rule and step convention. Section 4.4 separately gives
  fixed-height rectangle bounds. Our claim is an asymptotic improvement of
  the square estimate, not all rectangular estimates or the polynomial-bound
  open problem. His arc representation fixes one parity sector; our proof
  treats both sectors and all internal headings.
- Gajardo, Moreira and Goles, *Complexity of Langton's Ant* (2002),
  [author preprint](https://arxiv.org/abs/nlin/0306022v2),
  DOI 10.1016/S0166-218X(00)00334-6. Complete-state equality targets must be
  separated from local reachability and infinite-background constructions.
- Gajardo, Lutfalla and Rao, *Ants on the Highway*,
  [author preprint](https://arxiv.org/abs/2409.10124v1), published in Natural
  Computing 24, 497–509 (2025), DOI 10.1007/s11047-025-10018-9.
  Context for highways; no dependency of the clock argument.

## Search scope and limitation

Queries covered the exact Etse title, Langton escape/confinement upper bounds,
exponential bounds, rational clocks, and complete-state reachability. Inspected
Etse's reference list and conclusion, including the cubic-growth simulation
observation and open polynomial square bound. No competing exponential square
bound was identified in the inspected primary sources. This finite search does
not establish worldwide priority; no “first” or “best-known” language is used.

## Candidate venue

[Natural Computing aims and scope](https://link.springer.com/journal/11047/aims-and-scope)
includes theoretical natural computing, and the journal published the highway
paper above. This supports topic fit only. Submission is not performed and no
fee, timing, acceptance probability or venue-specific compliance claim is made.

## Critical revision — 15 October 2026

The [official proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol386-mfcs2026/LIPIcs.MFCS.2026.49/LIPIcs.MFCS.2026.49.pdf)
was checked again, including Theorem 12 on page 49:15. For width N at least
height H, it gives polynomial degrees H−1 for even H and H−2 for odd H.
The [extended preprint, Theorem 14](https://arxiv.org/html/2606.26677v1#S4.SS4)
contains the same parity-dependent estimate. The new degree floor(H/2)+1 is
strictly smaller for H>=6; the known linear H=2,3 estimates remain stronger.

The current square result removes the extra factor n from our prior
exponential estimate. This is a revision of the clock paper, retaining its
complete-state algorithms. No new priority claim is based solely on this
comparison, and the polynomial square-escape question remains open.

## Integer-clock revision — 15 October 2026

The integer-clock proof strengthens the same square theorem to
`(13*3^(n-1)-2*n^2-4*n-5)/2`. It improves our 0.3.0 constant without changing
the exponential order. Complete-state algorithms now use the integer clock
with unit increment; the anisotropic rectangular argument is retained.
The separate wake manuscript cites this project for the shared clock identity
and develops a different inverse-synthesis question. No separate novelty claim
is made for reusing the clock in the companion paper.
