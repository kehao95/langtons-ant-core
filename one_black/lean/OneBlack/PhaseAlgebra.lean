import OneBlack.PhaseForwardAvoid

namespace OneBlack.Phase

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks Ordinary PhaseChecks

set_option maxRecDepth 20000

theorem shift_comm (a b : Point) (s : State) :
    OneBlack.shift a (OneBlack.shift b s) =
      OneBlack.shift b (OneBlack.shift a s) := by
  rcases a with ⟨ax, ay⟩
  rcases b with ⟨bx, byValue⟩
  rcases s with ⟨black, ⟨x, y⟩, dir⟩
  apply State.ext
  · funext p
    rcases p with ⟨px, py⟩
    simp [OneBlack.shift, Point.sub]
    congr 2 <;> omega
  · simp [OneBlack.shift, Point.add]
    constructor <;> omega
  · rfl

theorem shiftState_comm (a b : Point) (s : State) : ∀ n,
    shiftState a n (OneBlack.shift b s) =
      OneBlack.shift b (shiftState a n s) := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simp only [shiftState, ih, shift_comm]

theorem drift_reverse_cancel (s : State) :
    OneBlack.shift drift (OneBlack.shift reverseDrift s) = s := by
  rcases s with ⟨black, ⟨x, y⟩, dir⟩
  apply State.ext
  · funext p
    rcases p with ⟨px, py⟩
    simp [OneBlack.shift, Point.sub, drift, reverseDrift]
  · simp [OneBlack.shift, Point.add, drift, reverseDrift]
    constructor <;> omega
  · rfl

theorem shifted_reverse_cancel (s : State) : ∀ n,
    shiftState drift n (shiftState reverseDrift n s) = s := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [shiftState, shiftState_comm, drift_reverse_cancel, ih]

theorem shiftState_add (v : Point) (s : State) (m n : Nat) :
    shiftState v (m + n) s = shiftState v m (shiftState v n s) := by
  induction m with
  | zero => simp [shiftState]
  | succ m ih =>
      rw [Nat.succ_add]
      change OneBlack.shift v (shiftState v (m + n) s) =
        OneBlack.shift v (shiftState v m (shiftState v n s))
      exact congrArg (OneBlack.shift v) ih

theorem shifted_reverse_net (s : State) (extra : Nat) :
    shiftState drift extra
        (shiftState reverseDrift (extra + hitCycles) s) =
      shiftState reverseDrift hitCycles s := by
  rw [shiftState_add, shifted_reverse_cancel]

def reverseArchive (extra : Nat) : BRegion :=
  BRegion.iterate drift extra
    (BRegion.accumulated reverseDrift reverseWake (extra + hitCycles))

def fixedCore : State :=
  shiftState reverseDrift hitCycles (run hitPhase reverseBase.toState)

def preHitArchive (extra : Nat) : BRegion :=
  BRegion.xor
    (BRegion.xor HistoryB (BRegion.accumulated drift cleanWake extra))
    (reverseArchive extra)

theorem bshift_comm (a b : Point) (r : BRegion) :
    BRegion.shift a (BRegion.shift b r) =
      BRegion.shift b (BRegion.shift a r) := by
  funext p
  rcases a with ⟨ax, ay⟩
  rcases b with ⟨bx, byValue⟩
  rcases p with ⟨px, py⟩
  simp [BRegion.shift, Point.sub]
  congr 2 <;> omega

theorem bshift_cancel (r : BRegion) :
    BRegion.shift drift (BRegion.shift reverseDrift r) = r := by
  funext p
  rcases p with ⟨x, y⟩
  simp [BRegion.shift, Point.sub, drift, reverseDrift]

theorem iterate_shift_comm (a b : Point) (r : BRegion) : ∀ n,
    BRegion.iterate a n (BRegion.shift b r) =
      BRegion.shift b (BRegion.iterate a n r) := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simp only [BRegion.iterate, ih, bshift_comm]

theorem iterate_xor (v : Point) (a b : BRegion) : ∀ n,
    BRegion.iterate v n (BRegion.xor a b) =
      BRegion.xor (BRegion.iterate v n a) (BRegion.iterate v n b) := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [BRegion.iterate, ih]
      exact BRegion.shift_xor v _ _

theorem iterate_drift_reverse (r : BRegion) (n : Nat) :
    BRegion.iterate drift (n + 1) (BRegion.shift reverseDrift r) =
      BRegion.iterate drift n r := by
  simp only [BRegion.iterate, iterate_shift_comm, bshift_cancel]

theorem reverseArchive_succ (extra : Nat) :
    reverseArchive (extra + 1) =
      BRegion.xor (BRegion.iterate drift (extra + 1) reverseWake)
        (reverseArchive extra) := by
  unfold reverseArchive
  rw [show extra + 1 + hitCycles = (extra + hitCycles) + 1 by omega]
  change BRegion.iterate drift (extra + 1)
      (BRegion.xor reverseWake
        (BRegion.shift reverseDrift
          (BRegion.accumulated reverseDrift reverseWake
            (extra + hitCycles)))) = _
  rw [iterate_xor, iterate_drift_reverse]

theorem iterate_add (v : Point) (r : BRegion) (m n : Nat) :
    BRegion.iterate v (m + n) r =
      BRegion.iterate v m (BRegion.iterate v n r) := by
  induction m with
  | zero => simp [BRegion.iterate]
  | succ m ih =>
      rw [Nat.succ_add]
      change BRegion.shift v (BRegion.iterate v (m + n) r) =
        BRegion.shift v
          (BRegion.iterate v m (BRegion.iterate v n r))
      exact congrArg (BRegion.shift v) ih

theorem bshift_empty (v : Point) :
    BRegion.shift v BRegion.empty = BRegion.empty := by
  funext p
  rfl

theorem accumulated_succ_far (v : Point) (r : BRegion) : ∀ n,
    BRegion.accumulated v r (n + 1) =
      BRegion.xor (BRegion.iterate v n r)
        (BRegion.accumulated v r n) := by
  intro n
  induction n with
  | zero =>
      simp only [BRegion.accumulated, BRegion.iterate, bshift_empty,
        BRegion.xor_empty]
  | succ n ih =>
      change BRegion.xor r
          (BRegion.shift v (BRegion.accumulated v r (n + 1))) =
        BRegion.xor (BRegion.shift v (BRegion.iterate v n r))
          (BRegion.xor r
            (BRegion.shift v (BRegion.accumulated v r n)))
      rw [ih, BRegion.shift_xor]
      rw [← BRegion.xor_assoc, BRegion.xor_comm r, BRegion.xor_assoc]

theorem preHitArchive_succ (extra : Nat) :
    preHitArchive (extra + 1) =
      BRegion.xor (BRegion.iterate drift extra
        (rawLayerWith (stableResult phaseHead)))
        (preHitArchive extra) := by
  rw [preHitArchive, preHitArchive,
    accumulated_succ_far, reverseArchive_succ]
  have shiftedReverse :
      BRegion.iterate drift extra
          (BRegion.iterate drift 1 reverseWake) =
        BRegion.iterate drift (extra + 1) reverseWake := by
    exact (iterate_add drift reverseWake extra 1).symm
  simp only [PhaseChecks.rawLayerWith]
  rw [iterate_xor, shiftedReverse]
  funext p
  repeat' rw [BRegion.xor_apply]
  exact (by decide : ∀ a b c d e : Bool,
    Bool.xor (Bool.xor a (Bool.xor b c)) (Bool.xor d e) =
      Bool.xor (Bool.xor b d) (Bool.xor (Bool.xor a c) e)) _ _ _ _ _

theorem iterate_raw_from_lag (extra : Nat) :
    BRegion.iterate drift (phaseLag + extra)
        (rawLayerWith (stableResult phaseHead)) =
      BRegion.iterate drift extra layer := by
  rw [Nat.add_comm, iterate_add]
  rfl

theorem preHitArchive_normal : ∀ extra,
    preHitArchive (phaseLag + extra) =
      BRegion.xor (BRegion.accumulated drift layer extra)
        (preHitArchive phaseLag) := by
  intro extra
  induction extra with
  | zero => rw [BRegion.accumulated, BRegion.empty_xor, Nat.add_zero]
  | succ extra ih =>
      rw [show phaseLag + (extra + 1) = (phaseLag + extra) + 1 by omega,
        preHitArchive_succ, iterate_raw_from_lag, ih,
        accumulated_succ_far]
      exact (BRegion.xor_assoc _ _ _).symm


end OneBlack.Phase
