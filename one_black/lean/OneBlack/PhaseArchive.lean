import OneBlack.PhaseHit

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

theorem clean_archive_avoids_reverse (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra k : Nat) :
    BRegion.accumulated drift cleanWake extra
      (run k (shiftState drift extra reverseBase.toState)).pos = false := by
  cases present : BRegion.accumulated drift cleanWake extra
      (run k (shiftState drift extra reverseBase.toState)).pos with
  | false => rfl
  | true =>
      exfalso
      rcases BRegion.accumulated_member present with
        ⟨source, copies, before, wakeIn, equal⟩
      have wakeMember : source ∈ wakeCells := by
        change decide (source ∈ wakeCells) = true at wakeIn
        exact of_decide_eq_true wakeIn
      have archived : archive drift Wake extra
          (run k (shiftState drift extra reverseBase.toState)).pos := by
        rw [equal]
        exact archive_contains_shift wakeMember before
      have future : shiftRegion drift extra (Corridor phaseHead)
          (run k (shiftState drift extra reverseBase.toState)).pos := by
        rw [← futureReads_shiftState]
        exact ⟨k, rfl⟩
      have disjoint := stable_archive_misses pristine phase.phaseMember extra
      exact disjoint _ archived future


end OneBlack.Phase
