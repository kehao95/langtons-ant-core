import Std.Data.TreeSet.Lemmas
import Lean.Elab.Tactic.Omega

namespace OneBlack

structure Point where
  x : Int
  y : Int
deriving DecidableEq, Repr

inductive Heading where
  | north | east | south | west
deriving DecidableEq, Repr

def Heading.right : Heading → Heading
  | .north => .east
  | .east => .south
  | .south => .west
  | .west => .north

def Heading.left : Heading → Heading
  | .north => .west
  | .west => .south
  | .south => .east
  | .east => .north

def Point.move (p : Point) : Heading → Point
  | .north => ⟨p.x, p.y + 1⟩
  | .east => ⟨p.x + 1, p.y⟩
  | .south => ⟨p.x, p.y - 1⟩
  | .west => ⟨p.x - 1, p.y⟩

structure State where
  black : Point → Bool
  pos : Point
  dir : Heading

@[ext] theorem State.ext {a b : State} (colour : a.black = b.black)
    (pos : a.pos = b.pos) (dir : a.dir = b.dir) : a = b := by
  cases a; cases b; simp_all

def toggle (black : Point → Bool) (current : Point) : Point → Bool :=
  fun p => if p = current then !(black p) else black p

def step (s : State) : State :=
  let d := if s.black s.pos then s.dir.left else s.dir.right
  ⟨toggle s.black s.pos, s.pos.move d, d⟩

def run : Nat → State → State
  | 0, s => s
  | n + 1, s => step (run n s)

theorem run_add (m n : Nat) (s : State) : run (m + n) s = run n (run m s) := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [run, Nat.add_succ] using congrArg step ih

def Point.add (a b : Point) : Point := ⟨a.x + b.x, a.y + b.y⟩
def Point.sub (a b : Point) : Point := ⟨a.x - b.x, a.y - b.y⟩
def Point.rot (p : Point) : Point := ⟨-p.y, p.x⟩
def Point.unrot (p : Point) : Point := ⟨p.y, -p.x⟩

def Heading.rot : Heading → Heading
  | .north => .west
  | .west => .south
  | .south => .east
  | .east => .north

def shift (v : Point) (s : State) : State :=
  ⟨fun p => s.black (p.sub v), v.add s.pos, s.dir⟩

def rotate (s : State) : State :=
  ⟨fun p => s.black p.unrot, s.pos.rot, s.dir.rot⟩

@[simp] theorem Point.sub_add (v p : Point) : (v.add p).sub v = p := by
  cases v; cases p; simp [Point.add, Point.sub]; omega

@[simp] theorem Point.add_sub (v p : Point) : v.add (p.sub v) = p := by
  cases v; cases p; simp [Point.add, Point.sub]; omega

@[simp] theorem Point.add_zero (p : Point) : p.add ⟨0, 0⟩ = p := by
  cases p
  simp [Point.add]

@[simp] theorem Point.zero_add (p : Point) : (⟨0, 0⟩ : Point).add p = p := by
  cases p
  simp [Point.add]

@[simp] theorem Point.rot_zero : (⟨0, 0⟩ : Point).rot = ⟨0, 0⟩ := rfl

@[simp] theorem Point.unrot_rot (p : Point) : p.rot.unrot = p := by
  cases p; simp [Point.rot, Point.unrot]

@[simp] theorem Point.rot_unrot (p : Point) : p.unrot.rot = p := by
  cases p; simp [Point.rot, Point.unrot]

theorem Point.add_move (v p : Point) (d : Heading) :
    v.add (p.move d) = (v.add p).move d := by
  cases v; cases p; cases d <;> simp [Point.add, Point.move] <;> omega

theorem Point.rot_move (p : Point) (d : Heading) :
    (p.move d).rot = p.rot.move d.rot := by
  cases p; cases d <;> simp [Point.rot, Point.move, Heading.rot] <;> omega

@[simp] theorem Heading.rot_right (d : Heading) : d.right.rot = d.rot.right := by
  cases d <;> rfl

@[simp] theorem Heading.rot_left (d : Heading) : d.left.rot = d.rot.left := by
  cases d <;> rfl

theorem step_shift (v : Point) (s : State) : step (shift v s) = shift v (step s) := by
  cases s with
  | mk black pos dir =>
    apply State.ext
    · funext p
      by_cases here : p = v.add pos
      · subst p; simp [step, shift, toggle]
      · have away : p.sub v ≠ pos := by
          intro eq
          apply here
          have := congrArg (Point.add v) eq
          simpa using this
        simp [step, shift, toggle, here, away]
    · simp [step, shift, Point.add_move]
    · simp [step, shift]

theorem step_rotate (s : State) : step (rotate s) = rotate (step s) := by
  cases s with
  | mk black pos dir =>
    apply State.ext
    · funext p
      by_cases here : p = pos.rot
      · subst p; simp [step, rotate, toggle]
      · have away : p.unrot ≠ pos := by
          intro eq
          apply here
          have := congrArg Point.rot eq
          simpa using this
        simp [step, rotate, toggle, here, away]
    · by_cases colour : black pos <;> simp [step, rotate, colour, Point.rot_move]
    · by_cases colour : black pos <;> simp [step, rotate, colour]

theorem run_shift (v : Point) (n : Nat) (s : State) :
    run n (shift v s) = shift v (run n s) := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [run, ih] using step_shift v (run n s)

theorem run_rotate (n : Nat) (s : State) :
    run n (rotate s) = rotate (run n s) := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [run, ih] using step_rotate (run n s)

abbrev Point.cmp : Point → Point → Ordering :=
  compareLex (compareOn Point.x) (compareOn Point.y)

@[simp] theorem Point.cmp_eq (a b : Point) : Point.cmp a b = .eq ↔ a = b := by
  cases a; cases b; simp [Point.cmp, compareLex, compareOn]

instance : Std.LawfulEqCmp Point.cmp where
  eq_of_compare := (Point.cmp_eq _ _).mp

abbrev PointSet := Std.TreeSet Point Point.cmp

def PointSet.ofList : List Point → PointSet
  | [] => {}
  | p :: ps => (ofList ps).insert p

@[simp] theorem PointSet.contains_ofList (ps : List Point) (p : Point) :
    (PointSet.ofList ps).contains p = decide (p ∈ ps) := by
  induction ps with
  | nil => simp [PointSet.ofList]
  | cons q qs ih =>
    by_cases eq : q = p
    · subst q; simp [PointSet.ofList, ih]
    · have cmp : Point.cmp q p ≠ .eq := fun h => eq ((Point.cmp_eq q p).mp h)
      have beq : (Point.cmp q p == .eq) = false := beq_false_of_ne cmp
      have ne : p ≠ q := fun h => eq h.symm
      simp [PointSet.ofList, ih, beq, ne]

def PointSet.flip (s : PointSet) (p : Point) : PointSet :=
  if s.contains p then s.erase p else s.insert p

theorem PointSet.contains_flip (s : PointSet) (current p : Point) :
    (s.flip current).contains p =
      if p = current then !(s.contains p) else s.contains p := by
  by_cases black : s.contains current <;> by_cases eq : p = current
  · subst p; simp [PointSet.flip, black]
  · simp [PointSet.flip, black, eq]; intro _ h; exact eq h.symm
  · subst p; simp [PointSet.flip, black]
  · simp [PointSet.flip, black, eq]; intro h; exact (eq h.symm).elim

structure FState where
  black : PointSet
  pos : Point
  dir : Heading

def FState.step (s : FState) : FState :=
  let d := if s.black.contains s.pos then s.dir.left else s.dir.right
  ⟨s.black.flip s.pos, s.pos.move d, d⟩

def FState.run : Nat → FState → FState
  | 0, s => s
  | n + 1, s => step (run n s)

def FState.reads : Nat → FState → List Point
  | 0, _ => []
  | n + 1, s => s.pos :: reads n s.step

theorem FState.run_step (n : Nat) (s : FState) :
    s.step.run n = s.run (n + 1) := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [FState.run] using congrArg FState.step ih

theorem FState.mem_reads_iff (p : Point) (n : Nat) (s : FState) :
    p ∈ s.reads n ↔ ∃ k, k < n ∧ (s.run k).pos = p := by
  induction n generalizing s with
  | zero => simp [FState.reads]
  | succ n ih =>
    constructor
    · intro h
      rcases (List.mem_cons.mp h) with h | h
      · exact ⟨0, Nat.zero_lt_succ _, by simpa using h.symm⟩
      · rcases (ih s.step).mp h with ⟨k, hk, eq⟩
        refine ⟨k + 1, Nat.succ_lt_succ hk, ?_⟩
        rw [← FState.run_step]
        exact eq
    · rintro ⟨k, hk, eq⟩
      cases k with
      | zero => exact List.mem_cons.mpr (Or.inl (by simpa using eq.symm))
      | succ k =>
        apply List.mem_cons.mpr; right
        apply (ih s.step).mpr
        refine ⟨k, Nat.lt_of_succ_lt_succ hk, ?_⟩
        rw [FState.run_step]
        exact eq

def FState.toState (s : FState) : State :=
  ⟨s.black.contains, s.pos, s.dir⟩

def FState.rotate (s : FState) : FState :=
  ⟨PointSet.ofList (s.black.toList.map Point.rot), s.pos.rot, s.dir.rot⟩

theorem FState.toState_rotate (s : FState) :
    s.rotate.toState = OneBlack.rotate s.toState := by
  apply State.ext
  · funext p
    simp only [FState.rotate, FState.toState, OneBlack.rotate,
      PointSet.contains_ofList]
    apply Bool.eq_iff_iff.mpr
    constructor
    · intro accepted
      rcases List.mem_map.mp (of_decide_eq_true accepted) with ⟨q, member, rfl⟩
      exact Std.TreeSet.contains_iff_mem.mpr
        (Std.TreeSet.mem_toList.mp (by simpa using member))
    · intro accepted
      apply decide_eq_true
      apply List.mem_map.mpr
      exact ⟨p.unrot, Std.TreeSet.mem_toList.mpr
        (Std.TreeSet.contains_iff_mem.mp accepted), Point.rot_unrot p⟩
  · rfl
  · rfl

def FState.rotateN : Nat → FState → FState
  | 0, s => s
  | n + 1, s => (rotateN n s).rotate

def Point.rotateN : Nat → Point → Point
  | 0, p => p
  | n + 1, p => (rotateN n p).rot

def rotateN : Nat → State → State
  | 0, s => s
  | n + 1, s => rotate (rotateN n s)

@[simp] theorem rotateN_pos (n : Nat) (s : State) :
    (rotateN n s).pos = s.pos.rotateN n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [rotateN, Point.rotateN, OneBlack.rotate, ih]

theorem run_rotateN (turns updates : Nat) (s : State) :
    run updates (rotateN turns s) = rotateN turns (run updates s) := by
  induction turns with
  | zero => rfl
  | succ turns ih => simpa [rotateN, run_rotate, ih]

theorem FState.toState_rotateN (n : Nat) (s : FState) :
    (s.rotateN n).toState = OneBlack.rotateN n s.toState := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [show n + 1 = Nat.succ n by omega]
      simp [FState.rotateN, OneBlack.rotateN, FState.toState_rotate, ih]

theorem FState.toState_step (s : FState) :
    s.step.toState = OneBlack.step s.toState := by
  apply State.ext
  · funext p; simp [FState.step, FState.toState, OneBlack.step, toggle,
      PointSet.contains_flip]
  · simp [FState.step, FState.toState, OneBlack.step]
  · simp [FState.step, FState.toState, OneBlack.step]

theorem FState.toState_run (n : Nat) (s : FState) :
    (s.run n).toState = OneBlack.run n s.toState := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [FState.run, OneBlack.run, FState.toState_step, ih]

def white : State := ⟨fun _ => false, ⟨0, 0⟩, .north⟩
def singleton (p : Point) : State := ⟨fun q => decide (q = p), ⟨0, 0⟩, .north⟩
def fwhite : FState := ⟨{}, ⟨0, 0⟩, .north⟩
def fsingleton (p : Point) : FState := ⟨PointSet.ofList [p], ⟨0, 0⟩, .north⟩

theorem fwhite_exact : fwhite.toState = white := by
  apply State.ext
  · funext p; simp [fwhite, FState.toState, white]
  · rfl
  · rfl

theorem fsingleton_exact (p : Point) : (fsingleton p).toState = singleton p := by
  apply State.ext
  · funext q; simp [fsingleton, FState.toState, singleton, eq_comm]
  · rfl
  · rfl

end OneBlack
