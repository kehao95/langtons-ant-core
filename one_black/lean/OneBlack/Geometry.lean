import OneBlack.Coupling

namespace OneBlack

abbrev Region := Point → Prop

def Region.union (a b : Region) : Region := fun p => a p ∨ b p
def Region.shift (v : Point) (r : Region) : Region := fun p => r (p.sub v)
def Region.Disjoint (a b : Region) : Prop := ∀ p, a p → ¬b p
def Region.Subset (a b : Region) : Prop := ∀ ⦃p⦄, a p → b p
def Region.empty : Region := fun _ => False
def Region.singleton (q : Point) : Region := fun p => p = q

def shiftPoint (v : Point) : Nat → Point → Point
  | 0, p => p
  | n + 1, p => v.add (shiftPoint v n p)

def shiftState (v : Point) : Nat → State → State
  | 0, s => s
  | n + 1, s => OneBlack.shift v (shiftState v n s)

def shiftRegion (v : Point) : Nat → Region → Region
  | 0, r => r
  | n + 1, r => Region.shift v (shiftRegion v n r)

@[simp] theorem shiftPoint_succ (v : Point) (n : Nat) (p : Point) :
    shiftPoint v (n + 1) p = v.add (shiftPoint v n p) := rfl

theorem shiftPoint_add (v : Point) (m n : Nat) (p : Point) :
    shiftPoint v (m + n) p = shiftPoint v m (shiftPoint v n p) := by
  induction m with
  | zero => simp [shiftPoint]
  | succ m ih => simpa [shiftPoint, Nat.succ_add, ih]

theorem run_shiftState (v : Point) (copies updates : Nat) (s : State) :
    run updates (shiftState v copies s) = shiftState v copies (run updates s) := by
  induction copies with
  | zero => rfl
  | succ copies ih => simpa [shiftState, run_shift, ih]

theorem SameOutside.shift (v : Point) {archive : Region} {a b : State}
    (same : SameOutside archive a b) :
    SameOutside (Region.shift v archive) (OneBlack.shift v a) (OneBlack.shift v b) := by
  rcases same with ⟨position, heading, colours⟩
  exact ⟨congrArg (Point.add v) position, heading,
    fun p outside => colours (p.sub v) outside⟩

theorem SameOutside.trans_union {a b c : State} {left right : Region}
    (ab : SameOutside left a b) (bc : SameOutside right b c) :
    SameOutside (Region.union left right) a c := by
  rcases ab with ⟨ap, ad, ac⟩
  rcases bc with ⟨bp, bd, bc⟩
  refine ⟨ap.trans bp, ad.trans bd, ?_⟩
  intro p outside
  exact (ac p (fun h => outside (Or.inl h))).trans
    (bc p (fun h => outside (Or.inr h)))

def reads (s : State) (n : Nat) : Region :=
  fun p => ∃ k, k < n ∧ (run k s).pos = p

def futureReads (s : State) : Region :=
  fun p => ∃ k, (run k s).pos = p

def AvoidsFor (region : Region) (s : State) (n : Nat) : Prop :=
  ∀ k, k < n → ¬region (run k s).pos

theorem SameOutside.symm {region : Region} {a b : State}
    (same : SameOutside region a b) : SameOutside region b a := by
  exact ⟨same.1.symm, same.2.1.symm,
    fun p outside => (same.2.2 p outside).symm⟩

theorem SameOutside.runFor {region : Region} {a b : State} (n : Nat)
    (same : SameOutside region a b) (avoids : AvoidsFor region b n) :
    SameOutside region (OneBlack.run n a) (OneBlack.run n b) := by
  induction n with
  | zero => simpa [OneBlack.run] using same
  | succ n ih =>
      have shorter : AvoidsFor region b n := fun k hk =>
        avoids k (Nat.lt_succ_of_lt hk)
      have atN := ih shorter
      have away := avoids n (Nat.lt_succ_self n)
      simpa [OneBlack.run] using atN.step away

theorem reads_eq_of_sameOutside {region : Region} {a b : State} (n : Nat)
    (same : SameOutside region a b) (avoids : AvoidsFor region b n) :
    reads a n = reads b n := by
  funext p
  apply propext
  constructor
  · rintro ⟨k, before, position⟩
    have atK := same.runFor k (fun j hj =>
      avoids j (Nat.lt_trans hj before))
    exact ⟨k, before, atK.1.symm ▸ position⟩
  · rintro ⟨k, before, position⟩
    have atK := same.runFor k (fun j hj =>
      avoids j (Nat.lt_trans hj before))
    exact ⟨k, before, atK.1 ▸ position⟩

theorem reads_add (s : State) (m n : Nat) :
    reads s (m + n) = Region.union (reads s m) (reads (run m s) n) := by
  funext p
  apply propext
  constructor
  · rintro ⟨k, bound, position⟩
    by_cases early : k < m
    · exact Or.inl ⟨k, early, position⟩
    · have le : m ≤ k := Nat.le_of_not_gt early
      refine Or.inr ⟨k - m, by omega, ?_⟩
      rw [← run_add]
      simpa [Nat.add_sub_of_le le] using position
  · rintro (⟨k, bound, position⟩ | ⟨k, bound, position⟩)
    · exact ⟨k, Nat.lt_add_right _ bound, position⟩
    · refine ⟨m + k, Nat.add_lt_add_left bound m, ?_⟩
      simpa [run_add] using position

theorem reads_shift (v : Point) (s : State) (n : Nat) :
    reads (OneBlack.shift v s) n = Region.shift v (reads s n) := by
  funext p
  apply propext
  constructor
  · rintro ⟨k, before, position⟩
    refine ⟨k, before, ?_⟩
    rw [run_shift] at position
    change v.add (run k s).pos = p at position
    have pulled := congrArg (Point.sub · v) position
    simpa using pulled
  · rintro ⟨k, before, position⟩
    refine ⟨k, before, ?_⟩
    rw [run_shift]
    change v.add (run k s).pos = p
    have placed := congrArg (Point.add v) position
    simpa using placed

theorem blacken_sameOutside (p : Point) (s : State) :
    SameOutside (Region.singleton p) (blacken p s) s := by
  refine ⟨rfl, rfl, ?_⟩
  intro q outside
  have different : q ≠ p := outside
  simp [blacken, different]

theorem SameOutside.blacken {region : Region} {a b : State}
    (same : SameOutside region a b) (p : Point) :
    SameOutside region (blacken p a) (blacken p b) := by
  rcases same with ⟨position, heading, colours⟩
  refine ⟨position, heading, ?_⟩
  intro q outside
  by_cases current : q = p
  · subst q
    change (if p = p then true else a.black p) =
      (if p = p then true else b.black p)
    simp
  · change (if q = p then true else a.black q) =
      (if q = p then true else b.black q)
    rw [if_neg current, if_neg current, colours q outside]

theorem run_blacken {p : Point} {s : State} (n : Nat)
    (avoids : Avoids p s n) : run n (blacken p s) = blacken p (run n s) := by
  have regionAvoids : AvoidsFor (Region.singleton p) s n := by
    intro k before equal
    exact avoids k before equal
  have coupled := (blacken_sameOutside p s).runFor n regionAvoids
  apply State.ext
  · funext q
    by_cases same : q = p
    · subst q
      have leftAvoids : Avoids p (blacken p s) n := by
        intro k before equal
        have pose := (blacken_sameOutside p s).runFor k (fun j earlier inside =>
          regionAvoids j (Nat.lt_trans earlier before) inside)
        exact avoids k before (pose.1 ▸ equal)
      have retained := colour_unchanged n leftAvoids
      simpa [blacken] using retained
    · have colour := coupled.2.2 q (by simpa [Region.singleton] using same)
      simpa [blacken, same] using colour
  · exact coupled.1
  · exact coupled.2.1

theorem shift_blacken (v p : Point) (s : State) :
    OneBlack.shift v (blacken p s) = blacken (v.add p) (OneBlack.shift v s) := by
  apply State.ext
  · funext q
    by_cases same : q = v.add p
    · subst q; simp [OneBlack.shift, blacken]
    · have pulled : q.sub v ≠ p := by
        intro equal
        apply same
        have := congrArg (Point.add v) equal
        simpa using this
      simp [OneBlack.shift, blacken, same, pulled]
  · rfl
  · rfl

theorem AvoidsForever.of_disjoint {archive : Region} {s : State}
    (h : Region.Disjoint archive (futureReads s)) : AvoidsForever archive s := by
  intro n inside
  exact h _ inside ⟨n, rfl⟩

theorem futureReads_shift (v : Point) (s : State) :
    futureReads (OneBlack.shift v s) = Region.shift v (futureReads s) := by
  funext p
  apply propext
  constructor
  · rintro ⟨n, position⟩
    refine ⟨n, ?_⟩
    rw [run_shift] at position
    change v.add (run n s).pos = p at position
    have := congrArg (Point.sub · v) position
    simpa using this
  · rintro ⟨n, position⟩
    refine ⟨n, ?_⟩
    rw [run_shift]
    change v.add (run n s).pos = p
    have := congrArg (Point.add v) position
    simpa using this

end OneBlack
