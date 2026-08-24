import OneBlack.PrefixData

namespace OneBlack.Prefix

open OneBlack Highway Terminal

@[irreducible] def reads : List Point := fwhite.reads entryTime

theorem reads_exact : reads = fwhite.reads entryTime := by
  unfold reads
  rfl

def domain : List Point := reads.eraseDups

def cases : List (Point × Nat) :=
  domain.zip FiniteData.prefixTimes

def casePoints : List Point := cases.map Prod.fst

def checks : List Bool :=
  cases.map fun c => lands (fsingleton c.1) c.2

def report : Bool :=
  decide (FiniteData.prefixTimes.length = domain.length) &&
  decide (casePoints = domain) && checks.all id

structure Certificate : Prop where
  lengthMatch : FiniteData.prefixTimes.length = domain.length
  pointsExact : casePoints = domain
  checksPass : checks.all id = true

theorem certificate_of_report (verified : report = true) : Certificate := by
  simp only [report, Bool.and_eq_true, decide_eq_true_eq] at verified
  exact ⟨verified.1.1, verified.1.2, verified.2⟩

theorem domain_checked (certificate : Certificate) {p : Point}
    (member : p ∈ domain) :
    ∃ updates, lands (fsingleton p) updates := by
  have inPoints : p ∈ casePoints := by
    rw [certificate.pointsExact]
    exact member
  rcases List.mem_map.mp inPoints with ⟨⟨q, updates⟩, inCases, equal⟩
  simp at equal
  subst q
  refine ⟨updates, (List.all_eq_true.mp certificate.checksPass) _ ?_⟩
  exact List.mem_map.mpr ⟨(p, updates), inCases, rfl⟩

theorem reaches (certificate : Certificate) {p : Point} (member : p ∈ domain) :
    ReachesP104 (singleton p) := by
  rcases domain_checked certificate member with ⟨updates, accepted⟩
  have reached := lands_sound accepted
  simpa [fsingleton_exact] using reached

theorem member_iff_read {p : Point} : p ∈ domain ↔
    ∃ k, k < entryTime ∧ (OneBlack.run k white).pos = p := by
  rw [domain, List.mem_eraseDups, reads_exact, FState.mem_reads_iff]
  constructor
  · rintro ⟨k, earlier, position⟩
    refine ⟨k, earlier, ?_⟩
    have bridge := congrArg State.pos (FState.toState_run k fwhite)
    simpa [fwhite_exact] using bridge.symm.trans position
  · rintro ⟨k, earlier, position⟩
    refine ⟨k, earlier, ?_⟩
    have bridge := congrArg State.pos (FState.toState_run k fwhite)
    simpa [fwhite_exact] using bridge.trans position

theorem unread {p : Point} (outside : p ∉ domain) :
    Avoids p white entryTime := by
  intro k earlier equal
  exact outside (member_iff_read.mpr ⟨k, earlier, equal⟩)

end OneBlack.Prefix
