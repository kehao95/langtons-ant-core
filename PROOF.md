# Proof

## Convention

A state is read immediately before an update. On white the ant turns right;
on black it turns left. It then toggles the current square and moves one edge.
North increases the second coordinate. `model.py` implements exactly this
definition with an immutable finite set of black lattice points.

## The finite P104 witness

Starting from the blank plane, `verify_blank_highway` performs 9,977 updates
and calls the result `E`. It then replays the next 104 updates and derives,
rather than stores, the colour required on every square when that square is
first read during the block. Repeated reads are checked for consistency.

The replay checks three finite facts:

1. after 104 updates the heading is unchanged and the displacement is
   `(-2, -2)`;
2. the relative read requirements of the next block are identical;
3. at both `E` and its successor, every initially black square outside the
   current block is absent from every later translated block footprint.

For the third fact, a footprint point has the form `o + n(-2,-2)`, where `o`
is one of the finitely many relative read positions and `n` is a nonnegative
integer. `_multiple` decides that equation exactly in integers. Only the
finite black support must be inspected.

## Recurrence lemma

Suppose a state has the witness heading and required local colours, and no
extra black square lies in a later block footprint. Induction over the 104
individual updates gives the same turns and visited positions as the finite
replay, because each decision reads a required colour and all earlier toggles
within the block are identical. Thus the endpoint is displaced by `(-2,-2)`
with the same heading and the same relative local requirements.

The only squares changed during the block are its footprint. An extra black
square is never read because later footprints were required clear. Removing
the completed footprint and translating the index `n` by one therefore gives
the same clear-corridor condition at the endpoint. The finite checks at `E`
and its successor cover the local overlap between adjacent footprints. Hence
the endpoint satisfies the same hypotheses. Induction on the number of
blocks proves an infinite translating period-104 highway.

Applying this lemma to `E` proves the blank-plane result.

## One black square under the ant

`verify_one_black_under_ant` starts with the ant at `(0,0)`, facing north,
and with `(0,0)` as the only black square. Exact replay for 9,978 updates
reaches one of the four rotated terminal P104 states above, so the recurrence
lemma proves permanent highway motion.

Translation and quarter-turn rotation commute with one ant update: they
preserve colour membership, exchange headings and unit moves in the same way,
and leave left and right turns unchanged. Induction on updates transports the
canonical replay to every initial position and heading. This proves the second
result stated in `README.md`.

## Scope and trust

Nothing here proves the case where the single black square starts away from
the ant, nor the general finite-support Highway Conjecture.

The trusted executable base is the Python interpreter, `model.py`, and the
finite arithmetic in `highway.py`. The recurrence lemma and symmetry argument
above are human-checked mathematics; there is no claim that they have been
formalized in a proof assistant.
