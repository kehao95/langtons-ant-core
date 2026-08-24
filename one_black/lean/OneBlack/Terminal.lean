import OneBlack.Highway

namespace OneBlack.Terminal

open OneBlack Highway

def offset (s : FState) : Point := baseF.pos.sub s.pos

def check (s : FState) : Bool :=
  let v := offset s
  decide (s.dir = baseF.dir) &&
  support.all (fun p =>
    s.black.contains (p.sub v) == baseF.black.contains p) &&
  s.black.toList.all (fun p =>
    let target := v.add p
    decide (target ∈ support) || separatedFromSupport target)

theorem check_sound {s : FState} (accepted : check s = true) :
    Boundary 0 (OneBlack.shift (offset s) s.toState) := by
  simp only [check, Bool.and_eq_true] at accepted
  rcases accepted with ⟨⟨dir, active⟩, background⟩
  let v := offset s
  constructor
  · refine ⟨?_, ?_, ?_⟩
    · change baseF.pos = v.add s.pos
      dsimp [v, offset]
      rcases baseF.pos with ⟨baseX, baseY⟩
      rcases s.pos with ⟨x, y⟩
      simp [Point.sub, Point.add]
    · change baseF.dir = s.dir
      exact (of_decide_eq_true dir).symm
    · intro p hp
      change baseF.black.contains p = s.black.contains (p.sub v)
      exact eq_of_beq ((List.all_eq_true.mp active) p hp) |>.symm
  · intro p black outside later positive
    change s.black.contains (p.sub v) = true at black
    change p ∉ support at outside
    have inTree : p.sub v ∈ s.black := by
      rw [← Std.TreeSet.contains_iff_mem]
      exact black
    have inList : p.sub v ∈ s.black.toList := Std.TreeSet.mem_toList.mpr inTree
    have accepted := (List.all_eq_true.mp background) (p.sub v) inList
    change (decide (v.add (p.sub v) ∈ support) ||
      separatedFromSupport (v.add (p.sub v))) = true at accepted
    have restored : v.add (p.sub v) = p := by
      rcases v with ⟨vx, vy⟩
      rcases p with ⟨px, py⟩
      simp [Point.add, Point.sub]
      constructor <;> omega
    have pair : separatedFromSupport p = true := by
      rw [restored] at accepted
      simpa [outside] using accepted
    exact separated_excludes (fun source hs =>
      separated_checked ((List.all_eq_true.mp pair) source hs)) later positive

theorem check_permanent {s : FState} (accepted : check s = true) :
    PermanentP104 s.toState := by
  let v := offset s
  let undo : Point := ⟨-v.x, -v.y⟩
  have pulled := tail_permanent (check_sound accepted).tail
  have returned := pulled.shift undo
  have cancel : OneBlack.shift undo (OneBlack.shift v s.toState) = s.toState := by
    rcases v with ⟨vx, vy⟩
    rcases s with ⟨black, ⟨x, y⟩, dir⟩
    apply State.ext
    · funext p
      rcases p with ⟨px, py⟩
      simp [OneBlack.shift, Point.sub, Point.add, undo]
    · simp [OneBlack.shift, Point.add, FState.toState, undo]
      constructor <;> omega
    · rfl
  rw [cancel] at returned
  exact returned

def orientation (s : FState) : Option Nat :=
  if check s then some 0 else if check (s.rotateN 1) then some 1
  else if check (s.rotateN 2) then some 2
  else if check (s.rotateN 3) then some 3 else none

def any (s : FState) : Bool := (orientation s).isSome

def turn (s : FState) : Nat := (orientation s).getD 0

def normalizedAt (turns : Nat) (s : FState) (p : Point) : Point :=
  let rotated := s.rotateN turns
  (offset rotated).add (p.rotateN turns)

def normalizedPoint (s : FState) (p : Point) : Point :=
  normalizedAt (turn s) s p

theorem orientation_sound {s : FState} {turns : Nat}
    (found : orientation s = some turns) :
    turns < 4 ∧ check (s.rotateN turns) = true := by
  unfold orientation at found
  split at found <;> rename_i zero
  · have : turns = 0 := by simpa using found.symm
    subst turns
    exact ⟨by omega, by simpa [FState.rotateN] using zero⟩
  · split at found <;> rename_i one
    · have : turns = 1 := by simpa using found.symm
      subst turns
      exact ⟨by omega, one⟩
    · split at found <;> rename_i two
      · have : turns = 2 := by simpa using found.symm
        subst turns
        exact ⟨by omega, two⟩
      · split at found <;> rename_i three
        · have : turns = 3 := by simpa using found.symm
          subst turns
          exact ⟨by omega, three⟩
        · simp at found

theorem turn_checked {s : FState} (accepted : any s = true) :
    check (s.rotateN (turn s)) = true := by
  unfold any at accepted
  cases found : orientation s with
  | none => simp [found] at accepted
  | some turns =>
      have checked := (orientation_sound found).2
      simpa [turn, found] using checked

theorem future_normalized {s : FState} (accepted : any s = true)
    {p : Point} (read : ∃ updates, (OneBlack.run updates s.toState).pos = p) :
    ∃ cycle, supportAt cycle (normalizedPoint s p) := by
  rcases read with ⟨updates, position⟩
  let rotated := s.rotateN (turn s)
  have boundary := check_sound (turn_checked accepted)
  rcases boundary.future_support updates with ⟨cycle, inside⟩
  refine ⟨cycle, ?_⟩
  change supportAt cycle
    ((offset rotated).add (p.rotateN (turn s)))
  change supportAt cycle
    (OneBlack.run updates (OneBlack.shift (offset rotated) rotated.toState)).pos
    at inside
  rw [run_shift, FState.toState_rotateN, run_rotateN] at inside
  change supportAt cycle
    ((offset rotated).add ((OneBlack.rotateN (turn s)
      (OneBlack.run updates s.toState)).pos)) at inside
  rw [rotateN_pos, position] at inside
  exact inside

theorem future_excluded {s : FState} (accepted : any s = true) {p : Point}
    (outside : normalizedPoint s p ∉ support)
    (separated : separatedFromSupport (normalizedPoint s p) = true) :
    ¬(∃ updates, (OneBlack.run updates s.toState).pos = p) := by
  intro read
  rcases future_normalized accepted read with ⟨cycle, inside⟩
  cases cycle with
  | zero => exact outside inside
  | succ cycle =>
      exact separated_excludes (fun source member =>
        separated_checked ((List.all_eq_true.mp separated) source member))
        (cycle + 1) (Nat.zero_lt_succ cycle) inside

theorem any_permanent {s : FState} (accepted : any s = true) :
    PermanentP104 s.toState := by
  unfold any at accepted
  cases found : orientation s with
  | none => simp [found] at accepted
  | some turns =>
    have sound := orientation_sound found
    have cases : turns = 0 ∨ turns = 1 ∨ turns = 2 ∨ turns = 3 := by omega
    rcases cases with rfl | rfl | rfl | rfl
    · exact check_permanent sound.2
    · have p := check_permanent sound.2
      rw [FState.toState_rotateN] at p
      simpa [OneBlack.rotateN] using p.rot.rot.rot
    · have p := check_permanent sound.2
      rw [FState.toState_rotateN] at p
      simpa [OneBlack.rotateN] using p.rot.rot
    · have p := check_permanent sound.2
      rw [FState.toState_rotateN] at p
      simpa [OneBlack.rotateN] using p.rot

def lands (s : FState) (updates : Nat) : Bool := any (s.run updates)

theorem lands_sound {s : FState} {updates : Nat}
    (accepted : lands s updates = true) : ReachesP104 s.toState := by
  refine ⟨updates, ?_⟩
  rw [← FState.toState_run]
  exact any_permanent accepted

def find : Nat → FState → Option Nat
  | 0, s => if any s then some 0 else none
  | fuel + 1, s =>
      if any s then some 0 else (find fuel s.step).map Nat.succ

theorem find_sound {fuel : Nat} {s : FState} {updates : Nat}
    (found : find fuel s = some updates) : lands s updates = true := by
  induction fuel generalizing s updates with
  | zero =>
      simp only [find] at found
      split at found
      · cases Option.some.inj found
        simpa [lands, FState.run] using ‹any s = true›
      · simp at found
  | succ fuel ih =>
      simp only [find] at found
      split at found
      · cases Option.some.inj found
        simpa [lands, FState.run] using ‹any s = true›
      · cases result : find fuel s.step with
        | none => simp [result] at found
        | some k =>
            simp [result] at found
            subst updates
            have accepted := ih result
            simpa [lands, FState.run_step] using accepted

theorem find_reaches {fuel : Nat} {s : FState} (found : (find fuel s).isSome) :
    ReachesP104 s.toState := by
  rcases value : find fuel s with _ | updates <;> simp_all
  exact lands_sound (find_sound value)

end OneBlack.Terminal
