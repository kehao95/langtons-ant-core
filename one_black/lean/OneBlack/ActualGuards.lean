import OneBlack.GuardFacts

namespace OneBlack.Ordinary

open OneBlack Highway RayGeometry Pristine PristineChecks ActualChecks

theorem history_misses_base_shift (certificate : ActualChecks.Certificate)
    {head historical source : Point} (ordinary : head ∈ ordinaryHeads)
    (old : History historical) (baseRead : BaseReads head source) : ∀ copies,
    historyLag head ≤ copies → historical ≠ shiftPoint drift copies source := by
  intro copies lower equal
  have facts := guard_facts certificate ordinary old
  have checked := (List.all_eq_true.mp facts.traceRays) source
    (base_read_recorded baseRead)
  have falseRay : shiftedAtLeast (historyLag head) historical source = false := by
    simpa using checked
  rw [shiftedAtLeast_complete lower equal] at falseRay
  contradiction

end OneBlack.Ordinary
