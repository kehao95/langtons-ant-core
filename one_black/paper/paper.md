---
title: "Every One-Black-Cell Langton Ant Reaches the Period-104 Highway: A Lean-Checked Proof"
author: |
  \begin{tabular}{c}
  Hao Ke\\
  Independent researcher\\
  \href{mailto:i@kehao.me}{\texttt{i@kehao.me}}
  \end{tabular}
author-meta: "Hao Ke"
date: ""
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
    \usepackage{booktabs,array,longtable,microtype,xcolor,tikz,graphicx,pdflscape}
    \usetikzlibrary{arrows.meta,positioning,shapes.geometric,decorations.pathreplacing}
    \definecolor{proofblue}{HTML}{28678D}
    \definecolor{proofgreen}{HTML}{2F855A}
    \definecolor{prooforange}{HTML}{C76B29}
    \definecolor{proofpurple}{HTML}{7355A3}
    \definecolor{proofred}{HTML}{C94F4F}
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
We prove that every classical Langton-ant state with exactly one black cell,
at any displacement and ant pose, eventually follows the complete standard
period-104 highway trace up to translation and quarter-turn rotation. The
proof couples the perturbed orbit to the finite blank-orbit transient and
reduces the unbounded part of the scattering problem to 22 affine frontier
channels.
Moving a defect farther down a channel accumulates translated changes to the
cell colours, allowing finite base simulations to extend by induction to every depth. Twenty-one
channels admit geometric separation from the blank orbit's historical wake.
The remaining channel creates a reverse highway that returns to a fixed
historical cell; an affine collision-time law and a second archive induction
then establish entry into the forward highway. The infinite reductions,
geometric guards and certificate-soundness theorems are formalized in Lean 4,
with three finite reports evaluated using \texttt{native\_decide}.
The accompanying artifact supplies the proof sources, witness tables and
reproduction commands.
\end{abstract}

\clearpage
\tableofcontents
\clearpage

# Introduction

Langton's ant is among the simplest deterministic systems in which a short
local rule produces a long irregular transient followed by rigid macroscopic
motion [@langton1986]. A cell of the square lattice is white or black. On each update the ant
reads its current cell, turns right on white and left on black, flips that
cell, and advances one lattice edge. From the all-white plane, the orbit is
observed to settle into a diagonal highway: every 104 updates the same local
behaviour recurs, translated by two cells in each coordinate [@gajardo2024, §1]. That source uses white-left/black-right;
reflection gives the white-right/black-left convention used here.
The central question is which finite perturbations provably enter this
permanent regime.

The general finite-support Highway Conjecture remains unresolved. Classical
unboundedness results rule out confinement to a finite region
(see the accessible corner proof in [@gajardo2024, §2]), yet unbounded motion need not have the period, drift, or
phase coherence of the standard highway. Complexity results sharpen the
obstruction: finite-support prediction already contains P-hard instances,
while universality and undecidability constructions use an infinite but
finitely described circuit background [@gajardo2002]. These input contracts
define complementary questions about spatial escape, computation and eventual
highway convergence.

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
singleton, then there exists a time $N$ such that its entire sequence of
positions, headings and read colours from update $N$ onward agrees with a
translation and quarter-turn rotation of the all-white orbit from update
9,977 onward.
In particular, this is the fixed standard period-104 read trace with a
quarter-turn rotation of drift $(-2,-2)$.
\end{theorem}

The exact observation-level meaning of ``permanent period-104'' is given in
Definition \ref{def:p104}. The proof is a scattering argument around a
certified blank-orbit boundary. After translation and rotation normalization,
let $q$ be the single black cell and $E$ the blank highway entry state.
If the blank transient reads $q$, a finite witness settles the case.
Otherwise a first-difference coupling
gives exactly $\operatorname{blacken}(q,E)$, where blackening forces $q$ black
and leaves every other cell and the ant pose unchanged. The future P104 read set
decomposes all remaining $q$ into cells that are inert, finitely many
active-support cells, and 22 affine channels $q=h+dv$. This turns an unbounded
plane into 22 one-parameter scattering problems.

The decisive structure is a $21+1$ channel classification. In 21 ordinary
channels, translated XOR wakes become inert archives and all sufficiently deep
collisions reduce inductively to a single pristine anchor; a second geometric
coupling transfers this result through the finite historical wake of $E$.
The exceptional channel creates an exact reverse highway with drift $(2,2)$,
travels back through the accumulated history, and hits the same historical
cell for every depth. Adding one unit of depth inserts one forward and one
reverse P104 block, so the hit time changes affinely by $208$ updates. A final
archive induction transfers one checked post-hit transient to every depth.

The proof is formalized in Lean 4 [@demoura2021]. Analytic proof terms handle
symmetry, coupling, affine geometry, recurrence, archive induction, and
universal assembly. Closed Boolean reports handle three finite leaves and are
reflected into typed certificates. They are evaluated using
\texttt{native\_decide}; as documented by the pinned Lean source, that mechanism uses
a dedicated axiom and relies on the native compiler and runtime
[@leanref2026]. Section \ref{sec:lean} records the proof components and their dependencies.

The contributions are:

1. a proof of Theorem \ref{thm:main} for every exactly-one-black state,
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
formal artifact and checked computation. Section 10 positions the result, Section 11 states limitations, and Section 12
summarizes the result.

# Dynamics, symmetries, and the main theorem

## States and updates

Write a lattice point as $p=(x,y)\in\Z^2$. A state is

$$s=(b,p,d),\qquad b:\Z^2\to\{0,1\},\quad d\in\{N,E,S,W\}.$$

Here $b(x)=1$ denotes black. Let $R$ and $L$ be clockwise and
counterclockwise quarter turns, and let $e_d$ be the unit vector in heading
$d$, with $e_N=(0,1)$, $e_E=(1,0)$, $e_S=(0,-1)$ and
$e_W=(-1,0)$. Define the canonical all-white state
$\omega=(\mathbf 0,(0,0),N)$. One update reads $c=b(p)$ and sets

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
In addition its first 104 read colours must equal the fixed word
$$
w_r=b_{\operatorname{run}(9977+r,\omega)}
       (p(\operatorname{run}(9977+r,\omega))),\qquad 0\le r<104.
$$
A state \emph{reaches P104} if $\operatorname{run}(N,s)$ has permanent P104
for some $N\ge0$.
\end{definition}

This is exactly the Lean predicate \texttt{PermanentP104};
\texttt{ReachesP104} existentially quantifies $N$. It fixes every later read,
turn, and translated ant position while allowing inert historical cells
outside the future read trace.

Every accepting terminal certificate couples to the fixed blank boundary,
so the fixed-word clause propagates through the scattering proof. The module
\texttt{StandardTrace} further proves full future observation equality with
a placement of the actual blank state at update 9,977: periodicity extends
the fixed first word to all times, equality of read colours and aligned
initial poses determines the same positions and headings inductively.
For this bridge, choose the quarter-turn rotation of the blank template that
aligns its initial heading with that of the terminal state, then translate
to align its position. Rotation and translation preserve the read-colour word.

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

Consequently Theorem \ref{thm:main} reduces to proving
$\operatorname{ReachesP104}(\sigma_q)$ for every $q\in\Z^2$.

## The certified blank boundary

Starting from the canonical all-white state $\omega$, exact replay supplies the
following data.

\begin{proposition}[Blank highway boundary]\label{prop:blank}
At time $T=9{,}977$, the blank orbit is in a state $E$ whose ant is at
$(-15,10)$ heading west. The next 104 updates read a support $S$ of 40
distinct cells, restore the heading, and translate the local observation by
$v=(-2,-2)$. Of the 40 cells in $S$, 13 are black in $E$ (the active black pattern)
and 27 are white. Outside $S$, there are 702 black cells, the historical wake.
Thus $E$ has 715 black cells in total.
Moreover, the 104-step block iterates permanently.
\end{proposition}

For a state $s$, write $\mathcal B(s)$ for its black set. The finite difference
$W_E=\mathcal B(\operatorname{run}(104,E))\mathbin{\triangle}\mathcal B(T_vE)$
compares one block with its translate. Affine ray checks show that all later
translated read supports avoid every archived copy of $W_E$. Induction then proves
Definition \ref{def:p104} for every future cycle.

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
the read set of the first $T$ updates.

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

Figure \ref{fig:prefix-dichotomy} displays the first-contact split established
by the read-set equality and coupling statement above.

\begin{figure}[p]
\centering
\includegraphics[width=.70\linewidth]{figures/stages/stage-01-untouched.png}

\smallskip
{\small\textbf{(a) Untouched placements.}}

\medskip
\includegraphics[width=.70\linewidth]{figures/stages/stage-02-prefix.png}

\smallskip
{\small\textbf{(b) Prefix-hit placements.}}
\caption{The finite-prefix dichotomy, exported from Stages 01 and 02 of the
interactive app. In (a), gray is the blank-orbit read footprint and blue is
its complement in the displayed window; the diagonal arrow indicates that the
gray P104 corridor continues indefinitely. In (b), the 1,376 blue cells are
exactly the deduplicated prefix set $P$, while gray shows the subsequent P104
corridor. The red outline marks the canonical time-zero ant position.}
\label{fig:prefix-dichotomy}
\end{figure}

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

\begin{enumerate}
\item $q$ is already black in $E$, so blackening changes nothing;
\item $q$ is one of the 27 white cells in the 40-cell active support, handled by
   finite replay;
\item $q\notin\bigcup_{k\ge0}(S+kv)$, so the blank highway never reads it; or
\item there are unique $h\in H$ and $d\ge1$ with $q=h+dv$.
\end{enumerate}

Furthermore, $|H|=22$.
\end{proposition}

All black cells of $E$ lie in $P$, since the blank prefix created them.
Thus Branch 1 is empty under $q\notin P$; the four-way partition also
applies to a general defect at the entry state, as in the formal proof.
Branches 1--3 already reach P104: Branch 1 leaves $E$ unchanged;
Branch 2 has the 27 checked replays; and Branch 3 follows the blank highway
by untouched-region coupling since its future reads are
$\bigcup_{k\ge0}(S+kv)$. For uniqueness in Branch 4, the checked heads have
distinct pairs $(h_x-h_y,h_x\bmod2)$. These invariants are constant along a
$v=(-2,-2)$ ray, so a point cannot lie on two head rays; a fixed head and point
then determine the depth uniquely. The heads occupy 11 diagonal lines, with
two parity classes per line.

The raw predicates need not be pairwise disjoint before earlier branches are
removed; the formal theorem uses the stated order. Uniqueness of $(h,d)$ in
the infinite remainder replaces two unrestricted coordinates by a 22-element
index and one positive natural number. For $h\in H$ and $d\ge1$, define

$$\Sigma_E(h,d)=\operatorname{blacken}(h+dv,E).$$

It remains to prove that every $\Sigma_E(h,d)$ reaches P104.

# Pristine single-defect scattering

To extend a finite scattering calculation to arbitrary depth, we first
separate the repeating highway mechanism from the fixed blank-orbit history.
The physical state $E$ contains both. Its pristine counterpart $B$ retains
the 13-cell active pattern and the same ant pose, with the remaining plane
white. In this setting, an extra clean highway block contributes a translated
XOR wake, which can be tracked uniformly as the defect moves down a channel.
This gives the archive induction below. The following two sections restore
the physical history, using geometric separation for the ordinary channels
and an explicit return-collision analysis for the exceptional channel. Put

$$\Sigma_B(h,d)=\operatorname{blacken}(h+dv,B).$$

For each head $h$, the finite certificate supplies a positive stable depth
$P_h$ and a witness time at depth $P_h$. Depths $1\le d<P_h$ are direct
replays. The stable case is extended by a generic archive theorem.

## XOR archives

The coupling principle is local: two states with the same pose generate the
same observations as long as their common path avoids the cells on which
their grids differ. We express agreement outside a set by the
\emph{same-outside} relation and prove avoidance separately using the read
sets. Thus a growing archive of differences can be carried through an
induction while the ant continues along the same path.

Boolean changes compose by exclusive-or, with cancellation on overlaps.
The induction uses only a union support envelope, not an exact XOR identity.
Write $\tau_v=T_v$ for translation by $v$, and $S\equiv_A S'$ for equal ant
poses and grid agreement outside $A$. Let $\operatorname{reads}(S,r)$ denote
the cells read at updates $0\le k<r$ and $\operatorname{futureReads}(S)$
all future read cells, including update zero.

\begin{lemma}[Archive induction]\label{lem:archive}
Fix a clean state $B$, drift $v$, obstacle anchor $a$, natural numbers $m,t$,
and regions $C,F,W,K$. Put
\[
L_n=\operatorname{blacken}(a+nv,B),\qquad Q=\operatorname{run}(t,L_0),
\]
and define
\[
D_0=F,\quad D_{n+1}=C\cup\tau_vD_n,\qquad
A_0=\varnothing,\quad A_{n+1}=W\cup\tau_vA_n.
\tag{1}\label{eq:archive}
\]
Assume the following seven conditions:

\begin{enumerate}
\item $\operatorname{reads}(B,m)=C$;
\item $\operatorname{run}(m,B)\equiv_W\tau_vB$;
\item $\operatorname{reads}(L_0,t)=F$;
\item $a+(n+1)v\notin C$ for every $n\ge0$;
\item $W\cap\tau_vD_n=\varnothing$ for every $n\ge0$;
\item $\operatorname{futureReads}(Q)\subseteq K$; and
\item $A_n\cap\tau_v^nK=\varnothing$ for every $n\ge0$.
\end{enumerate}

Then for every $n\ge0$,
\[
\operatorname{reads}(L_n,nm+t)=D_n,\qquad
\operatorname{run}(nm+t,L_n)\equiv_{A_n}\tau_v^nQ.
\]
If additionally $Q$ is permanent P104, every $L_n$ reaches P104 at time $nm+t$.
\end{lemma}

\begin{proof}
Condition 4 and untouched-region coupling show that the first $m$ reads of
$L_{n+1}$ are exactly $C$. Blackening commutes with translation. Applying
condition 2 with the same forced-black cell on both sides gives
\[
\operatorname{run}(m,L_{n+1})\equiv_W\tau_vL_n.
\]
At $n=0$, condition 3 gives the read set and $A_0=\varnothing$ gives the
terminal identity. Inductively the translated depth-$n$ trace reads exactly
$\tau_vD_n$. Condition 5 permits coupling through the $W$ discrepancy.
Composing its terminal discrepancy with the translated inductive discrepancy
bounds their support by $W\cup\tau_vA_n=A_{n+1}$. The full read set is
$C\cup\tau_vD_n=D_{n+1}$ and its duration is
$m+(nm+t)=(n+1)m+t$. Conditions 6 and 7 then make every future read of
$\tau_v^nQ$ avoid $A_n$. Coupling transfers its permanent P104 observations.
\end{proof}

The seven premises are exactly the fields of \texttt{Induction.Data}.
The normal form is \texttt{Induction.exact}; the final implication is
\texttt{Induction.reaches}, with its separate permanent-P104 premise for $Q$.
For head $h$ take $a=h+P_hv$, $m=104$ and $t$ its anchored scattering
duration, so $L_n=\Sigma_B(h,P_h+n)$. Explicitly,
$A_n=\bigcup_{0\le j<n}\tau_v^jW$ and
$D_n=(\bigcup_{0\le j<n}\tau_v^jC)\cup\tau_v^nF$.
Thus conditions 5 and 7 quantify over every required translated copy.
Exact affine-ray guards discharge these infinite conditions. No exact XOR
identity beyond support containment is required.

\begin{landscape}
\begin{figure}[p]
\centering
\setlength{\tabcolsep}{1.5pt}
\renewcommand{\arraystretch}{0.82}
\begin{tabular}{@{}cccccc@{}}
\includegraphics[width=.155\linewidth]{figures/scattering/phase-13-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-14-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-27-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-28-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-60-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-61-straight.png} \\
{\scriptsize\textcolor{proofblue}{P13 · straight}} &
{\scriptsize\textcolor{proofblue}{P14 · straight}} &
{\scriptsize\textcolor{proofblue}{P27 · straight}} &
{\scriptsize\textcolor{proofblue}{P28 · straight}} &
{\scriptsize\textcolor{proofblue}{P60 · straight}} &
{\scriptsize\textcolor{proofblue}{P61 · straight}} \\[2pt]

\includegraphics[width=.155\linewidth]{figures/scattering/phase-70-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-75-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-89-straight.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-29-right.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-32-right.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-38-right.png} \\
{\scriptsize\textcolor{proofblue}{P70 · straight}} &
{\scriptsize\textcolor{proofblue}{P75 · straight}} &
{\scriptsize\textcolor{proofblue}{P89 · straight}} &
{\scriptsize\textcolor{prooforange}{P29 · right}} &
{\scriptsize\textcolor{prooforange}{P32 · right}} &
{\scriptsize\textcolor{prooforange}{P38 · right}} \\[2pt]

\includegraphics[width=.155\linewidth]{figures/scattering/phase-55-right.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-56-right.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-62-right.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-71-right.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-15-left.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-45-left.png} \\
{\scriptsize\textcolor{prooforange}{P55 · right}} &
{\scriptsize\textcolor{prooforange}{P56 · right}} &
{\scriptsize\textcolor{prooforange}{P62 · right}} &
{\scriptsize\textcolor{prooforange}{P71 · right}} &
{\scriptsize\textcolor{proofpurple}{P15 · left}} &
{\scriptsize\textcolor{proofpurple}{P45 · left}} \\[2pt]

\includegraphics[width=.155\linewidth]{figures/scattering/phase-46-left.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-47-left.png} &
\includegraphics[width=.155\linewidth]{figures/scattering/phase-57-left.png} &
 & &
\fcolorbox{proofred}{white}{\includegraphics[width=.147\linewidth]{figures/scattering/phase-72-reverse.png}} \\
{\scriptsize\textcolor{proofpurple}{P46 · left}} &
{\scriptsize\textcolor{proofpurple}{P47 · left}} &
{\scriptsize\textcolor{proofpurple}{P57 · left}} &
 & &
{\scriptsize\bfseries\textcolor{proofred}{P72 · reverse (exceptional)}}
\end{tabular}
\caption{The complete $21+1$ pristine scattering spectrum, grouped by outgoing
orientation. Beige cells are the complete disturbed footprint, gray cells are
the undisturbed P104 reference, green cells show 20 terminal P104 cycles, the
black cell with a white outline is the selected perturbation $q$, and the
triangle is the ant. Each app canvas is independently fitted to its complete
footprint; lattice spacing remains visible in every panel. The boxed phase-72
panel is the unique reverse response and the exceptional channel in the
physical-history proof.}
\label{fig:scattering-spectrum}
\end{figure}
\end{landscape}

## All-depth pristine classification

For every head, the certificate checks the nonempty direct row, the stable
replay, its deduplicated read set, terminal orientation, and the ray guards
required by Lemma \ref{lem:archive}. There are 152 pristine replay
witnesses in total, including one stable witness per channel.

\begin{proposition}[Pristine scattering]\label{prop:pristine}
For all $h\in H$ and $d\ge1$, the pristine state $\Sigma_B(h,d)$ reaches P104.
Relative to the incoming highway, the stable outputs comprise nine straight,
seven right-turn and five left-turn standard highways. The remaining head
$h_{72}$ has reverse drift $-v=(2,2)$.
\end{proposition}

Figure \ref{fig:scattering-spectrum} displays one common-depth replay for every
frontier head. These panels are exported directly from Stage 03 of the
interactive app: the app runs the exact ant rule to the stored terminal witness
and then continues the resulting P104 orbit for 20 cycles. The checked
22-head list and archive induction extend this classification to all depths.


The subscript records the phase label used by the artifact, not a count. Its
coordinate relative to the pristine base pose is

$$h_{72}=p(B)+(-2,-8),\qquad P_{h_{72}}=11.$$

At this stage the reverse highway is already a valid P104 terminal state. The
difficulty appears only when the removed history is restored: the reverse ant
eventually travels toward that history rather than away from it.

# Restoring the physical history: 21 ordinary channels

For an ordinary channel, moving the defect sufficiently far down its ray
separates the translated pristine scattering trace and its final highway
corridor from the fixed historical wake. This gives a cutoff depth: shallower
cases are checked directly, while every deeper case transfers from the
pristine induction by untouched-region coupling. We now specify the cutoff
and the geometric guards that make this transfer uniform in depth.

Write

$$H_E=\{x:b_E(x)=1,\ x\notin S\}.$$

The exact entry certificate gives $|H_E|=702$. For an ordinary head $h$, let
$A_h$ be one plus the length of its checked physical direct row. The
certificate verifies $P_h\le A_h$. Thus

$$1\le d<A_h$$

is a finite direct band, while $d=A_h+n$ is the inductive region. The offset
$L_h=A_h-P_h$ aligns physical depth $A_h+n$ with pristine depth $P_h+L_h+n$.

Each channel's cutoff is certified by separation guards. The finite report
checks these guards for every historical cell and the ordinary stable
snapshot; ray lemmas extend them to all deeper translations.

\begin{lemma}[Historical transfer]\label{lem:history}
Let $h$ be ordinary and $n\ge0$. The states $\Sigma_E(h,A_h+n)$ and
the corresponding pristine state at depth $P_h+L_h+n$ agree outside $H_E$.
The pristine path avoids $H_E$ through the scattering trace and its permanent
terminal corridor. Untouched-region coupling therefore gives identical
positions, headings and read colours for the two orbits at every future update.
\end{lemma}

The key point is temporal as well as spatial. A finite check shows separation
from the anchored trace; the affine guard shows that translating the obstacle
farther cannot bring a historical cell into any new trace copy or output ray.
Untouched-region coupling then turns geometric nonintersection into exact
equality of observations.

Figure \ref{fig:ordinary-history-map} shows why a channel-specific cutoff is
needed: shallow channel points lie among the finite historical cloud, whereas
each stable lane eventually extends past it in the common drift direction.

\begin{figure}[t]
\centering
\includegraphics[width=.94\linewidth]{figures/stages/stage-04-finite-history.png}
\caption{The ordinary physical-history map, exported from Stage 04 of the
interactive app. Gray is the finite time-9,977 history together with the
active entry support. Orange cells are channel depths discharged by direct
physical replay; blue cells extend the 21 stable ordinary lanes through depth
30 to display their affine continuation. Red and cyan outlines mark the
time-zero ant origin and the time-9,977 P104 entry, respectively. The all-depth
extension follows from Lemma~\ref{lem:history}.}
\label{fig:ordinary-history-map}
\end{figure}

\begin{proposition}[Ordinary physical channels]\label{prop:ordinary}
For each of the 21 ordinary heads $h$ and every $d\ge1$,
$\Sigma_E(h,d)$ reaches P104.
\end{proposition}

For $d<A_h$ this is the physical replay table. For $d\ge A_h$, write
$d=A_h+n$, apply Lemma \ref{lem:history}, and invoke pristine archive
induction at parameter $L_h+n$. The generated physical rows contain 179 replay
witnesses across all 22 channels; the exceptional row is used separately
below.

# Exceptional backscattering and the affine hit law

For the exceptional head, the pristine stable depth is 11 but the physical
base depth is

$$P_{h_{72}}=11,\qquad A_{h_{72}}=15,\qquad A_{h_{72}}-P_{h_{72}}=4.$$

Depths 1 through 14 are direct physical cases. At depth 15, four clean forward
translations carry the physical state into the affine reverse family.

## The exact reverse block

Let $R$ be the reverse base state obtained after the checked pristine
scattering time of 52,262 updates. Let $v_r=-v=(2,2)$, and let $W_r$ be the
finite difference between one reverse block and the translated state. The
certificate and its soundness theorem establish the following identity.
For a state $s=(b,p,d)$ and cell set $A$, write
$s\oplus A=(b\oplus\mathbf 1_A,p,d)$: colours flip on $A$ while the pose
is unchanged. For cell sets, $\bigoplus$ denotes symmetric difference.
Thus

$$
\operatorname{run}(104,R)=T_{v_r}R\oplus W_r.
\tag{2}\label{eq:reverse}
$$

Positive-copy ray guards show that $W_r$ begins affecting the representation
only at the next translated copy and is never read by any later reverse block.
Equation \ref{eq:reverse} therefore iterates indefinitely in the
pristine setting.

## First historical collision

With the historical wake restored, the reverse path eventually meets a cell
that the blank transient had changed. The checked first-hit report shows that
the unshifted pristine reverse base $R$ avoids all 702 historical cells for
ten complete reverse cycles and phases 0 through 88 of the next cycle, then
reaches

$$c=(20,-22)$$

at phase 89. The reverse time measured from $R$ is therefore
$10\cdot104+89=1{,}129$ updates; the report also verifies $c\in H_E$.
The physical depth-15 orbit has a four-block forward prefix before the
52,262-step scattering segment. Its reverse segment starts four translations
further away, and takes $(4+10)\cdot104+89=1{,}545$ updates to reach $c$.
Measured from the entry state $\Sigma_E(h_{72},15)$, the total time is

$$
t_{\mathrm{hit}}(0)=4\cdot104+52{,}262+(4+10)\cdot104+89=54{,}223.
$$

For general $n$, $t_{\mathrm{hit}}(n)$ is likewise measured from the entry
state $\Sigma_E(h_{72},15+n)$, before its forward prefix.

Increasing physical obstacle depth from $15+n$ to $15+(n+1)$ inserts one
forward block before reversal and one reverse block before the collision. The
extra forward displacement $v$ is cancelled by the extra reverse displacement
$-v$, preserving the collision cell and phase. Consequently

$$t_{\mathrm{hit}}(n)=t_{\mathrm{hit}}(0)+208n.
\tag{3}\label{eq:hitlaw}
$$

Define the complete base collision state
$C=\operatorname{run}(54{,}223,\Sigma_E(h_{72},15))$; its pose is
$(20,-22)$ heading north. For the pristine entry state $B$, let
$W_{\mathrm{cl}}=\mathcal B(\operatorname{run}(104,B))\mathbin{\triangle}\mathcal B(T_vB)$.
The finite layer carried by each added depth is explicitly
$L=T_{4v}(W_{\mathrm{cl}}\mathbin{\triangle}T_vW_r)$,
where $W_r$ is the reverse wake in Equation \ref{eq:reverse}.
These are respectively \texttt{actualHit}, \texttt{cleanWake}, and
\texttt{layer} in \texttt{PhaseChecks}. The checked collision normal form is

$$
\operatorname{run}(t_{\mathrm{hit}}(n),\Sigma_E(h_{72},15+n))
=C\oplus\bigoplus_{j=0}^{n-1}(L+jv).
\tag{4}\label{eq:hitnormal}
$$

Equation \ref{eq:hitnormal}, formalized as
\texttt{Scattering.Classification.exceptionalAffine}, is the normal form that
closes the infinite family. It says more than equal collision coordinates:
the complete state at collision is fixed modulo an explicit translated
archive.

\begin{figure}[t]
\centering
\includegraphics[width=.92\linewidth]{figures/exceptional/phase-72-depth-15-history.png}
\caption{The exceptional phase-72 history replay at the inductive base depth
$15$, exported directly from Stage 05 of the interactive app. Gray cells are
the finite state present at the time-9,977 entry boundary; beige cells are the
complete disturbed footprint; the coral diagonal is the reverse P104 segment
returning toward the history; and the green diagonal is 20 cycles of the final
forward P104 highway after the fixed historical collision and post-hit
transient. The black square is the perturbation $q$ and the triangle is the
terminal ant. Cyan, red, and orange outlines mark the P104 entry, the original
time-zero ant position, and the fixed historical hit, respectively.}
\label{fig:exceptional}
\end{figure}

## The post-hit tail

From $C$, exact replay for 7,994 updates reaches a forward P104 terminal state.
The checked post-hit trace guard proves that every layer in
Equation \ref{eq:hitnormal} avoids this finite replay. A second forward
ray guard proves that every layer also avoids the infinite terminal corridor.
Once Equation \ref{eq:hitnormal} is established inductively, untouched-region
coupling outside the union envelope $\bigcup_{0\le j<n}(L+jv)$ directly
transfers the 7,994-step replay and subsequent permanent P104 corridor from
the fixed collision state $C$ to every depth $15+n$.

\begin{proposition}[Exceptional physical channel]\label{prop:exceptional}
For every $d\ge1$, $\Sigma_E(h_{72},d)$ reaches P104.
\end{proposition}

The finite band proves $1\le d<15$; the reverse-block, first-hit,
post-hit, and archive lemmas prove $d=15+n$. Together with
Proposition \ref{prop:ordinary}, this is the complete single-defect
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

Figure \ref{fig:global-map} combines those branches in one visible-domain map.
It provides a spatial index to the preceding propositions and their
exhaustive, inductive coverage.

\begin{figure}[t]
\centering
\includegraphics[width=.94\linewidth]{figures/stages/stage-06-global-map.png}
\caption{Global one-black proof map, exported from Stage 06 of the interactive
app. Every lattice cell in the visible window is assigned to one proof stage:
untouched (gray-blue), prefix hit (blue), pristine P104 scattering (green),
finite-history intersection (orange), or exceptional reverse highway
(purple). A point belonging geometrically to both Stages 03 and 04 is assigned
to Stage 04 exactly when its replay or terminal corridor meets the finite
history. The colored rays are displayed finite segments of affine classes that
the Lean proof extends to every depth.}
\label{fig:global-map}
\end{figure}

# Lean formalization and finite computation \label{sec:lean}

## Proof cone

In Lean, the same assembly is exposed at three levels. The theorem
\texttt{Scattering.single\_defect\_scattering} constructs the $21+1$
classification. The entry theorem combines that classification with the
geometric partition. Finally the exported statement is literally

```lean
theorem OneBlack.universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s
```

The Lean 4.30.0 development combines analytic proof terms with three finite
computation leaves. Its proof cone includes the dynamics, certificate modules
and explicit \texttt{StandardTrace} bridge. Table \ref{tab:modules} maps the mathematical stages to their
principal modules.

| Mathematical obligation | Principal Lean modules |
|---|---|
| Dynamics, observations, symmetries | `Core`, `Semantics` |
| Blank P104 replay and induction | `HighwayData`, `Highway` |
| First-contact coupling and prefix | `Coupling`, `Prefix`, `PrefixLeaf` |
| Entry partition and affine channels | `Geometry`, `Rays`, `Entry` |
| Pristine archive induction | `Induction`, `PristineChecks`, `Pristine` |
| Physical ordinary channels | `ActualChecks`, `ActualHistory`, `OrdinaryGeometry`, `Ordinary` |
| Exceptional reverse family | the `Phase*` modules |
| Spectrum and universal theorem | `Scattering`, `Universal`, `StandardTrace` |

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
updates of finite certificate work, respectively. Archive induction extends
these witnesses to deeper channel members.

Each stable snapshot computes its terminal state, deduplicated read set,
cached read list, terminal orientation, and acceptance result once. Multiple
proof guards consume the same values. Verification directly replays the
checked-in terminal times and checks their acceptance conditions.

## Reflection and trust boundary

Each Boolean report is connected to a typed certificate by a soundness
theorem of the form

```lean
theorem certificate_of_report (verified : report = true) : Certificate
```

and the typed certificates feed the analytic theorems. The closed equalities
\texttt{report = true} are discharged with \texttt{native\_decide}. This design
makes the finite obligations inspectable and reproducible. The trusted
computing base consists of Lean's kernel and foundational axioms together
with the native compiler, runtime, code-generation backend and any externally
linked native code used by \texttt{native\_decide}. The pinned Lean 4.30.0
source documents and implements this axiom construction in
\texttt{Lean.Meta.nativeEqTrue}; the tactic calls it from
\texttt{elabNativeDecideCore} [@leanref2026]. The final
theorems depend on three native-evaluation axioms, one for each finite report.

## Reproduction

The proof sources and checked witness data are available in the
[public repository](https://github.com/kehao95/langtons-ant-core)
[@hao2026artifact] at immutable commit
`e93252230ea9109908c23a009824d72d30fb91e2`. The accompanying Zenodo source
archive is version 0.2.0, `one-black-0.2.0-source.zip` [@hao2026preprint].
The development pins `leanprover/lean4:v4.30.0`. From the repository root, run

```console
python3 one_black/reproduce.py
```

This command builds both final theorem targets in a fresh temporary directory,
checks the witness tables by direct simulation, and records the build output,
source digests and axiom dependencies. The complete trace conclusion is


```lean
theorem OneBlack.universal_one_black_standard_trace
    (s : State) (one : ExactlyOneBlack s) :
    ∃ n, HasStandardTrace (run n s)
```

Here `HasStandardTrace` quantifies a symmetry placement of the fixed actual
blank state at update 9977 and equality of every future position, heading and
read colour. Both final theorems have exactly the same three native computation
leaves. The trace bridge is proved without additional native computation.
The [interactive proof guide](https://www.kehao.me/langtons-ant-core/one-black.html)
illustrates the proof geometry and channel classification; its source is
`docs/one-black.html` in the accompanying repository.

# Related work

## Classical ant dynamics

Langton introduced the model in the context of artificial life and reported
the emergence of organized motion from simple local rules [@langton1986].
Gajardo, Lutfalla, and Rao present an accessible proof of unboundedness for
every initial configuration in §2 of [@gajardo2024], attributing the classical
result to Bunimovich and Troubetzkoy. Their corner argument applies also to
the reflected classical rule used here. Unboundedness is a
qualitatively weaker conclusion than Theorem \ref{thm:main}: it excludes
finite confinement but neither selects the period-104 orbit nor gives a time
after which translated phase equality holds. Gale, Propp, Sutherland, and
Troubetzkoy studied further ant rules and symmetry phenomena [@gale1995].

## Complexity and generalized highways

Gajardo, Moreira, and Goles embedded Boolean-circuit computation in finite
configurations and obtained P-hardness; their universality and undecidability
construction uses an infinite, finitely described trapezoidal circuit array
[@gajardo2002]. Their circuit construction can route an ant to a highway seed,
giving an infinite family of highway-reaching configurations. The present
theorem covers the exhaustive natural family defined solely by ``exactly one
black cell'', with arbitrary relative position.

For generalized reversible ants with an additional unchanged, straight-going
gray-cell state, recognition of repeatable configurations can
be PSPACE-hard [@tsukiji2011]. Recent work shows that generalized rules may
possess unboundedly or infinitely many distinct highways [@gajardo2024], and
may also exhibit qualitatively different finite-configuration asymptotics
[@lutfalla2025]. These results motivate separating the theorem's classical LR
rule and exact P104 predicate from broader claims about generalized ants.

## A geometric method for unbounded perturbations

The proof architecture separates a finite
baseline transient from a translated renewal boundary, classifies the
first-contact frontier into affine channels, and promotes finite anchors with
geometric archive guards. In the exceptional channel, a reverse renewal orbit
and an affine collision law account for the return through the historical wake.
Together these mechanisms extend finitely checked anchors to every channel
depth and suggest a route to studying interactions among several defects.

# Limitations

The theorem covers exactly one initial black cell on the infinite square
lattice with the white-right/black-left rule. Its conclusion equates every
future position, heading and read colour with a placed standard P104 orbit.
Inert historical debris may differ outside future reads; whole-grid translation
equality is not asserted. Several-defect convergence and the general
finite-support Highway Conjecture remain open. Generalized ant rules are
outside the theorem's scope.

The three finite native leaves retain trust in Lean's compiler, runtime and
native backend, as detailed in Section 9. The infinite reductions are checked
relative to these leaves. The formal artifact and finite witnesses record
this evidence boundary.

# Conclusion

Every classical Langton-ant state with exactly one black cell reaches the
standard period-104 highway, in the precise observation-level sense of
Definition \ref{def:p104}. The proof has no coordinate cutoff. It reduces
the 1,376 early-contact cells to finite replay and every later relevant cell to
one of 22 affine channels. Twenty-one channels become insensitive to the
blank-orbit history after channel-specific cutoffs. The remaining channel
creates a reverse highway, returns to a fixed historical cell with the affine
law $t_{\mathrm{hit}}(n)=t_{\mathrm{hit}}(0)+208n$, and then enters forward
P104 through an archived post-hit tail.

The Lean development checks both the infinite reductions and the completeness
of the case split. Its three finite leaves are evaluated natively, with the
corresponding compiler/runtime dependencies recorded in the artifact. The
result establishes a fully quantified convergence theorem for an unbounded
perturbation family through scattering geometry and induction.

The next mathematical question is whether the frontier-channel method survives
multiple defects. A second defect introduces interactions between independent
contact times and between accumulated wakes, so a successful extension will
likely require a compositional renewal invariant.

\clearpage
\appendix

# Certificate inventory

Table \ref{tab:inventory} collects numerical constants used in the proof.
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
| Unshifted reverse first-hit time | 1,129 | from pristine reverse base $R$ |
| Physical depth-15 first-hit time | 54,223 | from $\Sigma_E(h_{72},15)$ |
| Historical hit point | $(20,-22)$ | depth-independent collision |
| Post-hit replay | 7,994 | terminal forward P104 witness |
| Pristine / physical replay witnesses | 152 / 179 | finite scattering leaves |

: Checked certificate inventory. \label{tab:inventory}

# References

::: {#refs}
:::


# Acknowledgements

Generative AI assisted in proof development, code, auditing and manuscript
preparation.
