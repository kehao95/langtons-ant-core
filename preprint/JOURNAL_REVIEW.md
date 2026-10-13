# One-black journal revision audit — 2026-10-13

Version 0.2.0-review. Baseline public source:
`3e9fa6229cc5667e2869887d21e07c6ea55697a5`; existing public preprint:
[Zenodo 22086968](https://doi.org/10.5281/zenodo.22086968), published 2026-08-24.
The previous record identifies Hao Ke, affiliation Independent, ORCID
0009-0001-2818-4986. The revision follows that attribution.

## The substantive repair

At baseline, `PermanentP104` asserted observation recurrence every 104 steps
and one of four diagonal drifts. It did not identify the standard read word.
This is a real distinction between statements; the old definition must not be
silently represented as a fixed-template theorem.

The revision adds `HasStandardWord`: its first 104 read colours equal those of
`run 9977 white`. `Highway.tail_permanent` derives it from the existing exact
boundary coupling, and the translation, rotation and trace-transfer lemmas
preserve it. The complete old assembly then proves the stronger predicate
using unchanged finite witness data and no new native computation.

`StandardTrace.lean` proves the further explicit endpoint:

```lean
OneBlack.universal_one_black_standard_trace (s) (one : ExactlyOneBlack s) :
  ∃ n, HasStandardTrace (run n s)
```

`HasStandardTrace` supplies a translation/quarter-turn placement of the fixed
actual blank state at update 9977 and equality of every future observation
(position, heading, and read colour). This aligns the public manuscript with
the research repository's fixed-standard-trace contract. The two repositories
have different Lean types; no cross-package definitional equality or rebuild
of the unchanged private proof package is claimed. Their semantic contracts
are compared through the same literal rule, blank entry, allowed symmetries,
and full future observation equality.

## Proof dependencies and actual verification

The core still consists of blank entry, the 1,376-cell first-contact domain,
22 affine frontier channels, 21 ordinary classes, the phase-72 reverse channel,
and finite terminal certificates plus all-depth archive-separation inductions.
The 702-cell history is retained. The revision adds a semantic strengthening
at the terminal interface, so all downstream Lean modules are rebuilt.

`python3 preprint/verify.py` makes a new temporary copy with **no .lake cache**,
builds both default targets under Lean 4.30.0, scans source placeholders and
explicit axiom declarations, records SHA256 hashes, and prints/validates the
actual axiom dependencies. Reports are in `verification/`.

The expected six dependencies of each final theorem are:

- propext, Classical.choice, Quot.sound;
- Highway.checks_pass._native.native_decide.ax_1_1;
- PrefixLeaf.verified._native.native_decide.ax_1_1;
- ScatteringLeaf.verified._native.native_decide.ax_1_1.

This is T1 native evaluation, not kernel-only verification or an axiom-free
claim. The bridge itself adds no axiom. The script does not regenerate witness
times and does not claim that doing so is necessary to check the theorem.

## Claim–evidence map and reviewer questions

| Claim | Evidence | Status |
|---|---|---|
| All exactly-one-black states, arbitrary pose | Universal normalization and final theorem | Lean-checked |
| Standard word, not merely period/drift | Strengthened Semantics + StandardTrace bridge | Lean-checked |
| Complete historical residual retained | Boundary guards, ordinary and phase-72 inductions | Lean-checked |
| Unlimited channel depth | Induction modules; finite anchors only at leaves | Lean-checked |
| Computation trusted boundary is exactly three native leaves | Final axiom report | Machine-audited |
| 104 is the least possible period | No separate least-period theorem in this package | Not asserted |
| First theorem of this scope in world literature | No exhaustive priority proof | Not asserted |
| Independent human referee approval | None obtained | Pending |

Five review dimensions: contribution is the unbounded family and proof method;
clarity is improved by the explicit fixed-template statement; evidence is a
fresh complete build and named computational trust; coverage is infinite via
induction, not coordinate sampling; design keeps finite replay and all-depth
soundness separate. The native computation path remains a declared limitation.

## Journal and version plan

[Journal of Automated Reasoning](https://link.springer.com/journal/10817/aims-and-scope)
explicitly includes formal proof assistants and mathematical formalization.
That supports a candidate venue, not an acceptance prediction. The manuscript
keeps the 22 / 21+1 / phase-72 / archive-induction narrative and discloses the
existing preprint and substantive AI assistance. The revised PDF is a new
version of the existing result; it is not a second independent publication.

Two-black audit is parked at the owner's request. No external theorem is
imported, no external author is contacted, and no two-black authorship is claimed.

## Open

External referee-level mathematical reading; final human author review;
complete venue formatting/declarations and broader citation-chain audit.
The original preprint remains the published version until separate publication
instruction is given for the prepared new draft.
