# Integer-clock proof audit

The current [proof](../../PROOF.md) and [manuscript](../../paper/main.tex) derive
unit clock gain, the localized square range and complete-state time budgets.

- `audit.json`: all 24 heading/colour/sign branches verified as exact polynomial
  identities in z=3^k, with the central value handled separately.
- `check.json`: all 18,696 initial states in squares through side three, 12,416
  internal-transition identities, direct range formulas for 100 side lengths,
  and exact small-square maximum exit times 1, 6, 17.

The code imports no private repository. The symbolic branch audit imports no
clock implementation; the state enumeration uses the formula in `clock.py`
and an independent vector-turn stepper. Universal escape follows from the
written localized range and T-1 internal-update argument. The new clock and
range are analytic, not included in the earlier Lean local lemmas.

Run `python3 clock_escape/reproduce.py --integer-only` from the repository root.
