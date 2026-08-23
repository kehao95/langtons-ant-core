# The open bridge to the highway

Once a sound terminal predicate exists, the remaining global problem is to
show that every finite initial state reaches it. That implication is separate
from recognising a highway phase, and it is the main unresolved bridge in this
repository.

Two research routes are intentionally kept distinct:

- **Descent route.** Define a complete history representation and a
  well-founded quantity that strictly decreases across every nonterminal legal
  renewal.
- **Finite-obstruction route.** Define a family of finite witnesses showing
  that each proposed nonterminal continuation is impossible, then prove the
  family covers all continuations.

Either route must account for all legal histories, not merely the cases found
by a search. Exploratory enumeration can suggest invariants and witnesses, but
it cannot close this bridge by itself.
