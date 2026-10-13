# Universal one-black theorem

This directory is the complete proof artifact for

```text
∀ s, ExactlyOneBlack s → ReachesP104 s.
```

[`PROOF.md`](./PROOF.md) gives the mathematical argument in the same order as
the Lean dependency graph. [`lean/`](./lean/) contains the formal proof and
all finite witness data. [`langtons_ant/`](./langtons_ant/) contains the exact
Python dynamics used by [`lean/generate.py`](./lean/generate.py) to regenerate
the two witness-time tables.

Run the complete check from any directory:

```sh
python3 /path/to/langtons-ant-core/one_black/check.py
```

The command builds one Lean target. Internally, the blank certificate is a
shared upstream computation leaf; then Lake checks the prefix leaf and the
shared-snapshot scattering leaf in parallel. Its final theorem is
`OneBlack.universal_one_black` in [`lean/OneBlack.lean`](./lean/OneBlack.lean).
The finite checker gives every frontier channel its own earliest useful replay
band. It binds each of the 22 stable lane results and terminal orientations
once, then shares them between the pristine, ordinary-wake, and phase-72
certificates. Each ordinary cutoff is the first one satisfying the exact
historical-wake separation guard. The exceptional channel uses pristine depth
11, four clean translations, and an actual affine-family base at depth 15.

The proof cone has four layers:

```text
Core, Semantics
       ↓
blank P104 and prefix coupling
       ↓
entry partition and 22-channel scattering
       ↓
21 ordinary returns + 1 phase-72 backscatter
       ↓
universal assembly
```

Generated witness tables live beside the Lean modules that consume them:
`PrefixData.lean` and `EntryData.lean`. Regenerate them with
`python3 one_black/lean/generate.py`; verification itself uses the checked-in
tables and exact Lean replay.


## Standard-trace revision (2026-10-13)

`PermanentP104` now also pins the first read word to the actual blank orbit
at update 9977. [`lean/StandardTrace.lean`](lean/StandardTrace.lean) proves
`universal_one_black_standard_trace`: every singleton eventually has the
entire future read trace of a symmetry placement of that fixed blank state.
Unobserved historical debris remains unrestricted. The proof reuses the same
three native leaves. Run `python3 preprint/verify.py` from the repository root
for a fresh temporary-directory build and both final axiom reports.
