# Contribution, literature and claim audit — 15 October 2026

The revised paper is **Uniqueness of the Classical Langton Ant Highway Under Its
Standard Wake**, prepared as version 0.2.0 of the existing wake preprint
(concept [23402421](https://doi.org/10.5281/zenodo.23402421)). The renamed paper
retains the general results from [Reading the Wake, version 0.1.0](https://doi.org/10.5281/zenodo.23402422)
and resolves its standard-wake inverse problem.

## Primary-source comparison

| Primary source | Established content | Role in this manuscript |
|---|---|---|
| Gajardo, [A symbolic projection of Langton's ant](https://doi.org/10.46298/dmtcs.2312) | Symbolic dynamics of the ant and an algebraic characterization of forbidden factors | Background for using forbidden factors. Our finite context graph and integer period certificate are specified and regenerated explicitly. |
| Jillhewar, [Finite-Support Periodic Highways](https://doi.org/10.21203/rs.3.rs-10516269/v1), [pinned manuscript](https://raw.githubusercontent.com/Atharva12456/langtons-ant-highway/76a7e234e577d992d086c204c3dea00ae72cf10a/paper/main.tex) | Exact finite-word realization and finite seed; checker-axis invariant and diagonal extremal rigidity; special-width structural exclusions | The supplied-word criterion and extremal argument are attributed and recalled with proofs. The new main result classifies every period for the twelve prescribed full classes and drift `(2,-2)`. |
| Same author's [width-four note](https://raw.githubusercontent.com/Atharva12456/langtons-ant-highway/76a7e234e577d992d086c204c3dea00ae72cf10a/research-notes/width4_research_2026-07-21.md) | A special geometric period bound and bounded-period search | Prior example of deriving a finite search domain; Appendix A retains the general wake-dependent cutoffs. |
| Ke, [An Ant on the Clock, 0.4.0](https://doi.org/10.5281/zenodo.23402379) | Integer clock, quantitative escape and complete-state orbit algorithms | Own companion paper owns the shared integer clock. Appendix A gives its diagonal period application and the reciprocal-moment synthesis argument. |
| Ke, [Reading the Wake, 0.1.0](https://doi.org/10.5281/zenodo.23402422) | General non-axis wake-dependent cutoffs, terminating inverse synthesis and wake-preserving detour obstruction | Previous version of this same preprint. All general proofs are retained in Appendix A; the previous unresolved standard example now has a complete classification. |

The pinned Jillhewar source was read again on 15 October 2026, including its
criterion, checker-axis formulation and stated transverse restrictions. The
Gajardo publisher page was checked directly for its symbolic and forbidden-word
claims. Citation metadata uses the DMCS'03 volume designation; the publisher's
migration metadata also displays an earlier calendar publication date.

The theorem's complete wake includes the longitudinal residue modulo the full
drift. This is the input used in both the normalized event representation and
the exact search. General growth or width totals alone are different inputs.

## Article structure

1. Introduce the inverse question and state standard-wake uniqueness.
2. Define complete classes and derive the canonical phase from extremal visits.
3. Bound every period by a finite integer context-graph certificate.
4. Give the exact ordered-event representation and prove the pruning rules.
5. Report completed classification and independent all-future seed verification.
6. Retain general budgets and inverse synthesis in Appendix A, followed by the
   literal word, seed and certificate reconstruction.

## Claim–evidence map

| Claim | Evidence | Status |
|---|---|---|
| Exact standard wake and drift force the standard 104-step trace | Canonical-phase proof; integer `P<=168` certificate; complete ordered-event enumeration; full finite-seed verification | Supported by analytic coverage arguments and exact finite computation |
| Every candidate has `P<=168` | Every actual periodic trace lifts to a closed walk; every edge satisfies the integer potential inequality; wake excess sums to -168 | Supported |
| Event enumeration covers all normalized realizations | Forced stable matching, voltage-one cycle and stable rank-time criterion | Supported |
| Degree peeling retains every candidate closed walk | First-deletion proof; independently checked deletion order and retained edge inequalities | Supported |
| Consecutive visits on a fixed open chain have consecutive class ranks | Contiguous physical-motion argument; separate geometric test harness | Supported |
| Ordered events in distinct fixed chains require disjoint ordered chain intervals | Period-copy interval proof; strengthened integer difference constraints; independent positive embeddings and crossing controls | Supported |
| General prescribed-wake inverse synthesis terminates for non-axis drift | Integer/crossing bounds in the diagonal case and reciprocal-moment bound in general; supplied-word realization criterion | Supported; retained from version 0.1.0 |
| Closed-pose insertion strictly increases the appropriate wake budgets | Positive local clock increments summed over the inserted steps | Supported; retained from version 0.1.0 |

Exact replay statistics and any further pruning refinements are maintained in
[the evidence directory](../evidence/standard_wake/) and the manuscript's
completed-classification subsection. A search prefix is an internal partial
event assignment; its count is not a count of distinct complete words.

## Editorial self-review

- **Contribution:** the main theorem closes the concrete inverse problem left
  open in version 0.1.0; the old general contributions remain available with proofs.
- **Clarity:** the paper states the full drift and all twelve class labels before
  the theorem. Checker sector and initial pose are derived, and notation is
  consistent between the upper certificate and exact search.
- **Computational strength:** proof acceptance requires completed enumeration and
  exact edge inequalities. The accepted seed is checked for all future time.
- **Evaluation completeness:** baseline and pruned outputs are compared; positive
  witnesses, rotations, altered seeds, far blockers and interrupted runs test
  their respective interfaces. Degree peeling and chain separation each have
  an explicit soundness proof.
- **Method soundness:** the finite graph is justified by one-way trace coverage;
  the ordered-event representation has both directions. The paper states these
  distinct roles before using them to prove uniqueness.
