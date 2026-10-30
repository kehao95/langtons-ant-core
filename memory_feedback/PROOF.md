# Prediction, complete history and remote feedback

## Crossing information and spatial growth

For any complete finite initial state whose orbit is not eventually translating,
whole-prefix width w(T) along a non-axis normal normalized by
`min(|alpha|,|beta|)=1` satisfies
`liminf w(T)/log(log(T)) >= 1/log(2)`.
The finite inequality is uniform over normalized normals. Eventual translation
here allows any nonzero displacement and repeating turn word.

The article derives this from a protected crossing-record pumping lemma,
exact alternating-parity signature capacity, minimum packing work, a finite
profile deadline, and the ant's local corner read bound. Crossing cuts lie beyond
all initial black cells; the forward blank guard refers to the complete field.
The proof also supplies speed/spread bounds and a certificate-or-width-violation
procedure for rational normals. Optional execution caps return UNKNOWN.

[Crossing checks](verification/crossing_gap/) compare full Python/C++ trajectories,
capacity and packing identities, corner inequalities and remote-cell guards.
Run `python3 memory_feedback/reproduce.py --crossing-only`.
The geometric argument and the S_D feedback argument are separate necessary
conditions. Their event budgets are not substituted for one another.


## Arithmetic and feedback constructions

The construction gives [birth-filtered feedback](proof/birth-filtered-feedback.md):
the first remote old lifetime created since the source checkpoint is totally
computable, with exact birth, consumption and complete XOR endpoint. Initially
black coordinates remain eligible after erasure and rebirth. On non-eventually-
translating orbits, uniform deadlines yield `Omega(sqrt(H)/log(H))` late-born
lifetimes at simultaneously growing radius and age. Complexity is polynomial
for fixed D and fixed K on explicit sparse input; the theorem is not uniform
polynomial in binary D or K's diameter.

## Proof dependencies

The proof follows five dependencies in order:

1. [Stale-memory prediction](proof/stale-memory.md): the intrinsic S_D identity,
   finite suffix cycle and exact first mismatch on every sparse finite input.
2. [Symbolic macros](proof/symbolic-stale-macros.md): finite XOR segments,
   arithmetic-progression intersection and exact reusable complete endpoints.
3. [Event geometry](proof/stale-event-geometry.md): the convex halo and quadratic
   finite-event time budget, strengthening the earlier exponential bound.
4. [Remote feedback](proof/remote-stale-feedback.md): endpoint tube, fixed-region
   burst bound, total filtered decision and simultaneous remote/late-born/long-lived consumption.
5. [Twenty-cell circuit](proof/scalable-feedback-circuit.md): all-parameter
   execution, 31 intermediate S_128 reads and exact first P104 entry.

The manuscript uses the current clock bound from version 0.4.0; the retained
remote checker uses the sufficient conservative older bound. Both are stated
explicitly. The code and proof do not exchange S_D, J10 or physical gate budgets.

## Request reconstruction and stronger capacity

For cuts beyond the complete initial support, each incoming-height list
uniquely determines all completed right-side replies and retained writes.
Normalize by the minimum entry height and divide by two. Distinct genuine
records then inject into words of length j+1 containing zero, over an alphabet
of q=floor(H/2)+1 symbols. Their upper capacity is q^(j+1)-(q-1)^(j+1).
Shortest-code packing gives the all-prefix horizontal-work inequality. The
same cumulative capacity sharpens the profile deadline; its entropy form gives
exponent 4v/(1-2v) for positive-speed subsequences on nontranslating orbits.
The double-logarithmic oblique-width coefficient remains 1/log(2).

The complete proofs are in the article's crossing-information section;
[request checks](verification/crossing_supply/) retain complete fields and
pin the unchanged crossing baseline. Request uniqueness concerns actual
completed histories. It does not assert termination of an arbitrary requested
excursion or physical realizability of every counted code.
