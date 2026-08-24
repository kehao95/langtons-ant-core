import OneBlack.Geometry
import OneBlack.EntryData

namespace OneBlack.Entry

open OneBlack Highway Terminal

def force (p : Point) (s : FState) : FState :=
  { s with black := s.black.insert p }

@[simp] theorem force_toState (p : Point) (s : FState) :
    (force p s).toState = blacken p s.toState := by
  apply State.ext
  · funext q
    by_cases same : q = p
    · subst q; simp [force, FState.toState, blacken]
    · have reverse : p ≠ q := Ne.symm same
      simp [force, FState.toState, blacken, same, reverse]
  · rfl
  · rfl

def actual (p : Point) : FState := force p entryF
def active : List Point := support.filter fun p => !(entryF.black.contains p)

def activeCases : List (Point × Nat) :=
  active.zip FiniteData.actualActiveTimes

def activeChecks : List Bool :=
  activeCases.map fun c => lands (actual c.1) c.2

def activeReport : Bool :=
  decide (FiniteData.actualActiveTimes.length = active.length) &&
  decide (activeCases.map Prod.fst = active) && activeChecks.all id

structure ActiveCertificate : Prop where
  lengthMatch : FiniteData.actualActiveTimes.length = active.length
  pointsExact : activeCases.map Prod.fst = active
  checksPass : activeChecks.all id = true

theorem active_certificate_of_report
    (verified : activeReport = true) : ActiveCertificate := by
  simp only [activeReport, Bool.and_eq_true, decide_eq_true_eq] at verified
  exact ⟨verified.1.1, verified.1.2, verified.2⟩

theorem active_reaches (certificate : ActiveCertificate) {p : Point}
    (member : p ∈ active) :
    ReachesP104 (blacken p entry) := by
  have inPoints : p ∈ activeCases.map Prod.fst := by
    rw [certificate.pointsExact]
    exact member
  rcases List.mem_map.mp inPoints with ⟨⟨q, updates⟩, inCases, equal⟩
  simp at equal
  subst q
  have accepted : lands (actual p) updates = true :=
    (List.all_eq_true.mp certificate.checksPass) _
      (List.mem_map.mpr ⟨(p, updates), inCases, rfl⟩)
  have reached := lands_sound accepted
  simpa [actual, entry] using reached

theorem already_black {p : Point} (black : entry.black p = true) :
    blacken p entry = entry := by
  apply State.ext
  · funext q
    by_cases same : q = p
    · subst q; simp [blacken, black]
    · simp [blacken, same]
  · rfl
  · rfl

theorem separated_reaches {p : Point} (outside : p ∉ support)
    (separated : separatedFromSupport p = true) :
    ReachesP104 (blacken p entry) := by
  have off : Terminal.offset (actual p) = ⟨0, 0⟩ := by
    unfold Terminal.offset actual force
    change baseF.pos.sub entryF.pos = ⟨0, 0⟩
    rw [entry_pos_fact]
    rcases baseF.pos with ⟨x, y⟩
    simp [Point.sub]
  have terminal : Terminal.check (actual p) = true := by
    unfold Terminal.check
    rw [off]
    simp only [Bool.and_eq_true]
    refine ⟨⟨?_, ?_⟩, ?_⟩
    · exact decide_eq_true entry_dir_fact
    · apply List.all_eq_true.mpr
      intro q member
      have different : q ≠ p := fun equal => outside (equal ▸ member)
      have reverse : p ≠ q := Ne.symm different
      have cmp : Point.cmp p q ≠ .eq := fun equal =>
        reverse ((Point.cmp_eq p q).mp equal)
      have cmpFalse : (Point.cmp p q == .eq) = false := beq_false_of_ne cmp
      have checked := (List.all_eq_true.mp entry_active_fact) q member
      simpa [actual, force, Point.sub, different, reverse, cmpFalse] using checked
    · apply List.all_eq_true.mpr
      intro q member
      have inTree : q ∈ (actual p).black := Std.TreeSet.mem_toList.mp member
      have old : q = p ∨ q ∈ entryF.black := by
        have raw : p = q ∨ q ∈ entryF.black := by
          simpa [actual, force] using inTree
        rcases raw with equal | old
        · exact Or.inl equal.symm
        · exact Or.inr old
      rcases old with rfl | old
      · simp [Point.add, outside, separated]
      · have checked := (List.all_eq_true.mp entry_background_fact) q
          (Std.TreeSet.mem_toList.mpr old)
        simpa [Point.add] using checked
  have accepted : lands (actual p) 0 = true := by
    change any (actual p) = true
    simp [any, orientation, terminal]
  have reached := lands_sound accepted
  simpa [actual, entry] using reached

end OneBlack.Entry
