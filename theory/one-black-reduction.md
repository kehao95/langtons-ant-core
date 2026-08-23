# Reduction for an arbitrary one-black offset

Normalize an arbitrary one-black initial state by translation and quarter-turn
rotation so that the ant begins at the origin facing north. The remaining
parameter is the location `q` of its unique black square.

## Finite prefix split

The blank trajectory before its P104 entry reads 1,376 distinct squares. The
set is derived by `blank_entry_prefix_domain()` rather than stored as a copied
case list.

- If `q` is outside that set, the blank and perturbed trajectories have equal
  read colours at every update before entry. They therefore make the same
  turns, flips, and moves. At entry the perturbed state is exactly the blank
  entry state with `q` toggled.
- If `q` is inside the set, the interaction occurs in a finite, explicitly
  derived domain of 1,376 locations. Those cases still require a terminating
  certificate or a proof-producing solver; they have not been discharged here.

The first bullet follows by induction on time: before the first visit to `q`,
the two black sets differ only at `q`, which is not under the ant. The checker
in [`engine/langtons_ant/coupling.py`](../engine/langtons_ant/coupling.py)
checks a representative unread reduction against the literal dynamics and
rejects a point in the read domain.

## Remaining obligations

This reduction turns the arbitrary-offset theorem into two independent tasks:

1. prove that the P104 entry state with one arbitrary additional black square
   eventually reaches a standard boundary; the off-ray subfamily is now closed
   by [`entry-obstacle.md`](./entry-obstacle.md), while the footprint rays
   remain open; and
2. close the finite prefix domain without using an unchecked cutoff.

Neither task is claimed complete in this repository yet.
