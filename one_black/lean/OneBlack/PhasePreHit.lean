import OneBlack.PhaseAlgebra

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

theorem pre_hit_exact (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    run (duration period localTime (phaseLag + extra) +
        ((phaseLag + extra + hitCycles) * period + hitPhase))
        (actualInitial phaseHead (extra + phaseBaseDepth)).toState =
      xorState (preHitArchive (phaseLag + extra)) fixedCore := by
  rw [run_add, forward_actual_exact pristine phase extra,
    run_xorState _ (forward_archive_avoids_reverse pristine phase
      (phaseLag + extra)),
    run_shiftState,
    (reverse_block phase).normal_phase (phaseLag + extra + hitCycles) hitPhase
      (by unfold hitPhase period; omega),
    shiftState_xorState, shifted_reverse_net,
    xorState_xor]
  rfl


end OneBlack.Phase
