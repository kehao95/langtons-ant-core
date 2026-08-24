import OneBlack.OrdinaryGeometry

namespace OneBlack.Ordinary

open OneBlack Highway Terminal Entry Induction Pristine PristineChecks
  ActualChecks

theorem cutoff_order (actual : ActualChecks.Certificate) {head : Point}
    (ordinary : head ∈ ordinaryHeads) : stableDepth head ≤ actualCutoff head := by
  exact of_decide_eq_true
    ((List.all_eq_true.mp actual.cutoffOrder) head ordinary)

theorem ordinary_tail_reaches (pristine : PristineChecks.Certificate)
    (actual : ActualChecks.Certificate) {head : Point}
    (member : head ∈ heads) (ordinary : head ∈ ordinaryHeads)
    (extra : Nat) :
    ReachesP104
      (blacken (obstacle head (extra + actualCutoff head)) entry) := by
  let lag := historyLag head
  let pristineExtra := lag + extra
  have order := cutoff_order actual ordinary
  have lagLower : historyLag head ≤ pristineExtra := by
    simp [pristineExtra, lag]
  have disjoint : Region.Disjoint History (Envelope head pristineExtra) := by
    intro p old inside
    rcases inside with footprintInside | corridorInside
    · exact history_misses_footprint actual ordinary pristineExtra lagLower
        p old footprintInside
    · exact history_misses_corridor pristine actual member ordinary pristineExtra
        lagLower p old corridorInside
  have avoids : AvoidsForever History
      (lane base drift (obstacle head (stableDepth head)) pristineExtra) := by
    apply AvoidsForever.of_disjoint
    exact Region.Disjoint.mono_right disjoint
      (pristine_future_subset pristine member pristineExtra)
  have depthEq : stableDepth head + pristineExtra = actualCutoff head + extra := by
    dsimp [pristineExtra, lag, historyLag]
    omega
  have laneEqual :
      lane base drift (obstacle head (stableDepth head)) pristineExtra =
        blacken (obstacle head (extra + actualCutoff head)) base := by
    unfold lane obstacle
    rw [← shiftPoint_add]
    congr 2
    omega
  rw [laneEqual] at avoids
  have trace := sameReadTrace_of_archive
    (forced_same (obstacle head (extra + actualCutoff head))) avoids
  have reached := stable_lane_reaches pristine member pristineExtra
  rw [laneEqual] at reached
  exact ReachesP104.of_sameReadTrace trace reached

theorem shallow_reaches (certificate : ActualChecks.Certificate) {head : Point}
    (member : head ∈ heads) {depth : Nat}
    (positive : 0 < depth) (shallow : depth < actualCutoff head) :
    ReachesP104 (blacken (obstacle head depth) entry) := by
  have index : depth - 1 ∈ List.range (actualCutoff head - 1) := by
    rw [List.mem_range]
    omega
  have checkMember :
      lands (actualInitial head depth) (actualTime head depth) ∈
        ActualChecks.directChecks := by
    apply List.mem_flatMap.mpr
    refine ⟨head, member, ?_⟩
    apply List.mem_map.mpr
    refine ⟨depth - 1, index, ?_⟩
    congr 2 <;> omega
  have accepted := (List.all_eq_true.mp certificate.directPass) _ checkMember
  have reached := lands_sound accepted
  simpa [actualInitial, obstacle, entry] using reached

theorem lane_reaches (pristine : PristineChecks.Certificate)
    (actual : ActualChecks.Certificate) {head : Point}
    (member : head ∈ heads) (ordinary : head ∈ ordinaryHeads)
    {depth : Nat} (positive : 0 < depth) :
    ReachesP104 (blacken (obstacle head depth) entry) := by
  by_cases shallow : depth < actualCutoff head
  · exact shallow_reaches actual member positive shallow
  · have stableLe : actualCutoff head ≤ depth := Nat.le_of_not_gt shallow
    have reached := ordinary_tail_reaches pristine actual member ordinary
      (depth - actualCutoff head)
    have depthEq : depth - actualCutoff head + actualCutoff head = depth := by
      omega
    rw [depthEq] at reached
    exact reached

end OneBlack.Ordinary
