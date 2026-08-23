# The blank-orbit P104 witness

This is the first promoted finite result in the clean-room repository. It is
an oriented statement about the all-white initial state, not the one-black
theorem.

## Finite witness

Starting from the blank state at the origin facing north, the reference model
reaches an entry boundary after 9,977 updates. Over the next 104 updates it:

- finishes with the same heading;
- moves the ant by `(-2,-2)`; and
- reads only 40 distinct squares.

For each of those squares the checker reconstructs the colour required at the
start of the period. Thirteen requirements are black. The period toggles a
fixed set of 32 relative squares. At the next boundary, the complete set of
relative requirements and the toggle set are identical. The checker derives
these values directly from the dynamics in
[`engine/langtons_ant/highway.py`](../engine/langtons_ant/highway.py); no
external table is trusted.

## Why the local recurrence is sufficient

Call a state a *local boundary* when its heading and the colours on those 40
relative squares agree with the witness. During the 104-step execution every
read is one of those squares. Thus an induction over the 104 individual updates
fixes every turn and flip for that period.

Local agreement alone is not terminal: an extra black square can be outside
the current footprint but on a later footprint ray. The terminal predicate
therefore also requires the future corridor to be white: no black square may
have first future-read period greater than zero. The finite ray equation decides
that condition over the finite black support. The macro transition preserves
both the local boundary and the clear corridor, so its induction gives a
permanent sequence of P104 boundaries.

The checker supplies the finite premises of this argument: entry, displacement,
heading preservation, equality of the two requirement maps, and equality of
the two toggle masks. The induction
above is the analytic step; it is intentionally stated here rather than hidden
inside a simulation cutoff.

## Exact conclusion and boundary

The blank initial state reaches a permanent oriented P104 highway boundary at
update 9,977. The reference model also checks that quarter-turn rotation
commutes with the classical step, so the same local boundary is available in
each of four orientations. This conclusion does **not** establish that other
finite states, including a one-black state, reach any such boundary.
