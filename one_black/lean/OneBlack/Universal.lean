import OneBlack.Prefix
import OneBlack.Scattering

namespace OneBlack.Universal

open OneBlack Highway Terminal Entry Rays RayGeometry PristineChecks
  ActualChecks PhaseChecks Scattering

theorem entry_reaches (entryCases : Entry.ActiveCertificate)
    (spectrum : Scattering.Classification)
    (p : Point) : ReachesP104 (blacken p entry) := by
  by_cases inside : p ∈ support
  · by_cases black : entry.black p = true
    · rw [already_black black]
      exact ⟨0, blank_entry_permanent⟩
    · apply active_reaches entryCases
      rw [Entry.active, List.mem_filter]
      refine ⟨inside, ?_⟩
      have white : entry.black p = false := by
        cases value : entry.black p <;> simp_all
      change entryF.black.contains p = false at white
      simp [white]
  · by_cases separated : separatedFromSupport p = true
    · exact separated_reaches inside separated
    · have failed : separatedFromSupport p = false := by
        cases value : separatedFromSupport p <;> simp_all
      rcases outside_corridor_has_lane inside failed with
        ⟨head, headProperty, depth, positive, obstacleEq⟩
      have member : head ∈ heads := Pristine.head_iff.mpr headProperty
      rw [obstacleEq]
      exact Scattering.lane_reaches spectrum member positive

theorem canonical_reaches (prefixCert : Prefix.Certificate)
    (entryCases : Entry.ActiveCertificate) (spectrum : Scattering.Classification)
    (p : Point) : ReachesP104 (singleton p) := by
  by_cases readEarly : p ∈ Prefix.domain
  · exact Prefix.reaches prefixCert readEarly
  · have coupled := unread_singleton p entryTime (Prefix.unread readEarly)
    rw [← entry_from_white] at coupled
    rcases entry_reaches entryCases spectrum p with
      ⟨tail, permanent⟩
    refine ⟨entryTime + tail, ?_⟩
    rw [run_add, coupled]
    exact permanent

theorem shift_singleton (v p : Point) :
    shift v (singleton p) = singletonAt (v.add p) v .north := by
  apply State.ext
  · funext q
    change decide (q.sub v = p) = decide (q = v.add p)
    apply Bool.eq_iff_iff.mpr
    constructor
    · intro equal
      apply decide_eq_true
      simpa using congrArg (Point.add v) (of_decide_eq_true equal)
    · intro equal
      apply decide_eq_true
      simpa using congrArg (Point.sub · v) (of_decide_eq_true equal)
  · change v.add ⟨0, 0⟩ = v
    exact Point.add_zero v
  · rfl

theorem rotate_singletonAt (cell pos : Point) (dir : Heading) :
    rotate (singletonAt cell pos dir) =
      singletonAt cell.rot pos.rot dir.rot := by
  apply State.ext
  · funext q
    change decide (q.unrot = cell) = decide (q = cell.rot)
    apply Bool.eq_iff_iff.mpr
    constructor
    · intro equal
      apply decide_eq_true
      rw [← Point.rot_unrot q]
      exact congrArg Point.rot (of_decide_eq_true equal)
    · intro equal
      apply decide_eq_true
      simpa using congrArg Point.unrot (of_decide_eq_true equal)
  · rfl
  · rfl

theorem shift_singletonAt (v cell pos : Point) (dir : Heading) :
    shift v (singletonAt cell pos dir) =
      singletonAt (v.add cell) (v.add pos) dir := by
  apply State.ext
  · funext q
    change decide (q.sub v = cell) = decide (q = v.add cell)
    apply Bool.eq_iff_iff.mpr
    constructor
    · intro equal
      apply decide_eq_true
      simpa using congrArg (Point.add v) (of_decide_eq_true equal)
    · intro equal
      apply decide_eq_true
      simpa using congrArg (Point.sub · v) (of_decide_eq_true equal)
  · rfl
  · rfl

theorem pose_decomposition (cell pos : Point) (dir : Heading) :
    ∃ q turns, singletonAt cell pos dir =
      shift pos (rotateN turns (singleton q)) := by
  let delta := cell.sub pos
  cases dir with
  | north =>
      refine ⟨delta, 0, ?_⟩
      simp only [rotateN]
      rw [shift_singleton]
      simp [delta]
  | west =>
      refine ⟨delta.unrot, 1, ?_⟩
      simp only [rotateN]
      rw [show rotate (singleton delta.unrot) =
        singletonAt delta ⟨0, 0⟩ .west by
          change rotate (singletonAt delta.unrot ⟨0, 0⟩ .north) = _
          rw [rotate_singletonAt]
          simp [Heading.rot]]
      rw [shift_singletonAt]
      simp [delta]
  | south =>
      refine ⟨delta.unrot.unrot, 2, ?_⟩
      simp only [rotateN]
      rw [show rotate (rotate (singleton delta.unrot.unrot)) =
        singletonAt delta ⟨0, 0⟩ .south by
          change rotate (rotate
            (singletonAt delta.unrot.unrot ⟨0, 0⟩ .north)) = _
          rw [rotate_singletonAt, rotate_singletonAt]
          simp [Heading.rot]]
      rw [shift_singletonAt]
      simp [delta]
  | east =>
      refine ⟨delta.unrot.unrot.unrot, 3, ?_⟩
      simp only [rotateN]
      rw [show rotate (rotate (rotate (singleton delta.unrot.unrot.unrot))) =
        singletonAt delta ⟨0, 0⟩ .east by
          change rotate (rotate (rotate
            (singletonAt delta.unrot.unrot.unrot ⟨0, 0⟩ .north))) = _
          rw [rotate_singletonAt, rotate_singletonAt, rotate_singletonAt]
          simp [Heading.rot]]
      rw [shift_singletonAt]
      simp [delta]

theorem universal_one_black (prefixCert : Prefix.Certificate)
    (entryCases : Entry.ActiveCertificate) (spectrum : Scattering.Classification)
    (s : State) (one : ExactlyOneBlack s) : ReachesP104 s := by
  rcases (exactlyOneBlack_iff s).mp one with ⟨cell, stateEq⟩
  rcases pose_decomposition cell s.pos s.dir with ⟨q, turns, equal⟩
  have reached : ReachesP104 (singletonAt cell s.pos s.dir) := by
    rw [equal]
    exact (canonical_reaches prefixCert entryCases spectrum q).rotateN
      turns |>.shift s.pos
  rw [← stateEq] at reached
  exact reached

end OneBlack.Universal
