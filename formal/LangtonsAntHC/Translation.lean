import LangtonsAntHC.Dynamics

namespace LangtonsAntHC

def translateBoard (displacement : Point) (board : Board) : Board := fun point =>
  board (untranslatePoint displacement point)

def translateState (displacement : Point) (state : State) : State where
  board := translateBoard displacement state.board
  position := translatePoint displacement state.position
  heading := state.heading

theorem translateBoard_at_translated_point (displacement : Point) (board : Board) (point : Point) :
    translateBoard displacement board (translatePoint displacement point) = board point := by
  simp [translateBoard, untranslate_translate]

theorem translateBoard_flip (displacement : Point) (board : Board) (point : Point) :
    translateBoard displacement (flip board point) =
      flip (translateBoard displacement board) (translatePoint displacement point) := by
  funext candidate
  by_cases h : untranslatePoint displacement candidate = point
  · have h' : candidate = translatePoint displacement point := by
      calc
        candidate = translatePoint displacement (untranslatePoint displacement candidate) :=
          (translate_untranslate displacement candidate).symm
        _ = translatePoint displacement point := congrArg (translatePoint displacement) h
    simp [translateBoard, flip, h', untranslate_translate]
  · have h' : candidate ≠ translatePoint displacement point := by
      intro candidate_eq
      apply h
      calc
        untranslatePoint displacement candidate =
            untranslatePoint displacement (translatePoint displacement point) :=
          congrArg (untranslatePoint displacement) candidate_eq
        _ = point := untranslate_translate displacement point
    simp [translateBoard, flip, h, h']

theorem translate_step (displacement : Point) (state : State) :
    translateState displacement (step state) = step (translateState displacement state) := by
  dsimp [translateState, step]
  have read_translated : translateBoard displacement state.board
      (translatePoint displacement state.position) = state.board state.position :=
    translateBoard_at_translated_point displacement state.board state.position
  by_cases h : state.board state.position = true
  · simp [h, read_translated, translateBoard_flip, translate_move]
  · simp [h, read_translated, translateBoard_flip, translate_move]

theorem translate_evolve (displacement : Point) (updates : Nat) (state : State) :
    translateState displacement (evolve updates state) =
      evolve updates (translateState displacement state) := by
  induction updates generalizing state with
  | zero => rfl
  | succ updates induction_hypothesis =>
    simp [evolve, induction_hypothesis, translate_step]

end LangtonsAntHC
