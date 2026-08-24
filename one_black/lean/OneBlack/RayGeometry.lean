import OneBlack.Induction
import OneBlack.Terminal

namespace OneBlack.RayGeometry

open OneBlack Highway

def backwardPoint (turn steps : Nat) (p : Point) : Point :=
  match turn with
  | 0 => ⟨p.x + 2 * steps, p.y + 2 * steps⟩
  | 1 => ⟨p.x - 2 * steps, p.y + 2 * steps⟩
  | 2 => ⟨p.x - 2 * steps, p.y - 2 * steps⟩
  | _ => ⟨p.x + 2 * steps, p.y - 2 * steps⟩

@[simp] theorem backwardPoint_zero (turn : Nat) (p : Point) :
    backwardPoint turn 0 p = p := by
  rcases p with ⟨x, y⟩
  rcases turn with _ | turn
  · simp [backwardPoint]
  rcases turn with _ | turn
  · simp [backwardPoint]
  rcases turn with _ | turn <;> simp [backwardPoint]

def highwayPoint (steps : Nat) (p : Point) : Point :=
  ⟨p.x - 2 * steps, p.y - 2 * steps⟩

def raysMeet (turn : Nat) (a b : Point) : Bool :=
  match turn with
  | 0 => decide (a.x - a.y = b.x - b.y ∧
      (b.x - a.x) % 2 = 0 ∧ a.x + 2 ≤ b.x)
  | 1 => decide ((b.x + b.y - a.x - a.y) % 4 = 0 ∧
      0 ≤ b.x + b.y - a.x - a.y ∧
      (b.y - b.x - (a.y - a.x)) % 4 = 0 ∧
      4 ≤ b.y - b.x - (a.y - a.x))
  | 2 => decide (a.x - a.y = b.x - b.y ∧ (b.x - a.x) % 2 = 0)
  | _ => decide ((b.x + b.y - a.x - a.y) % 4 = 0 ∧
      0 ≤ b.x + b.y - a.x - a.y ∧
      (a.y - a.x - (b.y - b.x)) % 4 = 0 ∧
      4 ≤ a.y - a.x - (b.y - b.x))

/-- Whether `target` lies on the highway-drift ray from `source`, starting at
the given copy. -/
def shiftedAtLeast (minimum : Nat) (target source : Point) : Bool :=
  decide (target.x - target.y = source.x - source.y ∧
    (source.x - target.x) % 2 = 0 ∧
    2 * (minimum : Int) ≤ source.x - target.x)

theorem backwardPoint_add (turn left right : Nat) (p : Point)
    (bounded : turn < 4) :
    backwardPoint turn (left + right) p =
      backwardPoint turn right (backwardPoint turn left p) := by
  have cases : turn = 0 ∨ turn = 1 ∨ turn = 2 ∨ turn = 3 := by omega
  rcases cases with rfl | rfl | rfl | rfl <;>
    rcases p with ⟨x, y⟩ <;>
    simp [backwardPoint] <;> omega

theorem raysMeet_complete {turn j n : Nat} {a b : Point}
    (bounded : turn < 4) (positive : 0 < j)
    (equal : backwardPoint turn j a = highwayPoint n b) :
    raysMeet turn a b = true := by
  have cases : turn = 0 ∨ turn = 1 ∨ turn = 2 ∨ turn = 3 := by omega
  rcases cases with rfl | rfl | rfl | rfl <;>
    rcases a with ⟨ax, ay⟩ <;> rcases b with ⟨bx, baseY⟩ <;>
    simp [backwardPoint, highwayPoint, raysMeet] at equal ⊢ <;> omega

theorem rays_disjoint {turn : Nat} {a b : Point} (bounded : turn < 4)
    (checked : raysMeet turn a b = false) :
    ∀ j, 0 < j → ∀ n, backwardPoint turn j a ≠ highwayPoint n b := by
  intro j positive n equal
  rw [raysMeet_complete bounded positive equal] at checked
  contradiction

theorem drift_shift (n : Nat) (p : Point) :
    shiftPoint drift n p = highwayPoint n p := by
  induction n with
  | zero => rcases p with ⟨x, y⟩; simp [shiftPoint, highwayPoint]
  | succ n ih =>
      simp only [shiftPoint, ih]
      rcases p with ⟨x, y⟩
      simp [drift, Point.add, highwayPoint]
      constructor <;> omega

theorem shiftedAtLeast_complete {minimum copies : Nat} {target source : Point}
    (lower : minimum ≤ copies)
    (equal : target = shiftPoint drift copies source) :
    shiftedAtLeast minimum target source = true := by
  rw [drift_shift] at equal
  rcases target with ⟨tx, ty⟩
  rcases source with ⟨sx, sy⟩
  simp [highwayPoint, shiftedAtLeast, Point.mk.injEq] at equal ⊢
  omega

theorem backward_shift (n : Nat) (p : Point) :
    shiftPoint ⟨2, 2⟩ n p = ⟨p.x + 2 * n, p.y + 2 * n⟩ := by
  induction n with
  | zero => rcases p with ⟨x, y⟩; simp [shiftPoint]
  | succ n ih =>
      simp only [shiftPoint, ih]
      rcases p with ⟨x, y⟩
      simp [Point.add]
      constructor <;> omega

theorem rotate_backward (turn n : Nat) (p : Point) (bounded : turn < 4) :
    (shiftPoint ⟨2, 2⟩ n p).rotateN turn =
      backwardPoint turn n (p.rotateN turn) := by
  have cases : turn = 0 ∨ turn = 1 ∨ turn = 2 ∨ turn = 3 := by omega
  rw [backward_shift]
  rcases cases with rfl | rfl | rfl | rfl <;>
    rcases p with ⟨x, y⟩ <;>
    simp [Point.rotateN, Point.rot, backwardPoint] <;> omega

end OneBlack.RayGeometry
