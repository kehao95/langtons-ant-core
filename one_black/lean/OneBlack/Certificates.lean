import OneBlack.Scattering

namespace OneBlack.Certificates

open OneBlack Highway Pristine PristineChecks ActualChecks PhaseChecks

/-- The exceptional result is bound once; every channel keeps its own cutoff. -/
def snapshotsWithPhase (phaseResult : FState × PointSet) :
    List PristineChecks.Snapshot :=
  heads.map fun head =>
    let time := stableTime head
    let result := if head = phaseHead then phaseResult else stableResult head
    let found := Terminal.orientation result.1
    ⟨head, time, result, result.2.toList, found.getD 0, found.isSome⟩

theorem snapshotsWithPhase_exact :
    snapshotsWithPhase (stableResult phaseHead) = snapshots := by
  unfold snapshotsWithPhase snapshots
  apply List.map_congr_left
  intro head member
  by_cases exceptional : head = phaseHead
  · simp [exceptional, stableTime, stableResult, stableInitial]
  · simp [exceptional, stableTime, stableResult, stableInitial]

/-- The 22-channel finite leaf, with each stable replay evaluated once. -/
def report : Bool :=
  let phaseResult := stableResult phaseHead
  let stable := snapshotsWithPhase phaseResult
  Entry.activeReport && PristineChecks.reportWith stable &&
    ActualChecks.reportWith stable &&
    PhaseChecks.reportWith phaseResult

structure Bundle : Prop where
  entry : Entry.ActiveCertificate
  pristine : PristineChecks.Certificate
  actual : ActualChecks.Certificate
  phase : PhaseChecks.Certificate

theorem bundle_of_report (verified : report = true) : Bundle := by
  simp only [report, Bool.and_eq_true] at verified
  rcases verified with
    ⟨⟨⟨entryVerified, pristineVerified⟩, actualVerified⟩, phaseVerified⟩
  exact {
    entry := Entry.active_certificate_of_report entryVerified
    pristine := PristineChecks.certificate_of_reportWith
      snapshotsWithPhase_exact pristineVerified
    actual := ActualChecks.certificate_of_reportWith
      snapshotsWithPhase_exact actualVerified
    phase := PhaseChecks.certificate_of_reportWith phaseVerified
  }

end OneBlack.Certificates
