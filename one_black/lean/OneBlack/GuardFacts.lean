import OneBlack.EntryHistory

namespace OneBlack.Ordinary

open OneBlack Highway Terminal Entry RayGeometry Pristine PristineChecks
  ActualChecks

def historyAnchor (head historical : Point) : Point :=
  backwardPoint (stableTurn head) (historyLag head)
    (normalizedAt (stableTurn head) (stableFinal head) historical)

structure GuardFacts (head historical : Point) : Prop where
  traceRays : (stableResult head).2.toList.all
    (fun source => !(shiftedAtLeast (historyLag head) historical source)) = true
  corridorOutside : historyAnchor head historical ∉ support
  corridorSeparated :
    separatedFromSupport (historyAnchor head historical) = true
  corridorRays : support.all (fun source =>
    !(raysMeet (stableTurn head) (historyAnchor head historical) source)) = true

theorem guard_facts (certificate : ActualChecks.Certificate) {head historical : Point}
    (ordinary : head ∈ ordinaryHeads) (old : History historical) :
    GuardFacts head historical := by
  have historicalMember : historical ∈ historyCells := history_iff_mem.mp old
  have snapshotCheck := all_of_mem certificate.guardPass
    (stable_snapshot_mem (List.mem_filter.mp ordinary).1)
  have checked := all_of_mem (snapshotCheck ordinary) historicalMember
  rcases guardResult_parts checked with
    ⟨traceRays, outside, separated, rays⟩
  simpa [stableTurn, stableFinal, historyAnchor] using
    (show GuardFacts head historical from
      ⟨traceRays, outside, separated, rays⟩)

end OneBlack.Ordinary
