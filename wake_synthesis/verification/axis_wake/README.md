# Axis-wake inversion parity

For full axis displacement (a,0), a>0 even, represent odd-visit translation
classes in 0<=x<a. Their strict inversion count must be even.

Run `python3 wake_synthesis/reproduce.py --axis-only` from the repository root.
Only standard-library Python 3.10+ is needed. The three exact regression reports
cover closed patterns, independent parity identities and the cycle-edge family.
`axis_wake.py` implements the sparse O(g log(g+1)) integer-operation screen;
a passing parity test is a necessary condition, not a physical realization.
The article proves circulation invariance and the endpoint formula analytically.
The inherited stabilized-class criterion and port method are attributed there.
`manifest.json` binds the checker sources and evidence; reports are compared
without regeneration. This module does not replay the non-axis classification.
