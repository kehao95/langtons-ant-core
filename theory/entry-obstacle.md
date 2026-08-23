# A one-obstacle theorem outside the future P104 footprint

Let `E` be a state at the oriented P104 boundary, and add one black square at
an arbitrary point `q`. The 104-step witness reads a finite set of 40 relative
positions and then translates the ant by `(-2,-2)`. Hence every square ever
read by the unperturbed future highway lies on one of 40 discrete forward
rays. Their overlaps reduce to 22 distinct forward lanes:

```text
anchor + footprint_offset + n * (-2,-2),    n >= 0.
```

If `q` is on none of these rays, `E` with the colour at `q` toggled still has
the same read colour at every future update as `E`. It preserves the terminal
predicate's clear-future-corridor condition, so induction over successive P104
periods gives a permanent boundary. The classifier in
[`engine/langtons_ant/obstacles.py`](../engine/langtons_ant/obstacles.py)
solves the ray equation from the finite footprint; it does not search a long
future trace.

This is a substantial but partial entry-obstacle theorem. A point on a ray may
interact with the active highway and is deliberately left unresolved. The ray
cases are the only remaining infinite part of the arbitrary-offset one-black
bridge.
