import OneBlack.Core

namespace OneBlack

structure Observation where
  pos : Point
  dir : Heading
  black : Bool
deriving DecidableEq, Repr

@[ext] theorem Observation.ext {a b : Observation} (pos : a.pos = b.pos)
    (dir : a.dir = b.dir) (black : a.black = b.black) : a = b := by
  cases a; cases b; simp_all

def observe (s : State) : Observation := ⟨s.pos, s.dir, s.black s.pos⟩
def Observation.shift (v : Point) (o : Observation) : Observation :=
  ⟨v.add o.pos, o.dir, o.black⟩
def Observation.rot (o : Observation) : Observation :=
  ⟨o.pos.rot, o.dir.rot, o.black⟩

def repeatShift (v : Point) : Nat → Observation → Observation
  | 0, o => o
  | n + 1, o => (repeatShift v n o).shift v

def highwayDrift : Point := ⟨-2, -2⟩

def StandardDrift (v : Point) : Prop :=
  v = highwayDrift ∨ v = highwayDrift.rot ∨
  v = highwayDrift.rot.rot ∨ v = highwayDrift.rot.rot.rot

def PermanentP104 (s : State) : Prop :=
  ∃ v, StandardDrift v ∧ ∀ cycle phase, phase < 104 →
    observe (run (cycle * 104 + phase) s) =
      repeatShift v cycle (observe (run phase s))

def ReachesP104 (s : State) : Prop := ∃ n, PermanentP104 (run n s)

def ExactlyOneBlack (s : State) : Prop :=
  ∃ p, ∀ q, s.black q = decide (q = p)

@[simp] theorem observe_shift (v : Point) (s : State) :
    observe (shift v s) = (observe s).shift v := by
  cases s; simp [observe, shift, Observation.shift]

@[simp] theorem observe_rotate (s : State) :
    observe (rotate s) = (observe s).rot := by
  cases s; simp [observe, rotate, Observation.rot]

theorem Observation.shift_comm (u v : Point) (o : Observation) :
    (o.shift u).shift v = (o.shift v).shift u := by
  cases u; cases v; cases o with
  | mk p d b => cases p; simp [Observation.shift, Point.add]; omega

theorem Observation.shift_repeat (u v : Point) (n : Nat) (o : Observation) :
    (repeatShift v n o).shift u = repeatShift v n (o.shift u) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [repeatShift]
    rw [Observation.shift_comm v u, ih]

theorem Observation.rot_shift (v : Point) (o : Observation) :
    (o.shift v).rot = o.rot.shift v.rot := by
  cases v; cases o with
  | mk p d b => cases p; simp [Observation.shift, Observation.rot, Point.add,
      Point.rot]; omega

theorem Observation.rot_repeat (v : Point) (n : Nat) (o : Observation) :
    (repeatShift v n o).rot = repeatShift v.rot n o.rot := by
  induction n with
  | zero => rfl
  | succ n ih => simp [repeatShift, Observation.rot_shift, ih]

theorem StandardDrift.rot {v : Point} (h : StandardDrift v) :
    StandardDrift v.rot := by
  rcases h with h | h | h | h
  · exact Or.inr (Or.inl (congrArg Point.rot h))
  · exact Or.inr (Or.inr (Or.inl (congrArg Point.rot h)))
  · exact Or.inr (Or.inr (Or.inr (congrArg Point.rot h)))
  · left; rw [h]; rfl

theorem PermanentP104.shift (v : Point) {s : State} (h : PermanentP104 s) :
    PermanentP104 (OneBlack.shift v s) := by
  rcases h with ⟨d, standard, trace⟩
  refine ⟨d, standard, ?_⟩
  intro cycle phase bound
  rw [run_shift, observe_shift, trace cycle phase bound, run_shift, observe_shift]
  exact Observation.shift_repeat v d cycle _

theorem PermanentP104.rot {s : State} (h : PermanentP104 s) :
    PermanentP104 (rotate s) := by
  rcases h with ⟨d, standard, trace⟩
  refine ⟨d.rot, standard.rot, ?_⟩
  intro cycle phase bound
  rw [run_rotate, observe_rotate, trace cycle phase bound, run_rotate,
    observe_rotate]
  exact Observation.rot_repeat d cycle _

theorem PermanentP104.rotateN (n : Nat) {s : State} (h : PermanentP104 s) :
    PermanentP104 (OneBlack.rotateN n s) := by
  induction n with
  | zero => exact h
  | succ n ih => exact ih.rot

@[simp] theorem rotate_four (s : State) :
    rotate (rotate (rotate (rotate s))) = s := by
  cases s with
  | mk black pos dir =>
    apply State.ext
    · funext p
      rcases p with ⟨x, y⟩
      simp [rotate, Point.unrot]
    · rcases pos with ⟨x, y⟩
      simp [rotate, Point.rot]
    · cases dir <;> simp [rotate, Heading.rot]

theorem ReachesP104.shift (v : Point) {s : State} (h : ReachesP104 s) :
    ReachesP104 (OneBlack.shift v s) := by
  rcases h with ⟨n, terminal⟩
  exact ⟨n, by rw [run_shift]; exact terminal.shift v⟩

theorem ReachesP104.rot {s : State} (h : ReachesP104 s) :
    ReachesP104 (rotate s) := by
  rcases h with ⟨n, terminal⟩
  exact ⟨n, by rw [run_rotate]; exact terminal.rot⟩

theorem ReachesP104.rotateN (turns : Nat) {s : State} (h : ReachesP104 s) :
    ReachesP104 (OneBlack.rotateN turns s) := by
  induction turns with
  | zero => exact h
  | succ turns ih => exact ih.rot

def SameExcept (p : Point) (a b : State) : Prop :=
  a.pos = b.pos ∧ a.dir = b.dir ∧
  (∀ q, q ≠ p → a.black q = b.black q) ∧ a.black p = !(b.black p)

def Avoids (p : Point) (s : State) (n : Nat) : Prop :=
  ∀ k, k < n → (run k s).pos ≠ p

theorem sameExcept_step {p : Point} {a b : State} (same : SameExcept p a b)
    (away : a.pos ≠ p) : SameExcept p (step a) (step b) := by
  rcases same with ⟨pos, dir, colours, opposite⟩
  cases a with
  | mk ab ap ad =>
    cases b with
    | mk bb bp bd =>
      simp only at pos dir colours opposite away
      subst bp; subst bd
      have read : ab ap = bb ap := colours ap away
      refine ⟨?_, ?_, ?_, ?_⟩
      · simp [step, read]
      · simp [step, read]
      · intro q neq
        by_cases current : q = ap
        · subst q; simp [step, toggle, read]
        · simp [step, toggle, current, colours q neq]
      · have neq : p ≠ ap := Ne.symm away
        simp [step, toggle, neq, opposite]

theorem sameExcept_run {p : Point} {a b : State} (n : Nat)
    (same : SameExcept p a b) (avoids : Avoids p a n) :
    SameExcept p (run n a) (run n b) := by
  induction n with
  | zero => simpa [run] using same
  | succ n ih =>
    have shorter : Avoids p a n := fun k hk => avoids k (Nat.lt.step hk)
    have current : (run n a).pos ≠ p := avoids n (Nat.lt_succ_self n)
    simpa [run] using sameExcept_step (ih shorter) current

def blacken (p : Point) (s : State) : State :=
  { s with black := fun q => if q = p then true else s.black q }

theorem colour_unchanged {p : Point} {s : State} (n : Nat)
    (away : Avoids p s n) : (run n s).black p = s.black p := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have shorter : Avoids p s n := fun k hk => away k (Nat.lt_succ_of_lt hk)
    have current : (run n s).pos ≠ p := away n (Nat.lt_succ_self n)
    simpa [run, step, toggle, current.symm] using ih shorter

theorem white_singleton_except (p : Point) : SameExcept p white (singleton p) := by
  refine ⟨rfl, rfl, ?_, ?_⟩
  · intro q neq; simp [white, singleton, neq]
  · simp [white, singleton]

theorem unread_singleton (p : Point) (n : Nat) (away : Avoids p white n) :
    run n (singleton p) = blacken p (run n white) := by
  have same := sameExcept_run n (white_singleton_except p) away
  have whiteAt : (run n white).black p = false := by
    simpa [white] using colour_unchanged n away
  rcases same with ⟨pos, dir, colours, opposite⟩
  apply State.ext
  · funext q
    by_cases eq : q = p
    · subst q; simp [blacken, whiteAt] at opposite ⊢; exact opposite
    · simp [blacken, eq, colours q eq]
  · exact pos.symm
  · exact dir.symm

def singletonAt (cell pos : Point) (dir : Heading) : State :=
  ⟨fun q => decide (q = cell), pos, dir⟩

theorem exactlyOneBlack_iff (s : State) :
    ExactlyOneBlack s ↔ ∃ cell, s = singletonAt cell s.pos s.dir := by
  constructor
  · rintro ⟨cell, colours⟩
    refine ⟨cell, ?_⟩
    apply State.ext
    · funext q; exact colours q
    · rfl
    · rfl
  · rintro ⟨cell, h⟩
    rw [h]
    exact ⟨cell, fun q => rfl⟩

end OneBlack
