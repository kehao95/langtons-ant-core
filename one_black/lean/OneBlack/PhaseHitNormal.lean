import OneBlack.PhasePreHit

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

theorem actual_hit_exact (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) :
    actualHit.toState = xorState (preHitArchive phaseLag) fixedCore := by
  calc
    actualHit.toState = run
        (duration period localTime phaseLag +
          ((phaseLag + hitCycles) * period + hitPhase))
        (actualInitial phaseHead phaseBaseDepth).toState := by
      unfold actualHit
      exact FState.toState_run _ _
    _ = run (duration period localTime (phaseLag + 0) +
          ((phaseLag + 0 + hitCycles) * period + hitPhase))
        (actualInitial phaseHead (0 + phaseBaseDepth)).toState := by
      congr 3 <;> omega
    _ = xorState (preHitArchive (phaseLag + 0)) fixedCore :=
      pre_hit_exact pristine phase 0

def hitTime (extra : Nat) : Nat :=
  duration period localTime (phaseLag + extra) +
    ((phaseLag + extra + hitCycles) * period + hitPhase)

theorem hit_normal (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    run (hitTime extra)
        (actualInitial phaseHead (extra + phaseBaseDepth)).toState =
      xorState (BRegion.accumulated drift layer extra) actualHit.toState := by
  rw [hitTime, pre_hit_exact pristine phase extra,
    preHitArchive_normal, ← xorState_xor, ← actual_hit_exact pristine phase]

end OneBlack.Phase
