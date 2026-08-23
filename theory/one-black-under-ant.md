# One black square under the ant

## Statement

For any lattice point `p` and any heading `h`, start with exactly one black
square at `p` and place the ant at `p` with heading `h`. The trajectory reaches
a permanent standard P104 boundary.

## Finite core

The canonical presentation puts both the ant and black square at `(0,0)` and
uses north. The reference model reaches a rotated P104 boundary after 9,978
updates. [`engine/langtons_ant/one_black.py`](../engine/langtons_ant/one_black.py)
computes that finite prefix and rejects it unless the boundary predicate from
[`blank-highway.md`](./blank-highway.md) accepts the endpoint.

Translation commutes with every update because the rule depends only on
relative lattice positions. Quarter-turn rotation commutes because it preserves
white/right and black/left while rotating heading and coordinates together.
Therefore translation and rotation carry the finite core to every `p` and `h`.
The permanent conclusion then follows from the P104 recurrence.

## Scope

This is a genuine one-black theorem, but only for the subfamily where the ant
starts on the black square. It does not quantify over an arbitrary offset
between the ant and the one black square. That larger universal one-black claim
remains an explicit open reconstruction task.
