---
title: "Every One-Black-Cell Langton Ant Reaches the Period-104 Highway: A Lean-Checked Proof"
author: "Hao"
date: "Draft, 24 August 2026"
bibliography: references.bib
link-citations: true
documentclass: article
classoption: [11pt]
geometry: [margin=1in]
colorlinks: true
linkcolor: MidnightBlue
urlcolor: MidnightBlue
citecolor: MidnightBlue
toc: false
toc-depth: 2
numbersections: true
header-includes:
  - |
    \usepackage{fontspec}
    \setmonofont{DejaVu Sans Mono}
    \usepackage{amsmath,amssymb,amsthm,mathtools}
    \usepackage{booktabs,array,longtable,microtype,xcolor,tikz}
    \usetikzlibrary{arrows.meta,positioning,shapes.geometric,decorations.pathreplacing}
    \definecolor{proofblue}{HTML}{28678D}
    \definecolor{proofgreen}{HTML}{2F855A}
    \definecolor{prooforange}{HTML}{C76B29}
    \definecolor{proofpurple}{HTML}{7355A3}
    \newtheorem{theorem}{Theorem}[section]
    \newtheorem{lemma}[theorem]{Lemma}
    \newtheorem{proposition}[theorem]{Proposition}
    \newtheorem{corollary}[theorem]{Corollary}
    \theoremstyle{definition}
    \newtheorem{definition}[theorem]{Definition}
    \newtheorem{remark}[theorem]{Remark}
    \newcommand{\Z}{\mathbb{Z}}
    \newcommand{\Ponezerofour}{\mathrm{P104}}
---

\begin{abstract}
Langton's ant is a deterministic walk on the square lattice whose blank-plane
orbit eventually exhibits a diagonal period-104 highway, but the corresponding
finite-support Highway Conjecture remains open. We prove a complete unbounded
subfamily: from every initial state having exactly one black cell, with no
restriction on that cell's position or on the ant's pose, the classical
two-colour ant eventually reaches permanent period-104 behaviour. The proof
normalizes the pose, couples the perturbed orbit to the first 9,977 steps of the
blank orbit, and reduces every untouched defect to one of 22 affine frontier
channels. Twenty-one channels admit an ordinary scattering induction after a
channel-specific finite cutoff. The remaining channel first creates a reverse
period-104 highway; in the physical historical state it returns to a fixed old
cell, with collision time increasing by 208 steps per unit depth, and then
enters the forward highway after a checked finite transient. The infinite
reductions, geometric separation arguments, recurrence relations, and
certificate-soundness theorems are formalized in Lean 4. Three closed finite
reports---the blank highway, 1,376 prefix contacts, and the shared scattering
certificate---are evaluated with \texttt{native\_decide}. We state this trust
boundary explicitly: native evaluation adds Lean's compiler, runtime, and
code-generation path to the trusted base. The checked sources, witness tables,
and reproduction command are available in the accompanying artifact.
\end{abstract}

\clearpage
\tableofcontents
\clearpage

# Introduction

Langton's ant is among the simplest deterministic systems in which a short
local rule produces a long irregular transient followed by rigid macroscopic
motion. A cell of the square lattice is white or black. On each update the ant
reads its current cell, turns right on white and left on black, flips that
cell, and advances one lattice edge. From the all-white plane, the orbit is
observed to settle into a diagonal highway: every 104 updates the same local
behaviour recurs, translated by two cells in each coordinate [@langton1986].
The question is not whether this particular computation can be run for long
enough, but which finite perturbations can be proved to enter such a permanent
regime.

The general finite-support Highway Conjecture remains unresolved. Classical
unboundedness results rule out confinement to a finite region
[@bunimovich1992], yet unbounded motion need not have the period, drift, or
phase coherence of the standard highway. Complexity results sharpen the
obstruction: finite-support prediction already contains P-hard instances,
while universality and undecidability constructions use an infinite but
finitely described circuit background [@gajardo2002]. These input contracts
must be kept separate. Neither unboundedness nor universality supplies a
convergence theorem for arbitrary finite support.

This paper isolates the smallest translation-invariant nonblank family: states
with exactly one black cell, at an arbitrary displacement from an arbitrarily
posed ant. The family is infinite in two independent senses. There is no bound
on the defect coordinate, and a late defect can interact with an arbitrarily
long highway history. A simulation cutoff therefore cannot close the theorem.
Recent experiments reported one-black runs in a bounded radius-three domain
and substantial transients [@gajardo2024]; our task is to remove the spatial
cutoff by proving an all-depth reduction.

\begin{theorem}[Universal one-black theorem]\label{thm:main}
For every Langton-ant state $s$ on $\Z^2$, if the black set of $s$ is a
singleton, then there exists a time $N$ such that the observation sequence
from $\operatorname{run}(N,s)$ is permanently 104-periodic up to one of the
four quarter-turn rotations of the standard drift $(-2,-2)$.
\end{theorem}

The exact observation-level meaning of ``permanent period-104'' is given in
Definition~\ref{def:p104}. The proof is a scattering argument around a
certified blank-orbit boundary. After translation and rotation normalization,
let $q$ be the single black cell. The blank orbit reaches its highway entry
state $E$ after 9,977 updates, having read 1,376 distinct cells. If $q$ was
read, a finite witness settles the case. Otherwise a first-difference coupling
gives exactly $\operatorname{blacken}(q,E)$. The future P104 read set
decomposes all remaining $q$ into cells that are inert, finitely many
active-support cells, and 22 affine channels $q=h+dv$. This turns an unbounded
plane into 22 one-parameter scattering problems.

The decisive structure is a $21+1$ channel classification. In 21 ordinary
channels, translated XOR wakes become inert archives and all sufficiently deep
collisions reduce inductively to a single pristine anchor; a second geometric
coupling transfers this result through the 702-cell historical wake of $E$.
The exceptional channel creates an exact reverse highway with drift $(2,2)$,
travels back through the accumulated history, and hits the same historical
cell for every depth. Adding one unit of depth inserts one forward and one
reverse P104 block, so the hit time changes affinely by $208$ updates. A final
archive induction transfers one checked post-hit transient to every depth.

The proof is formalized in Lean 4 [@demoura2021]. Analytic proof terms handle
symmetry, coupling, affine geometry, recurrence, archive induction, and
universal assembly. Closed Boolean reports handle three finite leaves and are
reflected into typed certificates. They are evaluated using
\texttt{native\_decide}; according to the Lean reference, that mechanism uses
a dedicated axiom and relies on the native compiler and runtime
[@leanref2026]. We therefore call the result *Lean-checked*, not kernel-only.

The contributions are:

1. a proof of Theorem~\ref{thm:main} for every exactly-one-black state,
   without coordinate or time bounds;
2. a geometric reduction of all late defects to 22 unique affine frontier
   channels and an all-depth $21+1$ scattering classification;
3. an explicit analysis of the exceptional reverse-highway collision,
   including its affine hit law; and
4. a reproducible Lean artifact whose finite/native trust boundary is explicit
   and whose proof checking performs no generation-time search.

\begin{figure}[t]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
  node distance=5mm and 6mm,
  box/.style={draw,rounded corners,align=center,minimum height=8mm,
              text width=26mm,font=\scriptsize},
  arr/.style={-{Latex[length=1.8mm]},thick},
  split/.style={diamond,draw,aspect=2,align=center,font=\scriptsize,inner sep=1pt}
]
\node[box,draw=proofblue] (all) {arbitrary one-black state};
\node[box,draw=proofblue,right=of all] (canon) {canonical pose\\defect $q$};
\node[split,right=of canon] (prefix) {$q$ read before\\time 9,977?};
\node[box,draw=proofgreen,above right=6mm and 6mm of prefix] (finite) {1,376 prefix\\witnesses};
\node[box,draw=proofblue,below right=6mm and 6mm of prefix] (entry) {$\operatorname{blacken}(q,E)$\\entry geometry};
\node[box,draw=prooforange,right=of entry] (channels) {22 frontier\\channels};
\node[box,draw=proofpurple,above right=6mm and 6mm of channels] (ordinary) {21 ordinary\\inductions};
\node[box,draw=proofpurple,below right=6mm and 6mm of channels] (exceptional) {1 reverse\\collision family};
\node[box,draw=proofgreen,right=16mm of channels] (p104) {permanent\\P104};
\draw[arr] (all)--(canon); \draw[arr] (canon)--(prefix);
\draw[arr] (prefix)--node[above,sloped,font=\tiny]{yes}(finite);
\draw[arr] (prefix)--node[below,sloped,font=\tiny]{no}(entry);
\draw[arr] (entry)--(channels); \draw[arr] (channels)--(ordinary);
\draw[arr] (channels)--(exceptional); \draw[arr] (finite.east)-|(p104.north);
\draw[arr] (ordinary)--(p104); \draw[arr] (exceptional)--(p104);
\end{tikzpicture}
}
\caption{Proof architecture. Finite replay closes early contact; all unbounded
late-contact cases are discharged by channel induction.}
\label{fig:architecture}
\end{figure}

Sections 2--4 define the dynamics and reduce the plane to frontier channels.
Sections 5--7 prove pristine scattering, ordinary historical transfer, and the
exceptional family. Section 8 assembles the theorem. Section 9 describes the
formal artifact and checked computation. Sections 10 and 11 position and
summarize the result.

# Dynamics, symmetries, and the main theorem

## States and updates

Write a lattice point as $p=(x,y)\in\Z^2$. A state is

$$s=(b,p,d),\qquad b:\Z^2\to\{0,1\},\quad d\in\{N,E,S,W\}.$$

Here $b(x)=1$ denotes black. Let $R$ and $L$ be clockwise and
counterclockwise quarter turns, and let $e_d$ be the unit vector in heading
$d$. One update reads $c=b(p)$ and sets

$$
d'=\begin{cases}R(d),&c=0,\\L(d),&c=1,\end{cases}\qquad
b'=b\oplus\mathbf 1_{\{p\}},\qquad p'=p+e_{d'}.
$$

Thus turning and flipping occur before movement. This convention fixes every
reported time and coordinate. Write $\operatorname{step}(s)$ for this map and
$\operatorname{run}(n,s)$ for its $n$-fold iterate, with time zero equal to
the supplied state.

Define the local observation
$\operatorname{obs}(s)=(p(s),d(s),b_s(p(s)))$. For $u\in\Z^2$, translation
of an observation changes only its position component.

\begin{definition}[Permanent P104]\label{def:p104}
Let $v_0=(-2,-2)$ and let $D$ be its four quarter-turn rotations. A state $s$
has \emph{permanent P104} if some $v\in D$ satisfies, for every $k\ge0$ and
$0\le r<104$,
$$
\operatorname{obs}(\operatorname{run}(104k+r,s))
=kv+\operatorname{obs}(\operatorname{run}(r,s)).
$$
A state \emph{reaches P104} if $\operatorname{run}(N,s)$ has permanent P104
for some $N\ge0$.
\end{definition}

This is exactly the Lean predicate \texttt{PermanentP104};
\texttt{ReachesP104} existentially quantifies $N$. It fixes every later read,
turn, and translated ant position. It does not claim that inert cells
arbitrarily far behind the ant translate with the active pattern.

## Equivariance and canonical states

Translations and quarter-turn rotations act simultaneously on the grid,
position, and heading. Direct calculation gives

$$
\operatorname{step}(T_u s)=T_u\operatorname{step}(s),\qquad
\operatorname{step}(\rho s)=\rho\operatorname{step}(s),
$$

and hence the same identities for every iterate. Both actions preserve
\texttt{ReachesP104}; a rotation merely rotates the standard drift.

\begin{lemma}[Pose normalization]\label{lem:normalize}
Every state with exactly one black cell is a translation and a quarter-turn
rotation of a state $\sigma_q$ whose ant is at the origin, points north, and
whose unique black cell is $q\in\Z^2$.
\end{lemma}

Consequently Theorem~\ref{thm:main} reduces to proving
$\operatorname{ReachesP104}(\sigma_q)$ for every $q\in\Z^2$.

## The certified blank boundary

Let $\omega$ be the all-white canonical state. Exact replay supplies the
following data.

\begin{proposition}[Blank highway boundary]\label{prop:blank}
At time $T=9{,}977$, the blank orbit is in a state $E$ whose ant is at
$(-15,10)$ heading west. The next 104 updates read a support $S$ of 40
distinct cells, restore the heading, and translate the local observation by
$v=(-2,-2)$. Thirteen cells form the active black pattern. The state $E$ has
715 black cells in total: 13 active cells and a 702-cell historical wake.
Moreover, the 104-step block iterates permanently.
\end{proposition}

The last sentence is not inferred from observing several repeated blocks. A
finite XOR comparison between one block and its translate produces a wake
$W$; affine ray checks prove that all later translated read supports avoid all
archived copies of $W$. Induction then proves
Definition~\ref{def:p104} for every future cycle.

# The finite prefix and first-contact coupling

Let $P=\{p(\operatorname{run}(t,\omega)):0\le t<T\}$ be the set of cells read
before the blank highway boundary. Deduplication of the exact trace gives
$|P|=1{,}376$.

## Prefix contacts

If $q\in P$, the orbit of $\sigma_q$ first differs from the blank orbit within
the finite prefix. For each possible cell, the checked table stores a terminal
witness time and exact replay verifies that the resulting state reaches a
certified P104 boundary.

\begin{proposition}[Prefix certificate]\label{prop:prefix}
For every $q\in P$, $\sigma_q$ reaches P104.
\end{proposition}

Completeness follows from equality between the stored deduplicated list and
the read set of the first $T$ updates, rather than from a bounding box.

## Untouched defects

For a point $q$, say that an orbit avoids $q$ for $n$ steps when its current
position differs from $q$ at every time $0,\ldots,n-1$. Two states are the
same except at $q$ when their poses agree, all other colours agree, and their
colours at $q$ are opposite.

\begin{lemma}[First-difference coupling]\label{lem:coupling}
If states $a$ and $b$ are the same except at $q$, and the orbit of $a$ avoids
$q$ for $n$ steps, then $\operatorname{run}(n,a)$ and
$\operatorname{run}(n,b)$ remain the same except at $q$.
\end{lemma}

The proof is induction on $n$. Away from $q$ the two ants read the same colour,
make the same turn, flip the same cell, and move together. Since the initial
white state and $\sigma_q$ differ only at $q$, this gives an exact state
identity.

\begin{corollary}[Untouched entry]\label{cor:entry}
If $q\notin P$, then
$$\operatorname{run}(T,\sigma_q)=\operatorname{blacken}(q,E).$$
\end{corollary}

# Entry geometry and the 22 frontier channels

The future clean highway reads exactly $S,S+v,S+2v,\ldots$. A defect untouched
by the prefix can matter only if it lies in their union. Define

$$H=\{h\in S:h+v\notin S\},\qquad
\operatorname{obstacle}(h,d)=h+dv\quad(d\ge1).$$

The sign is important: depth increases in the forward drift direction.
Checked diagonal, parity, and order conditions on the 40 points of $S$ give an
exhaustive decomposition.

\begin{proposition}[Entry partition]\label{prop:partition}
For every $q\notin P$, an ordered case split gives one of the following:

1. $q$ is already black in $E$, so blackening changes nothing;
2. $q$ is one of the 27 white cells in the 40-cell active support, handled by
   finite replay;
3. $q\notin\bigcup_{k\ge0}(S+kv)$, so the blank highway never reads it; or
4. there are unique $h\in H$ and $d\ge1$ with $q=h+dv$.

Furthermore, $|H|=22$.
\end{proposition}

The raw predicates need not be pairwise disjoint before earlier branches are
removed; the formal theorem uses the stated order. Uniqueness of $(h,d)$ in
the infinite remainder replaces two unrestricted coordinates by a 22-element
index and one positive natural number. For $h\in H$ and $d\ge1$, define

$$\Sigma_E(h,d)=\operatorname{blacken}(h+dv,E).$$

It remains to prove that every $\Sigma_E(h,d)$ reaches P104.

# Pristine single-defect scattering

The physical state $E$ contains both the active P104 pattern and the entire
blank-orbit wake. It is useful first to remove the history and study a pristine
boundary state $B$ containing only the 13-cell active pattern with the same
pose. Put

$$\Sigma_B(h,d)=\operatorname{blacken}(h+dv,B).$$

For each head $h$, the finite certificate supplies a positive stable depth
$P_h$ and a witness time at depth $P_h$. Depths $1\le d<P_h$ are direct
replays. The stable case is extended by a generic archive theorem.

## XOR archives

For Boolean grids, finite changes compose by exclusive-or. Let $W$ be the
finite difference between one clean 104-step block and its translated target.
If the obstacle is moved one additional period down a channel, the ant first
executes one additional clean block and deposits one additional translated
copy of $W$. After $n$ clean blocks the difference has the form

$$
\mathcal A_n(W)=W\oplus(W+v)\oplus\cdots\oplus(W+(n-1)v).
\tag{1}\label{eq:archive}
$$

Cancellation is retained in this expression; it is not replaced by a set
union. The proof relates XOR algebra to orbit equality through a
\emph{same-outside} relation: two grids may differ on an archive, but generate
identical updates while the common ant path avoids it.

\begin{lemma}[Archive induction]\label{lem:archive}
Fix a clean state, drift $v$, obstacle anchor, period, anchored scattering
trace, wake $W$, and terminal P104 corridor. Suppose that:

1. the clean block is exact up to $W$;
2. all translated clean and anchored read sets avoid the relevant copies of
   $W$; and
3. the accumulated archive avoids the translated infinite terminal corridor.

Then the depth-$P+n$ scattering state reaches the translated anchored terminal
state for every $n\ge0$, up to the inert archive $\mathcal A_n(W)$, and hence
reaches P104.
\end{lemma}

The Lean proof packages the three assumptions as
\texttt{Induction.Data}. It first proves an exact normal form for the finite
trace and then uses untouched-region coupling for the infinite corridor. The
separation premises are discharged by exact affine-ray predicates rather than
by testing a fixed number of copies.

## All-depth pristine classification

For every head, the certificate checks the nonempty direct row, the stable
replay, its deduplicated read set, terminal orientation, and the ray guards
required by Lemma~\ref{lem:archive}. There are 152 pristine replay
witnesses in total, including one stable witness per channel.

\begin{proposition}[Pristine scattering]\label{prop:pristine}
For all $h\in H$ and $d\ge1$, the pristine state $\Sigma_B(h,d)$ reaches P104.
For 21 heads the stable output has the forward standard drift. For the
remaining head $h_{72}$, the stable output has reverse drift $-v=(2,2)$.
\end{proposition}

The subscript records the phase label used by the artifact, not a count. Its
coordinate relative to the pristine base pose is

$$h_{72}=p(B)+(-2,-8),\qquad P_{h_{72}}=11.$$

At this stage the reverse highway is already a valid P104 terminal state. The
difficulty appears only when the removed history is restored: the reverse ant
eventually travels toward that history rather than away from it.

# Restoring the physical history: 21 ordinary channels

Write

$$H_E=\{x:E(x)=1,\ x\notin S\}.$$

The exact entry certificate gives $|H_E|=702$. For an ordinary head $h$, let
$A_h$ be one plus the length of its checked physical direct row. The
certificate verifies $P_h\le A_h$. Thus

$$1\le d<A_h$$

is a finite direct band, while $d=A_h+n$ is the inductive region. The offset
$L_h=A_h-P_h$ aligns physical depth $A_h+n$ with pristine depth $P_h+L_h+n$.

The cutoff is channel-specific. It is chosen so that the translated pristine
scattering footprint and its eventual terminal corridor are separated from
every historical cell. The finite report checks the base guards for each
historical cell and each ordinary stable snapshot; ray lemmas extend those
guards to all deeper translations.

\begin{lemma}[Historical transfer]\label{lem:history}
Let $h$ be ordinary and $n\ge0$. Up to the historical region $H_E$, the orbit
from $\Sigma_E(h,A_h+n)$ agrees with the corresponding pristine orbit at depth
$P_h+L_h+n$. The common path avoids $H_E$ through the scattering trace and
through its permanent terminal corridor.
\end{lemma}

The key point is temporal as well as spatial. A finite check shows separation
from the anchored trace; the affine guard shows that translating the obstacle
farther cannot bring a historical cell into any new trace copy or output ray.
Untouched-region coupling then turns geometric nonintersection into exact
equality of observations.

\begin{proposition}[Ordinary physical channels]\label{prop:ordinary}
For each of the 21 ordinary heads $h$ and every $d\ge1$,
$\Sigma_E(h,d)$ reaches P104.
\end{proposition}

For $d<A_h$ this is the physical replay table. For $d\ge A_h$, write
$d=A_h+n$, apply Lemma~\ref{lem:history}, and invoke pristine archive
induction at parameter $L_h+n$. The generated physical rows contain 179 replay
witnesses across all 22 channels; the exceptional row is used separately
below.

# Exceptional backscattering and the affine hit law

For the exceptional head, the pristine stable depth is 11 but the physical
base depth is

$$P_{h_{72}}=11,qquad A_{h_{72}}=15,qquad A_{h_{72}}-P_{h_{72}}=4.$$

Depths 1 through 14 are direct physical cases. At depth 15, four clean forward
translations carry the physical state into the affine reverse family.

## The exact reverse block

Let $R$ be the reverse base state obtained after the checked pristine
scattering time of 52,262 updates. Let $v_r=-v=(2,2)$, and let $W_r$ be the
finite difference between one reverse block and the translated state. The
certificate and its soundness theorem establish

$$
\operatorname{run}(104,R)=T_{v_r}R\oplus W_r.
\tag{2}\label{eq:reverse}
$$

Positive-copy ray guards show that $W_r$ begins affecting the representation
only at the next translated copy and is never read by any later reverse block.
Equation~\ref{eq:reverse} therefore iterates indefinitely in the
pristine setting.

## First historical collision

With the historical wake restored, the reverse path eventually meets a cell
that the blank transient had changed. The checked first-hit report proves that
the base reverse trajectory avoids all 702 historical cells for ten complete
reverse cycles and phases 0 through 88 of the next cycle, then reaches

$$c=(20,-22)$$

at phase 89. Thus the elapsed reverse time is
$10\cdot104+89=1{,}129$ updates. The report separately verifies $c\in H_E$;
the phrase ``historical hit'' is not inferred merely from the coordinate.

Increasing physical obstacle depth from $15+n$ to $15+(n+1)$ inserts one
forward block before reversal and one reverse block before the collision. The
remaining phase and collision cell are unchanged. Consequently

$$t_{\mathrm{hit}}(n)=t_{\mathrm{hit}}(0)+208n.
\tag{3}\label{eq:hitlaw}
$$

More strongly, there is a finite XOR layer $L$ and a checked collision state
$C$ such that

$$
\operatorname{run}(t_{\mathrm{hit}}(n),\Sigma_E(h_{72},15+n))
=C\oplus\bigoplus_{j=0}^{n-1}(L+jv).
\tag{4}\label{eq:hitnormal}
$$

Equation~\ref{eq:hitnormal}, formalized as
\texttt{Scattering.Classification.exceptionalAffine}, is the normal form that
closes the infinite family. It says more than equal collision coordinates:
the complete state at collision is fixed modulo an explicit translated
archive.

\begin{figure}[t]
\centering
\begin{tikzpicture}[x=0.78cm,y=0.78cm,
  arr/.style={-{Latex[length=2mm]},very thick},
  lab/.style={font=\small,fill=white,inner sep=1.5pt}]
\draw[step=0.5cm,gray!18,very thin] (-6,-2.5) grid (6,3);
\draw[arr,proofblue] (-5,-1.6)--(-1.2,2.2)
  node[midway,lab,sloped]{forward P104, $v$};
\draw[arr,proofpurple] (-0.9,2.2)--(4.4,-1.6)
  node[midway,lab,sloped]{reverse P104, $-v$};
\fill[prooforange] (4.4,-1.6) circle (2.2pt);
\node[lab,anchor=west] at (4.55,-1.6) {fixed hit $c$};
\draw[prooforange,densely dotted,thick] (3.8,-2.1)--(5.1,-0.8);
\node[lab,prooforange] at (4.4,-2.25) {historical wake};
\draw[<->,proofgreen,thick] (-4.7,-2.15)--(-1.4,1.15)
  node[midway,lab,sloped,below] {$n$ added blocks};
\end{tikzpicture}
\caption{Exceptional mechanism. One added depth contributes one forward and
one reverse 104-step block before the same historical collision.}
\label{fig:exceptional}
\end{figure}

## The post-hit tail

From $C$, exact replay for 7,994 updates reaches a forward P104 terminal state.
The checked post-hit trace guard proves that every layer in
Equation~\ref{eq:hitnormal} avoids this finite replay. A second forward
ray guard proves that every layer also avoids the infinite terminal corridor.
Archive induction therefore transfers the depth-15 computation to all
$15+n$.

\begin{proposition}[Exceptional physical channel]\label{prop:exceptional}
For every $d\ge1$, $\Sigma_E(h_{72},d)$ reaches P104.
\end{proposition}

The finite band proves $1\le d<15$; the reverse-block, first-hit,
post-hit, and archive lemmas prove $d=15+n$. Together with
Proposition~\ref{prop:ordinary}, this is the complete single-defect
scattering spectrum.

# Universal assembly

We can now prove the main theorem without any remaining search bound.

\begin{proof}[Proof of Theorem \ref{thm:main}]
Apply Lemma~\ref{lem:normalize} and use translation and rotation
equivariance to reduce to $\sigma_q$. If $q\in P$, apply the prefix certificate,
Proposition~\ref{prop:prefix}. Otherwise Corollary~\ref{cor:entry}
identifies the time-9,977 state with $\operatorname{blacken}(q,E)$. Apply the
entry partition, Proposition~\ref{prop:partition}. The already-black branch
is the blank highway; active-support cells are finite checked cases; a
geometrically separated cell is never read by the permanent blank highway. In
the remaining branch, write uniquely $q=h+dv$ with $h\in H$ and $d\ge1$. If
$h$ is ordinary, apply Proposition~\ref{prop:ordinary}; if
$h=h_{72}$, apply Proposition~\ref{prop:exceptional}. Every branch reaches
P104, and equivariance restores the original pose.
\end{proof}

In Lean, the same assembly is exposed at three levels. The theorem
\texttt{Scattering.single\_defect\_scattering} constructs the $21+1$
classification. The entry theorem combines that classification with the
geometric partition. Finally the exported statement is literally

```lean
theorem OneBlack.universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s
```

# Lean formalization and finite computation

## Proof cone

The artifact is implemented in Lean 4.30.0 and is organized so that the final
theorem imports two reflected certificate leaves through a small verification
boundary. The mathematical proof cone contains 42 Lean source files (the root
module plus 41 modules under \texttt{OneBlack/}), totalling 5,424 lines in the
current revision. Table~\ref{tab:modules} maps the mathematical stages to
their principal modules.

| Mathematical obligation | Principal Lean modules |
|---|---|
| Dynamics, observations, symmetries | `Core`, `Semantics` |
| Blank P104 replay and induction | `HighwayData`, `Highway` |
| First-contact coupling and prefix | `Coupling`, `Prefix`, `PrefixLeaf` |
| Entry partition and affine channels | `Geometry`, `Rays`, `Entry` |
| Pristine archive induction | `Induction`, `PristineChecks`, `Pristine` |
| Physical ordinary channels | `ActualChecks`, `ActualHistory`, `OrdinaryGeometry`, `Ordinary` |
| Exceptional reverse family | the `Phase*` modules |
| Spectrum and universal theorem | `Scattering`, `Universal` |

: Proof-to-module map. \label{tab:modules}

## Finite leaves

The complete build has three native computation leaves.

1. **Blank leaf.** It replays 9,977 blank updates, checks the 104-step boundary,
   and validates the finite separation data used by the permanent highway
   induction.
2. **Prefix leaf.** It checks all 1,376 first-contact cells against stored
   terminal witness times.
3. **Scattering leaf.** It checks the 27 active-support cases, direct pristine
   and physical channel rows, one stable pristine snapshot per head, ordinary
   historical guards, and the exceptional reverse, first-hit, post-hit, and
   layer guards.

The lane tables contain 152 pristine replay witnesses and 179 physical-entry
replay witnesses. Their stored witness times total 1,380,384 and 2,761,211
updates, respectively. These totals describe finite certificate work, not a
uniform upper bound on the theorem's eventual-entry time. Deeper channel
members are discharged analytically.

Each stable snapshot computes its terminal state, deduplicated read set,
cached read list, terminal orientation, and acceptance result once. Multiple
proof guards consume the same values. Witness generation may originally have
searched for terminal times, but verification uses the checked-in times and
performs direct replay only; no search procedure is trusted by the theorem.

## Reflection and trust boundary

The Boolean reports are not accepted as untyped assertions. Each report has a
soundness theorem of the form

```lean
theorem certificate_of_report (verified : report = true) : Certificate
```

and the typed certificates feed the analytic theorems. The closed equalities
\texttt{report = true} are discharged with \texttt{native\_decide}. This design
makes the finite obligations inspectable and reproducible, but it has a larger
trusted computing base than reduction inside Lean's kernel. In current Lean,
native decision uses a dedicated axiom and trusts the compiler, runtime,
code-generation backend, and any externally linked native code
[@leanref2026]. There is no external oracle or generated theorem statement in
the final build, but ``axiom-free'' and ``kernel-only'' would be inaccurate
descriptions.

## Reproduction

The repository [@hao2026artifact] pins `leanprover/lean4:v4.30.0`. From its
root, the complete theorem is rebuilt with

```console
python3 one_black/check.py
```

The command validates generated-data consistency and builds the closed theorem
from checked-in sources and witness tables. The interactive website is an
explanatory companion; it is not an input to the proof.

# Related work and scope

## Classical ant dynamics

Langton introduced the model in the context of artificial life and reported
the emergence of organized motion from simple local rules [@langton1986].
Bunimovich and Troubetzkoy proved recurrence and unboundedness results for the
associated Lorentz lattice-gas dynamics [@bunimovich1992]. Unboundedness is a
qualitatively weaker conclusion than Theorem~\ref{thm:main}: it excludes
finite confinement but neither selects the period-104 orbit nor gives a time
after which translated phase equality holds. Gale, Propp, Sutherland, and
Troubetzkoy studied further ant rules and symmetry phenomena [@gale1995].

## Complexity and generalized highways

Gajardo, Moreira, and Goles embedded Boolean-circuit computation in finite
configurations and obtained P-hardness; their universality and undecidability
construction uses an infinite, finitely described trapezoidal circuit array
[@gajardo2002]. Their circuit construction can route an ant to a highway seed,
so the present work should not be advertised as the first infinite family ever
known to reach a highway. Its distinction is instead the exhaustive natural
family defined solely by ``exactly one black cell'', with arbitrary relative
position.

For generalized reversible ants, recognition of repeatable configurations can
be PSPACE-hard [@tsukiji2011]. Recent work shows that generalized rules may
possess unboundedly or infinitely many distinct highways [@gajardo2024], and
may also exhibit qualitatively different finite-configuration asymptotics
[@lutfalla2025]. These results motivate separating the theorem's classical LR
rule and exact P104 predicate from broader claims about generalized ants.

## Claim boundary

Our primary-source audit did not find an earlier theorem covering every
classical exactly-one-black state with arbitrary pose. This is a report about
the audited literature, not a mathematical priority theorem, so the manuscript
does not use ``first'' in its title, abstract, or contribution list. The
general finite-support Highway Conjecture also remains outside our result.
Nothing here proves convergence for two black cells, for an arbitrary finite
black set, or for arbitrary generalized rule words.

The proof architecture may nevertheless be reusable. It separates a finite
baseline transient from a translated renewal boundary, classifies the
first-contact frontier into affine channels, and promotes finite anchors with
geometric archive guards. In the exceptional channel, a reverse renewal orbit
and an affine collision law replace a failed one-direction coupling. These are
structural mechanisms rather than larger simulations, but their applicability
to other support sizes remains an open question.

# Conclusion

Every classical Langton-ant state with exactly one black cell reaches the
standard period-104 highway, in the precise observation-level sense of
Definition~\ref{def:p104}. The proof has no coordinate cutoff. It reduces
the 1,376 early-contact cells to finite replay and every later relevant cell to
one of 22 affine channels. Twenty-one channels become insensitive to the
blank-orbit history after channel-specific cutoffs. The remaining channel
creates a reverse highway, returns to a fixed historical cell with the affine
law $t_{\mathrm{hit}}(n)=t_{\mathrm{hit}}(0)+208n$, and then enters forward
P104 through an archived post-hit tail.

The Lean development checks both the infinite reductions and the completeness
of the case split. Its three finite leaves are evaluated natively, with the
corresponding compiler/runtime trust boundary stated explicitly. This result
does not settle the finite-support Highway Conjecture, but it provides a
fully quantified test case in which an unbounded perturbation family is closed
by scattering geometry and induction rather than by extending a simulation
window.

The next mathematical question is whether the frontier-channel method survives
multiple defects. A second defect introduces interactions between independent
contact times and between accumulated wakes, so a successful extension will
likely require a compositional renewal invariant rather than a larger table.

\clearpage
\appendix

# Certificate inventory

Table~\ref{tab:inventory} collects numerical constants used in the proof.
Every value is asserted by a checked report or derived from a checked list;
none is a parameter of the theorem statement.

| Quantity | Value | Role |
|---|---:|---|
| Blank boundary time | 9,977 | start of certified P104 |
| Distinct prefix read cells | 1,376 | complete early-contact branch |
| P104 period and drift | 104; $(-2,-2)$ | standard highway convention |
| One-period support | 40 | entry geometry |
| Active white support cells | 27 | finite entry cases |
| Entry black cells | 715 | active pattern plus history |
| Historical cells | 702 | physical-history guards |
| Frontier heads | 22 | all unbounded future contacts |
| Ordinary / exceptional heads | 21 / 1 | scattering classification |
| Exceptional pristine / physical depth | 11 / 15 | reverse-family anchors |
| Exceptional reverse scattering time | 52,262 | exact pristine anchor replay |
| Reverse first-hit elapsed time | 1,129 | $10\cdot104+89$ |
| Historical hit point | $(20,-22)$ | depth-independent collision |
| Post-hit replay | 7,994 | terminal forward P104 witness |
| Pristine / physical replay witnesses | 152 / 179 | finite scattering leaves |

: Checked certificate inventory. \label{tab:inventory}

# References

::: {#refs}
:::
