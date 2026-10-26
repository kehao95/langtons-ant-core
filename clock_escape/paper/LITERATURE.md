# Literature and contributions

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

## Fixed-height comparison

The [official proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol386-mfcs2026/LIPIcs.MFCS.2026.49/LIPIcs.MFCS.2026.49.pdf)
gives Theorem 12 on page 49:15. For width N at least
height H, it gives polynomial degrees H−1 for even H and H−2 for odd H.
The [extended preprint, Theorem 14](https://arxiv.org/html/2606.26677v1#S4.SS4)
contains the same parity-dependent estimate. The new degree floor(H/2)+1 is
strictly smaller for H>=6; the known linear H=2,3 estimates remain stronger.

## Integer clock and complete states

The integer clock gives the square bound
`(13*3^(n-1)-2*n^2-4*n-5)/2` and complete-state orbit algorithms.
The anisotropic potential gives the fixed-height rectangular bound. The wake
paper applies the clock to a distinct prescribed-wake inverse problem.
