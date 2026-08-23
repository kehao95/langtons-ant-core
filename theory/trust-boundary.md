# Trust boundary

## What the current checker establishes

The Python reference model is a small executable definition of the classical
rule. It deterministically derives the blank entry, the 104-step local
requirements, the toggle mask, the drift, the future-lane cover, and the
finite canonical one-black prefix. Unit tests reject changes to those finite
facts and to the distinction between a local boundary and a clear-corridor
terminal state.

The Lean project independently formalizes the rule and proves that rotation
and translation commute with every finite number of updates. It does not call
the Python code and does not yet formalize the P104 finite calculation.

## What remains mathematical prose

The local-to-infinite P104 step uses a short induction: a clear future corridor
prevents later reads from seeing an unaccounted black square, and the checked
macro transition restores the same condition. The arbitrary-offset one-black
reduction uses the analogous first-read induction. These arguments are written
in `theory/`; their finite premises are checked by Python, but the inductions
are not yet Lean theorems.

## What is not in the trusted result

No historical certificate, generated table, external database, Go checker, or
predecessor Lean source is a dependency. No bounded experiment is accepted as
evidence for the 22 interactive lanes, the 1,376 prefix cases, arbitrary
one-black termination, or the Highway Conjecture.
