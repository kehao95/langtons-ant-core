const canvas = document.querySelector("#proof-map");
const context = canvas.getContext("2d");
const elements = {
  readout: document.querySelector("#cell-readout"),
  mapCaption: document.querySelector("#map-caption"),
  legend: document.querySelector("#legend"),
  reset: document.querySelector("#return-selection"),
  stageButtons: [...document.querySelectorAll("[data-proof-stage]")],
  guideContainer: document.querySelector("#stage-guide"),
  guideBadge: document.querySelector("#guide-badge"),
  guideTitle: document.querySelector("#guide-title"),
  guideLeanCode: document.querySelector("#guide-lean-code"),
  guideMechanism: document.querySelector("#guide-mechanism"),
};

const COLORS = {
  background: "#102630",
  blue: "rgba(99, 184, 237, .68)",
  inactive: "rgba(45, 104, 130, .22)",
  gray: "rgba(190, 201, 203, .92)",
  disturbed: "rgba(231, 211, 174, .92)",
  highway: "rgba(112, 239, 167, .96)",
  highwayTrail: "rgba(139, 255, 188, .96)",
  grid: "rgba(10, 34, 44, .42)",
  border: "rgba(229, 241, 243, .38)",
  hover: "#fff4c7",
  black: "#05090b",
  ant: "#f2ba52",
  origin: "#ff5b61",
  scattering: ["#63b8ed", "#f2b84b", "#ef746f", "#b798f5"],
  historyDirect: "#e89b55",
  historyStable: "#63b8ed",
  reverseBase: "#b798f5",
  reverseHighway: "#ef746f",
  overview: ["#31586b", "#63b8ed", "#70cfa7", "#e89b55", "#b798f5"],
};

const SCATTERING_DIRECTIONS = ["straight", "turn right", "reverse", "turn left"];

const MOVE_X = [0, 1, 0, -1];
const MOVE_Y = [1, 0, -1, 0];
const VISIBLE_TAIL_CYCLES = 20;
const VIEW_PADDING_CELLS = 3;
const HOVER_DELAY_MS = 1000;
const PREFIX_ANIMATION_MS = 5600;
const SCATTERING_HISTORY_MS = 7000;
const PRISTINE_REFERENCE_AFTER_HIT_CYCLES = 15;
const REVERSE_APPROACH_MS = 8000;
const REVERSE_HIGHWAY_MS = 6000;
const REVERSE_POST_HIT_MS = 7000;
const HIGHWAY_ANIMATION_MS = 10500;
const HIGHWAY_CYCLES = 20;
const VISIBLE_STABLE_DEPTH = 30;
const VISIBLE_REVERSE_DEPTH = 20;

let proof;
let prefixSet;
let prefixFirstRead;
let prefixPoints;
let prefixCaseMap;
let pristineCaseMap;
let pristinePoints;
let pristinePointSet;
let pristineSupportSet;
let pristineReferencePoints;
let finiteHistoryCaseMap;
let finiteHistoryPoints;
let finiteHistoryPointSet;
let finiteHistoryWakeSet;
let finiteHistoryReferencePoints;
let finiteHistoryStableTailSet;
let finiteHistoryStableDepthMap;
let reverseCaseMap;
let reversePoints;
let reversePointSet;
let reverseReferenceSet;
let reverseReferencePoints;
let reverseStableTailSet;
let reverseStableDepthMap;
let visibleReferenceSet;
let transform;
let defaultTransform;
let defaultVisibleReferenceSet;
let pristineTransform;
let pristineVisibleReferenceSet;
let finiteHistoryTransform;
let finiteHistoryVisibleReferenceSet;
let reverseTransform;
let reverseVisibleReferenceSet;
let overviewTransform;
let overviewReferencePoints;
let overviewPrefixSet;
let overviewScatteringSet;
let overviewOrdinarySet;
let overviewScatteringRays;
let overviewReverseRay;
let simulation;
let selectedCase;
let proofStage = "outside";
let mode = "display";
let hoveredPoint;
let hoveredKey;
let selectedPoint;
let hoverTimer;
let animationFrame;
let animationStartedAt;
let fastTimer;
let evolutionGeneration = 0;
let highwayVisited = new Set();
let fastVisited = new Set();
let fastHighwayVisited = new Set();
let reverseVisited = new Set();
let fastReverseVisited = new Set();
let trail = [];
let highwayTrail = [];

const key = ([x, y]) => `${x},${y}`;
const addCycle = ([x, y], [dx, dy], cycle) => [x + dx * cycle, y + dy * cycle];

function createSimulation(initialBlack = [], heading = 0) {
  return {
    black: new Set(initialBlack.map(key)),
    x: 0,
    y: 0,
    heading,
    step: 0,
  };
}

function advanceOne(state) {
  const pointKey = `${state.x},${state.y}`;
  if (state.black.has(pointKey)) {
    state.heading = (state.heading + 3) % 4;
    state.black.delete(pointKey);
  } else {
    state.heading = (state.heading + 1) % 4;
    state.black.add(pointKey);
  }
  state.x += MOVE_X[state.heading];
  state.y += MOVE_Y[state.heading];
  state.step += 1;
}

function computeBlankPrefix() {
  const state = createSimulation();
  const read = new Set();
  const firstRead = new Map();
  for (let step = 0; step < proof.blank.entryStep; step += 1) {
    const pointKey = `${state.x},${state.y}`;
    read.add(pointKey);
    if (!firstRead.has(pointKey)) firstRead.set(pointKey, step);
    advanceOne(state);
  }
  const [entryX, entryY] = proof.blank.entryPosition;
  if (state.x !== entryX || state.y !== entryY) {
    throw new Error("The live rule did not reach the certified blank-orbit entry state");
  }
  return { read, firstRead };
}

function translationIndex(frontier, point, drift) {
  let index;
  for (let axis = 0; axis < 2; axis += 1) {
    const delta = point[axis] - frontier[axis];
    const stride = drift[axis];
    if (stride === 0) {
      if (delta !== 0) return undefined;
      continue;
    }
    if (delta % stride !== 0) return undefined;
    const candidate = delta / stride;
    if (index === undefined) index = candidate;
    else if (index !== candidate) return undefined;
  }
  return Number.isInteger(index) && index >= 0 ? index : undefined;
}

function isTailPoint(point) {
  return proof.blank.tailFrontier.some(
    (frontier) => translationIndex(frontier, point, proof.blank.drift) !== undefined,
  );
}

function isReferencePoint(point) {
  return prefixSet.has(key(point)) || isTailPoint(point);
}

function isSelectablePoint(point) {
  if (proofStage === "overview") return false;
  if (proofStage === "pristine") return pristinePointSet.has(key(point));
  if (proofStage === "finiteHistory") return finiteHistoryPointSet.has(key(point));
  if (proofStage === "reverseHighway") return reversePointSet.has(key(point));
  return proofStage === "outside"
    ? !isReferencePoint(point)
    : prefixSet.has(key(point));
}

function buildVisibleReferenceSet() {
  const result = new Set();
  if (proofStage === "overview") return result;
  if (proofStage === "pristine") {
    for (const pointKey of pristineSupportSet) result.add(pointKey);
    return result;
  }
  if (proofStage === "finiteHistory") {
    for (const pointKey of finiteHistoryWakeSet) result.add(pointKey);
    return result;
  }
  if (proofStage === "reverseHighway") {
    for (const pointKey of reverseReferenceSet) result.add(pointKey);
    return result;
  }
  for (let x = transform.minX; x <= transform.maxX; x += 1) {
    for (let y = transform.minY; y <= transform.maxY; y += 1) {
      const point = [x, y];
      if (isReferencePoint(point)) result.add(key(point));
    }
  }
  return result;
}

function makeTransform(extraPoints = [], basePoints) {
  const endpointPoints = proof.blank.tailFrontier.map(
    (point) => addCycle(point, proof.blank.drift, VISIBLE_TAIL_CYCLES - 1),
  );
  const points = basePoints
    ? [...basePoints, ...extraPoints]
    : [...prefixPoints, ...proof.blank.tailFrontier, ...endpointPoints, ...extraPoints];
  const xs = points.map(([x]) => x);
  const ys = points.map(([, y]) => y);
  const bounds = {
    minX: Math.min(...xs) - VIEW_PADDING_CELLS,
    maxX: Math.max(...xs) + VIEW_PADDING_CELLS,
    minY: Math.min(...ys) - VIEW_PADDING_CELLS,
    maxY: Math.max(...ys) + VIEW_PADDING_CELLS,
  };
  const margin = 28;
  const scale = Math.min(
    (canvas.width - margin * 2) / (bounds.maxX - bounds.minX + 1),
    (canvas.height - margin * 2) / (bounds.maxY - bounds.minY + 1),
  );
  const plotWidth = (bounds.maxX - bounds.minX + 1) * scale;
  const plotHeight = (bounds.maxY - bounds.minY + 1) * scale;
  const left = (canvas.width - plotWidth) / 2;
  const top = (canvas.height - plotHeight) / 2;
  return {
    ...bounds, scale, left, top,
    point([x, y]) {
      return [
        left + (x - bounds.minX + .5) * scale,
        top + (bounds.maxY - y + .5) * scale,
      ];
    },
    cellAt(screenX, screenY) {
      const x = Math.floor((screenX - left) / scale) + bounds.minX;
      const y = bounds.maxY - Math.floor((screenY - top) / scale);
      return x >= bounds.minX && x <= bounds.maxX && y >= bounds.minY && y <= bounds.maxY
        ? [x, y]
        : undefined;
    },
  };
}

function fillCell(point, color, inset = .12) {
  const [x, y] = transform.point(point);
  const size = transform.scale * (1 - inset * 2);
  context.fillStyle = color;
  context.fillRect(x - size / 2, y - size / 2, size, size);
}

function strokeCell(point, color) {
  const [x, y] = transform.point(point);
  const size = transform.scale * .9;
  context.strokeStyle = color;
  context.lineWidth = 2;
  context.strokeRect(x - size / 2, y - size / 2, size, size);
}

function selectedCoordinateLabel() {
  return `q = (${selectedPoint[0]}, ${selectedPoint[1]})`;
}

function setEvolutionReadout(message) {
  elements.readout.textContent = `${selectedCoordinateLabel()} · ${message}`;
}

function drawHoverCoordinate() {
  if (!hoveredPoint) return;
  const label = `(${hoveredPoint[0]}, ${hoveredPoint[1]})`;
  const [cellX, cellY] = transform.point(hoveredPoint);
  const fontSize = Math.max(11, Math.min(14, transform.scale * .82));
  const paddingX = 6;
  const paddingY = 4;
  const boxWidth = label.length * fontSize * .62 + paddingX * 2;
  const boxHeight = fontSize + paddingY * 2;
  const gap = Math.max(7, transform.scale * .65);
  let x = cellX + gap;
  let y = cellY - gap - boxHeight;
  if (x + boxWidth > canvas.width - transform.left) x = cellX - gap - boxWidth;
  if (y < transform.top) y = cellY + gap;
  x = Math.max(transform.left, Math.min(x, canvas.width - transform.left - boxWidth));
  y = Math.max(transform.top, Math.min(y, canvas.height - transform.top - boxHeight));
  context.fillStyle = "rgba(6, 22, 29, .9)";
  context.strokeStyle = "rgba(242, 246, 245, .72)";
  context.lineWidth = 1;
  context.fillRect(x, y, boxWidth, boxHeight);
  context.strokeRect(x, y, boxWidth, boxHeight);
  context.fillStyle = "#f2f6f5";
  context.font = `600 ${fontSize}px ui-monospace, SFMono-Regular, Menlo, monospace`;
  context.textBaseline = "middle";
  context.fillText(label, x + paddingX, y + boxHeight / 2);
}

function antOriginPoint() {
  return proofStage === "finiteHistory" || proofStage === "reverseHighway"
    ? proof.blank.entryPosition.map((coordinate) => -coordinate)
    : [0, 0];
}

function drawOrigin() {
  strokeCell(antOriginPoint(), COLORS.origin);
}

function drawHighwayEntry() {
  if (proofStage === "finiteHistory" || proofStage === "reverseHighway") {
    strokeCell([0, 0], "#58d5df");
  }
}

function drawHistoricalHit() {
  if (proofStage === "reverseHighway") {
    strokeCell(proof.reverseHighway.historicalHit, "#ffb454");
  }
}

function selectionColor(pointKey) {
  if (proofStage === "prefix") return COLORS.blue;
  if (proofStage === "pristine") {
    return COLORS.scattering[pristineCaseMap.get(pointKey).turns];
  }
  if (proofStage === "finiteHistory") {
    return finiteHistoryCaseMap.get(pointKey).stable
      ? COLORS.historyStable : COLORS.historyDirect;
  }
  return reverseCaseMap.get(pointKey).stable
    ? COLORS.reverseBase : COLORS.historyDirect;
}

function overviewStage(pointKey) {
  if (overviewPrefixSet.has(pointKey)) return 2;
  if (pointOnOverviewRay(pointKey, overviewReverseRay)) return 5;
  if (overviewOrdinarySet.has(pointKey)) return 4;
  if (
    overviewScatteringSet.has(pointKey)
    || overviewScatteringRays.some((ray) => pointOnOverviewRay(pointKey, ray))
  ) return 3;
  return 1;
}

function pointOnOverviewRay(pointKey, ray) {
  if (!ray) return false;
  const [x, y] = pointKey.split(",").map(Number);
  const dx = x - ray[0];
  const dy = y - ray[1];
  const [driftX, driftY] = proof.blank.drift;
  if (driftX === 0) {
    return dx === 0 && driftY !== 0 && dy % driftY === 0 && dy / driftY >= 1;
  }
  const depth = dx / driftX;
  return Number.isInteger(depth) && depth >= 1 && dy === depth * driftY;
}

function overviewCase(point) {
  const stage = overviewStage(key(point));
  if (stage === 1) return { stage, boundaryStep: proof.blank.entryStep };
  if (stage === 2) return { stage, ...prefixCaseMap.get(key(point)) };

  const canonical = [
    point[0] - proof.blank.entryPosition[0],
    point[1] - proof.blank.entryPosition[1],
  ];
  if (stage === 4) {
    const finiteCase = finiteHistoryCaseMap.get(key(canonical));
    return finiteCase && {
      ...finiteCase,
      stage,
      boundaryStep: proof.blank.entryStep + finiteCase.boundaryStep,
    };
  }
  if (stage === 5) {
    let reverseCase = reverseCaseMap.get(key(canonical));
    if (!reverseCase) {
      const formula = proof.scattering.laneFormulas.find((row) => row[0] === 72);
      const depth = translationIndex([formula[1], formula[2]], canonical, proof.blank.drift);
      const base = proof.reverseHighway.cases.find((row) => row[6] === 1);
      if (depth !== undefined && depth >= proof.reverseHighway.twoWayBaseDepth) {
        const offset = depth - proof.reverseHighway.twoWayBaseDepth;
        reverseCase = {
          phase: 72,
          depth,
          boundaryStep: base[4] + 2 * proof.blank.period * offset,
          turns: base[5],
          stable: true,
          reverseStartStep: proof.reverseHighway.reverseStartStep
            + proof.blank.period * offset,
          historicalHitStep: proof.reverseHighway.historicalHitStep
            + 2 * proof.blank.period * offset,
        };
      }
    }
    return reverseCase && {
      ...reverseCase,
      stage,
      boundaryStep: proof.blank.entryStep + reverseCase.boundaryStep,
      reverseStartStep: proof.blank.entryStep + reverseCase.reverseStartStep,
      historicalHitStep: proof.blank.entryStep + reverseCase.historicalHitStep,
    };
  }

  let pristineCase = pristineCaseMap.get(key(canonical));
  if (!pristineCase) {
    for (const [phase, frontierX, frontierY, terminalSteps] of proof.scattering.laneFormulas) {
      const depth = translationIndex(
        [frontierX, frontierY], canonical, proof.blank.drift,
      );
      if (depth === undefined || depth < 1) continue;
      const baseDepth = terminalSteps.length;
      pristineCase = {
        phase,
        depth,
        boundaryStep: depth <= baseDepth
          ? terminalSteps[depth - 1]
          : terminalSteps[baseDepth - 1]
            + (depth - baseDepth) * proof.blank.period,
        turns: proof.scattering.lanes.find((row) => row[0] === phase)?.[4],
      };
      break;
    }
  }
  return pristineCase && {
    ...pristineCase,
    stage,
    boundaryStep: proof.blank.entryStep + pristineCase.boundaryStep,
  };
}

function drawGrid() {
  context.strokeStyle = COLORS.grid;
  context.lineWidth = 1;
  for (let x = transform.minX; x <= transform.maxX; x += 1) {
    const [screenX] = transform.point([x, 0]);
    context.beginPath();
    context.moveTo(screenX - transform.scale / 2, transform.top);
    context.lineTo(screenX - transform.scale / 2, canvas.height - transform.top);
    context.stroke();
  }
  for (let y = transform.minY; y <= transform.maxY; y += 1) {
    const [, screenY] = transform.point([0, y]);
    context.beginPath();
    context.moveTo(transform.left, screenY + transform.scale / 2);
    context.lineTo(canvas.width - transform.left, screenY + transform.scale / 2);
    context.stroke();
  }
}

function drawContinuation() {
  const frontier = proof.blank.tailFrontier[0];
  const from = addCycle(frontier, proof.blank.drift, VISIBLE_TAIL_CYCLES - 4);
  const to = addCycle(frontier, proof.blank.drift, VISIBLE_TAIL_CYCLES + 1);
  const [fromX, fromY] = transform.point(from);
  const [toX, toY] = transform.point(to);
  const angle = Math.atan2(toY - fromY, toX - fromX);
  context.strokeStyle = COLORS.border;
  context.fillStyle = COLORS.border;
  context.lineWidth = 2;
  context.beginPath();
  context.moveTo(fromX, fromY);
  context.lineTo(toX, toY);
  context.stroke();
  context.beginPath();
  context.moveTo(toX, toY);
  context.lineTo(toX - 12 * Math.cos(angle - Math.PI / 6), toY - 12 * Math.sin(angle - Math.PI / 6));
  context.lineTo(toX - 12 * Math.cos(angle + Math.PI / 6), toY - 12 * Math.sin(angle + Math.PI / 6));
  context.closePath();
  context.fill();
}

function drawAnt([x, y, heading]) {
  const [screenX, screenY] = transform.point([x, y]);
  const angles = [-Math.PI / 2, 0, Math.PI / 2, Math.PI];
  const angle = angles[heading];
  const radius = Math.max(11, transform.scale * 1.05);
  context.fillStyle = "rgba(242, 186, 82, .25)";
  context.beginPath();
  context.arc(screenX, screenY, radius * 1.65, 0, Math.PI * 2);
  context.fill();
  context.fillStyle = COLORS.ant;
  context.strokeStyle = "#2d2517";
  context.lineWidth = 2;
  context.beginPath();
  context.moveTo(screenX + Math.cos(angle) * radius, screenY + Math.sin(angle) * radius);
  context.lineTo(screenX + Math.cos(angle + 2.45) * radius * .82, screenY + Math.sin(angle + 2.45) * radius * .82);
  context.lineTo(screenX + Math.cos(angle - 2.45) * radius * .82, screenY + Math.sin(angle - 2.45) * radius * .82);
  context.closePath();
  context.fill();
  context.stroke();
}

function drawTrail(points, color, width) {
  if (points.length < 2) return;
  context.strokeStyle = color;
  context.lineWidth = width;
  context.lineJoin = "round";
  context.lineCap = "round";
  context.beginPath();
  const [startX, startY] = transform.point(points[0]);
  context.moveTo(startX, startY);
  for (const point of points.slice(1)) {
    const [x, y] = transform.point(point);
    context.lineTo(x, y);
  }
  context.stroke();
}

function drawRecentTrail() {
  drawTrail(trail.slice(-900), "rgba(244, 249, 248, .72)", Math.max(2.4, transform.scale * .3));
  drawTrail(highwayTrail.slice(-1400), COLORS.highwayTrail, Math.max(3.2, transform.scale * .42));
}

function drawReferenceField() {
  for (let x = transform.minX; x <= transform.maxX; x += 1) {
    for (let y = transform.minY; y <= transform.maxY; y += 1) {
      const point = [x, y];
      const pointKey = key(point);
      let color;
      if (proofStage === "overview") {
        color = COLORS.overview[overviewStage(pointKey) - 1];
      } else if (proofStage === "pristine") {
        if (pristinePointSet.has(pointKey)) {
          color = COLORS.scattering[pristineCaseMap.get(pointKey).turns];
        }
        else color = pristineSupportSet.has(pointKey) ? COLORS.gray : COLORS.inactive;
      } else if (proofStage === "finiteHistory") {
        if (finiteHistoryPointSet.has(pointKey)) {
          color = selectionColor(pointKey);
        } else if (finiteHistoryStableTailSet.has(pointKey)) {
          color = COLORS.historyStable;
        } else {
          color = finiteHistoryWakeSet.has(pointKey) ? COLORS.gray : COLORS.inactive;
        }
      } else if (proofStage === "reverseHighway") {
        if (reversePointSet.has(pointKey)) color = selectionColor(pointKey);
        else if (reverseStableTailSet.has(pointKey)) color = COLORS.reverseBase;
        else color = reverseReferenceSet.has(pointKey) ? COLORS.gray : COLORS.inactive;
      } else if (proofStage === "outside") {
        color = visibleReferenceSet.has(pointKey) ? COLORS.gray : COLORS.blue;
      } else if (prefixSet.has(pointKey)) {
        color = COLORS.blue;
      } else {
        color = visibleReferenceSet.has(pointKey) ? COLORS.gray : COLORS.inactive;
      }
      fillCell(point, color);
    }
  }
}

function drawDisplay() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = COLORS.background;
  context.fillRect(0, 0, canvas.width, canvas.height);
  drawReferenceField();
  drawGrid();
  if (proofStage === "outside" || proofStage === "prefix") drawContinuation();
  drawOrigin();
  drawHighwayEntry();
  drawHistoricalHit();
  if (hoveredPoint) {
    strokeCell(hoveredPoint, COLORS.hover);
    drawHoverCoordinate();
  }
}

function drawEvolution() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = COLORS.background;
  context.fillRect(0, 0, canvas.width, canvas.height);
  drawReferenceField();
  for (const pointKey of fastVisited) {
    const [x, y] = pointKey.split(",").map(Number);
    fillCell([x, y], COLORS.disturbed);
  }
  for (const pointKey of fastReverseVisited) {
    const [x, y] = pointKey.split(",").map(Number);
    fillCell([x, y], COLORS.reverseHighway);
  }
  for (const pointKey of reverseVisited) {
    const [x, y] = pointKey.split(",").map(Number);
    fillCell([x, y], COLORS.reverseHighway);
  }
  for (const pointKey of fastHighwayVisited) {
    const [x, y] = pointKey.split(",").map(Number);
    fillCell([x, y], COLORS.highway);
  }
  for (const pointKey of highwayVisited) {
    const [x, y] = pointKey.split(",").map(Number);
    fillCell([x, y], COLORS.highway);
  }
  if (proofStage !== "outside" && proofStage !== "overview") {
    if (proofStage === "finiteHistory") {
      for (const pointKey of finiteHistoryStableTailSet) {
        const [x, y] = pointKey.split(",").map(Number);
        fillCell([x, y], COLORS.historyStable);
      }
    }
    if (proofStage === "reverseHighway") {
      for (const pointKey of reverseStableTailSet) {
        const [x, y] = pointKey.split(",").map(Number);
        fillCell([x, y], COLORS.reverseBase);
      }
    }
    const selectableSet = proofStage === "prefix"
      ? prefixSet
      : proofStage === "pristine"
        ? pristinePointSet
        : proofStage === "finiteHistory" ? finiteHistoryPointSet : reversePointSet;
    for (const pointKey of selectableSet) {
      const [x, y] = pointKey.split(",").map(Number);
      fillCell([x, y], selectionColor(pointKey));
    }
  }
  drawGrid();
  drawRecentTrail();
  fillCell(selectedPoint, COLORS.black, .05);
  strokeCell(selectedPoint, "#f2f6f5");
  if (
    hoveredPoint
    && key(hoveredPoint) !== key(selectedPoint)
    && isSelectablePoint(hoveredPoint)
  ) {
    strokeCell(hoveredPoint, COLORS.hover);
  }
  drawOrigin();
  drawHighwayEntry();
  drawHistoricalHit();
  drawAnt([simulation.x, simulation.y, simulation.heading]);
  if (proofStage === "outside") drawContinuation();
  drawHoverCoordinate();
}

function advanceSimulation(toStep) {
  const boundaryStep = proofStage === "outside"
    ? proof.blank.entryStep
    : selectedCase.boundaryStep;
  while (simulation.step < toStep) {
    const point = [simulation.x, simulation.y];
    trail.push(point);
    if (simulation.step >= boundaryStep) {
      highwayVisited.add(key(point));
      highwayTrail.push(point);
    }
    if (
      proofStage === "reverseHighway"
      && selectedCase.stable
      && simulation.step >= selectedCase.reverseStartStep
      && simulation.step < selectedCase.historicalHitStep
    ) reverseVisited.add(key(point));
    advanceOne(simulation);
  }
}

function evolutionTiming() {
  const boundaryStep = proofStage === "outside"
    ? proof.blank.entryStep
    : selectedCase.boundaryStep;
  const historyStep = proofStage === "pristine"
    ? proof.scattering.cyclesBeforeHit * proof.blank.period
    : 0;
  const historyMs = proofStage === "pristine" ? SCATTERING_HISTORY_MS : 0;
  const scatteringMs = proofStage === "pristine"
    ? Math.max(7000, Math.min(18000, (boundaryStep - historyStep) / 5))
    : 0;
  const reverseProof = proofStage === "reverseHighway" && selectedCase.stable;
  const transientMs = boundaryStep === 0
    ? 0
    : proofStage === "outside"
    ? PREFIX_ANIMATION_MS
    : proofStage === "pristine"
      ? historyMs + scatteringMs
      : reverseProof
        ? REVERSE_APPROACH_MS + REVERSE_HIGHWAY_MS + REVERSE_POST_HIT_MS
      : Math.max(8000, Math.min(18000, boundaryStep / 5));
  return {
    boundaryStep, historyStep, historyMs, scatteringMs, transientMs,
    reverseProof,
    highwayMs: HIGHWAY_ANIMATION_MS,
    terminalStep: boundaryStep + proof.blank.period * HIGHWAY_CYCLES,
  };
}

function computeFastTerminal(generation) {
  if (proofStage === "outside" || generation !== evolutionGeneration) return;
  const state = createSelectedSimulation();
  const visited = new Set();
  const highway = new Set();
  while (state.step < selectedCase.boundaryStep) {
    const pointKey = `${state.x},${state.y}`;
    visited.add(pointKey);
    if (
      proofStage === "reverseHighway"
      && selectedCase.stable
      && state.step >= selectedCase.reverseStartStep
      && state.step < selectedCase.historicalHitStep
    ) fastReverseVisited.add(pointKey);
    advanceOne(state);
  }
  if (proofStage === "prefix" && (
    state.x !== selectedCase.boundaryPosition[0]
    || state.y !== selectedCase.boundaryPosition[1]
    || state.black.size !== selectedCase.blackCount
  )) {
    throw new Error("The live prefix replay disagrees with its certified boundary");
  }
  const terminalStep = selectedCase.boundaryStep + proof.blank.period * HIGHWAY_CYCLES;
  while (state.step < terminalStep) {
    const pointKey = `${state.x},${state.y}`;
    visited.add(pointKey);
    highway.add(pointKey);
    advanceOne(state);
  }
  if (generation !== evolutionGeneration) return;
  fastVisited = visited;
  fastHighwayVisited = highway;
  const finalPoints = [...visited].map((pointKey) => pointKey.split(",").map(Number));
  transform = proofStage === "pristine"
    ? makeTransform(finalPoints, pristineReferencePoints)
    : proofStage === "finiteHistory"
      ? makeTransform(finalPoints, finiteHistoryReferencePoints)
      : proofStage === "reverseHighway"
        ? makeTransform(finalPoints, reverseReferencePoints)
        : proofStage === "overview"
          ? makeTransform(finalPoints, overviewReferencePoints)
        : makeTransform(finalPoints);
  visibleReferenceSet = buildVisibleReferenceSet();
  elements.mapCaption.textContent = "Beige shows the complete disturbed footprint; gray preserves the blank reference or pre-existing history.";
  drawEvolution();
}

function createSelectedSimulation() {
  if (proofStage === "overview") return createSimulation([selectedPoint]);
  if (proofStage === "pristine") {
    return createSimulation([...proof.blank.blackRelative, selectedPoint], proof.blank.startHeading);
  }
  if (proofStage === "finiteHistory" || proofStage === "reverseHighway") {
    return createSimulation(
      [...proof.finiteHistory.entryBlackRelative, selectedPoint],
      proof.blank.startHeading,
    );
  }
  return createSimulation([selectedPoint]);
}

function animationStep(now) {
  const elapsed = Math.max(0, now - animationStartedAt);
  const timing = evolutionTiming();
  let targetStep;
  if (elapsed < timing.transientMs) {
    if (proofStage === "pristine" && elapsed < timing.historyMs) {
      targetStep = Math.floor(timing.historyStep * elapsed / timing.historyMs);
    } else if (proofStage === "pristine") {
      const scatteringElapsed = elapsed - timing.historyMs;
      targetStep = timing.historyStep + Math.floor(
        (timing.boundaryStep - timing.historyStep)
        * scatteringElapsed / timing.scatteringMs,
      );
    } else if (timing.reverseProof && elapsed < REVERSE_APPROACH_MS) {
      targetStep = Math.floor(
        selectedCase.reverseStartStep * elapsed / REVERSE_APPROACH_MS,
      );
    } else if (
      timing.reverseProof
      && elapsed < REVERSE_APPROACH_MS + REVERSE_HIGHWAY_MS
    ) {
      const reverseElapsed = elapsed - REVERSE_APPROACH_MS;
      targetStep = selectedCase.reverseStartStep + Math.floor(
        (selectedCase.historicalHitStep - selectedCase.reverseStartStep)
        * reverseElapsed / REVERSE_HIGHWAY_MS,
      );
    } else if (timing.reverseProof) {
      const postHitElapsed = elapsed - REVERSE_APPROACH_MS - REVERSE_HIGHWAY_MS;
      targetStep = selectedCase.historicalHitStep + Math.floor(
        (timing.boundaryStep - selectedCase.historicalHitStep)
        * postHitElapsed / REVERSE_POST_HIT_MS,
      );
    } else {
      targetStep = Math.floor(timing.boundaryStep * elapsed / timing.transientMs);
    }
  } else {
    const highwayElapsed = Math.min(elapsed - timing.transientMs, timing.highwayMs);
    const highwaySteps = proof.blank.period * HIGHWAY_CYCLES;
    targetStep = timing.boundaryStep + Math.floor(highwaySteps * highwayElapsed / timing.highwayMs);
  }
  targetStep = Math.min(targetStep, timing.terminalStep);
  advanceSimulation(targetStep);
  drawEvolution();
  if (targetStep < timing.boundaryStep) {
    if (proofStage === "outside") {
      setEvolutionReadout(`t = ${targetStep} / ${timing.boundaryStep} · remains unread`);
    } else if (proofStage === "pristine" && targetStep < timing.historyStep) {
      const cycle = Math.floor(targetStep / proof.blank.period) + 1;
      setEvolutionReadout(`undisturbed P104 history · cycle ${cycle} / ${proof.scattering.cyclesBeforeHit}`);
    } else if (proofStage === "pristine") {
      setEvolutionReadout(`hit in cycle ${proof.scattering.cyclesBeforeHit + 1} · scattering t = ${targetStep} / ${timing.boundaryStep}`);
    } else if (
      proofStage === "reverseHighway"
      && selectedCase.stable
      && targetStep >= selectedCase.reverseStartStep
      && targetStep < selectedCase.historicalHitStep
    ) {
      setEvolutionReadout(`reverse P104 · returning toward the t=9977 history · t = ${targetStep}`);
    } else if (
      proofStage === "reverseHighway"
      && selectedCase.stable
      && targetStep >= selectedCase.historicalHitStep
    ) {
      setEvolutionReadout(`fixed history cell reached · second scattering · t = ${targetStep}`);
    } else {
      setEvolutionReadout(`slow replay · t = ${targetStep} / ${timing.boundaryStep}`);
    }
  } else if (targetStep < timing.terminalStep) {
    const cycle = Math.floor((targetStep - timing.boundaryStep) / proof.blank.period) + 1;
    setEvolutionReadout(`t = ${targetStep} · terminal P104 cycle ${cycle} / ${HIGHWAY_CYCLES}`);
  } else {
    setEvolutionReadout(proofStage === "outside"
      ? `t = ${targetStep} · P104 · never read`
      : `t = ${targetStep} · certified P104 reached`);
    return;
  }
  animationFrame = requestAnimationFrame(animationStep);
}

function setEvolutionCopy() {
  elements.mapCaption.textContent = proofStage === "outside"
    ? "q uses the initial global coordinates. It is never read, so the evolution exactly follows the gray blank-orbit reference."
    : proofStage === "prefix"
      ? "q uses the initial global coordinates. The slow replay shows the process while the fast replay computes the complete beige footprint."
      : "q is relative to the t=9977 P104-entry state. The slow replay shows the process while the fast replay computes the complete beige footprint.";
  if (proofStage === "overview") {
    elements.mapCaption.textContent = "q uses the initial global coordinates. This is a direct replay from the origin; click the canvas again to return.";
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip overview-1"></i>01 Untouched</span><span class="legend-item"><i class="legend-chip overview-2"></i>02 Prefix</span><span class="legend-item"><i class="legend-chip overview-3"></i>03 Scattering</span><span class="legend-item"><i class="legend-chip overview-4"></i>04 History</span><span class="legend-item"><i class="legend-chip overview-5"></i>05 Reverse</span><span class="legend-item"><i class="legend-chip legend-black"></i>Perturbation q</span><span class="legend-item"><i class="legend-chip legend-disturbed"></i>Actual footprint</span><span class="legend-item"><i class="legend-chip legend-highway"></i>Terminal P104</span><span class="legend-item"><i class="legend-chip legend-ant"></i>Ant</span>';
  } else if (proofStage === "pristine") {
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-black"></i>Perturbation q</span><span class="legend-item"><i class="legend-chip legend-gray"></i>Undisturbed reference</span><span class="legend-item"><i class="legend-chip legend-disturbed"></i>Disturbed footprint</span><span class="legend-item"><i class="legend-chip scatter-straight"></i>Straight</span><span class="legend-item"><i class="legend-chip scatter-right"></i>Right</span><span class="legend-item"><i class="legend-chip scatter-reverse"></i>Reverse</span><span class="legend-item"><i class="legend-chip scatter-left"></i>Left</span><span class="legend-item"><i class="legend-chip legend-highway"></i>Terminal P104</span><span class="legend-item"><i class="legend-chip legend-ant"></i>Slow replay</span>';
  } else if (proofStage === "finiteHistory") {
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-black"></i>Perturbation q</span><span class="legend-item"><i class="legend-chip legend-origin"></i>Initial ant at t=0</span><span class="legend-item"><i class="legend-chip legend-entry"></i>P104 entry at t=9977</span><span class="legend-item"><i class="legend-chip legend-gray"></i>t=9977 finite history</span><span class="legend-item"><i class="legend-chip legend-disturbed"></i>Disturbed footprint</span><span class="legend-item"><i class="legend-chip history-direct"></i>Direct finite case</span><span class="legend-item"><i class="legend-chip history-stable"></i>Stable lane</span><span class="legend-item"><i class="legend-chip legend-highway"></i>Terminal P104</span><span class="legend-item"><i class="legend-chip legend-ant"></i>Slow replay</span>';
  } else if (proofStage === "reverseHighway") {
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-black"></i>Perturbation q</span><span class="legend-item"><i class="legend-chip legend-origin"></i>Initial ant at t=0</span><span class="legend-item"><i class="legend-chip legend-entry"></i>P104 entry at t=9977</span><span class="legend-item"><i class="legend-chip legend-gray"></i>t=9977 finite history</span><span class="legend-item"><i class="legend-chip legend-disturbed"></i>Disturbed footprint</span><span class="legend-item"><i class="legend-chip history-direct"></i>Shallow direct case</span><span class="legend-item"><i class="legend-chip reverse-base"></i>Two-way induction</span><span class="legend-item"><i class="legend-chip reverse-highway"></i>Reverse P104</span><span class="legend-item"><i class="legend-chip legend-highway"></i>Terminal P104</span><span class="legend-item"><i class="legend-chip legend-ant"></i>Slow replay</span>';
  } else {
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-black"></i>Perturbation q</span><span class="legend-item"><i class="legend-chip legend-blue"></i>Candidate placement</span><span class="legend-item"><i class="legend-chip legend-gray"></i>Blank-orbit reference</span><span class="legend-item"><i class="legend-chip legend-disturbed"></i>Disturbed footprint</span><span class="legend-item"><i class="legend-chip legend-highway"></i>Terminal P104</span><span class="legend-item"><i class="legend-chip legend-ant"></i>Slow replay</span>';
  }
  elements.reset.disabled = false;
  elements.reset.setAttribute("aria-hidden", "false");
}

function setDisplayCopy() {
  if (proofStage === "outside") {
    elements.mapCaption.textContent = "Gray is the complete blank-orbit footprint; every blue placement remains unread while the P104 tail continues indefinitely to the lower left.";
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-gray"></i>Blank-orbit reads</span><span class="legend-item"><i class="legend-chip legend-blue"></i>Untouched placements</span>';
  } else if (proofStage === "prefix") {
    elements.mapCaption.textContent = "The 1,376 blue cells are exactly those first read before the blank orbit reaches its P104 entry boundary at t=9977.";
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-blue"></i>Prefix-hit placements</span><span class="legend-item"><i class="legend-chip legend-gray"></i>Subsequent P104 tail</span>';
  } else if (proofStage === "pristine") {
    elements.mapCaption.textContent = `The perturbation is first read in cycle ${proof.scattering.cyclesBeforeHit + 1}, after ${proof.scattering.cyclesBeforeHit} undisturbed P104 cycles; the gray reference continues ${PRISTINE_REFERENCE_AFTER_HIT_CYCLES} more cycles for comparison.`;
    elements.legend.innerHTML = `<span class="legend-item"><i class="legend-chip scatter-straight"></i>Straight</span><span class="legend-item"><i class="legend-chip scatter-right"></i>Turn right</span><span class="legend-item"><i class="legend-chip scatter-reverse"></i>Reverse</span><span class="legend-item"><i class="legend-chip scatter-left"></i>Turn left</span><span class="legend-item"><i class="legend-chip legend-gray"></i>Undisturbed reference</span>`;
  } else if (proofStage === "finiteHistory") {
    elements.mapCaption.textContent = "Orange marks direct depths; blue extends stable lanes through depth 30. Red is the t=0 ant origin; cyan is the t=9977 P104 entry.";
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-origin"></i>Initial ant at t=0</span><span class="legend-item"><i class="legend-chip legend-entry"></i>P104 entry at t=9977</span><span class="legend-item"><i class="legend-chip legend-gray"></i>t=9977 finite history</span><span class="legend-item"><i class="legend-chip history-direct"></i>Direct finite depths</span><span class="legend-item"><i class="legend-chip history-stable"></i>Inductive stable tail</span>';
  } else if (proofStage === "reverseHighway") {
    elements.mapCaption.textContent = "Phase 72: depths 1–14 are direct; purple depths 15–20 represent the induction. Red is the t=0 ant origin; cyan is the t=9977 P104 entry.";
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip legend-origin"></i>Initial ant at t=0</span><span class="legend-item"><i class="legend-chip legend-entry"></i>P104 entry at t=9977</span><span class="legend-item"><i class="legend-chip legend-gray"></i>t=9977 finite history</span><span class="legend-item"><i class="legend-chip history-direct"></i>Depths 1–14</span><span class="legend-item"><i class="legend-chip reverse-base"></i>Depths 15–20</span><span class="legend-item"><i class="legend-chip history-hit"></i>Fixed history hit</span>';
  } else {
    elements.mapCaption.textContent = "Every visible cell has one class; a 03/04 overlap belongs to 04 exactly when its replay or terminal corridor meets the finite history. Click to replay; click again to return.";
    elements.legend.innerHTML = '<span class="legend-item"><i class="legend-chip overview-1"></i>01 Untouched</span><span class="legend-item"><i class="legend-chip overview-2"></i>02 Prefix hit</span><span class="legend-item"><i class="legend-chip overview-3"></i>03 P104 scattering</span><span class="legend-item"><i class="legend-chip overview-4"></i>04 History intersection</span><span class="legend-item"><i class="legend-chip overview-5"></i>05 Reverse highway</span>';
  }
  elements.reset.disabled = true;
  elements.reset.setAttribute("aria-hidden", "true");
  elements.readout.textContent = proofStage === "overview"
    ? "Move to inspect · click to replay"
    : "Hover over a cell to inspect its role";
}

function startEvolution(point, force = false) {
  if (
    (!force && !isSelectablePoint(point))
    || (selectedPoint && key(point) === key(selectedPoint))
  ) return;
  cancelAnimationFrame(animationFrame);
  clearTimeout(hoverTimer);
  clearTimeout(fastTimer);
  evolutionGeneration += 1;
  const generation = evolutionGeneration;
  mode = "evolution";
  selectedPoint = [...point];
  selectedCase = proofStage === "overview"
    ? overviewCase(point)
    : proofStage === "prefix"
    ? prefixCaseMap.get(key(point))
    : proofStage === "pristine"
      ? pristineCaseMap.get(key(point))
      : proofStage === "finiteHistory"
        ? finiteHistoryCaseMap.get(key(point))
        : reverseCaseMap.get(key(point));
  if (proofStage !== "outside" && !selectedCase) {
    throw new Error("The selected cell has no matching certificate case");
  }
  hoveredPoint = undefined;
  transform = proofStage === "pristine"
    ? pristineTransform
    : proofStage === "finiteHistory"
      ? finiteHistoryTransform
      : proofStage === "reverseHighway"
        ? reverseTransform
        : proofStage === "overview" ? overviewTransform : defaultTransform;
  visibleReferenceSet = proofStage === "pristine"
    ? pristineVisibleReferenceSet
    : proofStage === "finiteHistory"
      ? finiteHistoryVisibleReferenceSet
      : proofStage === "reverseHighway"
        ? reverseVisibleReferenceSet
        : proofStage === "overview" ? new Set() : defaultVisibleReferenceSet;
  simulation = createSelectedSimulation();
  highwayVisited = new Set();
  fastVisited = new Set();
  fastHighwayVisited = new Set();
  reverseVisited = new Set();
  fastReverseVisited = new Set();
  trail = [];
  highwayTrail = [];
  if (proofStage === "overview") computeFastTerminal(generation);
  setEvolutionCopy();
  const initialReadout = proofStage === "outside"
    ? `t = 0 / ${proof.blank.entryStep} · remains unread`
    : proofStage === "pristine"
      ? `Undisturbed P104 history · cycle 0 / ${proof.scattering.cyclesBeforeHit}`
      : proofStage === "finiteHistory"
        ? `${selectedCase.stable ? "Stable entry" : "Direct history case"} · depth ${selectedCase.depth} · t = 0`
        : proofStage === "reverseHighway"
          ? `${selectedCase.stable ? "Two-way induction case" : "Shallow direct case"} · depth ${selectedCase.depth} · t = 0`
          : proofStage === "overview"
            ? `Stage ${selectedCase.stage.toString().padStart(2, "0")} · t = 0 / ${selectedCase.boundaryStep}`
        : `Slow replay · t = 0 / ${selectedCase.boundaryStep}`;
  setEvolutionReadout(initialReadout);
  drawEvolution();
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const timing = evolutionTiming();
  animationFrame = requestAnimationFrame((now) => {
    animationStartedAt = now - (reducedMotion ? timing.transientMs + timing.highwayMs : 0);
    if (proofStage !== "outside" && proofStage !== "overview") {
      fastTimer = window.setTimeout(() => {
        try {
          computeFastTerminal(generation);
        } catch (error) {
          setEvolutionReadout("fast terminal replay failed");
          console.error(error);
        }
      }, 0);
    }
    animationFrame = requestAnimationFrame(animationStep);
  });
}

function startOverviewEvolution(point) {
  startEvolution(point, true);
}

function returnToDisplay() {
  cancelAnimationFrame(animationFrame);
  clearTimeout(hoverTimer);
  clearTimeout(fastTimer);
  evolutionGeneration += 1;
  mode = "display";
  selectedPoint = undefined;
  hoveredPoint = undefined;
  hoveredKey = undefined;
  simulation = undefined;
  selectedCase = undefined;
  fastVisited = new Set();
  fastHighwayVisited = new Set();
  reverseVisited = new Set();
  fastReverseVisited = new Set();
  transform = proofStage === "pristine"
    ? pristineTransform
    : proofStage === "finiteHistory"
      ? finiteHistoryTransform
      : proofStage === "reverseHighway"
        ? reverseTransform
        : proofStage === "overview" ? overviewTransform : defaultTransform;
  visibleReferenceSet = proofStage === "pristine"
    ? pristineVisibleReferenceSet
    : proofStage === "finiteHistory"
      ? finiteHistoryVisibleReferenceSet
      : proofStage === "reverseHighway"
        ? reverseVisibleReferenceSet
        : proofStage === "overview" ? new Set() : defaultVisibleReferenceSet;
  setDisplayCopy();
  drawDisplay();
}

function pointFromEvent(event) {
  const rect = canvas.getBoundingClientRect();
  return transform.cellAt(
    (event.clientX - rect.left) * canvas.width / rect.width,
    (event.clientY - rect.top) * canvas.height / rect.height,
  );
}

canvas.addEventListener("pointermove", (event) => {
  const point = pointFromEvent(event);
  if (!point || key(point) === hoveredKey) return;
  clearTimeout(hoverTimer);
  hoveredPoint = point;
  hoveredKey = key(point);
  const selectable = isSelectablePoint(point);
  if (mode === "display") {
    if (proofStage === "outside") {
      elements.readout.textContent = `${key(point)} · ${selectable ? "untouched placement · pause to replay" : "read by the blank orbit"}`;
    } else if (proofStage === "prefix" && selectable) {
      elements.readout.textContent = `${key(point)} · first blank-orbit read at t = ${prefixFirstRead.get(key(point))}`;
    } else if (proofStage === "pristine" && selectable) {
      const lane = pristineCaseMap.get(key(point));
      elements.readout.textContent = `${key(point)} · ${SCATTERING_DIRECTIONS[lane.turns]} · P104 phase ${lane.phase}`;
    } else if (proofStage === "finiteHistory" && selectable) {
      const lane = finiteHistoryCaseMap.get(key(point));
      elements.readout.textContent = `${key(point)} · depth ${lane.depth} · ${lane.stable ? "stable entry" : "direct history case"}`;
    } else if (proofStage === "finiteHistory" && finiteHistoryStableTailSet.has(key(point))) {
      elements.readout.textContent = `${key(point)} · depth ${finiteHistoryStableDepthMap.get(key(point))} · covered by P104 cycle induction`;
    } else if (proofStage === "reverseHighway" && selectable) {
      const lane = reverseCaseMap.get(key(point));
      elements.readout.textContent = `${key(point)} · phase 72 · depth ${lane.depth} · ${lane.stable ? "selectable two-way induction case" : "direct case"}`;
    } else if (proofStage === "reverseHighway" && reverseStableTailSet.has(key(point))) {
      elements.readout.textContent = `${key(point)} · phase 72 · depth ${reverseStableDepthMap.get(key(point))} · covered by two-way induction`;
    } else if (proofStage === "overview") {
      const stage = overviewStage(key(point));
      const labels = ["untouched", "prefix hit", "P104 scattering", "history intersection", "reverse highway"];
      elements.readout.textContent = `${key(point)} · stage ${stage.toString().padStart(2, "0")} · ${labels[stage - 1]}`;
    } else {
      elements.readout.textContent = `${key(point)} · outside this stage`;
    }
    drawDisplay();
  } else {
    drawEvolution();
  }
  if (
    proofStage !== "overview"
    && selectable
    && (!selectedPoint || key(point) !== key(selectedPoint))
  ) {
    hoverTimer = window.setTimeout(() => startEvolution(point), HOVER_DELAY_MS);
  }
});

canvas.addEventListener("click", (event) => {
  if (proofStage !== "overview") return;
  clearTimeout(hoverTimer);
  if (mode === "evolution") {
    returnToDisplay();
    return;
  }
  const point = pointFromEvent(event);
  if (point) startOverviewEvolution(point);
});

canvas.addEventListener("pointerleave", () => {
  clearTimeout(hoverTimer);
  hoveredPoint = undefined;
  hoveredKey = undefined;
  if (mode === "display") {
    elements.readout.textContent = proofStage === "overview"
      ? "Move to inspect · click to replay"
      : "Hover over a cell to inspect its role";
    drawDisplay();
  } else {
    drawEvolution();
  }
});

const STAGE_GUIDE_CONTENT = {
  outside: {
    badge: "Stage 01 · Untouched",
    title: "Untouched Placements & Asymptotic Spatial Immunity",
    leanSig: "theorem separated_reaches (p : Point) : p ∉ support → separatedFromSupport p = true → ReachesP104 (blacken p entry)",
    mechanismHtml: `
      <p><strong>Target scope:</strong> Any initial single black cell placed on lattice coordinates that the unperturbed (all-white) ant trajectory and its future highway envelope never visit.</p>
      <p><strong>Proof mechanism:</strong> From an all-white grid, the ant visits only a bounded set of cells during its initial 9,977 chaotic steps before entering a permanent period-104 (P104) highway moving in diagonal direction $v = (-2, -2)$. This highway sweeps an infinite but spatially bounded corridor toward the lower-left.</p>
      <p>By the <em>First Difference Lemma</em> of deterministic cellular automata, if a perturbation cell $p$ is never visited by the baseline trajectory up to time $t$, the actual evolution up to time $t$ is strictly identical to the baseline. Since cells in this vast complementary region are never reached by either the prefix or the periodic highway, the ant never reads cell $p$, guaranteeing permanent highway convergence. This geometric immunity argument immediately settles an infinite measure-1 subregion of $\\mathbb{Z}^2$.</p>
    `,
  },
  prefix: {
    badge: "Stage 02 · Prefix Hit",
    title: "Blank Prefix Collisions & Deterministic Finite Transients",
    leanSig: "theorem Prefix.reaches (cert : Prefix.Certificate) : p ∈ Prefix.domain → ReachesP104 (singleton p)",
    mechanismHtml: `
      <p><strong>Target scope:</strong> Any initial black cell placed on one of the cells visited by the ant during its first 9,977 steps from an all-white grid.</p>
      <p><strong>Proof mechanism:</strong> Before reaching the canonical highway entrance at step 9,977, the unperturbed ant visits an explicitly bounded set of exactly <strong>1,376 distinct lattice cells</strong>. When an initial black cell lies within this set, the trajectory collides with it during this chaotic transient phase and diverges from the baseline.</p>
      <p>Because the state space of this branch is strictly finite (1,376 discrete initial states), the proof proceeds by deterministic finite replay. Lean 4 native execution leaves (<code>PrefixData.lean</code> and <code>PrefixLeaf.lean</code>) formally evaluate each altered trajectory with zero runtime search, certifying that all 1,376 configurations escape the transient and enter a permanent P104 highway within at most 110,000 steps.</p>
    `,
  },
  pristine: {
    badge: "Stage 03 · P104 Scattering",
    title: "Pristine Frontier Channels & Affine Ray Induction",
    leanSig: "theorem Pristine.lane_reaches (member : head ∈ heads) (positive : 0 < depth) : ReachesP104 (blacken (obstacle head depth) pristineEntry)",
    mechanismHtml: `
      <p><strong>Target scope:</strong> An isolated black obstacle placed directly in the path of a mature P104 highway advancing into clean empty space (pristine channels).</p>
      <p><strong>Proof mechanism:</strong> The leading face of a P104 highway comprises exactly <strong>22 channel heads</strong> $H = \\{s \\in S \\mid s - v \\notin S\\}$. Any obstacle ahead is parameterized as an affine ray $q = h + d \\cdot v$ ($d \\ge 1$). Increasing the obstacle depth to $d = P_h + n$ causes the ant to execute $n$ clean P104 blocks before colliding with the obstacle, depositing a sequence of translated XOR difference wakes $W \\oplus (W+v) \\oplus \\dots \\oplus (W+(n-1)v)$.</p>
      <p>The <em>Affine Ray Induction Theorem</em> proves that these accumulated wake layers are strictly disjoint from all future scattering reads and the terminal highway corridor (acting as inert archives). Consequently, certifying a single finite anchor depth $P_h \\le 23$ per channel mathematically closes highway convergence for all infinite depths $d \\ge P_h$.</p>
    `,
  },
  finiteHistory: {
    badge: "Stage 04 · Finite History",
    title: "Historical Wake Decoupling on Ordinary Channels",
    leanSig: "theorem Ordinary.lane_reaches (head : Point) (ordinary : head ∈ ordinaryHeads) (positive : 0 < depth) : ReachesP104 (blacken (obstacle head depth) entry)",
    mechanismHtml: `
      <p><strong>Target scope:</strong> Highway scattering in the physical grid, where the ant's initial 9,977-step chaotic prefix left behind a cloud of <strong>702 pre-existing historical black cells</strong> ($H_E$), evaluated on the 21 ordinary channels.</p>
      <p><strong>Proof mechanism:</strong> For 21 of the 22 channels (the ordinary channels), post-collision scattering does not reverse deep into the historical cloud. Each ordinary channel is partitioned by a channel-local geometric cutoff depth $A_h$ ($\\ge P_h$):</p>
      <ul>
        <li><strong>Direct Replay Band ($1 \\le d < A_h$):</strong> Scattering may interact with the historical cloud. Lean 4 directly verifies 186 explicit witness cases (totaling 2,761,211 steps) via deterministic replay certificates.</li>
        <li><strong>Inductive Band ($d \\ge A_h$):</strong> The cutoff $A_h$ ensures that the entire post-collision read footprint and subsequent terminal corridor remain strictly disjoint from $H_E$. Using untouched-coupling with lag $L_h = A_h - P_h$, all deep historical cases reduce directly to the pristine induction theorem of Stage 03.</li>
      </ul>
    `,
  },
  reverseHighway: {
    badge: "Stage 05 · Reverse Highway",
    title: "Exceptional Backscattering, Affine Hit Law & History Collision",
    leanSig: "theorem Phase.lane_reaches (positive : 0 < depth) : ReachesP104 (blacken (obstacle phaseHead depth) entry)",
    mechanismHtml: `
      <p><strong>Target scope:</strong> The 22nd frontier channel ($h_{72} = \\text{base.pos} + (-2,-8)$), which exhibits an exceptional reverse highway that turns backward toward the 702-cell historical cloud $H_E$.</p>
      <p><strong>Proof mechanism:</strong> Striking an obstacle at depth $d \\ge 11$ on channel $h_{72}$ transforms the ant into a <strong>translating reverse P104 highway</strong> with opposite drift $-v = (+2, +2)$, retracing its path back toward the historical cloud $H_E$:</p>
      <ul>
        <li><strong>Affine Hit Normal Form:</strong> For depth $15+n$, the ant executes $n$ forward cycles and $n$ reverse cycles, striking $H_E$ at fixed lattice coordinate <strong>$(20, -22)$</strong> at exact step $t_{\\text{hit}}(n) = t_{\\text{hit}}(0) + 208n$.</li>
        <li><strong>Post-Hit Transient & Forward Highway:</strong> The collision triggers a 7,994-step chaotic transient that consumes part of $H_E$ and resolves into a permanent forward P104 highway.</li>
        <li><strong>XOR Archive Induction:</strong> Certified ray guards establish that accumulated forward/reverse wake layers miss the 7,994-step trace and terminal corridor for all $d \\ge 15$. Depths 1–14 are verified by explicit certificates.</li>
      </ul>
    `,
  },
  overview: {
    badge: "Stage 06 · Global Map",
    title: "Universal Theorem Assembly & Complete State Space Partition",
    leanSig: "theorem OneBlack.universal_one_black : ∀ s, ExactlyOneBlack s → ReachesP104 s",
    mechanismHtml: `
      <p><strong>Target scope:</strong> The entire discrete plane $\\mathbb{Z}^2$, covering every possible single-black-cell initial configuration for any ant position and heading.</p>
      <p><strong>Proof mechanism:</strong> Grid translation and quarter-turn rotation commute with Langton's ant dynamics, reducing all possible single-black-cell configurations to a canonical pose (ant at origin, heading north). The proof constructs an exhaustive and mutually disjoint partition of the discrete plane:</p>
      $$\\mathbb{Z}^2 = \\text{Prefix (1,376)} \\cup \\text{Immune/Untouched} \\cup \\text{Active Support (27)} \\cup \\text{21 Ordinary Channels} \\cup \\text{1 Exceptional Channel}$$
      <p>Each branch is formally proven to enter the P104 highway. The complete proof is closed in <strong>Lean 4</strong> with <strong>zero unverified axioms</strong> and <strong>zero runtime search</strong>, rigorously establishing the universal one-black theorem.</p>
    `,
  }
};

function renderMathIfAvailable() {
  if (typeof renderMathInElement === "function" && elements.guideContainer) {
    renderMathInElement(elements.guideContainer, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
      ],
      throwOnError: false,
    });
  }
}

function updateStageGuide(stageKey) {
  const content = STAGE_GUIDE_CONTENT[stageKey];
  if (!content) return;
  if (elements.guideBadge) elements.guideBadge.textContent = content.badge;
  if (elements.guideTitle) elements.guideTitle.textContent = content.title;
  if (elements.guideLeanCode) elements.guideLeanCode.textContent = content.leanSig;
  if (elements.guideMechanism) elements.guideMechanism.innerHTML = content.mechanismHtml;
  renderMathIfAvailable();
}

window.addEventListener("load", renderMathIfAvailable);

elements.reset.addEventListener("click", returnToDisplay);

elements.stageButtons.forEach((button) => button.addEventListener("click", () => {
  if (!proof) return;
  proofStage = button.dataset.proofStage;
  elements.stageButtons.forEach((candidate) => {
    if (candidate === button) candidate.setAttribute("aria-current", "page");
    else candidate.removeAttribute("aria-current");
  });
  updateStageGuide(proofStage);
  returnToDisplay();
}));

function validateProofMap(data) {
  const blank = data?.blank;
  if (
    data?.schema !== 15
    || !Number.isInteger(blank?.entryStep)
    || !Number.isInteger(blank?.period)
    || !Array.isArray(blank?.drift)
    || blank.drift.length !== 2
    || !Array.isArray(blank?.entryPosition)
    || blank.entryPosition.length !== 2
    || !Array.isArray(blank?.tailFrontier)
    || blank.tailFrontier.length !== 22
    || !Number.isInteger(blank?.startHeading)
    || !Array.isArray(blank?.blackRelative)
    || !Array.isArray(blank?.supportRelative)
    || !Array.isArray(data?.prefixCases)
    || data.prefixCases.length !== 1376
    || data.prefixCases.some((row) => !Array.isArray(row) || row.length !== 8)
    || data?.scattering?.cyclesBeforeHit !== 23
    || !Array.isArray(data?.scattering?.lanes)
    || data.scattering.lanes.length !== 22
    || data.scattering.lanes.some(
      (row) => !Array.isArray(row) || row.length !== 5 || ![0, 1, 2, 3].includes(row[4]),
    )
    || !Array.isArray(data.scattering.laneFormulas)
    || data.scattering.laneFormulas.length !== 22
    || !Array.isArray(data.scattering.activeCases)
    || data.scattering.activeCases.length !== 27
    || !Array.isArray(data?.finiteHistory?.entryBlackRelative)
    || data.finiteHistory.entryBlackRelative.length !== 715
    || !Array.isArray(data?.finiteHistory?.historicalWakeRelative)
    || data.finiteHistory.historicalWakeRelative.length !== 702
    || !Array.isArray(data?.finiteHistory?.ordinaryCases)
    || data.finiteHistory.ordinaryCases.length !== 186
    || data.finiteHistory.ordinaryCases.some(
      (row) => !Array.isArray(row) || row.length !== 7 || ![0, 1, 2, 3].includes(row[5]),
    )
    || !Array.isArray(data.finiteHistory.activeCases)
    || data.finiteHistory.activeCases.length !== 27
    || !Array.isArray(data.finiteHistory.historyRelevantRelative)
    || !Array.isArray(data?.reverseHighway?.historicalHit)
    || data.reverseHighway.historicalHit.length !== 2
    || data.reverseHighway.twoWayBaseDepth !== 15
    || !Number.isInteger(data.reverseHighway.reverseStartStep)
    || !Number.isInteger(data.reverseHighway.historicalHitStep)
    || data.reverseHighway.reverseStartStep >= data.reverseHighway.historicalHitStep
    || !Array.isArray(data.reverseHighway.cases)
    || data.reverseHighway.cases.length !== 15
    || data.reverseHighway.cases.some(
      (row) => !Array.isArray(row) || row.length !== 7 || row[0] !== 72,
    )
  ) {
    throw new Error("Proof-map data version mismatch; refresh the page");
  }
}

fetch("./proof-map.json?v=15", { cache: "no-store" })
  .then((response) => {
    if (!response.ok) throw new Error("proof-map.json could not be loaded");
    return response.json();
  })
  .then((data) => {
    validateProofMap(data);
    proof = data;
    const prefix = computeBlankPrefix();
    prefixSet = prefix.read;
    prefixFirstRead = prefix.firstRead;
    prefixCaseMap = new Map(data.prefixCases.map((row) => {
      const [x, y, checkStep, witnessOffset, turns, boundaryX, boundaryY, blackCount] = row;
      return [
        `${x},${y}`,
        {
          boundaryStep: checkStep + witnessOffset,
          turns,
          boundaryPosition: [boundaryX, boundaryY],
          blackCount,
        },
      ];
    }));
    pristineCaseMap = new Map(data.scattering.lanes.map(([phase, x, y, boundaryStep, turns]) => [
      `${x},${y}`,
      { phase, boundaryStep, turns },
    ]));
    const stableTurnsByPhase = new Map(data.scattering.lanes.map(
      ([phase, , , , turns]) => [phase, turns],
    ));
    for (const [phase, frontierX, frontierY, terminalSteps] of data.scattering.laneFormulas) {
      const baseDepth = terminalSteps.length;
      for (let depth = 1; depth <= VISIBLE_STABLE_DEPTH; depth += 1) {
        const point = [
          frontierX + depth * data.blank.drift[0],
          frontierY + depth * data.blank.drift[1],
        ];
        const boundaryStep = depth <= baseDepth
          ? terminalSteps[depth - 1]
          : terminalSteps[baseDepth - 1]
            + (depth - baseDepth) * data.blank.period;
        pristineCaseMap.set(key(point), {
          phase, depth, boundaryStep, turns: stableTurnsByPhase.get(phase),
        });
      }
    }
    for (const [x, y, boundaryStep, turns] of data.scattering.activeCases) {
      pristineCaseMap.set(`${x},${y}`, { phase: undefined, boundaryStep, turns });
    }
    for (const point of data.blank.blackRelative) {
      pristineCaseMap.set(key(point), { phase: undefined, boundaryStep: 0, turns: 0 });
    }
    pristinePoints = data.scattering.lanes.map(([, x, y]) => [x, y]);
    pristinePointSet = new Set(pristinePoints.map(key));
    const scatteringSupport = [];
    const referenceEndCycle = data.scattering.cyclesBeforeHit
      + PRISTINE_REFERENCE_AFTER_HIT_CYCLES;
    for (let cycle = 0; cycle <= referenceEndCycle; cycle += 1) {
      for (const point of data.blank.supportRelative) {
        scatteringSupport.push(addCycle(point, data.blank.drift, cycle));
      }
    }
    pristineSupportSet = new Set(scatteringSupport.map(key));
    pristineReferencePoints = [...scatteringSupport, ...pristinePoints, [0, 0]];
    finiteHistoryCaseMap = new Map(data.finiteHistory.ordinaryCases.map(
      ([phase, x, y, depth, boundaryStep, turns, stable]) => [
        `${x},${y}`,
        { phase, depth, boundaryStep, turns, stable: stable === 1 },
      ],
    ));
    const ordinaryStableDepthByPhase = new Map(
      data.finiteHistory.ordinaryCases
        .filter((row) => row[6] === 1)
        .map((row) => [row[0], row[3]]),
    );
    for (const [phase, frontierX, frontierY, terminalSteps] of data.scattering.laneFormulas) {
      if (phase === 72) continue;
      const baseDepth = terminalSteps.length;
      const stableDepth = ordinaryStableDepthByPhase.get(phase);
      for (let depth = 1; depth <= VISIBLE_STABLE_DEPTH; depth += 1) {
        const point = [
          frontierX + depth * data.blank.drift[0],
          frontierY + depth * data.blank.drift[1],
        ];
        if (depth <= stableDepth) continue;
        finiteHistoryCaseMap.set(key(point), {
          phase,
          depth,
          boundaryStep: terminalSteps[baseDepth - 1]
            + (depth - baseDepth) * data.blank.period,
          turns: stableTurnsByPhase.get(phase),
          stable: true,
        });
      }
    }
    for (const [x, y, boundaryStep, turns] of data.finiteHistory.activeCases) {
      finiteHistoryCaseMap.set(`${x},${y}`, {
        phase: undefined, depth: 0, boundaryStep, turns, stable: false, kind: "active",
      });
    }
    finiteHistoryPoints = data.finiteHistory.ordinaryCases.map(([, x, y]) => [x, y]);
    finiteHistoryPointSet = new Set(finiteHistoryPoints.map(key));
    const finiteHistoryStableRows = data.finiteHistory.ordinaryCases
      .filter((row) => row[6] === 1);
    const finiteHistoryStableTail = [];
    finiteHistoryStableDepthMap = new Map();
    for (const [, x, y, stableDepth] of finiteHistoryStableRows) {
      const start = [x, y];
      for (let depth = stableDepth; depth <= VISIBLE_STABLE_DEPTH; depth += 1) {
        const point = addCycle(start, data.blank.drift, depth - stableDepth);
        finiteHistoryStableTail.push(point);
        finiteHistoryStableDepthMap.set(key(point), depth);
      }
    }
    finiteHistoryStableTailSet = new Set(finiteHistoryStableTail.map(key));
    finiteHistoryWakeSet = new Set([
      ...data.finiteHistory.historicalWakeRelative,
      ...data.blank.supportRelative,
    ].map(key));
    finiteHistoryReferencePoints = [
      ...data.finiteHistory.historicalWakeRelative,
      ...data.blank.supportRelative,
      ...finiteHistoryPoints,
      ...finiteHistoryStableTail,
      [0, 0],
    ];
    const reverseBaseRow = data.reverseHighway.cases.find((row) => row[6] === 1);
    reverseCaseMap = new Map(data.reverseHighway.cases.map(
      ([phase, x, y, depth, boundaryStep, turns, stable]) => [
        `${x},${y}`,
        { phase, depth, boundaryStep, turns, stable: stable === 1 },
      ],
    ));
    reversePoints = data.reverseHighway.cases.map(([, x, y]) => [x, y]);
    const reverseBasePoint = [reverseBaseRow[1], reverseBaseRow[2]];
    const reverseStableTail = [];
    reverseStableDepthMap = new Map();
    for (
      let depth = data.reverseHighway.twoWayBaseDepth;
      depth <= VISIBLE_STABLE_DEPTH;
      depth += 1
    ) {
      const point = addCycle(
        reverseBasePoint,
        data.blank.drift,
        depth - data.reverseHighway.twoWayBaseDepth,
      );
      if (depth <= VISIBLE_REVERSE_DEPTH) {
        reverseStableTail.push(point);
        reverseStableDepthMap.set(key(point), depth);
      }
      const depthOffset = depth - data.reverseHighway.twoWayBaseDepth;
      reverseCaseMap.set(key(point), {
        phase: 72,
        depth,
        boundaryStep: reverseBaseRow[4] + 2 * data.blank.period * depthOffset,
        turns: reverseBaseRow[5],
        stable: true,
        reverseStartStep: data.reverseHighway.reverseStartStep
          + data.blank.period * depthOffset,
        historicalHitStep: data.reverseHighway.historicalHitStep
          + 2 * data.blank.period * depthOffset,
      });
    }
    reverseStableTailSet = new Set(reverseStableTail.map(key));
    reversePointSet = new Set([...reversePoints, ...reverseStableTail].map(key));
    reverseReferenceSet = finiteHistoryWakeSet;
    reverseReferencePoints = [
      ...data.finiteHistory.historicalWakeRelative,
      ...data.blank.supportRelative,
      ...reversePoints,
      ...reverseStableTail,
      data.reverseHighway.historicalHit,
      [0, 0],
    ];
    prefixPoints = [...prefixSet].map((pointKey) => pointKey.split(",").map(Number));
    const [entryX, entryY] = data.blank.entryPosition;
    const globalPoint = ([x, y]) => [x + entryX, y + entryY];
    const globalFrontier = ([, x, y]) => globalPoint([x, y]);
    overviewPrefixSet = prefixSet;
    overviewScatteringSet = new Set(data.blank.supportRelative.map(
      (point) => key(globalPoint(point)),
    ));
    overviewOrdinarySet = new Set(data.finiteHistory.historyRelevantRelative.map(
      (point) => key(globalPoint(point)),
    ));
    const reverseFormula = data.scattering.laneFormulas.find((row) => row[0] === 72);
    overviewReverseRay = globalFrontier(reverseFormula);
    overviewScatteringRays = data.scattering.laneFormulas
      .filter((row) => row[0] !== 72)
      .map(globalFrontier);
    const overviewRayEndpoints = [...overviewScatteringRays, overviewReverseRay].map(
      (frontier) => addCycle(frontier, data.blank.drift, VISIBLE_STABLE_DEPTH),
    );
    overviewReferencePoints = [
      ...prefixPoints,
      ...overviewScatteringSet,
      ...overviewOrdinarySet,
      ...overviewRayEndpoints,
      [0, 0],
    ].map((point) => typeof point === "string" ? point.split(",").map(Number) : point);
    transform = makeTransform();
    visibleReferenceSet = buildVisibleReferenceSet();
    defaultTransform = transform;
    defaultVisibleReferenceSet = visibleReferenceSet;
    proofStage = "pristine";
    pristineTransform = makeTransform([], pristineReferencePoints);
    pristineVisibleReferenceSet = buildVisibleReferenceSet();
    proofStage = "finiteHistory";
    finiteHistoryTransform = makeTransform([], finiteHistoryReferencePoints);
    finiteHistoryVisibleReferenceSet = buildVisibleReferenceSet();
    proofStage = "reverseHighway";
    reverseTransform = makeTransform([], reverseReferencePoints);
    reverseVisibleReferenceSet = buildVisibleReferenceSet();
    proofStage = "overview";
    overviewTransform = makeTransform([], overviewReferencePoints);
    proofStage = "outside";
    transform = defaultTransform;
    visibleReferenceSet = defaultVisibleReferenceSet;
    updateStageGuide(proofStage);
    drawDisplay();
  })
  .catch((error) => {
    elements.readout.textContent = "The proof-map data could not be loaded";
    console.error(error);
  });
