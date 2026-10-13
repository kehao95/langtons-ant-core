import Std

/-! Kernel-checked algebraic and interval lemmas for the manuscript.
This module does not formalize the ant, finite-field sums, integer powers,
or the geometric range estimate. See ../VERIFICATION.md for that boundary. -/
namespace ClockEscape

theorem increment_pp (r u v : Rat) :
    -(r+1)*(u+v)+2*(r*u-v)-2*(u-r*v) = (r-3)*(u+v) := by grind

theorem increment_mm (r u v : Rat) :
    -(r+1)*(u+v)+2*(r*v-u)-2*(v-r*u) = (r-3)*(u+v) := by grind

theorem increment_pm (r u v : Rat) :
    (r+1)*(u+v)+2*(r*v-u)-2*(u-r*v) = (r-3)*u+(5*r+1)*v := by grind

theorem increment_mp (r u v : Rat) :
    (r+1)*(u+v)+2*(r*u-v)-2*(v-r*u) = (5*r+1)*u+(r-3)*v := by grind

theorem reciprocal_sum (u v : Rat) (hu : 0 < u) (huv : u*v=1) :
    2 ≤ u+v := by
  have square : 0 ≤ (u-1)*(u-1) := by
    by_cases h : 0 ≤ u-1
    · exact Rat.mul_nonneg h h
    · have hh : 0 ≤ 1-u := by grind
      have := Rat.mul_nonneg hh hh
      grind
  have h : u*2 ≤ u*(u+v) := by grind
  exact Rat.le_of_mul_le_mul_left h hu

theorem scaled_increment_lower (r u v : Rat) (hr : 3 < r)
    (hu : 0 < u) (hv : 0 < v) (huv : u*v=1) :
    2*(r-3) ≤ (r-3)*(u+v) ∧
    2*(r-3) ≤ (r-3)*u+(5*r+1)*v ∧
    2*(r-3) ≤ (5*r+1)*u+(r-3)*v := by
  have hs := reciprocal_sum u v hu huv
  have hd : 0 ≤ r-3 := by grind
  have hm := Rat.mul_nonneg hd (show 0 ≤ u+v-2 by grind)
  have hrv : 0 ≤ (4*r+4)*v := Rat.mul_nonneg (by grind) (by grind)
  have hru : 0 ≤ (4*r+4)*u := Rat.mul_nonneg (by grind) (by grind)
  grind

theorem telescope (phi : Nat → Rat) (d : Rat) (n : Nat)
    (growth : ∀ k, k < n → d ≤ phi (k+1)-phi k) :
    d*(n : Rat) ≤ phi n-phi 0 := by
  induction n with
  | zero => simp; grind
  | succ n ih =>
    have old := ih (fun k hk => growth k (by omega))
    have last := growth n (by omega)
    have cast : ((n+1 : Nat) : Rat) = (n : Rat)+1 := by simp
    rw [cast]
    grind

theorem internal_interval (phi : Nat → Rat) (d lo hi : Rat) (t : Nat)
    (growth : ∀ k, k < t-1 → d ≤ phi (k+1)-phi k)
    (start : lo ≤ phi 0) (finish : phi (t-1) ≤ hi) :
    d*((t-1 : Nat) : Rat) ≤ hi-lo := by
  have h := telescope phi d (t-1) growth
  grind

#print axioms increment_pp
#print axioms increment_mm
#print axioms increment_pm
#print axioms increment_mp
#print axioms reciprocal_sum
#print axioms scaled_increment_lower
#print axioms telescope
#print axioms internal_interval
end ClockEscape
