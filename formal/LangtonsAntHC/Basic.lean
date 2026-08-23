namespace LangtonsAntHC

abbrev Point := Int × Int

inductive Heading where
  | north
  | east
  | south
  | west
  deriving DecidableEq, Repr

def Heading.right : Heading → Heading
  | .north => .east
  | .east => .south
  | .south => .west
  | .west => .north

def Heading.left : Heading → Heading
  | .north => .west
  | .east => .north
  | .south => .east
  | .west => .south

def move (heading : Heading) (point : Point) : Point :=
  match heading with
  | .north => (point.1, point.2 + 1)
  | .east => (point.1 + 1, point.2)
  | .south => (point.1, point.2 - 1)
  | .west => (point.1 - 1, point.2)

def rotatePointCW (point : Point) : Point := (point.2, -point.1)

def Heading.rotateCW : Heading → Heading
  | .north => .east
  | .east => .south
  | .south => .west
  | .west => .north

theorem left_eq_right_right_right (heading : Heading) :
    heading.left = heading.right.right.right := by
  cases heading <;> rfl

theorem rotate_move_cw (heading : Heading) (point : Point) :
    rotatePointCW (move heading point) = move heading.rotateCW (rotatePointCW point) := by
  cases heading <;> rcases point with ⟨x, y⟩ <;> simp [move, rotatePointCW, Heading.rotateCW] <;> omega

end LangtonsAntHC
