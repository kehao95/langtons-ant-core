import OneBlack.PristineChecks

namespace OneBlack.Pristine

open OneBlack Highway Terminal Entry Rays RayGeometry Induction PristineChecks

set_option maxRecDepth 10000

theorem replayFrom_final (n : Nat) (s : FState) (reads : PointSet) :
    (replayFrom n s reads).1 = s.run n := by
  induction n generalizing s reads with
  | zero => rfl
  | succ n ih => simpa [replayFrom, ih] using FState.run_step n s

theorem replay_final (n : Nat) (s : FState) :
    (replay n s).1 = s.run n := by
  exact replayFrom_final n s {}

theorem replayFrom_reads (p : Point) (n : Nat) (s : FState)
    (recorded : PointSet) :
    p ∈ (replayFrom n s recorded).2 ↔
      p ∈ recorded ∨ p ∈ s.reads n := by
  induction n generalizing s recorded with
  | zero => simp [replayFrom, FState.reads]
  | succ n ih =>
      simp only [replayFrom, ih, Std.TreeSet.mem_insert, Point.cmp_eq,
        FState.reads, List.mem_cons]
      constructor
      · rintro ((equal | old) | tail)
        · exact Or.inr (Or.inl equal.symm)
        · exact Or.inl old
        · exact Or.inr (Or.inr tail)
      · rintro (old | equal | tail)
        · exact Or.inl (Or.inr old)
        · exact Or.inl (Or.inl equal.symm)
        · exact Or.inr tail

theorem replay_reads (p : Point) (n : Nat) (s : FState) :
    p ∈ (replay n s).2 ↔ p ∈ s.reads n := by
  simpa [replay] using replayFrom_reads p n s {}

theorem head_iff {p : Point} : p ∈ heads ↔ Head p := by
  simp [heads, Head, Support]

theorem active_reaches (certificate : Certificate) {p : Point}
    (member : p ∈ PristineChecks.active) :
    ReachesP104 (blacken p base) := by
  have paired : p ∈
      (PristineChecks.active.zip FiniteData.pristineActiveTimes).map Prod.fst := by
    have lengths : PristineChecks.active.length =
        FiniteData.pristineActiveTimes.length := certificate.activeMatch
    simpa [List.map_fst_zip, lengths] using member
  rcases List.mem_map.mp paired with ⟨⟨q, updates⟩, inCases, equal⟩
  simp at equal
  subst q
  have accepted : lands (force p baseF) updates = true :=
    (List.all_eq_true.mp certificate.activePass) _
      (List.mem_map.mpr ⟨(p, updates), inCases, rfl⟩)
  have reached := lands_sound accepted
  simpa [base] using reached

theorem shallow_reaches (certificate : Certificate) {head : Point}
    (member : head ∈ heads)
    {depth : Nat} (positive : 0 < depth) (shallow : depth < stableDepth head) :
    ReachesP104 (blacken (obstacle head depth) base) := by
  have index : depth - 1 ∈ List.range (stableDepth head - 1) := by
    rw [List.mem_range]
    omega
  have checkMember :
      lands (initial head depth) (witnessTime head depth) ∈ directChecks := by
    apply List.mem_flatMap.mpr
    refine ⟨head, member, ?_⟩
    apply List.mem_map.mpr
    refine ⟨depth - 1, index, ?_⟩
    congr 2 <;> omega
  have accepted := (List.all_eq_true.mp certificate.directPass) _ checkMember
  have reached := lands_sound accepted
  simpa [initial, obstacle, base] using reached

abbrev CleanReads : Region := reads base period
abbrev Wake : Region := fun p => p ∈ wakeCells

def stableInitial (head : Point) : FState := initial head (stableDepth head)
def stableTime (head : Point) : Nat := witnessTime head (stableDepth head)
@[irreducible] def stableResult (head : Point) : FState × PointSet :=
  replay (stableTime head) (stableInitial head)
def stableFinal (head : Point) : FState := (stableResult head).1
def stableTurn (head : Point) : Nat := turn (stableFinal head)
abbrev BaseReads (head : Point) : Region :=
  reads (stableInitial head).toState (stableTime head)
abbrev Corridor (head : Point) : Region :=
  futureReads (stableFinal head).toState

theorem stable_snapshot_mem {head : Point} (member : head ∈ heads) :
    {
      head := head
      time := stableTime head
      result := stableResult head
      reads := (stableResult head).2.toList
      turns := stableTurn head
      accepted := orientation (stableFinal head) |>.isSome
    } ∈ snapshots := by
  apply List.mem_map.mpr
  refine ⟨head, member, ?_⟩
  unfold stableTurn stableFinal
  rw [stableResult]
  simp [stableTime, stableInitial, turn]

theorem stable_checked (certificate : Certificate) {head : Point}
    (member : head ∈ heads) :
    stableCheck {
      head := head
      time := stableTime head
      result := stableResult head
      reads := (stableResult head).2.toList
      turns := stableTurn head
      accepted := orientation (stableFinal head) |>.isSome
    } = true :=
  (List.all_eq_true.mp certificate.stablePass) _ (stable_snapshot_mem member)

theorem stable_accepted (certificate : Certificate) {head : Point}
    (member : head ∈ heads) :
    any (stableFinal head) = true := by
  have checked := stable_checked certificate member
  simp only [stableCheck, stableFinal, Bool.and_eq_true] at checked
  simpa [any] using checked.1

theorem stable_wake_checked (certificate : Certificate) {head : Point}
    (member : head ∈ heads)
    {wake : Point} (wakeMember : wake ∈ wakeCells) :
    support.all (fun target => !(raysMeet 0 wake target)) = true ∧
    (stableResult head).2.toList.all
      (fun target => !(raysMeet 0 wake target)) = true ∧
    support.all (fun source =>
      !(raysMeet (stableTurn head)
        (normalizedAt (stableTurn head) (stableFinal head) wake) source)) = true := by
  have checked := stable_checked certificate member
  simp only [stableCheck, stableFinal, Bool.and_eq_true] at checked
  have allWake : wakeCells.all (fun wake =>
      support.all (fun target => !(raysMeet 0 wake target)) &&
      (stableResult head).2.toList.all
        (fun target => !(raysMeet 0 wake target)) &&
      support.all (fun source =>
        !(raysMeet (stableTurn head)
          (normalizedAt (stableTurn head) (stableFinal head) wake) source))) = true := by
    exact checked.2
  have one := (List.all_eq_true.mp allWake) wake wakeMember
  simp only [Bool.and_eq_true] at one
  exact ⟨one.1.1, one.1.2, one.2⟩

theorem clean_block :
    SameOutside Wake (run period base) (OneBlack.shift drift base) := by
  refine ⟨?_, ?_, ?_⟩
  · change (run period baseF.toState).pos = drift.add baseF.pos
    rw [← FState.toState_run]
    exact transport_pos_fact
  · change (run period baseF.toState).dir = baseF.dir
    rw [← FState.toState_run]
    exact transport_dir_fact
  · intro p outside
    change (run period baseF.toState).black p =
      baseF.black.contains (p.sub drift)
    rw [← FState.toState_run]
    by_cases candidate : p ∈ support ++ shiftedSupport
    · have same :
          (baseF.run period).black.contains p =
            baseF.black.contains (p.sub drift) := by
        cases left : (baseF.run period).black.contains p <;>
          cases right : baseF.black.contains (p.sub drift) <;>
          simp_all [Wake, wakeCells, shiftedBaseColour]
      exact same
    · have notSupport : p ∉ support := by
        intro inside
        exact candidate (List.mem_append.mpr (Or.inl inside))
      have notShifted : p ∉ shiftedSupport := by
        intro inside
        exact candidate (List.mem_append.mpr (Or.inr inside))
      have initialWhite : base.black p = false := by
        by_cases colour : base.black p = true
        · exact (notSupport (base_black_supported colour)).elim
        · cases value : base.black p <;> simp_all
      have avoids : Avoids p base period := by
        intro k before equal
        exact notSupport (equal ▸ base_reads k before)
      have finalWhite : (run period base).black p = false :=
        (colour_unchanged period avoids).trans initialWhite
      have sourceWhite : base.black (p.sub drift) = false := by
        by_cases colour : base.black (p.sub drift) = true
        · have source := base_black_supported colour
          exfalso
          apply notShifted
          apply List.mem_map.mpr
          exact ⟨p.sub drift, source, Point.add_sub drift p⟩
        · cases value : base.black (p.sub drift) <;> simp_all
      have finalWhiteF : (baseF.run period).black.contains p = false := by
        change (baseF.run period).toState.black p = false
        rw [FState.toState_run]
        exact finalWhite
      have sourceWhiteF : baseF.black.contains (p.sub drift) = false :=
        sourceWhite
      exact finalWhiteF.trans sourceWhiteF.symm

theorem head_clear (certificate : Certificate) {head : Point}
    (member : head ∈ heads)
    {target : Point} (inside : target ∈ support) :
    Separated head target := by
  exact separated_checked ((List.all_eq_true.mp
    ((List.all_eq_true.mp certificate.headClearPass) head member)) target inside)

theorem separated_ne_shift {source target : Point}
    (apart : Separated source target) {depth : Nat} (positive : 0 < depth) :
    target ≠ shiftPoint drift depth source := by
  rw [drift_shift]
  rcases source with ⟨sx, sy⟩
  rcases target with ⟨tx, ty⟩
  simp only [Separated, highwayPoint, Point.mk.injEq] at apart ⊢
  intro equal
  rcases equal with ⟨xeq, yeq⟩
  rcases apart with diagonal | parity | order
  · apply diagonal
    omega
  · apply parity
    omega
  · omega

theorem stable_obstacle_misses (certificate : Certificate) {head : Point}
    (member : head ∈ heads) :
    ∀ extra, ¬CleanReads
      (shiftPoint drift (extra + 1) (obstacle head (stableDepth head))) := by
  intro extra read
  rcases read with ⟨k, before, position⟩
  have inside : (run k base).pos ∈ support := base_reads k before
  have apart := head_clear certificate member inside
  apply separated_ne_shift apart
    (depth := (extra + 1) + stableDepth head) (by omega)
  rw [position]
  exact (shiftPoint_add drift (extra + 1) (stableDepth head) head).symm

theorem shiftRegion_iff {v : Point} {region : Region} {n : Nat} {p : Point} :
    shiftRegion v n region p ↔
      ∃ source, region source ∧ p = shiftPoint v n source := by
  induction n generalizing p with
  | zero => exact ⟨fun inside => ⟨p, inside, rfl⟩,
      fun ⟨source, inside, equal⟩ => equal ▸ inside⟩
  | succ n ih =>
      constructor
      · intro inside
        rcases ih.mp inside with ⟨source, sourceInside, equal⟩
        refine ⟨source, sourceInside, ?_⟩
        change p = v.add (shiftPoint v n source)
        have placed := congrArg (Point.add v) equal
        simpa using placed
      · rintro ⟨source, sourceInside, equal⟩
        apply ih.mpr
        refine ⟨source, sourceInside, ?_⟩
        change p.sub v = shiftPoint v n source
        rw [equal]
        exact Point.sub_add v (shiftPoint v n source)

theorem footprint_member {v : Point} {clean baseRegion : Region}
    {n : Nat} {p : Point} (inside : footprint v clean baseRegion n p) :
    ∃ source, (clean source ∨ baseRegion source) ∧
      ∃ copies, copies ≤ n ∧ p = shiftPoint v copies source := by
  induction n generalizing p with
  | zero => exact ⟨p, Or.inr inside, 0, Nat.zero_le _, rfl⟩
  | succ n ih =>
      rcases inside with cleanHere | shifted
      · exact ⟨p, Or.inl cleanHere, 0, Nat.zero_le _, rfl⟩
      · rcases ih shifted with ⟨source, sourceInside, copies, bound, equal⟩
        refine ⟨source, sourceInside, copies + 1, by omega, ?_⟩
        change p = v.add (shiftPoint v copies source)
        have placed := congrArg (Point.add v) equal
        simpa using placed

theorem footprint_cases {v : Point} {clean baseRegion : Region}
    {n : Nat} {p : Point} (inside : footprint v clean baseRegion n p) :
    (∃ source, clean source ∧ ∃ copies, copies < n ∧
      p = shiftPoint v copies source) ∨
    (∃ source, baseRegion source ∧ p = shiftPoint v n source) := by
  induction n generalizing p with
  | zero => exact Or.inr ⟨p, inside, rfl⟩
  | succ n ih =>
      rcases inside with cleanHere | shifted
      · exact Or.inl ⟨p, cleanHere, 0, Nat.zero_lt_succ _, rfl⟩
      · rcases ih shifted with earlier | base
        · rcases earlier with ⟨source, sourceInside, copies, before, equal⟩
          refine Or.inl ⟨source, sourceInside, copies + 1,
            Nat.succ_lt_succ before, ?_⟩
          change p = v.add (shiftPoint v copies source)
          have placed := congrArg (Point.add v) equal
          simpa using placed
        · rcases base with ⟨source, sourceInside, equal⟩
          refine Or.inr ⟨source, sourceInside, ?_⟩
          change p = v.add (shiftPoint v n source)
          have placed := congrArg (Point.add v) equal
          simpa using placed

theorem shifted_footprint_member {v : Point} {clean baseRegion : Region}
    {n : Nat} {p : Point}
    (inside : Region.shift v (footprint v clean baseRegion n) p) :
    ∃ source, (clean source ∨ baseRegion source) ∧
      ∃ copies, 0 < copies ∧ p = shiftPoint v copies source := by
  rcases footprint_member inside with
    ⟨source, sourceInside, copies, _, equal⟩
  refine ⟨source, sourceInside, copies + 1, by omega, ?_⟩
  change p = v.add (shiftPoint v copies source)
  have placed := congrArg (Point.add v) equal
  simpa using placed

theorem ray_excludes_shift {a b : Point} (checked : raysMeet 0 a b = false)
    {copies : Nat} (positive : 0 < copies) :
    a ≠ shiftPoint drift copies b := by
  intro equal
  apply (rays_disjoint (turn := 0) (a := a) (b := b)
    (by omega) checked copies positive 0)
  rw [drift_shift] at equal
  rcases a with ⟨ax, ay⟩
  rcases b with ⟨bx, byValue⟩
  simp [backwardPoint, highwayPoint] at equal ⊢
  constructor <;> omega

theorem clean_read_supported {p : Point} (read : CleanReads p) : p ∈ support := by
  rcases read with ⟨k, before, rfl⟩
  exact base_reads k before

theorem base_read_recorded {head p : Point} (read : BaseReads head p) :
    p ∈ (stableResult head).2.toList := by
  apply Std.TreeSet.mem_toList.mpr
  rw [stableResult]
  apply (replay_reads p (stableTime head) (stableInitial head)).mpr
  rcases read with ⟨k, before, position⟩
  apply (FState.mem_reads_iff p (stableTime head) (stableInitial head)).mpr
  refine ⟨k, before, ?_⟩
  have bridge := congrArg State.pos (FState.toState_run k (stableInitial head))
  exact bridge.trans position

theorem stable_wake_misses (certificate : Certificate) {head : Point}
    (member : head ∈ heads) :
    ∀ extra, Region.Disjoint Wake
      (Region.shift drift (footprint drift CleanReads (BaseReads head) extra)) := by
  intro extra p wakeInside shifted
  rcases shifted_footprint_member shifted with
    ⟨source, clean | baseRead, copies, positive, equal⟩
  · have checked := (stable_wake_checked certificate member wakeInside).1
    have falseRay : raysMeet 0 p source = false := by
      have one := (List.all_eq_true.mp checked) source (clean_read_supported clean)
      simpa using one
    exact ray_excludes_shift falseRay positive equal
  · have checked := (stable_wake_checked certificate member wakeInside).2.1
    have falseRay : raysMeet 0 p source = false := by
      have one := (List.all_eq_true.mp checked) source (base_read_recorded baseRead)
      simpa using one
    exact ray_excludes_shift falseRay positive equal

theorem archive_member {v : Point} {wake : Region} {n : Nat} {p : Point}
    (inside : archive v wake n p) :
    ∃ source, wake source ∧ ∃ copies, copies < n ∧
      p = shiftPoint v copies source := by
  induction n generalizing p with
  | zero => exact inside.elim
  | succ n ih =>
      rcases inside with here | shifted
      · exact ⟨p, here, 0, Nat.zero_lt_succ _, rfl⟩
      · rcases ih shifted with ⟨source, sourceInside, copies, bound, equal⟩
        refine ⟨source, sourceInside, copies + 1, by omega, ?_⟩
        change p = v.add (shiftPoint v copies source)
        have placed := congrArg (Point.add v) equal
        simpa using placed

theorem shift_difference {wake corridor : Point} {earlier later : Nat}
    (before : earlier < later)
    (equal : shiftPoint drift earlier wake =
      shiftPoint drift later corridor) :
    corridor = shiftPoint ⟨2, 2⟩ (later - earlier) wake := by
  rw [drift_shift, drift_shift] at equal
  rw [backward_shift]
  rcases wake with ⟨wx, wy⟩
  rcases corridor with ⟨cx, cy⟩
  simp [highwayPoint, Point.mk.injEq] at equal ⊢
  constructor <;> omega

theorem turn_bounded (s : FState) : turn s < 4 := by
  cases found : orientation s with
  | none => simp [turn, found]
  | some turns =>
      simpa [turn, found] using (orientation_sound found).1

theorem normalized_backward (s : FState) (wake : Point) (copies : Nat) :
    normalizedPoint s (shiftPoint ⟨2, 2⟩ copies wake) =
      backwardPoint (turn s) copies (normalizedPoint s wake) := by
  unfold normalizedPoint normalizedAt
  rw [rotate_backward (turn s) copies wake (turn_bounded s)]
  have cases : turn s = 0 ∨ turn s = 1 ∨ turn s = 2 ∨ turn s = 3 := by
    have bound := turn_bounded s
    omega
  rcases offset (s.rotateN (turn s)) with ⟨ox, oy⟩
  rcases wake.rotateN (turn s) with ⟨wx, wy⟩
  rcases cases with h | h | h | h <;>
    simp [h, backwardPoint, Point.add] <;> omega

theorem not_separated_future {source target : Point}
    (failed : ¬Separated source target) :
    ∃ copies, 0 < copies ∧ target = highwayPoint copies source := by
  simp only [Separated, not_or] at failed
  rcases failed with ⟨diagonal, parity, order⟩
  let quotient : Int := (source.x - target.x) / 2
  have even : (source.x - target.x) % 2 = 0 := by omega
  have positive : 0 < quotient := by dsimp [quotient]; omega
  let copies := quotient.toNat
  have cast : (copies : Int) = quotient :=
    Int.toNat_of_nonneg (Int.le_of_lt positive)
  have copiesPositive : 0 < copies := by omega
  have horizontal : target.x + 2 * copies = source.x := by
    dsimp [quotient] at cast
    omega
  have invariants := back_invariants target copies
  rcases backEq : back copies target with ⟨bx, byValue⟩
  simp only [backEq] at invariants
  rcases invariants with ⟨backDiagonal, _, backHorizontal⟩
  have equal : back copies target = source := by
    rcases source with ⟨sx, sy⟩
    rcases target with ⟨tx, ty⟩
    simp only at diagonal horizontal backDiagonal backHorizontal
    rw [backEq]
    have xeq : bx = sx := by omega
    have yeq : byValue = sy := by omega
    rw [xeq, yeq]
  have shifted := shift_back copies target
  rw [equal, drift_shift] at shifted
  exact ⟨copies, copiesPositive, shifted.symm⟩

theorem stable_archive_misses (certificate : Certificate) {head : Point}
    (member : head ∈ heads) :
    ∀ extra, Region.Disjoint (archive drift Wake extra)
      (shiftRegion drift extra (Corridor head)) := by
  intro extra p archived shifted
  rcases archive_member archived with
    ⟨wake, wakeInside, earlier, before, fromWake⟩
  rcases shiftRegion_iff.mp shifted with
    ⟨corridor, future, fromCorridor⟩
  have shiftedEqual : shiftPoint drift earlier wake =
      shiftPoint drift extra corridor := fromWake.symm.trans fromCorridor
  have corridorBackward := shift_difference before shiftedEqual
  let copies := extra - earlier
  have copiesPositive : 0 < copies := by dsimp [copies]; omega
  let final := stableFinal head
  let normalizedWake := normalizedPoint final wake
  let normalizedCorridor := normalizedPoint final corridor
  have normalizedEqual : normalizedCorridor =
      backwardPoint (turn final) copies normalizedWake := by
    dsimp [normalizedCorridor, normalizedWake, final]
    rw [corridorBackward]
    exact normalized_backward (stableFinal head) wake copies
  have terminalGuard : support.all (fun source =>
      !(raysMeet (turn final) normalizedWake source)) = true := by
    simpa [final, normalizedWake] using
      (stable_wake_checked certificate member wakeInside).2.2
  have outside : normalizedCorridor ∉ support := by
    intro inside
    have checked := (List.all_eq_true.mp terminalGuard)
      normalizedCorridor inside
    have falseRay : raysMeet (turn final) normalizedWake normalizedCorridor =
        false := by simpa using checked
    apply (rays_disjoint (turn_bounded final) falseRay copies copiesPositive 0)
    simpa [highwayPoint] using normalizedEqual.symm
  have separated : separatedFromSupport normalizedCorridor = true := by
    apply List.all_eq_true.mpr
    intro source sourceInside
    change separated source normalizedCorridor = true
    apply decide_eq_true
    apply Classical.byContradiction
    intro failed
    rcases not_separated_future failed with
      ⟨later, laterPositive, targetEqual⟩
    have checked := (List.all_eq_true.mp terminalGuard) source sourceInside
    have falseRay : raysMeet (turn final) normalizedWake source = false := by
      simpa using checked
    apply (rays_disjoint (turn_bounded final) falseRay copies copiesPositive later)
    exact normalizedEqual.symm.trans targetEqual
  apply (future_excluded (stable_accepted certificate member) outside separated)
  simpa [Corridor, stableFinal] using future

theorem stable_initial (head : Point) :
    (stableInitial head).toState =
      lane base drift (obstacle head (stableDepth head)) 0 := by
  simp only [stableInitial, initial, force_toState, lane, shiftPoint, base]

theorem stable_final (head : Point) :
    (stableFinal head).toState =
      run (stableTime head)
        (lane base drift (obstacle head (stableDepth head)) 0) := by
  calc
    (stableFinal head).toState =
        ((stableInitial head).run (stableTime head)).toState := by
      rw [stableFinal, stableResult]
      exact congrArg FState.toState
        (replay_final (stableTime head) (stableInitial head))
    _ = run (stableTime head) (stableInitial head).toState :=
      FState.toState_run _ _
    _ = run (stableTime head)
        (lane base drift (obstacle head (stableDepth head)) 0) := by
      rw [stable_initial]

theorem lane_data (certificate : Certificate) {head : Point}
    (member : head ∈ heads) :
    Data base drift (obstacle head (stableDepth head)) period (stableTime head)
      CleanReads (BaseReads head) Wake (Corridor head) := by
  refine {
    cleanReadsExact := rfl
    cleanBlock := clean_block
    baseReadsExact := ?_
    obstacleMisses := stable_obstacle_misses certificate member
    wakeMisses := stable_wake_misses certificate member
    baseFuture := ?_
    archiveMisses := stable_archive_misses certificate member
  }
  · rw [← stable_initial]
  · intro p read
    rw [← stable_final] at read
    exact read

theorem stable_lane_reaches (certificate : Certificate) {head : Point}
    (member : head ∈ heads)
    (extra : Nat) :
    ReachesP104
      (lane base drift (obstacle head (stableDepth head)) extra) := by
  apply Induction.reaches (lane_data certificate member)
  rw [← stable_final]
  exact any_permanent (stable_accepted certificate member)

theorem lane_reaches (certificate : Certificate) {head : Point}
    (member : head ∈ heads)
    {depth : Nat} (positive : 0 < depth) :
    ReachesP104 (blacken (obstacle head depth) base) := by
  by_cases shallow : depth < stableDepth head
  · exact shallow_reaches certificate member positive shallow
  · have stableLe : stableDepth head ≤ depth := Nat.le_of_not_gt shallow
    have reached := stable_lane_reaches certificate member
      (depth - stableDepth head)
    have obstacleEqual :
        shiftPoint drift (depth - stableDepth head)
          (obstacle head (stableDepth head)) =
          obstacle head depth := by
      unfold obstacle
      rw [← shiftPoint_add]
      congr 2
      exact Nat.sub_add_cancel stableLe
    simpa [lane, obstacleEqual] using reached

theorem base_boundary : Boundary 0 base := by
  constructor
  · exact ⟨rfl, rfl, fun _ _ => rfl⟩
  · intro p black outside
    exact (outside (base_black_supported black)).elim

theorem base_permanent : PermanentP104 base :=
  tail_permanent base_boundary.tail

theorem blacken_eq {s : State} {p : Point} (black : s.black p = true) :
    blacken p s = s := by
  apply State.ext
  · funext q
    by_cases equal : q = p
    · subst q; simp [blacken, black]
    · simp [blacken, equal]
  · rfl
  · rfl

theorem separated_base_reaches {p : Point} (outside : p ∉ support)
    (separated : separatedFromSupport p = true) :
    ReachesP104 (blacken p base) := by
  have avoids : AvoidsForever (Region.singleton p) base := by
    intro n equal
    rcases base_boundary.future_support n with ⟨cycle, inside⟩
    have position : (run n base).pos = p := equal
    rw [position] at inside
    cases cycle with
    | zero => exact outside inside
    | succ cycle =>
        exact separated_excludes (fun source member =>
          separated_checked ((List.all_eq_true.mp separated) source member))
          (cycle + 1) (Nat.zero_lt_succ cycle) inside
  refine ⟨0, ?_⟩
  exact base_permanent.of_sameReadTrace
    (sameReadTrace_of_archive (blacken_sameOutside p base) avoids)

/-- Every black insertion at the canonical P104 boundary reaches P104. -/
theorem one_black (certificate : Certificate) (p : Point) :
    ReachesP104 (blacken p base) := by
  by_cases inside : p ∈ support
  · by_cases black : base.black p = true
    · rw [blacken_eq black]
      exact ⟨0, base_permanent⟩
    · apply active_reaches certificate
      apply List.mem_filter.mpr
      exact ⟨inside, by
        have whiteState : base.black p = false := by
          cases colour : base.black p <;> simp_all
        have white : baseF.black.contains p = false := whiteState
        simp [white]⟩
  · by_cases separated : separatedFromSupport p = true
    · exact separated_base_reaches inside separated
    · have failed : separatedFromSupport p = false := by
        cases value : separatedFromSupport p <;> simp_all
      rcases outside_corridor_has_lane inside failed with
        ⟨head, headProperty, depth, positive, equal⟩
      rw [equal]
      exact lane_reaches certificate (head_iff.mpr headProperty) positive

end OneBlack.Pristine
