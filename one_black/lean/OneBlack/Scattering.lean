import OneBlack.PhaseTail

namespace OneBlack.Scattering

open OneBlack Highway Induction Pristine PristineChecks ActualChecks
  PhaseChecks

/-- The complete single-defect scattering spectrum of the canonical P104
frontier: 21 returning channels and one affine reverse-highway channel. -/
structure Classification : Prop where
  channelCount : heads.length = 22
  ordinaryCount : ordinaryHeads.length = 21
  partition : ∀ {head}, head ∈ heads →
    head ∈ ordinaryHeads ∨ head = phaseHead
  ordinaryReturn : ∀ {head}, head ∈ ordinaryHeads → ∀ {depth}, 0 < depth →
    ReachesP104 (blacken (obstacle head depth) entry)
  exceptionalReverse :
    run period reverseBase.toState =
      xorState reverseWake (OneBlack.shift reverseDrift reverseBase.toState)
  exceptionalForward : ∀ extra,
    run (duration period localTime (phaseLag + extra))
        (actualInitial phaseHead (extra + phaseBaseDepth)).toState =
      xorState (BRegion.xor Phase.HistoryB
        (BRegion.accumulated drift cleanWake (phaseLag + extra)))
        (shiftState drift (phaseLag + extra) reverseBase.toState)
  exceptionalAffine : ∀ extra,
    run (Phase.hitTime extra)
        (actualInitial phaseHead (extra + phaseBaseDepth)).toState =
      xorState (BRegion.accumulated drift layer extra) actualHit.toState
  exceptionalReturn : ∀ {depth}, 0 < depth →
    ReachesP104 (blacken (obstacle phaseHead depth) entry)

theorem single_defect_scattering (pristine : PristineChecks.Certificate)
    (actual : ActualChecks.Certificate) (phase : PhaseChecks.Certificate) :
    Classification := by
  refine {
    channelCount := pristine.headCount
    ordinaryCount := actual.ordinaryCount
    partition := ?_
    ordinaryReturn := ?_
    exceptionalReverse := Phase.reverse_block_exact phase
    exceptionalForward := Phase.forward_actual_exact pristine phase
    exceptionalAffine := Phase.hit_normal pristine phase
    exceptionalReturn := Phase.lane_reaches pristine actual phase
  }
  · intro head member
    by_cases exceptional : head = phaseHead
    · exact Or.inr exceptional
    · apply Or.inl
      rw [ordinaryHeads, List.mem_filter]
      exact ⟨member, decide_eq_true exceptional⟩
  · intro head ordinary depth positive
    exact Ordinary.lane_reaches pristine actual
      (List.mem_filter.mp ordinary).1 ordinary positive

theorem lane_reaches (spectrum : Classification) {head : Point}
    (member : head ∈ heads) {depth : Nat} (positive : 0 < depth) :
    ReachesP104 (blacken (obstacle head depth) entry) := by
  rcases spectrum.partition member with ordinary | exceptional
  · exact spectrum.ordinaryReturn ordinary positive
  · subst head
    exact spectrum.exceptionalReturn positive

end OneBlack.Scattering
