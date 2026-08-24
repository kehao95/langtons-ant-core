import OneBlack.PhaseReverse

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

theorem archive_contains_shift {v : Point} {wake : Region}
    {source : Point} (inside : wake source) : ∀ {copies total : Nat},
    copies < total → archive v wake total (shiftPoint v copies source) := by
  intro copies total before
  induction total generalizing copies with
  | zero => omega
  | succ total ih =>
      cases copies with
      | zero => exact Or.inl inside
      | succ copies =>
          apply Or.inr
          change archive v wake total
            ((v.add (shiftPoint v copies source)).sub v)
          simpa using ih (Nat.lt_of_succ_lt_succ before)



end OneBlack.Phase
