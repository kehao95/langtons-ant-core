import OneBlack.Terminal

namespace OneBlack

def SameOutside (region : Point → Prop) (a b : State) : Prop :=
  a.pos = b.pos ∧ a.dir = b.dir ∧
    ∀ p, ¬region p → a.black p = b.black p

def AvoidsForever (region : Point → Prop) (s : State) : Prop :=
  ∀ n, ¬region (run n s).pos

theorem SameOutside.step {region : Point → Prop} {a b : State}
    (same : SameOutside region a b) (away : ¬region b.pos) :
    SameOutside region (OneBlack.step a) (OneBlack.step b) := by
  rcases same with ⟨position, heading, colours⟩
  cases a with
  | mk ab ap ad =>
    cases b with
    | mk bb bp bd =>
      simp only at position heading colours away
      subst bp; subst bd
      have read := colours ap away
      refine ⟨?_, ?_, ?_⟩
      · simp [OneBlack.step, read]
      · simp [OneBlack.step, read]
      · intro p outside
        by_cases current : p = ap
        · subst p; simp [OneBlack.step, toggle, read]
        · simp [OneBlack.step, toggle, current, colours p outside]

theorem SameOutside.run {region : Point → Prop} {a b : State}
    (same : SameOutside region a b) (avoids : AvoidsForever region b) :
    ∀ n, SameOutside region (run n a) (run n b) := by
  intro n
  induction n with
  | zero => exact same
  | succ n ih =>
      simpa [OneBlack.run] using ih.step (avoids n)

def SameReadTrace (a b : State) : Prop :=
  ∀ n, observe (run n a) = observe (run n b)

theorem sameReadTrace_of_archive {region : Point → Prop} {a b : State}
    (same : SameOutside region a b) (avoids : AvoidsForever region b) :
    SameReadTrace a b := by
  intro n
  have sameAt := same.run avoids n
  apply Observation.ext
  · exact sameAt.1
  · exact sameAt.2.1
  · change (run n a).black (run n a).pos =
      (run n b).black (run n b).pos
    rw [sameAt.1]
    exact sameAt.2.2 _ (avoids n)

theorem SameReadTrace.tail {a b : State} (same : SameReadTrace a b) (cut : Nat) :
    SameReadTrace (run cut a) (run cut b) := by
  intro n
  simpa [← run_add] using same (cut + n)

theorem PermanentP104.of_sameReadTrace {a b : State}
    (same : SameReadTrace a b) (terminal : PermanentP104 b) :
    PermanentP104 a := by
  rcases terminal with ⟨v, standard, repeats⟩
  refine ⟨v, standard, ?_⟩
  intro cycle phase bound
  exact (same _).trans ((repeats cycle phase bound).trans
    (congrArg (repeatShift v cycle) (same phase).symm))

theorem ReachesP104.of_sameReadTrace {a b : State}
    (same : SameReadTrace a b) (reached : ReachesP104 b) : ReachesP104 a := by
  rcases reached with ⟨cut, terminal⟩
  exact ⟨cut, terminal.of_sameReadTrace (same.tail cut)⟩

end OneBlack
