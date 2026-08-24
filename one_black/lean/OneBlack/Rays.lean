import OneBlack.Entry

namespace OneBlack.Rays

open OneBlack Highway

def Head (p : Point) : Prop := Support p ∧ drift.add p ∉ support
def OnLane (head p : Point) : Prop := ∃ depth, 0 < depth ∧
  p = shiftPoint drift depth head

theorem shift_back (n : Nat) (p : Point) :
    shiftPoint drift n (back n p) = p := by
  induction n generalizing p with
  | zero => rfl
  | succ n ih =>
      simp only [back, shiftPoint]
      rw [ih]
      exact Point.add_sub drift p

theorem drift_back_succ (n : Nat) (p : Point) :
    drift.add (back (n + 1) p) = back n p := by
  have later := back_invariants p (n + 1)
  have earlier := back_invariants p n
  rcases later with ⟨laterDiag, _, laterX⟩
  rcases earlier with ⟨earlierDiag, _, earlierX⟩
  rcases hLater : back (n + 1) p with ⟨lx, ly⟩
  rcases hEarlier : back n p with ⟨ex, ey⟩
  simp only [hLater, hEarlier, Point.add, Point.mk.injEq]
  simp only [hLater] at laterDiag laterX
  simp only [hEarlier] at earlierDiag earlierX
  simp [drift] at laterDiag laterX earlierDiag earlierX ⊢
  constructor <;> omega

theorem future_support_of_not_separated {p : Point}
    (failed : separatedFromSupport p = false) :
    ∃ n, 0 < n ∧ supportAt n p := by
  have witness : ∃ source ∈ support, separated source p = false := by
    simpa [separatedFromSupport, List.all_eq_false] using failed
  rcases witness with ⟨source, inside, rejected⟩
  have notSep : ¬Separated source p := by
    intro sep
    have : separated source p = true := decide_eq_true sep
    simp_all [separated, Separated]
    omega
  simp only [Separated, not_or] at notSep
  rcases notSep with ⟨diag, parity, horizontal⟩
  let z : Int := (source.x - p.x) / 2
  have even : (source.x - p.x) % 2 = 0 := by omega
  have zpos : 0 < z := by dsimp [z]; omega
  let n := z.toNat
  have cast : (n : Int) = z := by
    exact Int.toNat_of_nonneg (Int.le_of_lt zpos)
  have xeq : p.x + 2 * n = source.x := by
    dsimp [z] at cast
    omega
  have inv := back_invariants p n
  rcases hback : back n p with ⟨backXValue, backYValue⟩
  simp only [hback] at inv
  rcases inv with ⟨backDiag, _, backX⟩
  have equal : back n p = source := by
    rcases source with ⟨sx, sy⟩
    simp only at diag parity horizontal xeq backDiag backX
    rw [hback]
    have horizontalEqual : backXValue = sx := by omega
    have verticalEqual : backYValue = sy := by omega
    rw [horizontalEqual, verticalEqual]
  refine ⟨n, ?_, ?_⟩
  · have : 0 < (n : Int) := cast.symm ▸ zpos
    omega
  · change Support (back n p)
    simpa [equal] using inside

theorem least_witness {P : Nat → Prop} [DecidablePred P]
    (witnessExists : ∃ n, P n) : ∃ n, P n ∧ ∀ k, k < n → ¬P k := by
  rcases witnessExists with ⟨bound, found⟩
  induction bound using Nat.strongRecOn with
  | _ bound ih =>
      by_cases earlier : ∃ k, k < bound ∧ P k
      · rcases earlier with ⟨k, before, witness⟩
        exact ih k before witness
      · exact ⟨bound, found, fun k before witness =>
          earlier ⟨k, before, witness⟩⟩

theorem outside_corridor_has_lane {p : Point} (outside : p ∉ support)
    (failed : separatedFromSupport p = false) :
    ∃ head, Head head ∧ OnLane head p := by
  classical
  rcases least_witness (future_support_of_not_separated failed) with
    ⟨n, ⟨positive, inside⟩, minimal⟩
  let head := back n p
  have headInside : Support head := inside
  have predecessorOutside : drift.add head ∉ support := by
    obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt positive)
    rw [drift_back_succ]
    intro earlier
    by_cases zero : k = 0
    · subst k; exact outside earlier
    · exact minimal k (Nat.lt_succ_self k)
        ⟨Nat.zero_lt_of_ne_zero zero, earlier⟩
  exact ⟨head, ⟨headInside, predecessorOutside⟩,
    n, positive, (shift_back n p).symm⟩

end OneBlack.Rays
