import OneBlack.Induction

namespace OneBlack

abbrev BRegion := Point → Bool

namespace BRegion

def empty : BRegion := fun _ => false
def xor (a b : BRegion) : BRegion := fun p => Bool.xor (a p) (b p)
def ofList (points : List Point) : BRegion := fun p => decide (p ∈ points)
def shift (v : Point) (r : BRegion) : BRegion := fun p => r (p.sub v)

def iterate (v : Point) : Nat → BRegion → BRegion
  | 0, r => r
  | n + 1, r => shift v (iterate v n r)

def accumulated (v : Point) (r : BRegion) : Nat → BRegion
  | 0 => empty
  | n + 1 => xor r (shift v (accumulated v r n))

theorem xor_apply (a b : BRegion) (p : Point) :
    xor a b p = Bool.xor (a p) (b p) := rfl

@[simp] theorem xor_empty (r : BRegion) : xor r empty = r := by
  funext p; cases value : r p <;> simp [xor, empty, value]

@[simp] theorem empty_xor (r : BRegion) : xor empty r = r := by
  funext p; cases value : r p <;> simp [xor, empty, value]

@[simp] theorem xor_self (r : BRegion) : xor r r = empty := by
  funext p; cases r p <;> simp [xor, empty]

theorem xor_comm (a b : BRegion) : xor a b = xor b a := by
  funext p; exact Bool.xor_comm _ _

theorem xor_assoc (a b c : BRegion) :
    xor (xor a b) c = xor a (xor b c) := by
  funext p; exact Bool.xor_assoc _ _ _

theorem shift_xor (v : Point) (a b : BRegion) :
    shift v (xor a b) = xor (shift v a) (shift v b) := rfl

theorem iterate_apply (v : Point) (r : BRegion) (n : Nat) (p : Point) :
    iterate v n r (shiftPoint v n p) = r p := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change iterate v n r ((v.add (shiftPoint v n p)).sub v) = r p
      simpa using ih

theorem iterate_member {v : Point} {r : BRegion} {n : Nat} {p : Point}
    (present : iterate v n r p = true) :
    ∃ source, r source = true ∧ p = shiftPoint v n source := by
  induction n generalizing p with
  | zero => exact ⟨p, present, rfl⟩
  | succ n ih =>
      rcases ih present with ⟨source, sourceIn, equal⟩
      refine ⟨source, sourceIn, ?_⟩
      change p = v.add (shiftPoint v n source)
      have placed := congrArg (Point.add v) equal
      simpa using placed

theorem accumulated_member {v : Point} {r : BRegion} {n : Nat} {p : Point}
    (present : accumulated v r n p = true) :
    ∃ source copies, copies < n ∧ r source = true ∧
      p = shiftPoint v copies source := by
  induction n generalizing p with
  | zero => simp [accumulated, empty] at present
  | succ n ih =>
      change Bool.xor (r p) (accumulated v r n (p.sub v)) = true at present
      cases here : r p with
      | true => exact ⟨p, 0, Nat.zero_lt_succ _, here, rfl⟩
      | false =>
        have tail : accumulated v r n (p.sub v) = true := by
          simpa [here] using present
        rcases ih tail with ⟨source, copies, before, sourceIn, equal⟩
        refine ⟨source, copies + 1, Nat.succ_lt_succ before,
          sourceIn, ?_⟩
        change p = v.add (shiftPoint v copies source)
        have placed := congrArg (Point.add v) equal
        simpa using placed

end BRegion

def xorState (archive : BRegion) (s : State) : State :=
  { s with black := fun p => Bool.xor (archive p) (s.black p) }

theorem xorState_sameOutside (archive : BRegion) (s : State) :
    SameOutside (fun p => archive p = true) (xorState archive s) s := by
  refine ⟨rfl, rfl, ?_⟩
  intro p absent
  have white : archive p = false := by
    cases value : archive p <;> simp_all
  simp [xorState, white]

@[simp] theorem xorState_empty (s : State) : xorState BRegion.empty s = s := by
  apply State.ext
  · funext p; simp [xorState, BRegion.empty]
  · rfl
  · rfl

theorem xorState_xor (a b : BRegion) (s : State) :
    xorState a (xorState b s) = xorState (BRegion.xor a b) s := by
  apply State.ext
  · funext p; simp [xorState, BRegion.xor, Bool.xor_assoc]
  · rfl
  · rfl

def AvoidsBFor (archive : BRegion) (s : State) (n : Nat) : Prop :=
  ∀ k, k < n → archive (run k s).pos = false

theorem step_xorState {archive : BRegion} {s : State}
    (unread : archive s.pos = false) :
    step (xorState archive s) = xorState archive (step s) := by
  cases s with
  | mk black pos dir =>
      apply State.ext
      · funext p
        by_cases current : p = pos
        · subst p; simp [step, xorState, toggle, unread]
        · simp [step, xorState, toggle, current]
      · simp [step, xorState, unread]
      · simp [step, xorState, unread]

theorem run_xorState {archive : BRegion} {s : State} (n : Nat)
    (avoids : AvoidsBFor archive s n) :
    run n (xorState archive s) = xorState archive (run n s) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      have shorter : AvoidsBFor archive s n := fun k before =>
        avoids k (Nat.lt_succ_of_lt before)
      rw [run, run, ih shorter]
      exact step_xorState (avoids n (Nat.lt_succ_self n))

theorem blacken_xorState (p : Point) (archive : BRegion) (s : State)
    (outside : archive p = false) :
    blacken p (xorState archive s) = xorState archive (blacken p s) := by
  apply State.ext
  · funext q
    by_cases current : q = p
    · subst q; simp [blacken, xorState, outside]
    · simp [blacken, xorState, current]
  · rfl
  · rfl

theorem shift_xorState (v : Point) (archive : BRegion) (s : State) :
    OneBlack.shift v (xorState archive s) =
      xorState (BRegion.shift v archive) (OneBlack.shift v s) := by
  apply State.ext <;> rfl

theorem shiftState_xorState (v : Point) (n : Nat)
    (archive : BRegion) (s : State) :
    shiftState v n (xorState archive s) =
      xorState (BRegion.iterate v n archive) (shiftState v n s) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [shiftState, BRegion.iterate, ih]
      exact shift_xorState v (BRegion.iterate v n archive)
        (shiftState v n s)

theorem Point.add_left_injective (v : Point) : Function.Injective v.add := by
  intro a b equal
  have pulled := congrArg (Point.sub · v) equal
  simpa using pulled

theorem shiftPoint_injective (v : Point) (n : Nat) :
    Function.Injective (shiftPoint v n) := by
  induction n with
  | zero => exact fun _ _ equal => equal
  | succ n ih =>
      intro a b equal
      exact ih (Point.add_left_injective v equal)

theorem shiftState_pos (v : Point) (n : Nat) (s : State) :
    (shiftState v n s).pos = shiftPoint v n s.pos := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [shiftState, shiftPoint, OneBlack.shift, ih]

structure BlockData (s : State) (v : Point) (period : Nat)
    (wake : BRegion) : Prop where
  block : run period s = xorState wake (OneBlack.shift v s)
  avoidsShifted : ∀ copies, 0 < copies → ∀ k,
    wake (run k (shiftState v copies s)).pos = false

theorem BlockData.accumulated_avoids {s : State} {v : Point} {period : Nat}
    {wake : BRegion} (data : BlockData s v period wake) (cycles : Nat) :
    AvoidsBFor (BRegion.accumulated v wake cycles)
      (shiftState v cycles s) period := by
  intro phase _
  cases present : BRegion.accumulated v wake cycles
      (run phase (shiftState v cycles s)).pos with
  | false => rfl
  | true =>
      exfalso
      rcases BRegion.accumulated_member present with
        ⟨source, copies, before, sourceIn, equal⟩
      have shiftedPosition :
          (run phase (shiftState v cycles s)).pos =
            shiftPoint v cycles (run phase s).pos := by
        rw [run_shiftState, shiftState_pos]
      have cycleSplit : cycles = copies + (cycles - copies) := by omega
      have sourceEqual : source =
          shiftPoint v (cycles - copies) (run phase s).pos := by
        have shiftedEq : shiftPoint v copies source = shiftPoint v copies
            (shiftPoint v (cycles - copies) (run phase s).pos) := calc
          shiftPoint v copies source = (run phase (shiftState v cycles s)).pos :=
            equal.symm
          _ = shiftPoint v cycles (run phase s).pos := shiftedPosition
          _ = shiftPoint v copies
              (shiftPoint v (cycles - copies) (run phase s).pos) := by
            rw [← shiftPoint_add]
            congr 2
        exact shiftPoint_injective v copies shiftedEq
      have positive : 0 < cycles - copies := by omega
      have forbidden := data.avoidsShifted (cycles - copies) positive phase
      rw [run_shiftState, shiftState_pos, ← sourceEqual, sourceIn] at forbidden
      contradiction

theorem BlockData.normal {s : State} {v : Point} {period : Nat}
    {wake : BRegion} (data : BlockData s v period wake) : ∀ cycles,
    run (cycles * period) s =
      xorState (BRegion.accumulated v wake cycles) (shiftState v cycles s) := by
  intro cycles
  induction cycles with
  | zero => simp [run, BRegion.accumulated, shiftState]
  | succ cycles ih =>
      have wakeAvoids : AvoidsBFor wake (OneBlack.shift v s)
          (cycles * period) := by
        intro k _
        simpa [shiftState] using data.avoidsShifted 1 (by omega) k
      rw [show (cycles + 1) * period = period + cycles * period by
          simp [Nat.add_mul, Nat.add_comm],
        run_add, data.block,
        run_xorState _ wakeAvoids, run_shift, ih,
        shift_xorState, xorState_xor]
      rfl

theorem BlockData.normal_phase {s : State} {v : Point} {period : Nat}
    {wake : BRegion} (data : BlockData s v period wake)
    (cycles phase : Nat) (bound : phase ≤ period) :
    run (cycles * period + phase) s =
      xorState (BRegion.accumulated v wake cycles)
        (shiftState v cycles (run phase s)) := by
  have avoidsPhase : AvoidsBFor (BRegion.accumulated v wake cycles)
      (shiftState v cycles s) phase := fun k before =>
    data.accumulated_avoids cycles k (Nat.lt_of_lt_of_le before bound)
  rw [run_add, data.normal cycles,
    run_xorState phase avoidsPhase, run_shiftState]

def FState.shift (v : Point) (s : FState) : FState :=
  { black := PointSet.ofList (s.black.toList.map (v.add ·))
    pos := v.add s.pos
    dir := s.dir }

theorem FState.toState_shift (v : Point) (s : FState) :
    (s.shift v).toState = OneBlack.shift v s.toState := by
  apply State.ext
  · funext p
    simp only [FState.shift, FState.toState, PointSet.contains_ofList,
      OneBlack.shift]
    apply Bool.eq_iff_iff.mpr
    constructor
    · intro accepted
      rcases List.mem_map.mp (of_decide_eq_true accepted) with
        ⟨q, member, equal⟩
      apply Std.TreeSet.contains_iff_mem.mpr
      apply Std.TreeSet.mem_toList.mp
      rw [← equal]
      simpa using member
    · intro accepted
      apply decide_eq_true
      apply List.mem_map.mpr
      exact ⟨p.sub v, Std.TreeSet.mem_toList.mpr
        (Std.TreeSet.contains_iff_mem.mp accepted), Point.add_sub v p⟩
  · rfl
  · rfl

def differenceSources (left right : FState) : List Point :=
  (left.black.toList ++ right.black.toList).eraseDups.filter fun p =>
    Bool.xor (left.black.contains p) (right.black.contains p)

theorem mem_differenceSources_iff (left right : FState) (p : Point) :
    p ∈ differenceSources left right ↔
      Bool.xor (left.black.contains p) (right.black.contains p) = true := by
  simp only [differenceSources, List.mem_filter, List.mem_eraseDups,
    List.mem_append]
  constructor
  · exact fun pair => pair.2
  · intro differs
    refine ⟨?_, differs⟩
    cases leftValue : left.black.contains p with
    | false =>
        cases rightValue : right.black.contains p with
        | false => simp [leftValue, rightValue] at differs
        | true => exact Or.inr (Std.TreeSet.mem_toList.mpr
            (Std.TreeSet.contains_iff_mem.mp rightValue))
    | true => exact Or.inl (Std.TreeSet.mem_toList.mpr
        (Std.TreeSet.contains_iff_mem.mp leftValue))

theorem differenceSources_apply (left right : FState) (p : Point) :
    BRegion.ofList (differenceSources left right) p =
      Bool.xor (left.black.contains p) (right.black.contains p) := by
  cases differs : Bool.xor (left.black.contains p) (right.black.contains p) <;>
    simp [BRegion.ofList, differs, mem_differenceSources_iff]

theorem difference_exact {left right : FState}
    (position : left.pos = right.pos) (heading : left.dir = right.dir) :
    left.toState = xorState (BRegion.ofList (differenceSources left right))
      right.toState := by
  apply State.ext
  · funext p
    change left.black.contains p = Bool.xor
      (BRegion.ofList (differenceSources left right) p)
      (right.black.contains p)
    rw [differenceSources_apply]
    cases left.black.contains p <;> cases right.black.contains p <;> rfl
  · exact position
  · exact heading

end OneBlack
