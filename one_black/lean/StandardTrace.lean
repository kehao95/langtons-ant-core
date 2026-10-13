import OneBlack

namespace OneBlack

/-- A symmetry placement preserves the entire fixed template, including debris. -/
inductive PlacedTemplate (template : State) : State → Prop
  | canonical : PlacedTemplate template template
  | shifted (v : Point) {s : State} : PlacedTemplate template s →
      PlacedTemplate template (shift v s)
  | rotated {s : State} : PlacedTemplate template s →
      PlacedTemplate template (rotate s)

def HasStandardTrace (s : State) : Prop :=
  ∃ placed, PlacedTemplate (run 9977 white) placed ∧ SameReadTrace s placed

theorem repeatShift_black (v : Point) (n : Nat) (o : Observation) :
    (repeatShift v n o).black = o.black := by
  induction n with
  | zero => rfl
  | succ n ih => exact ih

theorem PermanentP104.read_word {s : State} (h : PermanentP104 s) (k : Nat) :
    (observe (run k s)).black =
      (observe (run (k % 104) (run 9977 white))).black := by
  rcases h with ⟨v, _, repeats, word⟩
  have bound : k % 104 < 104 := Nat.mod_lt _ (by decide)
  have eq := congrArg Observation.black (repeats (k / 104) (k % 104) bound)
  have split : k / 104 * 104 + k % 104 = k := by omega
  rw [split, repeatShift_black] at eq
  exact eq.trans (word _ bound)

theorem same_trace_of_read_colours {a b : State}
    (pos : a.pos = b.pos) (dir : a.dir = b.dir)
    (colours : ∀ k, (observe (run k a)).black = (observe (run k b)).black) :
    SameReadTrace a b := by
  have poses : ∀ k, (run k a).pos = (run k b).pos ∧
      (run k a).dir = (run k b).dir := by
    intro k
    induction k with
    | zero => exact ⟨pos, dir⟩
    | succ k ih =>
      have colour := colours k
      change (run k a).black (run k a).pos = (run k b).black (run k b).pos at colour
      simp only [run, step]
      rw [colour, ih.1, ih.2]
      exact ⟨rfl, rfl⟩
  intro k
  exact Observation.ext (poses k).1 (poses k).2 (colours k)

theorem align_heading (s : State) (d : Heading) :
    ∃ turns, (rotateN turns s).dir = d := by
  cases s with
  | mk black pos dir =>
    cases dir <;> cases d <;> first
      | exact ⟨0, rfl⟩
      | exact ⟨1, rfl⟩
      | exact ⟨2, rfl⟩
      | exact ⟨3, rfl⟩

theorem PlacedTemplate.rotateN {template s : State}
    (h : PlacedTemplate template s) (n : Nat) :
    PlacedTemplate template (OneBlack.rotateN n s) := by
  induction n with
  | zero => exact h
  | succ n ih => exact .rotated ih

/-- The strengthened terminal predicate entails the full fixed blank read trace,
not only matching periods or a matching displacement. -/
theorem PermanentP104.standard_trace {s : State} (h : PermanentP104 s) :
    HasStandardTrace s := by
  let template := run 9977 white
  have base : PermanentP104 template := by
    change PermanentP104 (run Highway.entryTime white)
    rw [← Highway.entry_from_white]
    exact Highway.blank_entry_permanent
  obtain ⟨turns, direction⟩ := align_heading template s.dir
  let rotated := OneBlack.rotateN turns template
  let offset := s.pos.sub rotated.pos
  let placed := OneBlack.shift offset rotated
  have placedTerminal : PermanentP104 placed := (base.rotateN turns).shift offset
  refine ⟨placed, .shifted offset ((PlacedTemplate.canonical).rotateN turns), ?_⟩
  apply same_trace_of_read_colours
  · change s.pos = (s.pos.sub rotated.pos).add rotated.pos
    cases hp : s.pos; cases hq : rotated.pos
    simp [Point.sub, Point.add]
  · exact direction.symm
  · intro k
    exact (h.read_word k).trans (placedTerminal.read_word k).symm

theorem universal_one_black_standard_trace (s : State) (one : ExactlyOneBlack s) :
    ∃ n, HasStandardTrace (run n s) := by
  obtain ⟨n, terminal⟩ := universal_one_black s one
  exact ⟨n, terminal.standard_trace⟩

#print axioms universal_one_black
#print axioms universal_one_black_standard_trace
end OneBlack
