import OneBlack.Ordinary
import OneBlack.Xor

namespace OneBlack.PhaseChecks

open OneBlack Highway Terminal Entry Pristine PristineChecks ActualChecks
  RayGeometry Induction

def reverseDrift : Point := ⟨2, 2⟩
abbrev phaseDepth : Nat := stableDepth phaseHead
def phaseLag : Nat := phaseBaseDepth - phaseDepth
def localTime : Nat := stableTime phaseHead
def hitCycles : Nat := 10
def hitPhase : Nat := 89
def hitElapsed : Nat := hitCycles * period + hitPhase
def postHitTime : Nat := 7994
def hitPoint : Point := ⟨20, -22⟩

def cleanWake : BRegion := BRegion.ofList wakeCells

def reverseBaseWith (stable : FState × PointSet) : FState := stable.1
def reverseShiftWith (stable : FState × PointSet) : FState :=
  (reverseBaseWith stable).shift reverseDrift
def reverseNextWith (stable : FState × PointSet) : FState :=
  (reverseBaseWith stable).run period
def reverseWakeSourcesWith (stable : FState × PointSet) : List Point :=
  differenceSources (reverseNextWith stable) (reverseShiftWith stable)
def reverseWakeWith (stable : FState × PointSet) : BRegion :=
  BRegion.ofList (reverseWakeSourcesWith stable)

abbrev reverseBase : FState := reverseBaseWith (stableResult phaseHead)
abbrev reverseShift : FState := reverseShiftWith (stableResult phaseHead)
abbrev reverseNext : FState := reverseNextWith (stableResult phaseHead)
abbrev reverseWakeSources : List Point :=
  reverseWakeSourcesWith (stableResult phaseHead)
abbrev reverseWake : BRegion := reverseWakeWith (stableResult phaseHead)

def oppositeTurn (turn : Nat) : Nat := (turn + 2) % 4

def forwardGuardAt (turns : Nat) (terminal : FState) (source : Point) : Bool :=
  let normalized := normalizedAt turns terminal source
  decide (normalized ∉ support) && separatedFromSupport normalized &&
  support.all fun target =>
    !(raysMeet (oppositeTurn turns) normalized target)

def forwardGuard (terminal : FState) (source : Point) : Bool :=
  forwardGuardAt (turn terminal) terminal source

def forwardGuardsAt (turns : Nat) (terminal : FState)
    (sources : List Point) : Bool :=
  sources.all (forwardGuardAt turns terminal)

def forwardGuards (terminal : FState) (sources : List Point) : Bool :=
  let turns := turn terminal
  forwardGuardsAt turns terminal sources

/-- The reverse block starts using its wake only at the next translated copy,
so its exact guard is the positive-copy ray condition. -/
def reverseRayGuardAt (turns : Nat) (terminal : FState)
    (source : Point) : Bool :=
  let normalized := normalizedAt turns terminal source
  support.all fun target =>
    !(raysMeet (oppositeTurn turns) normalized target)

def reverseGuardsAt (turns : Nat) (terminal : FState)
    (sources : List Point) : Bool :=
  sources.all (reverseRayGuardAt turns terminal)

def phaseTraceGuardFor (history : List Point) (stable : FState × PointSet) : Bool :=
  let sources := stable.2.toList
  history.all fun historical =>
  sources.all fun source =>
    !(shiftedAtLeast phaseLag historical source)

def phaseTraceGuardWith (stable : FState × PointSet) : Bool :=
  phaseTraceGuardFor historyCells stable

abbrev phaseTraceGuard : Bool := phaseTraceGuardWith (stableResult phaseHead)

def reverseGuardWith (stable : FState × PointSet) : Bool :=
  let terminal := reverseBaseWith stable
  reverseGuardsAt (turn terminal) terminal (reverseWakeSourcesWith stable)

abbrev reverseGuard : Bool := reverseGuardWith (stableResult phaseHead)

def reverseIndex (origin target : Point) : Option Int :=
  let dx := target.x - origin.x
  let dy := target.y - origin.y
  if dx = dy ∧ dx % 2 = 0 then some (dx / 2) else none

def firstHitChecksFor (history : List Point) (stable : FState × PointSet) : Bool :=
  (List.range period).all fun phase =>
  let position := ((reverseBaseWith stable).run phase).pos
  history.all fun historical =>
    match reverseIndex position historical with
    | none => true
    | some cycle => decide (hitCycles < cycle ∨
        (cycle = hitCycles ∧ hitPhase ≤ phase))

def firstHitChecksWith (stable : FState × PointSet) : Bool :=
  firstHitChecksFor historyCells stable

abbrev firstHitChecks : Bool := firstHitChecksWith (stableResult phaseHead)

def actualHit : FState :=
  let copies := phaseLag
  (actualInitial phaseHead phaseBaseDepth).run
    (duration period localTime copies +
      ((copies + hitCycles) * period + hitPhase))

def postHit := replay postHitTime actualHit
def postFinal : FState := postHit.1
def postReads : PointSet := postHit.2

def rawLayerWith (stable : FState × PointSet) : BRegion := BRegion.xor cleanWake
  (BRegion.iterate drift 1 (reverseWakeWith stable))

def layerWith (stable : FState × PointSet) : BRegion :=
  BRegion.iterate drift phaseLag (rawLayerWith stable)

abbrev layer : BRegion := layerWith (stableResult phaseHead)

def layerCandidatesWith (stable : FState × PointSet) : List Point :=
  (wakeCells ++ (reverseWakeSourcesWith stable).map (drift.add ·)).eraseDups.map
    (shiftPoint drift phaseLag)

abbrev layerCandidates : List Point :=
  layerCandidatesWith (stableResult phaseHead)

def layerSourcesWith (stable : FState × PointSet) : List Point :=
  (layerCandidatesWith stable).filter fun p => layerWith stable p

abbrev layerSources : List Point := layerSourcesWith (stableResult phaseHead)

def traceGuardFor (sources : List Point) (reads : PointSet) : Bool :=
  let targets := reads.toList
  sources.all fun source =>
  targets.all fun target =>
    decide (source ≠ target) && !(raysMeet 0 target source)

def traceGuardWith (stable : FState × PointSet) : Bool :=
  traceGuardFor (layerSourcesWith stable) postReads

abbrev traceGuard : Bool := traceGuardWith (stableResult phaseHead)

def terminalGuardWith (stable : FState × PointSet) : Bool :=
  forwardGuards postFinal (layerSourcesWith stable)

abbrev terminalGuard : Bool := terminalGuardWith (stableResult phaseHead)

def reportWith (stable : FState × PointSet) : Bool :=
  let history := historyCells
  let reverseBase := reverseBaseWith stable
  let reverseShift := reverseShiftWith stable
  let reverseNext := reverseNextWith stable
  let reverseSources := differenceSources reverseNext reverseShift
  let reverseFound := orientation reverseBase
  let reverseTurns := reverseFound.getD 0
  let hit := actualHit
  let post := replay postHitTime hit
  let postFinal := post.1
  let postFound := orientation postFinal
  let postTurns := postFound.getD 0
  let reverseWake := BRegion.ofList reverseSources
  let rawLayer := BRegion.xor cleanWake (BRegion.iterate drift 1 reverseWake)
  let layer := BRegion.iterate drift phaseLag rawLayer
  let layerCandidates :=
    (wakeCells ++ reverseSources.map (drift.add ·)).eraseDups.map
      (shiftPoint drift phaseLag)
  let layers := layerCandidates.filter fun p => layer p
  decide (phaseHead ∈ heads) && decide (phaseDepth = 11) &&
  decide (phaseBaseDepth = 15) && decide (phaseLag = 4) &&
  decide (localTime = 52262) &&
  decide (hitElapsed = 1129) && decide (postHitTime = 7994) &&
  phaseTraceGuardFor history stable &&
  decide (reverseNext.pos = reverseShift.pos) &&
  decide (reverseNext.dir = reverseShift.dir) &&
  reverseFound.isSome &&
  reverseGuardsAt reverseTurns reverseBase reverseSources &&
  firstHitChecksFor history stable &&
  decide ((reverseBase.run hitElapsed).pos = hitPoint) &&
  decide (hitPoint ∈ history) &&
  decide (hit.pos = hitPoint) && postFound.isSome &&
  traceGuardFor layers post.2 &&
  forwardGuardsAt postTurns postFinal layers

def report : Bool := reportWith (stableResult phaseHead)

structure Certificate : Prop where
  phaseMember : phaseHead ∈ heads
  pristineCutoff : phaseDepth = 11
  baseDepthExact : phaseBaseDepth = 15
  lagExact : phaseLag = 4
  localTimeExact : localTime = 52262
  hitElapsedExact : hitElapsed = 1129
  postHitExact : postHitTime = 7994
  phaseTracePass : phaseTraceGuard = true
  reversePosition : reverseNext.pos = reverseShift.pos
  reverseHeading : reverseNext.dir = reverseShift.dir
  reverseAccepted : any reverseBase = true
  reverseGuardPass : reverseGuard = true
  firstHitPass : firstHitChecks = true
  cleanHitPosition : (reverseBase.run hitElapsed).pos = hitPoint
  hitHistorical : hitPoint ∈ historyCells
  actualHitPosition : actualHit.pos = hitPoint
  postAccepted : any postFinal = true
  traceGuardPass : traceGuard = true
  terminalGuardPass : terminalGuard = true

theorem certificate_of_report (verified : report = true) : Certificate := by
  simp only [report, reportWith, Bool.and_eq_true, decide_eq_true_eq] at verified
  rcases verified with
    ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨phaseMember, pristineCutoff⟩,
      baseDepthExact⟩, lagExact⟩, localTimeExact⟩, hitElapsedExact⟩,
      postHitExact⟩, phaseTracePass⟩, reversePosition⟩,
      reverseHeading⟩, reverseAccepted⟩, reverseGuardPass⟩, firstHitPass⟩,
      cleanHitPosition⟩, hitHistorical⟩, actualHitPosition⟩, postAccepted⟩,
      traceGuardPass⟩, terminalGuardPass⟩
  exact ⟨phaseMember, pristineCutoff, baseDepthExact, lagExact, localTimeExact,
    hitElapsedExact, postHitExact,
    phaseTracePass, reversePosition, reverseHeading, reverseAccepted,
    reverseGuardPass, firstHitPass, cleanHitPosition, hitHistorical,
    actualHitPosition, postAccepted, traceGuardPass, terminalGuardPass⟩

theorem certificate_of_reportWith
    (verified : reportWith (stableResult phaseHead) = true) : Certificate :=
  certificate_of_report verified

end OneBlack.PhaseChecks
