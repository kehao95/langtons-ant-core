import OneBlack.ActualHistory

namespace OneBlack.Ordinary

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks

theorem history_misses_corridor (pristine : PristineChecks.Certificate)
    (actual : ActualChecks.Certificate) {head : Point}
    (member : head ∈ heads) (ordinary : head ∈ ordinaryHeads) : ∀ extra,
    historyLag head ≤ extra →
    Region.Disjoint History (shiftRegion drift extra (Corridor head)) := by
  intro extra lower historical old shifted
  obtain ⟨copies, rfl⟩ := Nat.exists_eq_add_of_le lower
  rcases shiftRegion_iff.mp shifted with ⟨corridor, future, equal⟩
  have facts := guard_facts actual ordinary old
  let final := stableFinal head
  let turns := stableTurn head
  let normalizedOld := normalizedAt turns final historical
  let normalizedCorridor := normalizedAt turns final corridor
  have corridorBackward : corridor =
      shiftPoint ⟨2, 2⟩ (historyLag head + copies) historical := by
    rw [drift_shift] at equal
    rw [backward_shift]
    rcases historical with ⟨hx, hy⟩
    rcases corridor with ⟨cx, cy⟩
    simp [highwayPoint, Point.mk.injEq] at equal ⊢
    constructor <;> omega
  have normalizedEqual : normalizedCorridor =
      backwardPoint turns copies (historyAnchor head historical) := by
    calc
      normalizedCorridor =
          backwardPoint turns (historyLag head + copies) normalizedOld := by
        dsimp [normalizedCorridor, normalizedOld, turns, final]
        rw [corridorBackward]
        simpa [stableTurn, normalizedPoint] using
          normalized_backward (stableFinal head) historical
            (historyLag head + copies)
      _ = backwardPoint turns copies
          (backwardPoint turns (historyLag head) normalizedOld) :=
        backwardPoint_add turns (historyLag head) copies normalizedOld (by
          dsimp [turns, stableTurn]
          exact turn_bounded (stableFinal head))
      _ = backwardPoint turns copies (historyAnchor head historical) := by
        rfl
  cases copies with
  | zero =>
      have normalizedAtAnchor : normalizedCorridor = historyAnchor head historical := by
        simpa only [backwardPoint_zero] using normalizedEqual
      have outside : normalizedPoint final corridor ∉ support := by
        rw [show normalizedPoint final corridor = normalizedCorridor by
          rfl, normalizedAtAnchor]
        exact facts.corridorOutside
      have separated : separatedFromSupport (normalizedPoint final corridor) = true := by
        rw [show normalizedPoint final corridor = normalizedCorridor by
          rfl, normalizedAtAnchor]
        exact facts.corridorSeparated
      apply future_excluded (stable_accepted pristine member) outside separated
      simpa [Corridor, final] using future
  | succ copies =>
      have bounded : turns < 4 := by
        dsimp [turns, stableTurn]
        exact turn_bounded (stableFinal head)
      have positive : 0 < copies + 1 := Nat.zero_lt_succ copies
      have outside : normalizedCorridor ∉ support := by
        intro inside
        have checked := (List.all_eq_true.mp facts.corridorRays)
          normalizedCorridor inside
        have falseRay : raysMeet turns (historyAnchor head historical)
            normalizedCorridor = false := by simpa using checked
        exact (rays_disjoint bounded falseRay (copies + 1) positive 0)
          (by simpa [highwayPoint] using normalizedEqual.symm)
      have separated : separatedFromSupport normalizedCorridor = true := by
        apply List.all_eq_true.mpr
        intro source sourceInside
        change separated source normalizedCorridor = true
        apply decide_eq_true
        apply Classical.byContradiction
        intro failed
        rcases not_separated_future failed with ⟨later, laterPositive, targetEqual⟩
        have checked := (List.all_eq_true.mp facts.corridorRays) source sourceInside
        have falseRay : raysMeet turns (historyAnchor head historical) source = false := by
          simpa using checked
        exact (rays_disjoint bounded falseRay (copies + 1) positive later)
          (normalizedEqual.symm.trans targetEqual)
      have outside' : normalizedPoint final corridor ∉ support := by
        exact outside
      have separated' :
          separatedFromSupport (normalizedPoint final corridor) = true := by
        exact separated
      apply future_excluded (stable_accepted pristine member) outside' separated'
      simpa [Corridor, final] using future

end OneBlack.Ordinary
