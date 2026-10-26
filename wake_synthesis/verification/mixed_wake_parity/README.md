# Mixed-wake interleaving parity — periodic HC branch

For full drift (2,-2), let V count odd translation classes on vertical-arrival
layers, and J count pairs (vertical-layer odd class, higher horizontal-layer odd
class). Every finite-support periodic realization obeys

    J + V/2 = 1 (mod 2).

Read `PROOF.md` for normalization, complete proof, attribution, the 512-case
Boolean algebra kernel, and unbounded-width growth-eight corollaries. This is
not a complete realization criterion. `NOT_EXCLUDED` NEVER means `YES`.

Run `python check.py`. Add `--enumerate` for the bounded width-10/12/14 arithmetic
screen. Standard library only. The finite table does not carry the unbounded
quantifier: the telescoping algebra identity does.

The general statements have analytic proofs without formalization. HC,
growth-eight existence, and all-seed periodic entrance remain open.
