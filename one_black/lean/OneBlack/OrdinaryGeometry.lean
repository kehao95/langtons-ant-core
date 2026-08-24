import OneBlack.OrdinaryCorridor

namespace OneBlack.Ordinary

open OneBlack Highway Terminal Entry Induction Pristine PristineChecks
  ActualChecks

def Envelope (head : Point) (extra : Nat) : Region :=
  Region.union (footprint drift CleanReads (BaseReads head) extra)
    (shiftRegion drift extra (Corridor head))

theorem pristine_future_subset (certificate : PristineChecks.Certificate)
    {head : Point} (member : head ∈ heads) (extra : Nat) :
    Region.Subset (futureReads
      (lane base drift (obstacle head (stableDepth head)) extra))
      (Envelope head extra) := by
  let data := lane_data certificate member
  let normal := Induction.exact data extra
  intro p read
  rcases read with ⟨updates, position⟩
  by_cases early : updates < duration period (stableTime head) extra
  · exact Or.inl (normal.readSet ▸ ⟨updates, early, position⟩)
  · let cut := duration period (stableTime head) extra
    let later := updates - cut
    have split : updates = cut + later := by dsimp [later]; omega
    have tailPosition :
        (run later (run cut
          (lane base drift (obstacle head (stableDepth head)) extra))).pos = p := by
      rw [← run_add, ← split]
      exact position
    have terminalFuture : Region.Subset
        (futureReads (shiftState drift extra
          (run (stableTime head)
            (lane base drift (obstacle head (stableDepth head)) 0))))
        (shiftRegion drift extra (Corridor head)) := by
      rw [futureReads_shiftState]
      exact shiftRegion_subset drift data.baseFuture extra
    have avoids : AvoidsForever (archive drift Wake extra)
        (shiftState drift extra
          (run (stableTime head)
            (lane base drift (obstacle head (stableDepth head)) 0))) := by
      apply AvoidsForever.of_disjoint
      exact Region.Disjoint.mono_right (data.archiveMisses extra) terminalFuture
    have trace := sameReadTrace_of_archive normal.final avoids
    apply Or.inr
    apply terminalFuture
    refine ⟨later, ?_⟩
    exact congrArg Observation.pos (trace later) |>.symm.trans tailPosition

end OneBlack.Ordinary
