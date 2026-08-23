import LangtonsAntHC.Dynamics

namespace LangtonsAntHC

def rotateBoardCW (board : Board) : Board := fun point => board (rotatePointCCW point)

def rotateStateCW (state : State) : State where
  board := rotateBoardCW state.board
  position := rotatePointCW state.position
  heading := state.heading.rotateCW

theorem rotateBoardCW_at_rotated_point (board : Board) (point : Point) :
    rotateBoardCW board (rotatePointCW point) = board point := by
  simp [rotateBoardCW, rotatePointCCW_rotatePointCW]

theorem rotateBoardCW_flip (board : Board) (point : Point) :
    rotateBoardCW (flip board point) = flip (rotateBoardCW board) (rotatePointCW point) := by
  funext candidate
  by_cases h : rotatePointCCW candidate = point
  · have h' : candidate = rotatePointCW point := by
      calc
        candidate = rotatePointCW (rotatePointCCW candidate) :=
          (rotatePointCW_rotatePointCCW candidate).symm
        _ = rotatePointCW point := congrArg rotatePointCW h
    simp [rotateBoardCW, flip, h', rotatePointCCW_rotatePointCW]
  · have h' : candidate ≠ rotatePointCW point := by
      intro candidate_eq
      apply h
      calc
        rotatePointCCW candidate = rotatePointCCW (rotatePointCW point) :=
          congrArg rotatePointCCW candidate_eq
        _ = point := rotatePointCCW_rotatePointCW point
    simp [rotateBoardCW, flip, h, h']

theorem rotate_step_cw (state : State) :
    rotateStateCW (step state) = step (rotateStateCW state) := by
  dsimp [rotateStateCW, step]
  have read_rotated : rotateBoardCW state.board (rotatePointCW state.position) =
      state.board state.position := rotateBoardCW_at_rotated_point state.board state.position
  by_cases h : state.board state.position = true
  · simp [h, read_rotated, rotateBoardCW_flip, rotate_left_cw, rotate_move_cw]
  · simp [h, read_rotated, rotateBoardCW_flip, rotate_right_cw, rotate_move_cw]

end LangtonsAntHC
