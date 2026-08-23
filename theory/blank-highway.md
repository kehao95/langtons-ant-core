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
start of the period. Thirteen requirements are black. At the next boundary,
the complete set of relative requirements is identical. The checker derives
these values directly from the dynamics in
[`engine/langtons_ant/highway.py`](../engine/langtons_ant/highway.py); no
external table is trusted.

## Why the local recurrence is sufficient

Call a state a boundary when its heading and the colours on those 40 relative
squares agree with the witness. During the 104-step execution every read is
one of those squares. Thus an induction over the 104 individual updates fixes
every turn and flip: black cells outside the read set cannot affect that
period. The finite check establishes that the state at the end has the same
requirements around the translated ant. Applying the same argument repeatedly
gives an infinite sequence of period boundaries.

The checker supplies the finite premises of this argument: entry, displacement,
heading preservation, and equality of the two requirement maps. The induction
above is the analytic step; it is intentionally stated here rather than hidden
inside a simulation cutoff.

## Exact conclusion and boundary

The blank initial state reaches a permanent oriented P104 highway boundary at
update 9,977. The reference model also checks that quarter-turn rotation
commutes with the classical step, so the same local boundary is available in
each of four orientations. This conclusion does **not** establish that other
finite states, including a one-black state, reach any such boundary.
