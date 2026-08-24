import OneBlack.Geometry

namespace OneBlack.Induction

open OneBlack

theorem Region.Disjoint.mono_right {a b c : Region}
    (disjoint : Region.Disjoint a b) (subset : Region.Subset c b) :
    Region.Disjoint a c := by
  intro p inA inC
  exact disjoint p inA (subset inC)

theorem avoidsFor_iff (archive : Region) (s : State) (n : Nat) :
    AvoidsFor archive s n ↔ Region.Disjoint archive (reads s n) := by
  constructor
  · intro avoids p inside read
    rcases read with ⟨k, before, rfl⟩
    exact avoids k before inside
  · intro disjoint k before inside
    exact disjoint _ inside ⟨k, before, rfl⟩

theorem reads_shiftState (v : Point) (copies : Nat) (s : State) (n : Nat) :
    reads (shiftState v copies s) n = shiftRegion v copies (reads s n) := by
  induction copies with
  | zero => rfl
  | succ copies ih => simpa [shiftState, shiftRegion, reads_shift, ih]

theorem futureReads_shiftState (v : Point) (copies : Nat) (s : State) :
    futureReads (shiftState v copies s) =
      shiftRegion v copies (futureReads s) := by
  induction copies with
  | zero => rfl
  | succ copies ih => simpa [shiftState, shiftRegion, futureReads_shift, ih]

theorem shiftRegion_subset (v : Point) {a b : Region}
    (subset : Region.Subset a b) : ∀ n,
    Region.Subset (shiftRegion v n a) (shiftRegion v n b) := by
  intro n
  induction n with
  | zero => exact subset
  | succ n ih =>
      intro p inside
      exact ih inside

def lane (clean : State) (v obstacle : Point) (extra : Nat) : State :=
  blacken (shiftPoint v extra obstacle) clean

def duration (period base : Nat) (extra : Nat) : Nat := extra * period + base

def footprint (v : Point) (clean base : Region) : Nat → Region
  | 0 => base
  | n + 1 => Region.union clean (Region.shift v (footprint v clean base n))

def archive (v : Point) (wake : Region) : Nat → Region
  | 0 => Region.empty
  | n + 1 => Region.union wake (Region.shift v (archive v wake n))

structure NormalForm (clean : State) (v obstacle : Point)
    (period baseTime : Nat) (cleanReads baseReads wake : Region)
    (extra : Nat) : Prop where
  readSet : reads (lane clean v obstacle extra) (duration period baseTime extra) =
    footprint v cleanReads baseReads extra
  final : SameOutside (archive v wake extra)
    (run (duration period baseTime extra) (lane clean v obstacle extra))
    (shiftState v extra (run baseTime (lane clean v obstacle 0)))

structure Data (clean : State) (v obstacle : Point)
    (period baseTime : Nat) (cleanReads baseReads wake corridor : Region) : Prop where
  cleanReadsExact : reads clean period = cleanReads
  cleanBlock : SameOutside wake (run period clean) (OneBlack.shift v clean)
  baseReadsExact : reads (lane clean v obstacle 0) baseTime = baseReads
  obstacleMisses : ∀ extra, ¬cleanReads (shiftPoint v (extra + 1) obstacle)
  wakeMisses : ∀ extra, Region.Disjoint wake
    (Region.shift v (footprint v cleanReads baseReads extra))
  baseFuture : Region.Subset
    (futureReads (run baseTime (lane clean v obstacle 0))) corridor
  archiveMisses : ∀ extra, Region.Disjoint (archive v wake extra)
    (shiftRegion v extra corridor)

theorem Data.cleanAvoids {clean : State} {v obstacle : Point}
    {period baseTime : Nat} {cleanReads baseReads wake corridor : Region}
    (data : Data clean v obstacle period baseTime cleanReads baseReads wake corridor)
    (extra : Nat) : Avoids (shiftPoint v (extra + 1) obstacle) clean period := by
  intro k before equal
  apply data.obstacleMisses extra
  rw [← data.cleanReadsExact]
  exact ⟨k, before, equal⟩

theorem Data.recurrence {clean : State} {v obstacle : Point}
    {period baseTime : Nat} {cleanReads baseReads wake corridor : Region}
    (data : Data clean v obstacle period baseTime cleanReads baseReads wake corridor)
    (extra : Nat) : SameOutside wake
      (run period (lane clean v obstacle (extra + 1)))
      (OneBlack.shift v (lane clean v obstacle extra)) := by
  unfold lane
  rw [run_blacken period (data.cleanAvoids extra), shift_blacken]
  change SameOutside wake
    (blacken (shiftPoint v (extra + 1) obstacle) (run period clean))
    (blacken (v.add (shiftPoint v extra obstacle)) (OneBlack.shift v clean))
  rw [show shiftPoint v (extra + 1) obstacle =
    v.add (shiftPoint v extra obstacle) by rfl]
  rcases data.cleanBlock with ⟨position, heading, colours⟩
  refine ⟨position, heading, ?_⟩
  intro p outside
  by_cases current : p = v.add (shiftPoint v extra obstacle)
  · subst p; simp [blacken]
  · simp [blacken, current, colours p outside]

theorem Data.cleanPrefix {clean : State} {v obstacle : Point}
    {period baseTime : Nat} {cleanReads baseReads wake corridor : Region}
    (data : Data clean v obstacle period baseTime cleanReads baseReads wake corridor)
    (extra : Nat) : reads (lane clean v obstacle (extra + 1)) period = cleanReads := by
  unfold lane
  have same := blacken_sameOutside (shiftPoint v (extra + 1) obstacle) clean
  have avoids : AvoidsFor
      (Region.singleton (shiftPoint v (extra + 1) obstacle)) clean period := by
    intro k before equal
    exact data.cleanAvoids extra k before equal
  rw [reads_eq_of_sameOutside period same avoids, data.cleanReadsExact]

theorem exact {clean : State} {v obstacle : Point}
    {period baseTime : Nat} {cleanReads baseReads wake corridor : Region}
    (data : Data clean v obstacle period baseTime cleanReads baseReads wake corridor) :
    ∀ extra, NormalForm clean v obstacle period baseTime cleanReads baseReads wake extra := by
  intro extra
  induction extra with
  | zero =>
      refine ⟨?_, ?_⟩
      · simpa [duration, footprint] using data.baseReadsExact
      · simpa [duration, shiftState, archive] using
          (show SameOutside Region.empty
              (run baseTime (lane clean v obstacle 0))
              (run baseTime (lane clean v obstacle 0)) from
            ⟨rfl, rfl, fun _ _ => rfl⟩)
  | succ extra ih =>
      have recurrence := data.recurrence extra
      have shiftedReads :
          reads (OneBlack.shift v (lane clean v obstacle extra))
              (duration period baseTime extra) =
            Region.shift v (footprint v cleanReads baseReads extra) := by
        rw [reads_shift, ih.readSet]
      have avoids : AvoidsFor wake
          (OneBlack.shift v (lane clean v obstacle extra))
          (duration period baseTime extra) := by
        rw [avoidsFor_iff, shiftedReads]
        exact data.wakeMisses extra
      have tailReads :
          reads (run period (lane clean v obstacle (extra + 1)))
              (duration period baseTime extra) =
            Region.shift v (footprint v cleanReads baseReads extra) := by
        rw [reads_eq_of_sameOutside _ recurrence avoids, shiftedReads]
      refine ⟨?_, ?_⟩
      · rw [show duration period baseTime (extra + 1) =
          period + duration period baseTime extra by
            simp [duration, Nat.add_mul, Nat.add_comm,
              Nat.add_left_comm],
          reads_add, data.cleanPrefix extra, tailReads]
        rfl
      · have tailSame := recurrence.runFor _ avoids
        rw [run_shift] at tailSame
        have shiftedIH := ih.final.shift v
        have composed := tailSame.trans_union shiftedIH
        simpa [duration, run_add, shiftState, archive, Nat.add_mul,
          Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using composed

theorem reaches {clean : State} {v obstacle : Point}
    {period baseTime : Nat} {cleanReads baseReads wake corridor : Region}
    (data : Data clean v obstacle period baseTime cleanReads baseReads wake corridor)
    (baseTerminal : PermanentP104 (run baseTime (lane clean v obstacle 0))) :
    ∀ extra, ReachesP104 (lane clean v obstacle extra) := by
  intro extra
  have normal := exact data extra
  refine ⟨duration period baseTime extra, ?_⟩
  have terminal : PermanentP104
      (shiftState v extra (run baseTime (lane clean v obstacle 0))) := by
    clear normal
    induction extra with
    | zero => exact baseTerminal
    | succ extra ih => exact ih.shift v
  apply terminal.of_sameReadTrace
  apply sameReadTrace_of_archive normal.final
  apply AvoidsForever.of_disjoint
  rw [futureReads_shiftState]
  exact Region.Disjoint.mono_right (data.archiveMisses extra) (by
    intro p inside
    exact shiftRegion_subset v data.baseFuture extra inside)

end OneBlack.Induction
