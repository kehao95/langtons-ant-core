import LangtonsAntHC.Basic

namespace LangtonsAntHC

abbrev Board := Point → Bool

structure State where
  board : Board
  position : Point
  heading : Heading

def flip (board : Board) (point : Point) : Board := fun candidate =>
  if candidate = point then !(board candidate) else board candidate

def step (state : State) : State :=
  let nextHeading := if state.board state.position then state.heading.left else state.heading.right
  {
    board := flip state.board state.position
    position := move nextHeading state.position
    heading := nextHeading
  }

theorem step_reads_before_flipping (state : State) :
    (step state).board state.position = !(state.board state.position) := by
  simp [step, flip]

theorem step_turns_left_on_black (state : State) (h : state.board state.position = true) :
    (step state).heading = state.heading.left := by
  simp [step, h]

theorem step_turns_right_on_white (state : State) (h : state.board state.position = false) :
    (step state).heading = state.heading.right := by
  simp [step, h]

end LangtonsAntHC
