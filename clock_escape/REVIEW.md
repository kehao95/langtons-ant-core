# Internal reviewer worksheet

## Narrative outline

1. First-exit theorem and explicit input/target conventions.
2. Rational clock and complete local increment proof.
3. Finite square range, endpoint count, exponential specialization.
4. Complete-state algorithms and infinite orbit section.
5. Verification evidence, mathematical conclusion and source availability.

Each mathematical subsection opens with its object or result; proofs then
explain the needed identity, deduction and exact scope. Algorithmic corollaries
follow the main escape result rather than displacing it.

## Claim–evidence map

| Claim | Evidence | Status |
|---|---|---|
| Increment >=2/5 | Local table + positivity; Lean scaled algebra | Analytically supported, local formal verification |
| Exit <=8*n*3^n+1 for every n>=1 | Square range, T-1 count, binomial estimate | Analytically supported; not fully formalized |
| Complete-state reachability and orbit normal form | Uniform clock, explicit inverse, two-sided divergence | Analytically supported |
| Infinitely many representatives | Row-parity invariant, one distinct vector per row | Analytically supported |
| Square asymptotic improvement over Etse Theorem 5 | Formal source and exponential vs factorial growth | Supported, no global priority claim |
| Finite maxima 1,6,17,46 | Complete independent finite graphs and witness replay | Computer-checked |
| Proof has received independent expert review | No such review obtained | Not claimed |

## Five review dimensions

- **Contribution:** explicit quantitative first-exit bound with a single mechanism
  yielding complete-state algorithms. Related-work comparison is narrow and
  sourced. The algorithmic conclusions specify complete finite-support state targets.
- **Clarity:** exact read convention, n cells rather than n+1 vertices, final
  move counted, all signs/colours/centres, negative powers and infinite exterior
  handled. Added three omitted expansions and an explicit infinitude proof.
- **Evidence strength:** analytic proof carries universal claims; tests and
  partial Lean proofs have named boundaries. No numerical-to-universal leap.
- **Coverage:** cases include r near 3, n=1, arbitrary headings, remote support,
  and huge integer positions. Coarse comparisons do not claim tight constants.
- **Method soundness:** full-state targets are not local observation targets;
  arbitrary history is retained. No hidden eventual-periodicity assumption.

## Open for journal preparation

The Zenodo preprint is published. Continue mathematical peer review, broader
citation chaining, and venue-specific manuscript and declaration preparation.
