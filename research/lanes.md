# P104 lane-contact research

The entry-obstacle theorem leaves exactly the future read lanes. A lane is not
a hand-written case label: it is an equivalence class of the 40-step footprint
under repeated P104 displacement. The reference model derives 22 such lanes.

`engine/langtons_ant/lanes.py` constructs a `LaneContact` from a lane and a
non-negative depth. It recomputes the literal first period in which the chosen
obstacle is read, because multiple footprint offsets may share one geometric
lane. The object contains the pre-contact boundary and the precise relative
obstacle position.

This representation is the required input to any scattering experiment or
inductive proof. A proposed lane theorem must state how its result depends on
depth, establish all base residues, and prove that its claimed transition does
not rely on an unrecorded portion of the historical wake.
