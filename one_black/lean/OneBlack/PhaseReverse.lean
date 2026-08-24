import OneBlack.Phase

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

theorem normalized_forward (s : FState) (source : Point) (copies : Nat) :
    normalizedPoint s (shiftPoint drift copies source) =
      backwardPoint (oppositeTurn (turn s)) copies
        (normalizedPoint s source) := by
  have turns : turn s = 0 ∨ turn s = 1 ∨ turn s = 2 ∨ turn s = 3 := by
    have := turn_bounded s
    omega
  unfold normalizedPoint normalizedAt
  rw [drift_shift]
  rcases offset (s.rotateN (turn s)) with ⟨ox, oy⟩
  rcases source with ⟨x, y⟩
  rcases turns with h | h | h | h <;>
    simp [h, highwayPoint, backwardPoint, oppositeTurn, Point.add,
      Point.rotateN, Point.rot] <;> omega

theorem forward_guard_parts {terminal : FState} {source : Point}
    (checked : forwardGuard terminal source = true) :
    normalizedPoint terminal source ∉ support ∧
    separatedFromSupport (normalizedPoint terminal source) = true ∧
    support.all (fun target =>
      !(raysMeet (oppositeTurn (turn terminal))
        (normalizedPoint terminal source) target)) = true := by
  simp only [forwardGuard, forwardGuardAt, Bool.and_eq_true,
    decide_eq_true_eq] at checked
  exact ⟨checked.1.1, checked.1.2, checked.2⟩

theorem forward_guard_excludes_shift {terminal : FState} {source : Point}
    (accepted : any terminal = true)
    (checked : forwardGuard terminal source = true)
    {copies : Nat} (positive : 0 < copies) (k : Nat) :
    source ≠ (run k (shiftState reverseDrift copies terminal.toState)).pos := by
  intro equal
  have path : shiftPoint drift copies source = (run k terminal.toState).pos := by
    rw [run_shiftState, shiftState_pos] at equal
    rw [equal]
    unfold reverseDrift
    rw [drift_shift, backward_shift]
    rcases source with ⟨sx, sy⟩
    rcases (run k terminal.toState).pos with ⟨px, py⟩
    simp [highwayPoint, Point.mk.injEq] at equal ⊢
  rcases future_normalized accepted (p := (run k terminal.toState).pos)
      ⟨k, rfl⟩ with ⟨cycle, supported⟩
  let target := back cycle (normalizedPoint terminal
    (run k terminal.toState).pos)
  have targetMember : target ∈ support := supported
  have terminalPoint : normalizedPoint terminal
      (run k terminal.toState).pos = highwayPoint cycle target := by
    dsimp [target]
    rw [← drift_shift, Rays.shift_back]
  have sourcePoint : normalizedPoint terminal
      (run k terminal.toState).pos =
      backwardPoint (oppositeTurn (turn terminal)) copies
        (normalizedPoint terminal source) := by
    rw [← path]
    exact normalized_forward terminal source copies
  have guard := forward_guard_parts checked
  have rayFalse : raysMeet (oppositeTurn (turn terminal))
      (normalizedPoint terminal source) target = false := by
    have one := (List.all_eq_true.mp guard.2.2) target targetMember
    simpa using one
  have bounded : oppositeTurn (turn terminal) < 4 := by
    unfold oppositeTurn
    exact Nat.mod_lt _ (by omega)
  exact (rays_disjoint bounded rayFalse copies positive cycle)
    (sourcePoint.symm.trans terminalPoint)

theorem reverse_ray_guard_excludes_shift {terminal : FState} {source : Point}
    (accepted : any terminal = true)
    (checked : reverseRayGuardAt (turn terminal) terminal source = true)
    {copies : Nat} (positive : 0 < copies) (k : Nat) :
    source ≠ (run k (shiftState reverseDrift copies terminal.toState)).pos := by
  intro equal
  have path : shiftPoint drift copies source = (run k terminal.toState).pos := by
    rw [run_shiftState, shiftState_pos] at equal
    rw [equal]
    unfold reverseDrift
    rw [drift_shift, backward_shift]
    rcases source with ⟨sx, sy⟩
    rcases (run k terminal.toState).pos with ⟨px, py⟩
    simp [highwayPoint, Point.mk.injEq] at equal ⊢
  rcases future_normalized accepted (p := (run k terminal.toState).pos)
      ⟨k, rfl⟩ with ⟨cycle, supported⟩
  let target := back cycle (normalizedPoint terminal
    (run k terminal.toState).pos)
  have targetMember : target ∈ support := supported
  have terminalPoint : normalizedPoint terminal
      (run k terminal.toState).pos = highwayPoint cycle target := by
    dsimp [target]
    rw [← drift_shift, Rays.shift_back]
  have sourcePoint : normalizedPoint terminal
      (run k terminal.toState).pos =
      backwardPoint (oppositeTurn (turn terminal)) copies
        (normalizedPoint terminal source) := by
    rw [← path]
    exact normalized_forward terminal source copies
  have rayFalse : raysMeet (oppositeTurn (turn terminal))
      (normalizedPoint terminal source) target = false := by
    have one := (List.all_eq_true.mp checked) target targetMember
    simpa [reverseRayGuardAt] using one
  have bounded : oppositeTurn (turn terminal) < 4 := by
    unfold oppositeTurn
    exact Nat.mod_lt _ (by omega)
  exact (rays_disjoint bounded rayFalse copies positive cycle)
    (sourcePoint.symm.trans terminalPoint)

theorem reverse_block_exact (phase : PhaseChecks.Certificate) :
    run period reverseBase.toState =
      xorState reverseWake (OneBlack.shift reverseDrift reverseBase.toState) := by
  calc
    run period reverseBase.toState = reverseNext.toState := by
      exact (FState.toState_run period reverseBase).symm
    _ = xorState reverseWake reverseShift.toState := by
      change reverseNext.toState =
        xorState (BRegion.ofList reverseWakeSources) reverseShift.toState
      exact difference_exact phase.reversePosition phase.reverseHeading
    _ = xorState reverseWake
        (OneBlack.shift reverseDrift reverseBase.toState) := by
      change xorState reverseWake (reverseBase.shift reverseDrift).toState = _
      rw [FState.toState_shift]

theorem reverse_block (phase : PhaseChecks.Certificate) :
    BlockData reverseBase.toState reverseDrift period reverseWake := by
  refine ⟨reverse_block_exact phase, ?_⟩
  intro copies positive k
  cases present : reverseWake
      (run k (shiftState reverseDrift copies reverseBase.toState)).pos with
  | false => rfl
  | true =>
      exfalso
      have member : (run k
          (shiftState reverseDrift copies reverseBase.toState)).pos ∈
          reverseWakeSources := by
        change decide ((run k
          (shiftState reverseDrift copies reverseBase.toState)).pos ∈
            reverseWakeSources) = true at present
        exact of_decide_eq_true present
      have checked := (List.all_eq_true.mp phase.reverseGuardPass) _ member
      exact reverse_ray_guard_excludes_shift phase.reverseAccepted checked positive k rfl

theorem reverse_prefix_position (phase : PhaseChecks.Certificate)
    (cycles phaseTime : Nat) (bound : phaseTime ≤ period) :
    (run (cycles * period + phaseTime) reverseBase.toState).pos =
      shiftPoint reverseDrift cycles
        (run phaseTime reverseBase.toState).pos := by
  rw [(reverse_block phase).normal_phase cycles phaseTime bound]
  exact shiftState_pos reverseDrift cycles _

theorem shifted_reverse_position (phase : PhaseChecks.Certificate)
    (extra cycles phaseTime : Nat) (bound : phaseTime ≤ period) :
    (run (cycles * period + phaseTime)
      (shiftState drift extra reverseBase.toState)).pos =
      shiftPoint drift extra
        (shiftPoint reverseDrift cycles
          (run phaseTime reverseBase.toState).pos) := by
  rw [run_shiftState, shiftState_pos, reverse_prefix_position phase _ _ bound]

theorem reverse_index_shifted (phase : PhaseChecks.Certificate)
    (extra cycles phaseTime : Nat) (bound : phaseTime ≤ period) :
    reverseIndex (reverseBase.run phaseTime).pos
      (run (cycles * period + phaseTime)
        (shiftState drift extra reverseBase.toState)).pos =
      some ((cycles : Int) - (extra : Int)) := by
  rw [shifted_reverse_position phase extra cycles phaseTime bound]
  have bridge := congrArg State.pos (FState.toState_run phaseTime reverseBase)
  change (reverseBase.run phaseTime).pos =
    (run phaseTime reverseBase.toState).pos at bridge
  rw [← bridge]
  unfold reverseIndex reverseDrift
  rw [drift_shift, backward_shift]
  rcases (reverseBase.run phaseTime).pos with ⟨x, y⟩
  simp [highwayPoint, Point.add, Point.sub]
  constructor
  · constructor <;> omega
  · omega

theorem history_avoids_reverse_prefix (phase : PhaseChecks.Certificate)
    (extra : Nat) :
    AvoidsBFor HistoryB (shiftState drift extra reverseBase.toState)
      ((extra + hitCycles) * period + hitPhase) := by
  intro time earlier
  cases present : HistoryB
      (run time (shiftState drift extra reverseBase.toState)).pos with
  | false => rfl
  | true =>
      exfalso
      have periodPositive : 0 < period := by decide
      let cycles := time / period
      let phaseTime := time % period
      have phaseBound : phaseTime < period := Nat.mod_lt _ periodPositive
      have timeEq : time = cycles * period + phaseTime := by
        simpa [cycles, phaseTime, Nat.mul_comm] using
          (Nat.div_add_mod time period).symm
      have oldMember : (run time
          (shiftState drift extra reverseBase.toState)).pos ∈ historyCells := by
        simpa [HistoryB, BRegion.ofList] using present
      have phaseChecked := (List.all_eq_true.mp phase.firstHitPass) phaseTime
        (List.mem_range.mpr phaseBound)
      have checked := (List.all_eq_true.mp phaseChecked) _ oldMember
      rw [timeEq, reverse_index_shifted phase extra cycles phaseTime
        (Nat.le_of_lt phaseBound)] at checked
      have lower := of_decide_eq_true checked
      unfold hitCycles hitPhase at earlier lower
      change time < (extra + 10) * period + 89 at earlier
      unfold period at earlier timeEq
      rw [timeEq] at earlier
      omega


end OneBlack.Phase
