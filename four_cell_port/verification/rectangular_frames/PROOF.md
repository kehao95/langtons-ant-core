# Rectangular frames and exact highway entrance

## 1. Complete input contracts and conclusions

States are `(B,p,h)` on Z², with complete finite black set B. White turns right, black turns left, then toggle the read cell and move one unit. State t precedes update t. All unspecified initial cells are white. `tau` is the FIRST time whose entire subsequent turn word is a cyclic phase of the fixed standard word in `verify.py`; it is not the chosen finite verification boundary of a long simulation. Whole-colouring translation is not required.

### A. Four-layer frames

For integers n,m≥10 let R=[0,n−1]×[0,m−1]∩Z², I=[4,n−5]×[4,m−5]∩Z², and G=R\I. For **every** A⊆I, start with exactly G∪A black and head (0,0), north. All these inputs have the same entire head/turn trace; I is never read. Their first permanent times are:

| n parity | m parity | tau | drift per 104 |
|---|---|---|---|
| even | even | 78n+44m+555 | (2,2) |
| even | odd | 30n+44m+438 | (2,−2) |
| odd | even | 38n+62m+1538 | (−2,2) |
| odd | odd | 28n+28m+287 | (−2,−2) |

At fixed dimensions this covers 2^((n−8)(m−8)) initial fields. Their full later fields satisfy B_t^A XOR B_t^(A')=A XOR A' at every time. Interior bits persist physically.

Four is sharp for **identical-trace shielding** over this domain. In the 10×10 solid source the first read of (3,3) is update 1242, requesting L. Removing this initial cell preserves the preceding 1242 turns and changes that turn to R. Both sources have a black three-layer frame. This does NOT disprove convergence with three layers.

### B. All solid rectangles

For every n,m≥1, exactly R black, and the same southwest/north pose, tau(n,m) is finite and

    tau(n,m) ≤ 242(n+m)+29325.

Both constants are sharp in this form: all odd n≥201 at height m=5 have tau=242n+8703, so a smaller coefficient fails with every fixed intercept; tau(30,4)=37553 forces intercept 29325 at coefficient 242.

The exact function is given by 40 affine domains and 3501 finite values. The four domains above cover n,m≥10. The 36 thin domains fix either n=i or m=i, 1≤i≤9, and put the other side L=200+p+2a for p∈{0,1}, a≥0. Their slope/intercept pairs are in `coverage_report.json` and the manuscript's thin table. The complement is exactly

    E={(n,m):1≤n,m<200 and min(n,m)≤9},  |E|=199²−190²=3501.

No finite spatial or temporal cutoff is used for the infinite domains.

### C. Centred solid odd-side squares

For r≥0 take exactly [−r,r]²∩Z² black, with head at the origin north. Every such state becomes standard, with

    tau_c(r)=248r+9475   for even r≥32,
    tau_c(r)=820r+24110  for odd r≥43.

The complement consists of the 37 radii 0,…,31,33,35,37,39,41, whose exact values are supplied and completely checked. Rotating the entire source proves the same entrance times for any cardinal heading at the centre. No corresponding all-heading assertion is made at a fixed rectangle corner.

## 2. Physical verification lemma

For a fixed finite turn word, geometry fixes all read cells. Execution on a supplied field is equivalent to matching its first requested bit at each cell and alternating all consecutive same-cell requests. Necessity is the flip rule. Sufficiency is induction through real time, because the last read flips the only bit that can affect the next read at that cell. The complete output field is the source XOR the odd visit set. This is the established symbolic framework (Gajardo 2003, Section 3), not a new method attribution.

Consider a heading-restoring word u, period P, nonzero drift d, phase offsets q_i. Its block origin p and its repetition count c are affine functions of the parameters. Let B be the complete field at the block start. At phase i of copy k the cell is p+q_i+k*d. Every earlier same-cell phase is a pair (j,s) with

    q_j−q_i=s*d,  s>0 or (s=0 and j<i),  k≥s.

Indeed it is phase j of copy k−s, whose update time is earlier precisely in those cases. The exact read condition is therefore

    1_B(p+q_i+k*d) XOR parity{eligible (j,s)} = 1_[u_i=L].

Check this for EVERY parameter tuple in the declared domain and every integer 0≤k<c. Induction then proves the whole block. Its complete output is

    B XOR XOR_(i=0,…,P−1) {p+q_i+k*d:0≤k<c}.

One phase stream is injective because d≠0. Distinct streams can overlap; XOR, not union, accounts for that. For a final infinite tail the same condition is checked over all k≥0. Induction proves every finite prefix and hence the entire future.

All repeated blocks restore heading; count-one blocks may rotate it. Thus every block anchor, elapsed time and finite repetition bound is affine. The current full black field starts as a rectangle and remains a finite Boolean combination of affine integer sets. The set of parameter/index pairs violating each read equation is Presburger-definable. `verify.py` reconstructs it with exact ISL/GMP operations and requires it to be empty. Its current field retains all unread initial black cells and every past write. Arithmetic errors raise exceptions and are not empty-set answers.

A repeated period is never accepted merely because a few numerical repetitions execute. Candidate generation by finite samples has no role in the acceptance argument. Dense rectangles are finite fibres of affine inequalities, not infinite physical backgrounds. Only the tail's quantification over future epochs is infinite.

## 3. Shielding lemma and exact entrance

For the four large branches, the same verifier additionally proves that the set of reads intersecting I is empty. It checks fixed pieces, repeated pieces and the entire infinite tail over the full two-parameter domains. For a solid reference and any source G∪A, their initial difference is contained in I. Until a first read of a differing cell they have identical poses and updates, preserving the same XOR difference. The certified reference never reads I, so a first differing read is impossible. This proves both trace equality and complete difference persistence.

Every universal program ends at its claimed first standard boundary. Its last actual letter disagrees with the aligned backward continuation of the certified tail. More generally the checker allows a matching suffix of length s and places first entrance at T−s, requiring a preceding mismatch. Any earlier standard tail would agree with the certified periodic future over a full period and therefore with that same backwards extension. The mismatch excludes it. This proves FIRST entrance rather than only an upper boundary. All 42 rebuilt certificates have s=0.

## 4. Complete parameter coverage and finite leaves

`coverage.py` does not trust certificate names as domain coverage. It checks each actual parameter domain against the entire required nonnegative orthant, verifies affine source rectangle and pose, reconstructs block length and endpoint algebra, checks the exact first-time formula, and binds each certificate to its replay report. There are precisely four large, 36 thin and two centre certificates. The elementary domain partitions in Section 1 prove that no size is omitted or counted as an inferred case.

The 42 certificates have 1922 spelled blocks. The acceptance check verifies 71484 read obligations: 2838 for the four large branches, 51863 for the thin branches and 16783 for centred squares. There are also 2838 all-parameter deep-interior avoidance obligations. A fixed-block obligation represents its first read at one cell, after the complete internal alternation test; a repeat obligation represents one phase over every allowed repetition and parameter tuple. These are not counts of sampled trajectories.

The 3501 finite rectangle pairs and 37 finite centre radii are all replayed with a C++ integer-vector simulator and a separate Python vector implementation. Each executes 32681376 literal updates. Every full turn prefix, pose and sorted complete endpoint field is compared before a hash is stored. The native infinite suffix test checks all old-field hits and self-write parity breakpoints, including the last infinite interval. The Python verifier separately uses the chronological full-drift class/minimal-seed criterion, credited to Jillhewar (2026), Theorem 3.1 and Remark 3.2. It accounts for all endpoint black cells outside the minimal active seed by exact future-ray disjointness. The full preceding prefix independently gives the earliest entrance.

For the uniform bound, subtract 242(n+m) from each accepted affine time. Every free-variable coefficient is nonpositive; each domain maximum is consequently at its origin and is ≤29325. Check every finite rectangle value separately. The maximum is exactly 29325 at (30,4). The height-five odd ray supplies the unbounded equality slope. No asymptotic fit is involved.

Additional controls verify all 42 programs at a finite complete source, and 736 frame assignments with complete output comparisons. This includes all 16+64+64+512 interiors at the four smallest parity representatives plus 80 deterministic larger examples. They certify the blank reference at time9977 using its complete715-black state, reject a blocker10^60 periods ahead, retain an inert remote cell, use translated coordinates of size10^80, and reject six malformed/corrupted programs. These controls are secondary to the universal proof.

## 5. Reproduction and mathematical status

    python check.py --full --jobs 3

This is an acceptance-only replay against immutable certificates/reports and source hashes. `--quick` is explicitly partial: four frame certificates and the scope controls, not a fresh replay of the complete 42-domain/3538-case classification. Do not run with Python `-O`.

The evidence is a written all-parameter argument plus exact computer-assisted finite premises, not Lean formalisation or external mathematical review. ISL/GMP is a trusted native decision backend; no independently kernel-checked proof objects for all its emptiness computations are supplied. The two literal implementations do not constitute an independent universal Presburger checker.

The fixed exterior-white and pose hypotheses are part of every claim. Arbitrary finite black seeds are not covered. Three-layer sensitivity is not a negative HC example. The original finite-support Highway Conjecture, a full-input event budget, and all-plane periodic uniqueness receive no new conclusion from this family alone.

## References

* A. Gajardo, *A symbolic projection of Langton's Ant (Extended Abstract)*, DMTCS Proceedings AB (DMCS2003), 57–68, 2003, DOI10.46298/dmtcs.2312. Section3, especially printed p.61, describes first-colour assignment and the same-cell/same-colour forbidden factors.
* A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant: Necessary Conditions, Transverse Exclusions, and Exact Search*, public preprint dated17August2026, Theorem3.1 and Remark3.2, printed p.4. The full-drift criterion is attributed, not claimed new.
* K. R. Etse, *How Long Can The Escaping Ant Be Confined?*, MFCS2026, LIPIcs386,49:1–49:17, DOI10.4230/LIPIcs.MFCS.2026.49. This concerns first exit from finite domains; the present problem concerns permanent entrance from specified finite initial patterns.
* Integer Set Library official manual, Introduction, Sets and Relations, Error Handling. The online manual consulted is0.28; this execution uses0.27-GMP.

The full standalone exposition, tables and bibliographic URLs are in the accompanying article.
