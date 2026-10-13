# Editorial revision — 2026-10-13

The reviewed Gemini suggestions are applied to the six-page manuscript.

## Reading order and changes

1. Abstract and introduction: lead with the square first-exit bound and outline
   how positive clock increments turn finite range into bounded residence time.
2. Clock: explain diagonal coordinates, parity and the compensating pose term
   before the formulas; distinguish the fixed r=4 clock from the tunable family.
3. Square escape: retain the proof and move the numerical bound comparison
   from the verification section to the square result it illustrates.
4. Orbit algorithms: introduce orbit labels before their infinitude proof.
5. Verification, conclusion and availability: retain evidence counts and the
   formalization scope, add a mathematical conclusion, and group source commands.

## Claim–evidence check

| Claim in revised prose | Existing evidence | Result |
|---|---|---|
| First exit <= 8*n*3^n+1, n cells per side | Square theorem and specialization | Same statement and proof |
| Fixed clock increment >=2/5 | Increment identity at r=4 | Same statement and proof |
| Field/pose compensation | Exact four-case increment table, including -e*e' sign | Preserved |
| Complete-state orbit algorithms | Reachability and section proofs | Preserved |
| Partial Lean coverage | Local algebra and telescoping source/evidence | Described precisely |

## Validation and self-review

Theorem, lemma, corollary, proof and displayed-equation blocks were compared
with the preceding Git revision. They are unchanged. Verification-code hashes
match the retained mathematical audit; no fresh proof build or exhaustive
simulation is claimed for this prose-only revision. Both PDF builds and final
layout/text checks are the editorial validation.

- Contribution: the explicit square bound is visible before technical algebra.
- Clarity: each new transition names the next object and explains its role.
- Evidence: universal statements remain tied to proofs; finite checks retain
  their original scope and counts.
- Coverage: all original hypotheses, endpoint conventions and proof cases remain.
- Method soundness: the parameter family is not assigned the r=4-only constant,
  and the field increment keeps its turn-dependent sign.

The publication artifact contains exact hashes of the revised manuscript;
`evidence/reproduction.json` remains the historical mathematical-audit record.
