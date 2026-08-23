# Terminal predicate contract

The eventual-highway statement needs a finite condition that can be checked on
a single state. This document specifies the role of that condition before any
particular period table is admitted to the repository.

## Required interface

A candidate predicate `H(state)` must come with:

1. a finite datum defining its reference phase or phases;
2. explicit rules for translation and rotation;
3. a checker that decides membership from the state at the fixed before-step
   convention; and
4. a soundness argument that every accepted state evolves indefinitely through
   the intended translating orbit.

The datum must say which finite window is inspected, what is required outside
that window, and how the ant's phase is encoded. A finite matching picture
alone is insufficient unless its exterior condition is also stated.

## Current status

No terminal predicate has yet been reconstructed in this clean-room project.
Accordingly, there is no claim here that a finite state has been recognized as
highway-bound.
