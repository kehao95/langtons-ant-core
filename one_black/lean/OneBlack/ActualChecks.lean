import OneBlack.Pristine

namespace OneBlack.ActualChecks

open OneBlack Highway Terminal Entry RayGeometry PristineChecks Pristine

def phaseHead : Point := baseF.pos.add ⟨-2, -8⟩
def phaseBaseDepth : Nat := 15

def History : Region := fun p => entry.black p = true ∧ p ∉ support

instance (p : Point) : Decidable (History p) := by
  unfold History
  infer_instance

def historyCells : List Point :=
  entryF.black.toList.filter fun p => decide (p ∉ support)

def ordinaryHeads : List Point := heads.filter fun head => decide (head ≠ phaseHead)

def actualInitial (head : Point) (depth : Nat) : FState :=
  force (obstacle head depth) entryF

def actualRow (head : Point) : List Nat :=
  FiniteData.actualLaneTimes.getD (heads.idxOf head) []

def actualTime (head : Point) (depth : Nat) : Nat :=
  (actualRow head).getD (depth - 1) 0

def actualCutoff (head : Point) : Nat := (actualRow head).length + 1
def historyLag (head : Point) : Nat := actualCutoff head - stableDepth head

def directChecks : List Bool := heads.flatMap fun head =>
  (List.range (actualCutoff head - 1)).map fun index =>
    lands (actualInitial head (index + 1)) (actualTime head (index + 1))

def guardResult (snapshot : PristineChecks.Snapshot)
    (historical : Point) : Bool :=
  let lag := historyLag snapshot.head
  let final := snapshot.result.1
  let normalized := normalizedAt snapshot.turns final historical
  let anchored := backwardPoint snapshot.turns lag normalized
  snapshot.reads.all
      (fun source => !(shiftedAtLeast lag historical source)) &&
  decide (anchored ∉ support) && separatedFromSupport anchored &&
  support.all (fun source =>
    !(raysMeet snapshot.turns anchored source))

def All {α : Type} (P : α → Prop) : List α → Prop
  | [] => True
  | item :: items => P item ∧ All P items

def decidableAll {α : Type} {P : α → Prop} [DecidablePred P] :
    (items : List α) → Decidable (All P items)
  | [] => isTrue trivial
  | item :: items =>
      match inferInstanceAs (Decidable (P item)), decidableAll items with
      | isTrue head, isTrue tail => isTrue ⟨head, tail⟩
      | isFalse head, _ => isFalse fun all => head all.1
      | _, isFalse tail => isFalse fun all => tail all.2

instance {α : Type} {P : α → Prop} [DecidablePred P] (items : List α) :
    Decidable (All P items) := decidableAll items

def GuardPropWith (stable : List PristineChecks.Snapshot) : Prop := All (fun snapshot =>
  snapshot.head ∈ ordinaryHeads →
    All (fun historical =>
      guardResult snapshot historical = true) historyCells) stable

def GuardProp : Prop := GuardPropWith snapshots

instance (stable : List PristineChecks.Snapshot) : Decidable (GuardPropWith stable) := by
  unfold GuardPropWith
  infer_instance

instance : Decidable GuardProp := by unfold GuardProp; infer_instance

def guardCheckWith (stable : List PristineChecks.Snapshot) : Bool :=
  decide (GuardPropWith stable)
def guardCheck : Bool := guardCheckWith snapshots

def reportWith (stable : List PristineChecks.Snapshot) : Bool :=
  decide (historyCells.length = 702) &&
  decide (heads.length = FiniteData.actualLaneTimes.length) &&
  decide (phaseHead ∈ heads) && decide (ordinaryHeads.length = 21) &&
  decide (actualCutoff phaseHead = phaseBaseDepth) &&
  ordinaryHeads.all (fun head => decide (stableDepth head ≤ actualCutoff head)) &&
  directChecks.all id && guardCheckWith stable

def report : Bool := reportWith snapshots

structure Certificate : Prop where
  historyCount : historyCells.length = 702
  rowsMatch : heads.length = FiniteData.actualLaneTimes.length
  phaseMember : phaseHead ∈ heads
  ordinaryCount : ordinaryHeads.length = 21
  phaseCutoff : actualCutoff phaseHead = phaseBaseDepth
  cutoffOrder : ordinaryHeads.all
    (fun head => decide (stableDepth head ≤ actualCutoff head)) = true
  directPass : directChecks.all id = true
  guardPass : GuardProp

theorem certificate_of_report (verified : report = true) : Certificate := by
  simp only [report, reportWith, guardCheckWith,
    Bool.and_eq_true, decide_eq_true_eq] at verified
  rcases verified with
    ⟨⟨⟨⟨⟨⟨⟨historyCount, rowsMatch⟩, phaseMember⟩, ordinaryCount⟩,
      phaseCutoff⟩, cutoffOrder⟩, directPass⟩, guardPass⟩
  exact ⟨historyCount, rowsMatch, phaseMember, ordinaryCount, phaseCutoff,
    cutoffOrder, directPass, guardPass⟩

theorem certificate_of_reportWith {stable : List PristineChecks.Snapshot}
    (exact : stable = snapshots) (verified : reportWith stable = true) :
    Certificate := by
  subst stable
  exact certificate_of_report verified

theorem all_of_mem {P : α → Prop} {items : List α} {item : α}
    (all : All P items) (member : item ∈ items) : P item := by
  induction items with
  | nil => simp at member
  | cons head tail ih =>
      rcases List.mem_cons.mp member with equal | member
      · exact equal ▸ all.1
      · exact ih all.2 member

theorem guardResult_parts {snapshot : PristineChecks.Snapshot}
    {historical : Point} (checked : guardResult snapshot historical = true) :
    snapshot.reads.all (fun source =>
      !(shiftedAtLeast (historyLag snapshot.head) historical source)) = true ∧
    backwardPoint snapshot.turns (historyLag snapshot.head)
      (normalizedAt snapshot.turns snapshot.result.1 historical) ∉ support ∧
    separatedFromSupport (backwardPoint snapshot.turns
      (historyLag snapshot.head)
      (normalizedAt snapshot.turns snapshot.result.1 historical)) = true ∧
    support.all (fun source =>
      !(raysMeet snapshot.turns
        (backwardPoint snapshot.turns (historyLag snapshot.head)
          (normalizedAt snapshot.turns snapshot.result.1 historical))
        source)) = true := by
  simp only [guardResult, Bool.and_eq_true,
    decide_eq_true_eq] at checked
  exact ⟨checked.1.1.1, checked.1.1.2, checked.1.2, checked.2⟩

end OneBlack.ActualChecks
