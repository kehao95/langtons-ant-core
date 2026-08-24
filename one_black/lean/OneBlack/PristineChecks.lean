import OneBlack.Rays
import OneBlack.RayGeometry

namespace OneBlack.PristineChecks

open OneBlack Highway Terminal Entry Rays RayGeometry

def heads : List Point := support.filter fun p => decide (drift.add p ∉ support)
def active : List Point := support.filter fun p => !(baseF.black.contains p)

def obstacle (head : Point) (depth : Nat) : Point :=
  shiftPoint drift depth head

def initial (head : Point) (depth : Nat) : FState :=
  force (obstacle head depth) baseF

def row (head : Point) : List Nat :=
  FiniteData.pristineLaneTimes.getD (heads.idxOf head) []

def witnessTime (head : Point) (depth : Nat) : Nat :=
  (row head).getD (depth - 1) 0

def stableDepth (head : Point) : Nat := (row head).length

def replayFrom : Nat → FState → PointSet → FState × PointSet
  | 0, s, reads => (s, reads)
  | n + 1, s, reads => replayFrom n s.step (reads.insert s.pos)

def replay (n : Nat) (s : FState) : FState × PointSet :=
  replayFrom n s {}

structure Snapshot where
  head : Point
  time : Nat
  result : FState × PointSet
  reads : List Point
  turns : Nat
  accepted : Bool

def snapshots : List Snapshot := heads.map fun head =>
  let depth := stableDepth head
  let time := witnessTime head depth
  let result := replay time (initial head depth)
  let found := orientation result.1
  ⟨head, time, result, result.2.toList, found.getD 0, found.isSome⟩

def shiftedBaseColour (p : Point) : Bool :=
  baseF.black.contains (p.sub drift)

def wakeCells : List Point :=
  (support ++ shiftedSupport).eraseDups.filter fun p =>
    (baseF.run period).black.contains p != shiftedBaseColour p

def directChecks : List Bool := heads.flatMap fun head =>
  (List.range (stableDepth head - 1)).map fun index =>
    lands (initial head (index + 1)) (witnessTime head (index + 1))

def activeChecks : List Bool :=
  (active.zip FiniteData.pristineActiveTimes).map fun c =>
    lands (force c.1 baseF) c.2

def stableCheck (s : Snapshot) : Bool :=
  let final := s.result.1
  s.accepted &&
  wakeCells.all (fun wake =>
    support.all (fun target => !(raysMeet 0 wake target)) &&
    s.reads.all (fun target => !(raysMeet 0 wake target)) &&
    support.all (fun source =>
      !(raysMeet s.turns (normalizedAt s.turns final wake) source)))

def headClearCheck : Bool := heads.all fun head =>
  support.all fun target => separated head target

def reportWith (stable : List Snapshot) : Bool :=
  decide (heads.length = FiniteData.pristineLaneTimes.length) &&
  decide (heads.length = 22) &&
  FiniteData.pristineLaneTimes.all (fun times => decide (¬times.isEmpty)) &&
  decide (active.length = FiniteData.pristineActiveTimes.length) &&
  activeChecks.all id && directChecks.all id && stable.all stableCheck &&
  headClearCheck

def report : Bool := reportWith snapshots

structure Certificate : Prop where
  rowsMatch : heads.length = FiniteData.pristineLaneTimes.length
  headCount : heads.length = 22
  rowsNonempty : FiniteData.pristineLaneTimes.all
    (fun row => decide (¬row.isEmpty)) = true
  activeMatch : active.length = FiniteData.pristineActiveTimes.length
  activePass : activeChecks.all id = true
  directPass : directChecks.all id = true
  stablePass : snapshots.all stableCheck = true
  headClearPass : headClearCheck = true

theorem certificate_of_report (verified : report = true) : Certificate := by
  simp only [report, reportWith, Bool.and_eq_true, decide_eq_true_eq] at verified
  rcases verified with ⟨⟨⟨⟨⟨⟨⟨rows, count⟩, lengths⟩, activeLength⟩,
    active⟩, direct⟩, stable⟩, headClear⟩
  exact ⟨rows, count, lengths, activeLength, active, direct, stable, headClear⟩

theorem certificate_of_reportWith {stable : List Snapshot}
    (exact : stable = snapshots) (verified : reportWith stable = true) :
    Certificate := by
  subst stable
  exact certificate_of_report verified

end OneBlack.PristineChecks
