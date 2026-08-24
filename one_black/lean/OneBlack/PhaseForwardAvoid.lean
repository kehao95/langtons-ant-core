import OneBlack.PhaseArchive

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

theorem forward_archive_avoids_reverse (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    AvoidsBFor (BRegion.xor HistoryB
      (BRegion.accumulated drift cleanWake extra))
      (shiftState drift extra reverseBase.toState)
      ((extra + hitCycles) * period + hitPhase) := by
  intro k before
  have historyFalse := history_avoids_reverse_prefix phase extra k before
  have cleanFalse := clean_archive_avoids_reverse pristine phase extra k
  rw [BRegion.xor_apply, historyFalse, cleanFalse]
  rfl

end OneBlack.Phase
