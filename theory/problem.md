# Problem and state convention

## The system

The board is the square lattice `Z²`. A state has a finite set of black
lattice squares, an ant position, and one of four headings. The reference
model in [`engine/langtons_ant/model.py`](../engine/langtons_ant/model.py)
uses the following update order:

1. Read the colour under the ant.
2. Turn right on white and left on black.
3. Toggle the colour of that square.
4. Advance one edge in the heading obtained at step 2.

Coordinates are oriented with north increasing the second coordinate. A state
is recorded just before its next update. These choices are part of the research
interface: later predicates and certificates must use them or state an explicit
translation.

## Target question

Starting from any finite black set, does the classical ant eventually enter a
translate, rotation, and phase of the familiar 104-step translating highway?

This repository treats that sentence as the research target, not as a theorem.
The model establishes only the local transition rule. A global conclusion needs
a terminal predicate, a soundness theorem for that predicate, and a bridge from
arbitrary finite support to one of its accepting states.
