# Research program

The repository keeps a small theorem ladder instead of a growing collection of
overlapping “renewal” scripts. A proposed result belongs to exactly one rung
and must name the previous rung it consumes.

| Rung | Research question | Required completion artefact |
| --- | --- | --- |
| P104 | What finite local condition perpetuates the highway? | phase data, local proof, checker |
| One defect | How is one black square absorbed from every relative offset? | entry-obstacle theorem plus finite-prefix closure |
| Many defects | Which interaction histories can finite support create? | complete state grammar and preservation proof |
| Descent | Why can no nonterminal history persist forever? | well-founded measure or complete obstruction cover |
| HC | How do the preceding facts quantify over all finite support? | assembled theorem with explicit induction or compactness argument |

## Current active questions

1. **Entry obstacle.** Classify the P104-entry state with one additional black
   square by a finite local description plus a small number of infinite rays.
   The target is a theorem, not an unbounded simulation.
2. **Prefix closure.** For the 1,376 positions reached before blank entry,
   construct proof-producing finite traces or a common invariant; do not store
   opaque pass/fail outcomes.
3. **History language.** Propose only a grammar whose objects can be shown both
   to preserve the literal dynamics and to represent every relevant encounter.
4. **Descent candidate.** Every proposed rank must identify its domain,
   transition relation, strict decrease statement, and base case before search
   begins.

## Promotion rule

Exploration may add a dated note, a generator, and raw results. Promotion to
`theory/` requires a closed statement and a dependency link; promotion to
`evidence/` additionally requires deterministic data validation. No separate
archive of speculative certificate formats is maintained.
