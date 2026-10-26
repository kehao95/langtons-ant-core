# Literature and contributions

These sources locate the one-black theorem within classical ant dynamics,
prediction complexity and formal verification.

## Primary sources

### Langton (1986)

Christopher Langton introduced the artificial-life setting in *Studying
Artificial Life with Cellular Automata*, *Physica D* 22, 120--149,
doi:10.1016/0167-2789(86)90237-X. The paper is the historical source for the
model. The exact time convention and 9,977-update witness are specified by the
one-black artifact.

### Bunimovich and Troubetzkoy (1992)

*Recurrence Properties of Lorentz Lattice Gas Cellular Automata*, *Journal of
Statistical Physics* 67, 289--302, doi:10.1007/BF01049035, is the source cited
by Gajardo--Moreira--Goles for unboundedness of the classical ant trajectory.
Unboundedness concerns confinement; the one-black theorem establishes entry
into the period-104 highway for a specified class of initial states.


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

The paper explicitly leaves decidability for finite-support inputs open. These are distinct input classes.

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
runtime, code-generation backend, and externally linked code. The one-black proof uses kernel-checked analytic proof terms and three
native computation leaves, with their dependencies recorded separately.
