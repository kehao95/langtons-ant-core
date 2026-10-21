# Nine-factor mass bound and the sharp factor-window threshold

This package proves the universal finite-word deficit bound
`3*length - 26*(R-L) <= 1004` under the standard nine-factor language.
The all-input interval bound is `deficit <= 1033*N9 + 1004`.
The numerical bound 1004 is not claimed optimal.

Two complete enumerations agree on all 164,283 physically feasible length-150
words. The checker independently rebuilds the overlap graph, SCCs, follower
projection, fourteen forbidden-factor conflicts, reachable suffix product,
9,550 integer edge inequalities and the whole condensation budget. It compares
the entire deterministic report, not only a checksum or a sample.

`eight_witness.py` verifies a different, eight-legal 22-letter word. Its infinite
initial colouring has five black rays; truncating each ray to n sites gives a
COMPLETE FINITE input with 3+5n black cells, an exact 22n-step prefix and deficit
66n. The first departure from that word is update 22n. This proves that nine is
the least window length admitting a seed-independent constant of this form.
It does not supply a finite-support nonstandard periodic ant.

Run from the repository root:

```sh
python experiments/hc_global/nine_mass/check.py --compare experiments/hc_global/nine_mass/check_results.json
```

Python 3.10+, a C++17 compiler and the standard library suffice. Runtime scratch
files and the native executable are created in a temporary directory. The native
enumerator source is in `research/nine_factor/enumerate.cpp`; no network is used.
The analytic all-length coverage and truncation proof are in
`proof/results/nine-factor-mass-bound.md`. This is not Lean formalization,
outside mathematical review, a nine-factor attraction theorem, or an HC proof.

`discovery.json` records a finite proposal/refinement search. It is not trusted
as proof: every forbidden factor and every final integer inequality is rechecked.
An earlier unverified 308-period narrative was withdrawn and is not part of this
certificate; do not resurrect it from transient messages or obsolete patches.
