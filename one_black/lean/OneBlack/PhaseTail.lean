import OneBlack.PhaseHitNormal

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

theorem raw_layer_candidate {p : Point}
    (present : rawLayerWith (stableResult phaseHead) p = true) :
    p ∈ (wakeCells ++ reverseWakeSources.map (drift.add ·)).eraseDups := by
  simp only [PhaseChecks.rawLayerWith, BRegion.xor_apply] at present
  have either : cleanWake p = true ∨ BRegion.iterate drift 1 reverseWake p = true := by
    cases clean : cleanWake p <;> cases reverse :
        BRegion.iterate drift 1 reverseWake p <;>
        simp_all
  rcases either with clean | reverse
  ·
    rw [List.mem_eraseDups]
    exact List.mem_append.mpr (Or.inl (by
      change decide (p ∈ wakeCells) = true at clean
      exact of_decide_eq_true clean))
  · have sourceMember : p.sub drift ∈ reverseWakeSources := by
      change reverseWake (p.sub drift) = true at reverse
      change decide (p.sub drift ∈ reverseWakeSources) = true at reverse
      exact of_decide_eq_true reverse
    rw [List.mem_eraseDups]
    apply List.mem_append.mpr
    apply Or.inr
    apply List.mem_map.mpr
    exact ⟨p.sub drift, sourceMember, Point.add_sub drift p⟩

theorem layer_candidate {p : Point} (present : layer p = true) :
    p ∈ layerCandidates := by
  rcases BRegion.iterate_member present with ⟨source, sourceIn, equal⟩
  apply List.mem_map.mpr
  exact ⟨source, raw_layer_candidate sourceIn, equal.symm⟩

theorem layer_iff_mem {p : Point} : layer p = true ↔ p ∈ layerSources := by
  change layer p = true ↔ p ∈ layerCandidates.filter fun p => layer p
  rw [List.mem_filter]
  exact ⟨fun present => ⟨layer_candidate present, present⟩, fun pair => pair.2⟩

theorem trace_guard_parts (phase : PhaseChecks.Certificate)
    {source target : Point} (sourceIn : layer source = true)
    (targetIn : target ∈ postReads.toList) :
    source ≠ target ∧ raysMeet 0 target source = false := by
  have checkedSource := (List.all_eq_true.mp phase.traceGuardPass) source
    (layer_iff_mem.mp sourceIn)
  have checked := (List.all_eq_true.mp checkedSource) target targetIn
  simp only [Bool.and_eq_true, decide_eq_true_eq] at checked
  have rayFalse : raysMeet 0 target source = false := by
    cases value : raysMeet 0 target source <;> simp_all
  exact ⟨checked.1, rayFalse⟩

theorem layer_avoids_post_trace (phase : PhaseChecks.Certificate)
    (extra : Nat) :
    AvoidsBFor (BRegion.accumulated drift layer extra)
      actualHit.toState postHitTime := by
  intro k before
  cases present : BRegion.accumulated drift layer extra
      (run k actualHit.toState).pos with
  | false => rfl
  | true =>
      exfalso
      rcases BRegion.accumulated_member present with
        ⟨source, copies, copiesBound, sourceIn, equal⟩
      have readF : (run k actualHit.toState).pos ∈ actualHit.reads postHitTime :=
        (FState.mem_reads_iff _ _ _).mpr ⟨k, before, by
          exact congrArg State.pos (FState.toState_run k actualHit)⟩
      have targetIn : (run k actualHit.toState).pos ∈ postReads.toList := by
        apply Std.TreeSet.mem_toList.mpr
        unfold postReads postHit
        exact (replay_reads _ postHitTime actualHit).mpr readF
      have guard := trace_guard_parts phase sourceIn targetIn
      cases copies with
      | zero =>
          apply guard.1
          simpa [shiftPoint] using equal.symm
      | succ copies =>
          exact ray_excludes_shift guard.2 (Nat.zero_lt_succ copies) equal

theorem post_final_exact : postFinal.toState =
    run postHitTime actualHit.toState := by
  unfold postFinal postHit
  rw [replay_final]
  exact FState.toState_run _ _

theorem forward_guard_excludes_forward {terminal : FState} {source : Point}
    (accepted : any terminal = true)
    (checked : forwardGuard terminal source = true)
    {copies : Nat} (positive : 0 < copies) (k : Nat) :
    shiftPoint drift copies source ≠ (run k terminal.toState).pos := by
  intro equal
  apply forward_guard_excludes_shift accepted checked positive k
  rw [run_shiftState, shiftState_pos]
  rw [← equal]
  unfold reverseDrift
  rw [drift_shift, backward_shift]
  rcases source with ⟨x, y⟩
  simp [highwayPoint]

theorem layer_avoids_post_future (phase : PhaseChecks.Certificate)
    (extra : Nat) :
    AvoidsForever (fun p =>
      BRegion.accumulated drift layer extra p = true) postFinal.toState := by
  intro k present
  rcases BRegion.accumulated_member present with
    ⟨source, copies, _, sourceIn, equal⟩
  have checked := (List.all_eq_true.mp phase.terminalGuardPass) source
    (layer_iff_mem.mp sourceIn)
  cases copies with
  | zero =>
      have guard := forward_guard_parts checked
      apply future_excluded phase.postAccepted guard.1 guard.2.1
      exact ⟨k, by simpa [shiftPoint] using equal⟩
  | succ copies =>
      exact forward_guard_excludes_forward phase.postAccepted checked
        (Nat.zero_lt_succ copies) k equal.symm

theorem hit_family_reaches (phase : PhaseChecks.Certificate) (extra : Nat) :
    ReachesP104
      (xorState (BRegion.accumulated drift layer extra) actualHit.toState) := by
  refine ⟨postHitTime, ?_⟩
  rw [run_xorState _ (layer_avoids_post_trace phase extra)]
  rw [← post_final_exact]
  apply (any_permanent phase.postAccepted).of_sameReadTrace
  exact sameReadTrace_of_archive
    (xorState_sameOutside _ _)
    (layer_avoids_post_future phase extra)

theorem tail_reaches (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    ReachesP104 (actualInitial phaseHead (extra + phaseBaseDepth)).toState := by
  rcases hit_family_reaches phase extra with ⟨tail, permanent⟩
  refine ⟨hitTime extra + tail, ?_⟩
  rw [run_add, hit_normal pristine phase extra]
  exact permanent

theorem lane_reaches (pristine : PristineChecks.Certificate)
    (actual : ActualChecks.Certificate) (phase : PhaseChecks.Certificate)
    {depth : Nat} (positive : 0 < depth) :
    ReachesP104 (blacken (obstacle phaseHead depth) entry) := by
  have cutoffEq : actualCutoff phaseHead = phaseBaseDepth := actual.phaseCutoff
  by_cases shallow : depth < phaseBaseDepth
  · apply Ordinary.shallow_reaches actual phase.phaseMember positive
    simpa [cutoffEq] using shallow
  · have phaseLe : phaseBaseDepth ≤ depth := Nat.le_of_not_gt shallow
    have reached := tail_reaches pristine phase (depth - phaseBaseDepth)
    have depthEq : depth - phaseBaseDepth + phaseBaseDepth = depth := by omega
    rw [depthEq] at reached
    simpa [actualInitial, force_toState] using reached

end OneBlack.Phase
