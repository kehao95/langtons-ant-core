import OneBlack.ActualChecks

namespace OneBlack.Ordinary

open OneBlack Highway Terminal Entry RayGeometry Induction Pristine
  PristineChecks ActualChecks

set_option maxRecDepth 10000

theorem history_iff_mem {p : Point} : History p ↔ p ∈ historyCells := by
  simp only [History, historyCells, List.mem_filter]
  constructor
  · rintro ⟨black, outside⟩
    refine ⟨?_, decide_eq_true outside⟩
    apply Std.TreeSet.mem_toList.mpr
    rw [← Std.TreeSet.contains_iff_mem]
    exact black
  · rintro ⟨member, outside⟩
    exact ⟨Std.TreeSet.contains_iff_mem.mpr
      (Std.TreeSet.mem_toList.mp member), of_decide_eq_true outside⟩

theorem entry_same_base : SameOutside History entry base := by
  refine ⟨entry_pos_fact, entry_dir_fact, ?_⟩
  intro p unchanged
  by_cases inside : p ∈ support
  · exact eq_of_beq ((List.all_eq_true.mp entry_active_fact) p inside)
  · have baseWhite : base.black p = false := by
      by_cases black : base.black p = true
      · exact (inside (base_black_supported black)).elim
      · cases value : base.black p <;> simp_all
    have entryWhite : entry.black p = false := by
      by_cases black : entry.black p = true
      · exact (unchanged ⟨black, inside⟩).elim
      · cases value : entry.black p <;> simp_all
    exact entryWhite.trans baseWhite.symm

theorem forced_same (p : Point) :
    SameOutside History (blacken p entry) (blacken p base) :=
  entry_same_base.blacken p

theorem supportAt_shiftPoint (p : Point) : ∀ n,
    supportAt n (shiftPoint drift n p) ↔ Support p := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
      change supportAt n ((drift.add (shiftPoint drift n p)).sub drift) ↔ _
      simpa using ih

theorem history_misses_clean_shift {historical source : Point}
    (old : History historical) (clean : CleanReads source) : ∀ copies,
    historical ≠ shiftPoint drift copies source := by
  intro copies equal
  have sourceSupport : Support source := clean_read_supported clean
  cases copies with
  | zero => exact old.2 (equal.symm ▸ sourceSupport)
  | succ copies =>
      have future : supportAt (copies + 1) historical := by
        rw [equal]
        exact (supportAt_shiftPoint source (copies + 1)).mpr sourceSupport
      exact entry_boundary.2 historical old.1 old.2
        (copies + 1) (Nat.zero_lt_succ copies) future

end OneBlack.Ordinary
