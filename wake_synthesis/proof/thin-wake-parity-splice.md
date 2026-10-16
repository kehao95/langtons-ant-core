# A parity splice in the thin width-ten rigidity proof

15 October 2026. Base read: `2f6010a6bbccf5d342648f1c730a8bd2ea628961`.
This shortens the proof of an existing theorem; it does not enlarge its input
class or establish full-drift-only uniqueness. Prior native certificates are
retained and not reclassified as newly run or newly formalized.

## 1. The two interfaces, with the same normalization

Use the classical finite-support LR ant. The period restores heading and has
FULL drift (2,-2); no division by gcd or reflection is used. In the top-rail
frame, sigma=-1, t=x+y, top t=0 and bottom t=-10. The odd class is (t,x mod 2).
The thin theorem assumes growth 12, width 10, and at most one odd class on each
strict interior level; it derives two full extreme rails and exactly one
missing odd-class layer h in {-9,-7,-5,-3,-1}.

The [mixed-wake theorem](mixed-wake-interleaving.md) is expressed in sigma=+1.
Translating the entire state by (0,1) changes t to t+1, preserves the lane and
the drift, and changes sigma to +1. Thus its Q layers are precisely the odd
original t, and its C layers the even original t. Ordering is unchanged.
The condition is J+V/2=1 modulo two, where V counts Q classes and J counts
Q-below-C pairs. This is necessary for actual periodic realization, not a
sufficient inverse test.

## 2. Remove three computed exclusions

With missing odd h the Q population is always V=4. The two full extreme C
rails contribute, and the other internal C layers are singletons. Directly,
J=(h+37)/2. Hence:

| h | V | J | J+V/2 mod 2 | conclusion |
|---:|---:|---:|---:|---|
| -9 | 4 | 14 | 0 | impossible by mixed parity |
| -7 | 4 | 15 | 1 | retain actual chronological exclusion |
| -5 | 4 | 16 | 0 | impossible by mixed parity |
| -3 | 4 | 17 | 1 | standard transverse profile |
| -1 | 4 | 18 | 0 | impossible by mixed parity |

The calculation is independent of the eight lane choices. It excludes all
three rows at once, not merely their residue-admissible masks.

The shortened proof is therefore:

    thin g=12, W=10 => five possible missing layers
    => h=-7 or h=-3 by mixed parity
    => h=-3 by the retained h=-7 chronological subcertificate
    => P104 by standard-layer-profile uniqueness.

For h=-7 use the twenty completed normalized cases in the original thin-wake
archive, with cap 168 and its original exact-event coverage proof. For h=-3
invoke [standard-layer-profile uniqueness](standard-layer-profile-uniqueness.md),
which already covers all longitudinal residue assignments without a period
premise. Its proof is not repeated here. Merely passing mixed parity would
NOT permit replacing either of these remaining arguments.

The former complete five-profile enumeration stays as a valid alternative
proof and regression artifact. The new dependency chain needs no enumeration
for h=-9,-5,-1. The historical counts 76 cases/83 jobs describe the original
run, not a new faster replay; no runtime speedup is asserted here.

## 3. General version of the elementary calculation

Suppose a normalized thin wake has two full extremes at -2k,0, and one odd
class at every strict interior layer except h=-2k+1+2j, 0<=j<k. Its growth is
2k+2, so heading restoration forces k odd. There are k-1 Q classes. Before
removing that Q, the k Q classes have k(k+3)/2 Q-below-C pairs; the removed Q
had k+1-j C classes above it. Therefore

    V=k-1, J=(k+2)(k-1)/2+j,
    J+V/2=(k-1)(k+3)/2+j = j (mod 2).

The mixed theorem requires j odd, equivalently h=1 mod 4. This is an analytic
necessary condition for the specified single-gap family, not a theorem that
arbitrary drift-(2,-2) wakes have this family form. For k=5 it gives the table.

## 4. Drift-only target and retained gap

The desired final theorem would classify EVERY finite-support periodic word
with full drift (2,-2) as standard P104, without growth/width/thinness premises.
Clock and parity formulas plus the present splice have not proved that every
such word has g=12, W=10 and thinness, or the standard layer profile directly.

In the sigma=+1 frame the formal eight-class set

    {(1,0),(1,1),(2,0),(3,0),(5,1),(6,1),(11,0),(11,1)}

passes signed residues and mixed parity (V=2,J=6) but is not a standard profile.
Replacing (t,r) by (kt,r) for any positive odd k preserves those necessary
screens and gives width 10k. This is a countermodel to an inference about
SCREEN OUTPUTS, not a physical ant family or counterexample. No finite seed
or complete word is supplied. Nor is this claimed to pass every other test.
The true missing bridge must use realizability, not only those screen values.

## 5. Scoped replay

    python experiments/hc_global/thin_parity_bridge/check.py

The checker pins the unchanged mixed-wake implementation, independently counts
pairs in both coordinate conventions for all 1280 thin masks, tests the
closed general formula, and retains formal growth-eight and full-drift controls.
It emits the report to stdout and does not modify existing certificates.
The all-k conclusion is proved in Section 3, not extrapolated from finite tests.
No old native search, old Lean theorem, public manuscript or external review
is claimed to have been rerun. This is proof refactoring plus an elementary
family consequence, not a new full-drift classification.
