import OneBlack.PhaseChecks

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

abbrev HistoryB : BRegion := BRegion.ofList historyCells

theorem clean_block_exact :
    run period base = xorState cleanWake (OneBlack.shift drift base) := by
  apply State.ext
  · funext p
    unfold base
    rw [← FState.toState_run]
    change (baseF.run period).black.contains p = Bool.xor
      (cleanWake p) (baseF.black.contains (p.sub drift))
    by_cases changed : p ∈ wakeCells
    · have filtered := (List.mem_filter.mp changed).2
      change ((baseF.run period).black.contains p !=
        shiftedBaseColour p) = true at filtered
      have archive : cleanWake p = true := by
        simp [PhaseChecks.cleanWake, BRegion.ofList, changed]
      rw [archive]
      cases left : (baseF.run period).black.contains p <;>
        cases right : baseF.black.contains (p.sub drift) <;>
          simp_all [shiftedBaseColour]
    · have same := clean_block.2.2 p changed
      unfold base at same
      rw [← FState.toState_run] at same
      change (baseF.run period).black.contains p =
        baseF.black.contains (p.sub drift) at same
      have archive : cleanWake p = false := by
        simp [PhaseChecks.cleanWake, BRegion.ofList, changed]
      simpa [archive] using same
  · exact clean_block.1
  · exact clean_block.2.1

theorem wake_misses_obstacle (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    cleanWake (shiftPoint drift (extra + 1) (obstacle phaseHead phaseDepth)) = false := by
  cases present : cleanWake
      (shiftPoint drift (extra + 1) (obstacle phaseHead phaseDepth)) with
  | false => rfl
  | true =>
      exfalso
      have wakeMember : shiftPoint drift (extra + 1)
          (obstacle phaseHead phaseDepth) ∈ wakeCells := by
        simpa [PhaseChecks.cleanWake, BRegion.ofList] using present
      have headSupport := (head_iff.mp phase.phaseMember).1
      have checked := (stable_wake_checked pristine phase.phaseMember wakeMember).1
      have falseRay : raysMeet 0
          (shiftPoint drift (extra + 1) (obstacle phaseHead phaseDepth)) phaseHead = false := by
        simpa using (List.all_eq_true.mp checked) phaseHead headSupport
      apply ray_excludes_shift falseRay (copies := extra + 1 + phaseDepth) (by
        rw [phase.pristineCutoff]
        omega)
      unfold obstacle
      rw [← shiftPoint_add]

theorem clean_recurrence_exact (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    run period (lane base drift (obstacle phaseHead phaseDepth) (extra + 1)) =
      xorState cleanWake
        (OneBlack.shift drift
          (lane base drift (obstacle phaseHead phaseDepth) extra)) := by
  unfold lane
  rw [run_blacken period
      ((lane_data pristine phase.phaseMember).cleanAvoids extra),
    clean_block_exact,
    blacken_xorState _ _ _ (wake_misses_obstacle pristine phase extra),
    shift_blacken]
  congr 3

theorem clean_wake_avoids_tail (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    AvoidsBFor cleanWake
      (OneBlack.shift drift
        (lane base drift (obstacle phaseHead phaseDepth) extra))
      (duration period localTime extra) := by
  have normal := Induction.exact (lane_data pristine phase.phaseMember) extra
  have disjoint := (lane_data pristine phase.phaseMember).wakeMisses extra
  intro k before
  cases present : cleanWake
      (run k (OneBlack.shift drift
        (lane base drift (obstacle phaseHead phaseDepth) extra))).pos with
  | false => rfl
  | true =>
      exfalso
      apply disjoint _ (by
        simpa [PhaseChecks.cleanWake, BRegion.ofList] using present)
      have readShifted : reads
          (OneBlack.shift drift
            (lane base drift (obstacle phaseHead phaseDepth) extra))
          (duration period localTime extra)
          (run k (OneBlack.shift drift
            (lane base drift (obstacle phaseHead phaseDepth) extra))).pos :=
        ⟨k, before, rfl⟩
      unfold PhaseChecks.localTime at readShifted
      rw [reads_shift, normal.readSet] at readShifted
      exact readShifted

theorem pristine_exact (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) : ∀ extra,
    run (duration period localTime extra)
        (lane base drift (obstacle phaseHead phaseDepth) extra) =
      xorState (BRegion.accumulated drift cleanWake extra)
        (shiftState drift extra reverseBase.toState) := by
  intro extra
  induction extra with
  | zero =>
      unfold PhaseChecks.localTime PhaseChecks.reverseBase
      unfold duration
      simp only [Nat.zero_mul, Nat.zero_add]
      change run (stableTime phaseHead)
          (lane base drift (obstacle phaseHead phaseDepth) 0) =
        xorState (BRegion.accumulated drift cleanWake 0)
          (shiftState drift 0 (stableFinal phaseHead).toState)
      rw [BRegion.accumulated, shiftState, xorState_empty]
      exact (stable_final phaseHead).symm
  | succ extra ih =>
      rw [show duration period localTime (extra + 1) =
          period + duration period localTime extra by
            simp [duration, Nat.add_mul, Nat.add_comm,
              Nat.add_left_comm],
        run_add, clean_recurrence_exact pristine phase extra,
        run_xorState _ (clean_wake_avoids_tail pristine phase extra),
        run_shift, ih, shift_xorState, xorState_xor]
      rfl

theorem phase_trace_parts (phase : PhaseChecks.Certificate)
    {historical : Point} (old : History historical) :
    (stableResult phaseHead).2.toList.all
      (fun source => !(shiftedAtLeast phaseLag historical source)) = true := by
  have member := history_iff_mem.mp old
  have checked := (List.all_eq_true.mp phase.phaseTracePass) historical member
  simpa [phaseTraceGuard, Bool.not_eq_true] using checked

theorem history_misses_base_shift (phase : PhaseChecks.Certificate)
    {historical source : Point} (old : History historical)
    (baseRead : BaseReads phaseHead source) {copies : Nat}
    (lower : phaseLag ≤ copies) :
    historical ≠ shiftPoint drift copies source := by
  intro equal
  have recorded := base_read_recorded baseRead
  have checked := (List.all_eq_true.mp (phase_trace_parts phase old))
    source recorded
  have absent : shiftedAtLeast phaseLag historical source = false := by
    simpa using checked
  rw [shiftedAtLeast_complete lower equal] at absent
  contradiction

theorem history_misses_pristine (phase : PhaseChecks.Certificate) (extra : Nat) :
    Region.Disjoint History
      (footprint drift CleanReads (BaseReads phaseHead) (phaseLag + extra)) := by
  intro historical old inside
  rcases footprint_cases inside with clean | baseRead
  · rcases clean with ⟨source, read, copies, _, equal⟩
    exact history_misses_clean_shift old read copies equal
  · rcases baseRead with ⟨source, read, equal⟩
    exact history_misses_base_shift phase old read (by omega) equal

theorem history_avoids_pristine (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    AvoidsBFor HistoryB
      (lane base drift (obstacle phaseHead phaseDepth) (phaseLag + extra))
      (duration period localTime (phaseLag + extra)) := by
  have normal := Induction.exact (lane_data pristine phase.phaseMember)
    (phaseLag + extra)
  intro k before
  cases present : HistoryB
      (run k (lane base drift (obstacle phaseHead phaseDepth)
        (phaseLag + extra))).pos with
  | false => rfl
  | true =>
      exfalso
      apply history_misses_pristine phase extra _
        (history_iff_mem.mpr (by
          simpa [HistoryB, BRegion.ofList] using present))
      rw [← normal.readSet]
      exact ⟨k, before, rfl⟩

theorem entry_exact : entry = xorState HistoryB base := by
  apply State.ext
  · funext p
    cases present : HistoryB p with
    | false =>
        have outside : ¬History p := by
          intro old
          have member := history_iff_mem.mp old
          simp [HistoryB, BRegion.ofList, member] at present
        simpa [xorState, present] using entry_same_base.2.2 p outside
    | true =>
        have old : History p := history_iff_mem.mpr (by
          simpa [HistoryB, BRegion.ofList] using present)
        have baseWhite : base.black p = false := by
          cases colour : base.black p with
          | false => rfl
          | true => exact (old.2 (base_black_supported colour)).elim
        simp [xorState, present, old.1, baseWhite]
  · exact entry_pos_fact
  · exact entry_dir_fact

theorem history_misses_obstacle (phase : PhaseChecks.Certificate) (extra : Nat) :
    HistoryB (obstacle phaseHead (extra + phaseBaseDepth)) = false := by
  cases present : HistoryB (obstacle phaseHead (extra + phaseBaseDepth)) with
  | false => rfl
  | true =>
      exfalso
      have old : History (obstacle phaseHead (extra + phaseBaseDepth)) :=
        history_iff_mem.mpr (by
          simpa [HistoryB, BRegion.ofList] using present)
      have supportHead := (head_iff.mp phase.phaseMember).1
      apply entry_boundary.2 _ old.1 old.2 (extra + phaseBaseDepth) (by
        rw [phase.baseDepthExact]
        omega)
      unfold obstacle
      exact (supportAt_shiftPoint phaseHead (extra + phaseBaseDepth)).mpr
        supportHead

theorem actual_initial_exact (phase : PhaseChecks.Certificate) (extra : Nat) :
    (actualInitial phaseHead (extra + phaseBaseDepth)).toState =
      xorState HistoryB
        (lane base drift (obstacle phaseHead phaseDepth) (phaseLag + extra)) := by
  rw [actualInitial, force_toState]
  change blacken (obstacle phaseHead (extra + phaseBaseDepth)) entry = _
  rw [entry_exact,
    blacken_xorState _ _ _ (history_misses_obstacle phase extra)]
  unfold lane obstacle
  rw [← shiftPoint_add]
  congr 3
  unfold phaseLag
  rw [phase.pristineCutoff, phase.baseDepthExact]
  omega

theorem forward_actual_exact (pristine : PristineChecks.Certificate)
    (phase : PhaseChecks.Certificate) (extra : Nat) :
    run (duration period localTime (phaseLag + extra))
        (actualInitial phaseHead (extra + phaseBaseDepth)).toState =
      xorState (BRegion.xor HistoryB
        (BRegion.accumulated drift cleanWake (phaseLag + extra)))
        (shiftState drift (phaseLag + extra) reverseBase.toState) := by
  rw [actual_initial_exact phase, run_xorState _
      (history_avoids_pristine pristine phase extra),
    pristine_exact pristine phase (phaseLag + extra), xorState_xor]

end OneBlack.Phase
