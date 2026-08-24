# Literature audit

This note records the primary-source claims that may be used in the preprint.
It is not a substitute for the bibliography; it is the claim boundary behind
the prose.

## Audited sources

### Langton (1986)

Christopher Langton introduced the artificial-life setting in *Studying
Artificial Life with Cellular Automata*, *Physica D* 22, 120--149,
doi:10.1016/0167-2789(86)90237-X. The paper is the historical source for the
model. The preprint should not attribute our exact time convention or the
9,977 boundary to this paper; those belong to the present artifact.

### Bunimovich and Troubetzkoy (1992)

*Recurrence Properties of Lorentz Lattice Gas Cellular Automata*, *Journal of
Statistical Physics* 67, 289--302, doi:10.1007/BF01049035, is the source cited
by Gajardo--Moreira--Goles for unboundedness of the classical ant trajectory.
The safe comparison is: unboundedness excludes confinement to a finite region
but does not imply entry into the period-104 highway.

The popular “Cohen--Kong theorem” attribution is not used in the manuscript.
Kong--Cohen work on related lattice-gas models and later expository accounts
make the attribution history ambiguous; this is unnecessary to our argument.

### Gale, Propp, Sutherland, and Troubetzkoy (1995)

*Further Travels with My Ant*, *Mathematical Intelligencer* 17(3), 48--56,
studies generalized ants and bilateral symmetries. It is relevant historical
background but is not cited as the source of the classical unboundedness
theorem.

### Gajardo, Moreira, and Goles (2002)

*Complexity of Langton's Ant*, *Discrete Applied Mathematics* 117, 41--50,
doi:10.1016/S0166-218X(00)00334-6, states the finite-support Highway
Conjecture and makes two input contracts explicit:

- Boolean-circuit evaluation gives a P-hard problem on finite-support initial
  configurations.
- The Turing-machine simulation and associated undecidability use an infinite
  but finitely described trapezoidal circuit array.

The paper explicitly leaves decidability for finite-support inputs open. The
preprint must preserve this distinction.

The circuit construction ends by routing the ant into a highway seed. It
therefore also prevents any broad claim that the present work is the first
rigorous infinite family of finite configurations known to reach a highway.

### Tsukiji and Hagiwara (2011)

*Recognizing the Repeatable Configurations of Time-Reversible Generalized
Langton's Ant Is PSPACE-Hard*, *Algorithms* 4(1), 1--15,
doi:10.3390/a4010001, studies recognition complexity for generalized variants.
It independently attributes classical unboundedness to Bunimovich and
Troubetzkoy. Its modified-cell and generalized-ant results are contextual, not
direct competitors to the exactly-one-black theorem.

### Gajardo, Lutfalla, and Rao (2024)

*Ants on the Highway*, arXiv:2409.10124, reports extensive generalized-ant
experiments and proves that a generalized rule may have unboundedly many, or
even infinitely many, distinct highways. Its introduction reports classical
one-black simulations only for black cells within radius three of the ant,
with observed transients typically between 1,000 and 100,000 updates.

This source supports the significance of removing a spatial cutoff, but by
itself cannot establish priority for the present theorem.

### Lutfalla (2025)

*Sideways on the Highways*, arXiv:2505.05426, constructs generalized ants with
highways and qualitatively different asymptotic behaviors from finite
configurations. It shows why claims about the classical LR rule should not be
silently generalized to arbitrary rule words.

### de Moura and Ullrich (2021), Lean reference manual

The Lean 4 system paper is the formal-methods citation. The current Lean
reference manual states that `native_decide` asserts each native result through
a dedicated axiom and extends the trusted computing base to the compiler,
runtime, code-generation backend, and externally linked code. The manuscript
must therefore distinguish kernel-checked analytic proof terms from the three
native computation leaves.

## Priority boundary

The audited sources do not contain a theorem covering every initial state of
the classical LR ant with exactly one black cell and arbitrary ant pose. This
is a literature-search result, not a mathematical theorem. Until a broader
database and citation-chain audit is complete, the manuscript states the
result directly and avoids “first,” “for the first time,” and “no prior
nontrivial infinite family.”

## Claim--evidence map

| Claim | Evidence | Status |
|---|---|---|
| Classical finite-support Highway Conjecture remains open in the cited literature | Gajardo et al. 2002; Lutfalla 2025 | supported |
| Classical trajectories are unbounded | Bunimovich--Troubetzkoy 1992, as cited by Gajardo et al. 2002 and Tsukiji--Hagiwara 2011 | supported |
| Finite-support prediction has a P-hard instance | Gajardo et al. 2002 | supported |
| Universality/undecidability construction uses infinite support | Gajardo et al. 2002 | supported |
| Recent one-black experiments used a bounded radius-three domain | Gajardo et al. 2024 | supported |
| This is the first exactly-one-black theorem | complete primary-source audit | not established; do not claim |
| Every one-black state reaches P104 | current Lean artifact | supported |
