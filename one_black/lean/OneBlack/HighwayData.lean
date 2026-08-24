import OneBlack.Semantics

namespace OneBlack.Highway

open OneBlack

set_option maxRecDepth 10000

def entryTime : Nat := 9977
def period : Nat := 104
def drift : Point := ⟨-2, -2⟩

structure Snapshot where
  reads : List Point
  support : List Point
  pattern : List Point
  base : FState

@[irreducible] def computedEntry : FState := fwhite.run entryTime

theorem computedEntry_exact : computedEntry = fwhite.run entryTime := by
  unfold computedEntry
  exact Eq.refl _

opaque snapshot : Snapshot :=
  let entry := computedEntry
  let reads := entry.reads period
  let support := reads.eraseDups
  let pattern := support.filter entry.black.contains
  ⟨reads, support, pattern,
    ⟨PointSet.ofList pattern, entry.pos, entry.dir⟩⟩

def entryF : FState := computedEntry
def blockReads : List Point := snapshot.reads
def support : List Point := snapshot.support
def pattern : List Point := snapshot.pattern
def baseF : FState := snapshot.base
def entry : State := entryF.toState
def base : State := baseF.toState
def shiftedSupport : List Point := support.map drift.add

def separated (source target : Point) : Bool := decide (
  target.x - target.y ≠ source.x - source.y ∨
  target.x % 2 ≠ source.x % 2 ∨ source.x ≤ target.x)

def separatedFromSupport (target : Point) : Bool :=
  support.all fun source => separated source target

structure Report where
  supportCard : Bool
  patternCard : Bool
  entrySize : Bool
  entryPos : Bool
  entryDir : Bool
  baseReads : Bool
  entryActive : Bool
  transportPos : Bool
  transportDir : Bool
  transportColour : Bool
  baseSupported : Bool
  supportWake : Bool
  entryBackground : Bool

def report : Report :=
  let s := snapshot
  let entry := computedEntry
  let shifted := s.support.map drift.add
  let separatedFrom (target : Point) :=
    s.support.all fun source => separated source target
  let final := s.base.run period
  ⟨decide (s.support.length = 40), decide (s.pattern.length = 13),
    decide (entry.black.size = 715), decide (entry.pos = s.base.pos),
    decide (entry.dir = s.base.dir),
    (s.base.reads period).all fun p => decide (p ∈ s.support),
    s.support.all fun p =>
      entry.black.contains p == s.base.black.contains p,
    decide (final.pos = drift.add s.base.pos), decide (final.dir = s.base.dir),
    s.support.all fun p =>
      final.black.contains (drift.add p) == s.base.black.contains p,
    s.base.black.toList.all fun p => decide (p ∈ s.support),
    s.support.all fun target =>
      decide (target ∈ shifted) || separatedFrom target,
    entry.black.toList.all fun target =>
      decide (target ∈ s.support) || separatedFrom target⟩

def checks : List Bool := [report.supportCard, report.patternCard,
  report.entrySize, report.entryPos, report.entryDir, report.baseReads,
  report.entryActive, report.transportPos, report.transportDir,
  report.transportColour, report.baseSupported, report.supportWake,
  report.entryBackground]

theorem checks_pass : checks.all id = true := by native_decide

private theorem checked (c : Bool) (h : c ∈ checks) : c = true :=
  (List.all_eq_true.mp checks_pass) c h

theorem baseRead_checked : report.baseReads = true := checked _ (by simp [checks])
theorem entryActive_checked : report.entryActive = true := checked _ (by simp [checks])
theorem entryPos_checked : report.entryPos = true := checked _ (by simp [checks])
theorem entryDir_checked : report.entryDir = true := checked _ (by simp [checks])
theorem transportPos_checked : report.transportPos = true := checked _ (by simp [checks])
theorem transportDir_checked : report.transportDir = true := checked _ (by simp [checks])
theorem transportColour_checked : report.transportColour = true := checked _ (by simp [checks])
theorem baseSupported_checked : report.baseSupported = true := checked _ (by simp [checks])
theorem supportWake_checked : report.supportWake = true := checked _ (by simp [checks])
theorem entryBackground_checked : report.entryBackground = true := checked _ (by simp [checks])

theorem base_reads_fact :
    (baseF.reads period).all (fun p => decide (p ∈ support)) = true := by
  change report.baseReads = true
  exact baseRead_checked

theorem entry_active_fact : support.all (fun p =>
    entryF.black.contains p == baseF.black.contains p) = true := by
  change report.entryActive = true
  exact entryActive_checked

theorem entry_pos_fact : entryF.pos = baseF.pos := by
  apply of_decide_eq_true
  change report.entryPos = true
  exact entryPos_checked

theorem entry_dir_fact : entryF.dir = baseF.dir := by
  apply of_decide_eq_true
  change report.entryDir = true
  exact entryDir_checked

theorem transport_pos_fact : (baseF.run period).pos = drift.add baseF.pos := by
  apply of_decide_eq_true
  change report.transportPos = true
  exact transportPos_checked

theorem transport_dir_fact : (baseF.run period).dir = baseF.dir := by
  apply of_decide_eq_true
  change report.transportDir = true
  exact transportDir_checked

theorem transport_colour_fact : support.all (fun p =>
    (baseF.run period).black.contains (drift.add p) ==
      baseF.black.contains p) = true := by
  change report.transportColour = true
  exact transportColour_checked

theorem base_supported_fact : baseF.black.toList.all
    (fun p => decide (p ∈ support)) = true := by
  change report.baseSupported = true
  exact baseSupported_checked

theorem support_wake_fact : support.all (fun target =>
    decide (target ∈ shiftedSupport) || separatedFromSupport target) = true := by
  change report.supportWake = true
  exact supportWake_checked

theorem entry_background_fact : entryF.black.toList.all (fun target =>
    decide (target ∈ support) || separatedFromSupport target) = true := by
  change report.entryBackground = true
  exact entryBackground_checked

end OneBlack.Highway
