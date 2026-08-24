import OneBlack.ActualGuards

namespace OneBlack.Ordinary

open OneBlack Highway Induction Pristine ActualChecks

theorem history_misses_footprint (certificate : ActualChecks.Certificate)
    {head : Point} (ordinary : head ∈ ordinaryHeads) : ∀ extra,
    historyLag head ≤ extra →
    Region.Disjoint History (footprint drift CleanReads (BaseReads head) extra) := by
  intro extra lower historical old inside
  rcases footprint_cases inside with clean | baseRead
  · rcases clean with ⟨source, read, copies, _, equal⟩
    exact history_misses_clean_shift old read copies equal
  · rcases baseRead with ⟨source, read, equal⟩
    exact history_misses_base_shift certificate ordinary old read extra lower equal

end OneBlack.Ordinary
