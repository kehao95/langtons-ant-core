# Fixed-schema query optimization without changing physical coverage

This is an exact algorithmic refinement of the supplied-schema resource backend,
not a new HC implication, an all-schema exclusion, or a polynomial-time theorem
for general Presburger arithmetic. Proofs are analytic and unformalized; exact
checks use libisl/GMP and the unchanged SHA256-pinned two-file baseline.

## 1. The avoidable numeric-threshold dimension

The retained `Schema.cardinality_at_most(F,m)` checks whether a unary integer
fibre F has at most the supplied INTEGER m elements by constructing m+1 ordered
members of F. It takes m flat products, then imposes t0<...<tm and projects to
parameters. Its explicit tuple dimension is m+1, in addition to parameters.
For large numeric m this representation is unnecessary.

Let D be the supplied parameter domain. For each lambda in D define

    C_lambda = {(a,b): a,b in F_lambda and a<b}.

Composition always retains the SAME parameter values. For every integer m>=1,

    |F_lambda|>m  iff  C_lambda^m is nonempty.                 (1)

Indeed, a path of m strict-order edges gives m+1 distinct members of F. Conversely
any m+1 ordered members supply such a path. No adjacency assumption is needed.
The statement also holds for infinite integer fibres: each finite threshold is
exceeded. For m=0 use nonemptiness of F directly. D may contain parameters for
which the fibre is empty. Overlapping set descriptions do not count duplicates.

Thus `CountQuery.at_most(m)` returns

    D minus params(C^m),    m>=1;
    D minus params(F),      m=0.                             (2)

Repeated squaring constructs powers C^(2^j); multiply only the powers for set
bits of m. A fresh nonzero query uses exactly

    floor(log2 m)+popcount(m)-1                               (3)

binary relation compositions. Stored maps have one input and one output time
coordinate, rather than m+1 explicit tuple coordinates. A reusable query caches
these powers for subsequent bounds. Parameters, existential variables eliminated
inside a composition, and ISL local division variables are NOT included in this
explicit dimension count. The representation size of the intermediate maps is
not proved bounded by a polynomial in log m. Relation composition and coalescing
may still be costly. Equation (3) bounds calls, NOT their total bit complexity.
No approximate transitive-closure operation is invoked.

Unary time fibres include the first-L times used by the existing initial-black
cost and the forbidden-window end times used by its defect cost. A physical
resource domain must still be intersected with the supplied schema's feasibility
domain, exactly as in the old API; an infeasible schema is not made realizable by
a cardinality check. The backend does not add or erase any physical cell.

## 2. Sharing exact factor-language tests

For a schema turn word and k-letter whitelist, let U be the set of end times
of complete k-windows. For each offset i let R_i and L_i be the shifted sets
of right and left turn times. For each valid parameter and time in U, these
sets partition U, because the schema gives exactly one turn at each consecutive
time. This remains true for empty and zero-power branches.

The old matcher unions one intersection of k masks for each allowed word.
The new matcher builds a reduced ordered Boolean decision DAG for membership
in the finite whitelist, using R=0 and L=1. Identical suffix functions share a
node. A node with identical children is removed; partition of U is necessary
for this simplification. Terminals represent the empty set and U. Evaluation is

    Value(node(i,r,l)) = (R_i intersect Value(r))
                         union (L_i intersect Value(l)).    (4)

Structural induction proves that a node's value is exactly its accepted end-time
set. The answer U minus Value(root) is therefore precisely the old forbidden-
window set. No per-parameter sampling or physical-history deletion occurs.
All nodes are exactly coalesced. Omitting this simplification in a development
version caused avoidable intermediate disjunction growth, despite fewer Python
operations; that version is not the delivered backend.

For the existing 84 standard ten-factors, complete reconstruction has 117
nonterminal nodes. It evaluates 183 mask intersections and 66 mask unions,
instead of 840 intersections and 84 unions. Both implementations use 20 shifted
letter masks. These counts exclude setup/final subtraction; the new method also
performs per-node coalescing. They are not a general worst-case speedup theorem.
The whitelist and event definition are unchanged. The DAG truth table was
checked on all 1024 ten-letter words.

## 3. Exact implementation checks

`fast.py` supplies an opt-in `FastSchema` subclass and reusable `CountQuery`.
It checks the two inherited source hashes at import and refuses changed baselines.
All other Schema methods, especially read-order feasibility and complete endpoint
fields, are inherited unchanged. Old source files and manuscript backends are
not silently replaced. The new global schema coverage is exactly the old one.

The deterministic theorem-local replay checks:

- 224 finite-subset/threshold answers, including 96 baseline equalities;
- 60 unrestricted symbolic threshold-domain equalities and 360 fixed-fibre counts;
- a 10^60 threshold on a two-residue fibre, with a symbolic exact answer and 259
  compositions; a cached follow-up needs 61 additional compositions;
- exact factor sets on five named schemas, 24 additional random schemas and 20
  extra small whitelist tests; 96 independent parameter instances and 892 requested
  turns, including 63 physically feasible controls;
- a complete three-sweep endpoint with a genuinely unqueried 10^60-coordinate
  marker preserved; ten malformed-input, mixed-context and native-quota controls.

For rail/sweep and random schemas the old and new matcher sets are compared
exactly. For the large standard, marker and fold examples, the optimized sets
are checked against independently specified exact expected sets and finite
literal windows; a timed-out old matcher is NOT recorded as an equivalence pass.
General equivalence follows from (4) and the Boolean truth-table control.
Arithmetic failures and resource exhaustion remain exceptions/INCONCLUSIVE.

## 4. Matched fresh-process measurements

All completed comparisons use the same named input, native isl-0.27-GMP and
five new child processes per method, alternating execution order. Timing covers
the named query only, not common construction. Linux peak RSS is whole-process
memory, including imports/construction, not incremental allocation of the query.
The address-space cap is 1 GiB and child wall-time cap is 10 seconds. Every pair
of completed result sets is checked for exact equality. Stored measurements are
individual samples, not fitted timings or extrapolations.

| Query | Old median (s) | New median (s) | Measured ratio |
|---|---:|---:|---:|
| Interval threshold 32 | 0.020412759 | 0.000324740 | 62.86 |
| Interval threshold 64 | 0.146469349 | 0.000333433 | 439.28 |
| Interval threshold 128 | 1.562235160 | 0.000315175 | 4956.72 |
| LRRL rail initial-cost threshold 4 | 0.010839026 | 0.002723455 | 3.98 |
| LRRL rail defect threshold 128 | 1.702296193 | 0.000517059 | 3292.27 |
| Rail ten-factor matching | 0.015891810 | 0.008942572 | 1.78 |
| Three-sweep ten-factor matching | 0.417802281 | 0.113633619 | 3.68 |
| Standard W^n ten-factor matching | INCONCLUSIVE at cap | 1.306533325 | not reported |

For the rail defect threshold, median whole-process RSS decreases from 112676
KiB to 97824 KiB. The factor matcher does NOT uniformly reduce peak RSS: for
three sweeps the medians are 98076 and 99484 KiB respectively. Millisecond and
submillisecond timings are machine-dependent. No end-to-end solver speedup is
inferred. The initial unconstrained baseline standard probe also exceeded its
45-second process limit; the table uses only the common controlled 10-second cap.

## 5. Remaining complexity and HC boundary

Neither optimization enumerates the full nonzero-budget path-schema disjunction.
The number of candidate schemas, parameters and Presburger pieces may still grow
rapidly with event budget. The current-state read-order construction also remains
a possible bottleneck. No new mu(N) value, initial-mass budget, uniform event
termination result, finite HC counterexample or all-input HC proof follows.

The useful change is narrower and executable: supplied unary threshold queries
no longer allocate a number of explicit tuple coordinates proportional to the
numeric threshold, and standard-factor matching shares exact logical structure.
This reduces two actual backend costs without changing the physical question.

## 6. Reproduction and attribution

Run `python scripts/check_defect_compiler_optimization.py` for disposable,
deterministic report-comparison correctness replay. Run the module's `benchmark.py` separately
for new measurements; timing reports are not byte-comparison certificates.
The committed benchmark JSON losslessly deduplicates repeated output sets and
operation counts while retaining all per-process measurements and source hashes.

Repeated squaring and decision DAGs are standard algorithmic techniques, not new
mathematical inventions. Native operations use the public ISL interfaces documented
in the Integer Set Library manual (https://libisl.sourceforge.io/user.html).
The source geometry, physical feasibility and root-cost semantics are inherited
from `defect-resource-spectrum.md`; the all-coordinate finite-budget theorem in
`presburger-defect-reachability.md` is neither re-proved nor upgraded here.
