import OneBlack.HighwayData

namespace OneBlack.Highway

open OneBlack

set_option maxRecDepth 10000

def Support (p : Point) : Prop := p ∈ support

def SameOn (r : Point → Prop) (a b : State) : Prop :=
  a.pos = b.pos ∧ a.dir = b.dir ∧ ∀ p, r p → a.black p = b.black p

theorem SameOn.step {r : Point → Prop} {a b : State} (h : SameOn r a b)
    (read : r a.pos) : SameOn r (OneBlack.step a) (OneBlack.step b) := by
  rcases h with ⟨pos, dir, colours⟩
  cases a with
  | mk ab ap ad =>
    cases b with
    | mk bb bp bd =>
      simp only at pos dir colours read
      subst bp; subst bd
      have colour := colours ap read
      refine ⟨?_, ?_, ?_⟩
      · simp [OneBlack.step, colour]
      · simp [OneBlack.step, colour]
      · intro p hp
        by_cases current : p = ap
        · subst p; simp [OneBlack.step, toggle, colour]
        · simp [OneBlack.step, toggle, current, colours p hp]

theorem SameOn.run {r : Point → Prop} {a b : State} (n : Nat)
    (h : SameOn r a b) (reads : ∀ k, k < n → r (OneBlack.run k a).pos) :
    SameOn r (OneBlack.run n a) (OneBlack.run n b) := by
  induction n with
  | zero => simpa [OneBlack.run] using h
  | succ n ih =>
    have shorter := fun k hk => reads k (Nat.lt_succ_of_lt hk)
    simpa [OneBlack.run] using (ih shorter).step (reads n (Nat.lt_succ_self n))

theorem SameOn.shift (v : Point) {r : Point → Prop} {a b : State}
    (h : SameOn r a b) :
    SameOn (fun p => r (p.sub v)) (OneBlack.shift v a) (OneBlack.shift v b) := by
  rcases h with ⟨pos, dir, colours⟩
  exact ⟨congrArg (Point.add v) pos, dir, fun p hp => colours (p.sub v) hp⟩

def back : Nat → Point → Point
  | 0, p => p
  | n + 1, p => back n (p.sub drift)

def supportAt (n : Nat) (p : Point) : Prop := Support (back n p)

def reference : Nat → State
  | 0 => base
  | n + 1 => OneBlack.shift drift (reference n)

@[simp] theorem supportAt_zero (p : Point) : supportAt 0 p = Support p := rfl
@[simp] theorem supportAt_succ (n : Nat) (p : Point) :
    supportAt (n + 1) p = supportAt n (p.sub drift) := rfl
@[simp] theorem reference_zero : reference 0 = base := rfl
@[simp] theorem reference_succ (n : Nat) :
    reference (n + 1) = OneBlack.shift drift (reference n) := rfl

theorem base_reads : ∀ k, k < period → Support (OneBlack.run k base).pos := by
  intro k hk
  have member : (baseF.run k).pos ∈ baseF.reads period :=
    (FState.mem_reads_iff _ _ _).mpr ⟨k, hk, rfl⟩
  have accepted := (List.all_eq_true.mp base_reads_fact) _ member
  change Support (OneBlack.run k baseF.toState).pos
  rw [← FState.toState_run]
  change (baseF.run k).pos ∈ support
  exact of_decide_eq_true accepted

theorem base_transport :
    SameOn (supportAt 1) (OneBlack.run period base) (reference 1) := by
  have colours : support.all (fun p =>
      (baseF.run period).black.contains (drift.add p) ==
        baseF.black.contains p) = true := transport_colour_fact
  refine ⟨?_, ?_, ?_⟩
  · change (OneBlack.run period baseF.toState).pos = _
    rw [← FState.toState_run]
    change (baseF.run period).pos = drift.add baseF.pos
    exact transport_pos_fact
  · change (OneBlack.run period baseF.toState).dir = _
    rw [← FState.toState_run]
    change (baseF.run period).dir = baseF.dir
    exact transport_dir_fact
  · intro p hp
    have source : p.sub drift ∈ support := hp
    have accepted := (List.all_eq_true.mp colours) (p.sub drift) source
    have eq := eq_of_beq accepted
    change (OneBlack.run period baseF.toState).black p = _
    rw [← FState.toState_run]
    change (baseF.run period).black.contains p =
      baseF.black.contains (p.sub drift)
    have point : drift.add (p.sub drift) = p := by
      rcases p with ⟨x, y⟩
      simp only [Point.add, Point.sub, Point.mk.injEq]
      constructor <;> omega
    exact (congrArg (baseF.run period).black.contains point).symm.trans eq

theorem reads_at (cycle k : Nat) (hk : k < period) :
    supportAt cycle (OneBlack.run k (reference cycle)).pos := by
  induction cycle with
  | zero => simpa using base_reads k hk
  | succ cycle ih =>
    rw [reference_succ, run_shift]
    simpa [OneBlack.shift] using ih

theorem transport_at (cycle : Nat) :
    SameOn (supportAt (cycle + 1))
      (OneBlack.run period (reference cycle)) (reference (cycle + 1)) := by
  induction cycle with
  | zero => simpa using base_transport
  | succ cycle ih =>
    rw [reference_succ, run_shift, reference_succ]
    simpa using ih.shift drift

theorem base_black_supported {p : Point} (black : base.black p = true) : Support p := by
  have inTree : p ∈ baseF.black := by
    rw [← Std.TreeSet.contains_iff_mem]
    exact black
  have inList : p ∈ baseF.black.toList := Std.TreeSet.mem_toList.mpr inTree
  change p ∈ support
  exact of_decide_eq_true ((List.all_eq_true.mp base_supported_fact) p inList)

theorem reference_white (cycle : Nat) {p : Point} (outside : ¬supportAt cycle p) :
    (reference cycle).black p = false := by
  induction cycle generalizing p with
  | zero =>
    by_cases black : base.black p = true
    · exact (outside (base_black_supported black)).elim
    · cases h : base.black p <;> simp_all
  | succ cycle ih =>
    simp only [reference_succ, OneBlack.shift]
    exact ih (by simpa using outside)

def Separated (source target : Point) : Prop :=
  target.x - target.y ≠ source.x - source.y ∨
  target.x % 2 ≠ source.x % 2 ∨ source.x ≤ target.x

instance (source target : Point) : Decidable (Separated source target) := by
  unfold Separated
  infer_instance

theorem separated_checked {source target : Point}
    (h : separated source target = true) : Separated source target := by
  exact of_decide_eq_true h

theorem back_invariants (target : Point) (n : Nat) :
    let source := back n target
    source.x - source.y = target.x - target.y ∧
    source.x % 2 = target.x % 2 ∧
    source.x = target.x + 2 * n := by
  induction n generalizing target with
  | zero => simp [back]
  | succ n ih =>
    simp only [back]
    rcases ih (target.sub drift) with ⟨diag, parity, horizontal⟩
    simp [Point.sub, drift] at diag parity horizontal ⊢
    constructor <;> omega

theorem separated_excludes {target : Point}
    (all : ∀ source, Support source → Separated source target) :
    ∀ n, 0 < n → ¬supportAt n target := by
  intro n positive inFuture
  let source := back n target
  have hs : Support source := inFuture
  have sep := all source hs
  have inv := back_invariants target n
  dsimp [source] at sep inv
  rcases inv with ⟨diag, parity, horizontal⟩
  rcases sep with h | h | h
  · exact h diag.symm
  · exact h parity.symm
  · omega

theorem base_separation {target : Point} (inside : Support target)
    (outsideNext : ¬supportAt 1 target) :
    ∀ later, 0 < later → ¬supportAt later target := by
  have targetCheck := (List.all_eq_true.mp support_wake_fact) target inside
  have notShifted : target ∉ shiftedSupport := by
    intro member
    rcases List.mem_map.mp member with ⟨source, hs, eq⟩
    subst target
    apply outsideNext
    change Support (back 1 (drift.add source))
    simpa [back] using hs
  have pair : separatedFromSupport target = true := by
    simpa [notShifted] using targetCheck
  apply separated_excludes
  intro source hs
  exact separated_checked ((List.all_eq_true.mp pair) source hs)

theorem separation_at : ∀ cycle p, supportAt cycle p →
    ¬supportAt (cycle + 1) p → ∀ later, cycle < later → ¬supportAt later p := by
  intro cycle
  induction cycle with
  | zero =>
    intro p inside next later positive
    exact base_separation inside next later positive
  | succ cycle ih =>
    intro p inside next later laterBound
    cases later with
    | zero => exact (Nat.not_lt_zero _ laterBound).elim
    | succ later =>
      have inside' : supportAt cycle (p.sub drift) := by simpa using inside
      have next' : ¬supportAt (cycle + 1) (p.sub drift) := by simpa using next
      have bound' : cycle < later := Nat.lt_of_succ_lt_succ laterBound
      simpa using ih (p.sub drift) inside' next' later bound'

def Boundary (cycle : Nat) (s : State) : Prop :=
  SameOn (supportAt cycle) (reference cycle) s ∧
  ∀ p, s.black p = true → ¬supportAt cycle p →
    ∀ later, cycle < later → ¬supportAt later p

theorem Boundary.next {cycle : Nat} {s : State} (h : Boundary cycle s) :
    Boundary (cycle + 1) (OneBlack.run period s) := by
  rcases h with ⟨same, guard⟩
  let current := supportAt cycle
  let next := supportAt (cycle + 1)
  let region := fun p => current p ∨ next p
  have enlarged : SameOn region (reference cycle) s := by
    rcases same with ⟨pos, dir, colours⟩
    refine ⟨pos, dir, ?_⟩
    intro p hp
    rcases hp with hp | hp
    · exact colours p hp
    · by_cases old : current p
      · exact colours p old
      · have refWhite := reference_white cycle old
        by_cases actual : s.black p = true
        · exact (guard p actual old (cycle + 1) (Nat.lt_succ_self cycle) hp).elim
        · cases colour : s.black p <;> simp_all
  have readRegion : ∀ k, k < period → region (OneBlack.run k (reference cycle)).pos :=
    fun k hk => Or.inl (reads_at cycle k hk)
  have after := enlarged.run period readRegion
  have transport := transport_at cycle
  constructor
  · rcases after with ⟨pos, dir, colours⟩
    rcases transport with ⟨tpos, tdir, tcolours⟩
    refine ⟨tpos.symm.trans pos, tdir.symm.trans dir, ?_⟩
    intro p hp
    exact (tcolours p hp).symm.trans (colours p (Or.inr hp))
  · intro p black outside later laterBound
    by_cases old : current p
    · exact separation_at cycle p old outside later
        (Nat.lt_trans (Nat.lt_succ_self cycle) laterBound)
    · have avoids : Avoids p s period := by
        intro k hk eq
        have witnessed := enlarged.run k
          (fun j hj => readRegion j (Nat.lt_trans hj hk))
        apply old
        rw [← eq, ← witnessed.1]
        exact reads_at cycle k hk
      have unchanged := colour_unchanged period avoids
      have before : s.black p = true := unchanged.symm.trans black
      exact guard p before old later
        (Nat.lt_trans (Nat.lt_succ_self cycle) laterBound)

def HasTail (s : State) : Prop :=
  ∀ cycle, Boundary cycle (OneBlack.run (cycle * period) s)

theorem Boundary.tail {s : State} (h : Boundary 0 s) : HasTail s := by
  intro cycle
  induction cycle with
  | zero => simpa [OneBlack.run] using h
  | succ cycle ih =>
    rw [Nat.succ_mul, OneBlack.run_add]
    exact ih.next

theorem Boundary.future_support {s : State} (h : Boundary 0 s) (n : Nat) :
    ∃ cycle, supportAt cycle (OneBlack.run n s).pos := by
  let cycle := n / period
  let phase := n % period
  have periodPositive : 0 < period := by decide
  have phaseBound : phase < period := Nat.mod_lt n periodPositive
  have same := (h.tail cycle).1.run phase (fun k hk =>
    reads_at cycle k (Nat.lt_trans hk phaseBound))
  have decomposition : cycle * period + phase = n := by
    simpa [cycle, phase, Nat.add_comm] using Nat.mod_add_div' n period
  refine ⟨cycle, ?_⟩
  have referenceRead := reads_at cycle phase phaseBound
  rw [same.1] at referenceRead
  rw [← decomposition, OneBlack.run_add]
  exact referenceRead

theorem entry_boundary : Boundary 0 entry := by
  have active : support.all (fun p =>
      entryF.black.contains p == baseF.black.contains p) = true :=
    entry_active_fact
  constructor
  · have pos := entry_pos_fact
    have dir := entry_dir_fact
    refine ⟨by simpa [entry, base, FState.toState] using pos.symm,
      by simpa [entry, base, FState.toState] using dir.symm, ?_⟩
    intro p hp
    exact eq_of_beq ((List.all_eq_true.mp active) p hp) |>.symm
  · intro p black outside later positive
    have inTree : p ∈ entryF.black := by
      rw [← Std.TreeSet.contains_iff_mem]
      exact black
    have inList : p ∈ entryF.black.toList := Std.TreeSet.mem_toList.mpr inTree
    have accepted := (List.all_eq_true.mp entry_background_fact) p inList
    have notSupport : p ∉ support := outside
    have pair : separatedFromSupport p = true := by
      simpa [notSupport] using accepted
    exact separated_excludes (fun source hs =>
      separated_checked ((List.all_eq_true.mp pair) source hs)) later positive

theorem ref_observe (cycle phase : Nat) :
    observe (OneBlack.run phase (reference cycle)) =
      repeatShift drift cycle (observe (OneBlack.run phase base)) := by
  induction cycle with
  | zero => rfl
  | succ cycle ih =>
    rw [reference_succ, run_shift, observe_shift, ih]
    rfl

theorem Boundary.observe {cycle phase : Nat} {s : State} (h : Boundary cycle s)
    (bound : phase < period) :
    observe (OneBlack.run phase s) =
      observe (OneBlack.run phase (reference cycle)) := by
  have same := h.1.run phase (fun k hk =>
    reads_at cycle k (Nat.lt_trans hk bound))
  apply Observation.ext
  · exact same.1.symm
  · exact same.2.1.symm
  · change (OneBlack.run phase s).black (OneBlack.run phase s).pos =
      (OneBlack.run phase (reference cycle)).black
        (OneBlack.run phase (reference cycle)).pos
    rw [← same.1]
    exact (same.2.2 _ (reads_at cycle phase bound)).symm

theorem tail_permanent {s : State} (h : HasTail s) : PermanentP104 s := by
  refine ⟨drift, Or.inl rfl, ?_⟩
  intro cycle phase bound
  have pbound : phase < period := by simpa [period] using bound
  rw [OneBlack.run_add]
  have atCycle := (h cycle).observe pbound
  have atZero := (h 0).observe pbound
  exact atCycle.trans ((ref_observe cycle phase).trans
    (congrArg (repeatShift drift cycle) atZero.symm))

theorem blank_entry_permanent : PermanentP104 entry :=
  tail_permanent entry_boundary.tail

theorem entry_from_white : entry = OneBlack.run entryTime white := by
  calc
    entry = computedEntry.toState := rfl
    _ = (fwhite.run entryTime).toState := congrArg FState.toState computedEntry_exact
    _ = OneBlack.run entryTime fwhite.toState := FState.toState_run _ _
    _ = OneBlack.run entryTime white := congrArg (OneBlack.run entryTime) fwhite_exact

theorem blank_reaches : ReachesP104 white := by
  refine ⟨entryTime, ?_⟩
  rw [← entry_from_white]
  exact blank_entry_permanent

end OneBlack.Highway
