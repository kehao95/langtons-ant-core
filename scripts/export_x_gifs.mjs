#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const playwrightModule = process.env.PLAYWRIGHT_MODULE ?? "playwright";
let chromium;

function getChromium() {
  chromium ??= require(playwrightModule).chromium;
  return chromium;
}

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(scriptDirectory, "..");
const proofMapPath = path.join(repositoryRoot, "docs/proof-map.json");
const outputDirectory = path.join(repositoryRoot, "media/x");
const scatteringDirectory = path.join(repositoryRoot, "preprint/figures/scattering");
const baseUrl = process.argv.find((argument) => argument.startsWith("http://") || argument.startsWith("https://"))
  ?? "http://127.0.0.1:4173";
const tempParent = process.env.X_GIF_TMP ?? os.tmpdir();
const fontPath = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf";
const captureFps = 5;
const webLimitBytes = 15 * 1024 * 1024;
const affineDepths = [15, 16, 20, 30];

const profiles = [
  { width: 720, fps: 5, colors: 96 },
  { width: 640, fps: 4, colors: 80 },
  { width: 600, fps: 4, colors: 64 },
  { width: 540, fps: 3, colors: 64 },
];

function run(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(`${command} failed:\n${result.stderr || result.stdout}`);
  }
  return result;
}

function escapeDrawText(text) {
  return text
    .replaceAll("\\", "\\\\")
    .replaceAll(":", "\\:")
    .replaceAll("'", "\\'");
}

function drawTextFilter(text, enable) {
  const fontSize = text.length > 48 ? 22 : text.length > 38 ? 24 : 28;
  const parts = [
    `drawtext=fontfile='${fontPath}'`,
    `text='${escapeDrawText(text)}'`,
    "fontcolor=0x17313a",
    `fontsize=${fontSize}`,
    "x=24",
    "y=18",
  ];
  if (enable) parts.push(`enable='${enable}'`);
  return parts.join(":");
}

function panelLabelFilter(text, enable) {
  const parts = [
    `drawtext=fontfile='${fontPath}'`,
    `text='${escapeDrawText(text)}'`,
    "fontcolor=0x17313a",
    "fontsize=30",
    "x=24",
    "y=20",
    "box=1",
    "boxcolor=0xfbfaf6dd",
    "boxborderw=10",
  ];
  if (enable) parts.push(`enable='${enable}'`);
  return parts.join(":");
}

async function encodeGif({ frameDirectory, outputPath, title, timedLabels = [] }) {
  for (const profile of profiles) {
    const filters = [
      `fps=${profile.fps}`,
      `scale=${profile.width}:-2:flags=lanczos`,
      "pad=iw:ih+64:0:64:color=0xfbfaf6",
    ];
    if (title) filters.push(drawTextFilter(title));
    for (const { text, firstFrame, lastFrame } of timedLabels) {
      const first = Math.floor(firstFrame * profile.fps / captureFps);
      const last = Math.ceil((lastFrame + 1) * profile.fps / captureFps) - 1;
      filters.push(drawTextFilter(text, `between(n,${first},${last})`));
    }
    const graph = [
      `[0:v]${filters.join(",")},split[paletteSource][gifSource]`,
      `[paletteSource]palettegen=max_colors=${profile.colors}:stats_mode=diff[palette]`,
      "[gifSource][palette]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle[out]",
    ].join(";");
    const candidatePath = `${outputPath}.candidate.gif`;
    run("ffmpeg", [
      "-hide_banner", "-loglevel", "error", "-y",
      "-framerate", String(captureFps),
      "-start_number", "0",
      "-i", path.join(frameDirectory, "frame-%04d.png"),
      "-filter_complex", graph,
      "-map", "[out]",
      "-loop", "0",
      candidatePath,
    ]);
    const { size } = await fs.stat(candidatePath);
    if (size <= webLimitBytes || profile === profiles.at(-1)) {
      await fs.rename(candidatePath, outputPath);
      return { ...profile, size };
    }
    await fs.rm(candidatePath);
  }
  throw new Error(`No encoding profile produced ${outputPath}`);
}

function applyCaptureTheme(source) {
  const replacements = new Map([
    ['background: "#102630"', 'background: "#fbfaf6"'],
    ['blue: "rgba(99, 184, 237, .68)"', 'blue: "rgba(62, 137, 181, .78)"'],
    ['inactive: "rgba(45, 104, 130, .22)"', 'inactive: "rgba(221, 228, 226, .62)"'],
    ['gray: "rgba(190, 201, 203, .92)"', 'gray: "rgba(137, 151, 154, .82)"'],
    ['disturbed: "rgba(231, 211, 174, .92)"', 'disturbed: "rgba(211, 174, 108, .88)"'],
    ['highway: "rgba(112, 239, 167, .96)"', 'highway: "rgba(49, 158, 94, .95)"'],
    ['highwayTrail: "rgba(139, 255, 188, .96)"', 'highwayTrail: "rgba(55, 166, 99, .92)"'],
    ['grid: "rgba(10, 34, 44, .42)"', 'grid: "rgba(86, 105, 110, .20)"'],
    ['border: "rgba(229, 241, 243, .38)"', 'border: "rgba(56, 77, 83, .48)"'],
    ['hover: "#fff4c7"', 'hover: "#374b52"'],
    ['strokeCell(selectedPoint, "#f2f6f5")', 'strokeCell(selectedPoint, "#25373d")'],
    ['"rgba(244, 249, 248, .72)"', '"rgba(42, 63, 68, .62)"'],
    ["const REVERSE_APPROACH_MS = 8000", "const REVERSE_APPROACH_MS = 5000"],
    ["const REVERSE_HIGHWAY_MS = 6000", "const REVERSE_HIGHWAY_MS = 4500"],
    ["const REVERSE_POST_HIT_MS = 7000", "const REVERSE_POST_HIT_MS = 5000"],
    ["const HIGHWAY_ANIMATION_MS = 10500", "const HIGHWAY_ANIMATION_MS = 6000"],
    [": Math.max(8000, Math.min(18000, boundaryStep / 5));",
      ": Math.max(6000, Math.min(10000, boundaryStep / 10));"],
  ]);
  let themed = source;
  for (const [before, after] of replacements) {
    if (!themed.includes(before)) {
      throw new Error(`capture-theme source marker not found: ${before}`);
    }
    themed = themed.replace(before, after);
  }
  return `${themed}\nwindow.__xCapture = {
    start(point) { startEvolution(point, true); },
    reset() { returnToDisplay(); },
    finish() {
      cancelAnimationFrame(animationFrame);
      const timing = evolutionTiming();
      advanceSimulation(timing.terminalStep);
      drawEvolution();
      return timing;
    },
    manual(initialBlack, marker) {
      cancelAnimationFrame(animationFrame);
      clearTimeout(hoverTimer);
      clearTimeout(fastTimer);
      evolutionGeneration += 1;
      proofStage = "outside";
      COLORS.blue = "rgba(221, 228, 226, .18)";
      mode = "evolution";
      selectedPoint = [...marker];
      selectedCase = undefined;
      hoveredPoint = undefined;
      transform = defaultTransform;
      visibleReferenceSet = defaultVisibleReferenceSet;
      simulation = createSimulation(initialBlack);
      highwayVisited = new Set();
      fastVisited = new Set();
      fastHighwayVisited = new Set();
      reverseVisited = new Set();
      fastReverseVisited = new Set();
      trail = [];
      highwayTrail = [];
      drawEvolution();
    },
    advance(toStep) {
      while (simulation.step < toStep) {
        fastVisited.add(key([simulation.x, simulation.y]));
        advanceSimulation(simulation.step + 1);
      }
      drawEvolution();
    },
    overview(colors) {
      cancelAnimationFrame(animationFrame);
      clearTimeout(hoverTimer);
      clearTimeout(fastTimer);
      evolutionGeneration += 1;
      proofStage = "overview";
      mode = "display";
      COLORS.overview = colors;
      selectedPoint = undefined;
      hoveredPoint = undefined;
      simulation = undefined;
      transform = overviewTransform;
      visibleReferenceSet = new Set();
      drawDisplay();
    },
    affineBounds(toStep) {
      const state = createSelectedSimulation();
      const points = [];
      while (state.step < toStep) {
        points.push([state.x, state.y]);
        advanceOne(state);
      }
      return points.reduce((bounds, [x, y]) => ({
        minX: Math.min(bounds.minX, x), maxX: Math.max(bounds.maxX, x),
        minY: Math.min(bounds.minY, y), maxY: Math.max(bounds.maxY, y),
      }), { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity });
    },
    affinePause(bounds) {
      cancelAnimationFrame(animationFrame);
      clearTimeout(fastTimer);
      fastVisited = new Set();
      fastHighwayVisited = new Set();
      fastReverseVisited = new Set();
      transform = makeTransform([], [
        ...reverseReferencePoints,
        [bounds.minX, bounds.minY], [bounds.minX, bounds.maxY],
        [bounds.maxX, bounds.minY], [bounds.maxX, bounds.maxY],
      ]);
      visibleReferenceSet = reverseVisibleReferenceSet;
      drawEvolution();
    },
    affineAdvance(toStep) {
      advanceSimulation(toStep);
      drawEvolution();
    },
    status() {
      return {
        mode,
        stage: proofStage,
        readout: elements.readout.textContent,
        caption: elements.mapCaption.textContent,
      };
    },
  };\n`;
}

async function createCapturePage(context) {
  const page = await context.newPage();
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error));
  await page.route("**/app.js*", async (route) => {
    const response = await route.fetch();
    const source = await response.text();
    await route.fulfill({
      response,
      body: applyCaptureTheme(source),
      contentType: "text/javascript",
    });
  });
  await page.goto(baseUrl, { waitUntil: "networkidle" });
  return { page, canvas: page.locator("#proof-map"), pageErrors };
}

async function copyHeldFrame(source, frameDirectory, start, count) {
  for (let index = 0; index < count; index += 1) {
    await fs.copyFile(
      source,
      path.join(frameDirectory, `frame-${String(start + index).padStart(4, "0")}.png`),
    );
  }
  return start + count;
}

async function combineSequences({
  inputs, labels = [], timedPanelLabels = [], outputDirectory: destination, layout,
}) {
  await fs.mkdir(destination, { recursive: true });
  const frameCounts = await Promise.all(inputs.map(async (input) => (
    (await fs.readdir(input)).filter((name) => name.endsWith(".png")).length
  )));
  const args = ["-hide_banner", "-loglevel", "error", "-y"];
  for (const input of inputs) {
    args.push("-framerate", String(captureFps), "-start_number", "0", "-i", path.join(input, "frame-%04d.png"));
  }
  const panelFilters = inputs.map((_, index) => {
    const filters = [];
    if (labels[index]) filters.push(panelLabelFilter(labels[index]));
    for (const { text, firstFrame, lastFrame } of timedPanelLabels[index] ?? []) {
      filters.push(panelLabelFilter(text, `between(n,${firstFrame},${lastFrame})`));
    }
    return `[${index}:v]${filters.length > 0 ? filters.join(",") : "null"}[p${index}]`;
  });
  let stack;
  if (layout === "side") {
    stack = `${inputs.map((_, index) => `[p${index}]`).join("")}hstack=inputs=${inputs.length}[out]`;
  } else {
    const positions = ["0_0", "w0_0", "0_h0", "w0_h0"].slice(0, inputs.length).join("|");
    stack = `${inputs.map((_, index) => `[p${index}]`).join("")}xstack=inputs=${inputs.length}:layout=${positions}:fill=0xfbfaf6[out]`;
  }
  args.push(
    "-filter_complex", [...panelFilters, stack].join(";"),
    "-map", "[out]",
    "-frames:v", String(Math.min(...frameCounts)),
    path.join(destination, "frame-%04d.png"),
  );
  run("ffmpeg", args);
}

async function captureManualEvolution({ page, canvas, frameDirectory, initialBlack, marker, steps }) {
  await page.evaluate(({ black, selected }) => window.__xCapture.manual(black, selected), {
    black: initialBlack,
    selected: marker,
  });
  for (let index = 0; index < steps.length; index += 1) {
    await page.evaluate((step) => window.__xCapture.advance(step), steps[index]);
    await canvas.screenshot({
      path: path.join(frameDirectory, `frame-${String(index).padStart(4, "0")}.png`),
    });
  }
}

function piecewiseSteps(frameCount, segments) {
  const result = [];
  for (let frame = 0; frame < frameCount; frame += 1) {
    const progress = frame / Math.max(1, frameCount - 1);
    const segment = segments.find(({ until }) => progress <= until) ?? segments.at(-1);
    const previous = segments[segments.indexOf(segment) - 1];
    const fromProgress = previous?.until ?? 0;
    const local = Math.max(0, Math.min(1, (progress - fromProgress) / (segment.until - fromProgress)));
    result.push(Math.floor(segment.from + (segment.to - segment.from) * local));
  }
  return result;
}

async function captureTerminal(page, canvas, stage, point, outputPath) {
  await page.locator(`[data-proof-stage="${stage}"]`).click();
  await page.evaluate((selected) => window.__xCapture.start(selected), point);
  await page.waitForFunction(() => (
    window.__xCapture.status().caption.includes("complete disturbed footprint")
  ));
  await page.evaluate(() => window.__xCapture.finish());
  await canvas.screenshot({ path: outputPath });
  await page.evaluate(() => window.__xCapture.reset());
}

async function captureEvolution({ page, canvas, frameDirectory, stage, caption, point, seconds }) {
  await page.locator(`[data-proof-stage="${stage}"]`).click();
  await page.waitForFunction(
    (expected) => document.querySelector("#map-caption")?.textContent?.includes(expected),
    caption,
  );
  await page.evaluate((selected) => window.__xCapture.start(selected), point);
  await page.waitForFunction(() => (
    window.__xCapture.status().caption.includes("complete disturbed footprint")
  ));
  const frameCount = Math.ceil(seconds * captureFps);
  const startedAt = Date.now();
  for (let index = 0; index < frameCount; index += 1) {
    const target = startedAt + index * 1000 / captureFps;
    const wait = target - Date.now();
    if (wait > 0) await page.waitForTimeout(wait);
    await canvas.screenshot({
      path: path.join(frameDirectory, `frame-${String(index).padStart(4, "0")}.png`),
    });
  }
}

async function computeAffineBounds(page, point, toStep) {
  await page.locator('[data-proof-stage="reverseHighway"]').click();
  await page.waitForFunction(() => (
    document.querySelector("#map-caption")?.textContent?.includes("depths 1–14")
  ));
  await page.evaluate((selected) => window.__xCapture.start(selected), point);
  await page.waitForFunction(() => (
    window.__xCapture.status().caption.includes("complete disturbed footprint")
  ));
  return page.evaluate((target) => window.__xCapture.affineBounds(target), toStep);
}

async function captureAffineClock({ page, canvas, frameDirectory, point, bounds, steps }) {
  await page.locator('[data-proof-stage="reverseHighway"]').click();
  await page.waitForFunction(() => (
    document.querySelector("#map-caption")?.textContent?.includes("depths 1–14")
  ));
  await page.evaluate((selected) => window.__xCapture.start(selected), point);
  await page.waitForFunction(() => (
    window.__xCapture.status().caption.includes("complete disturbed footprint")
  ));
  await page.evaluate((frameBounds) => window.__xCapture.affinePause(frameBounds), bounds);
  for (let index = 0; index < steps.length; index += 1) {
    await page.evaluate((step) => window.__xCapture.affineAdvance(step), steps[index]);
    await canvas.screenshot({
      path: path.join(frameDirectory, `frame-${String(index).padStart(4, "0")}.png`),
    });
  }
}

async function prepareScatteringGroupFrames(data, frameDirectories) {
  const groups = [
    { turns: 0, label: "straight", sourceName: "straight" },
    { turns: 1, label: "turn right", sourceName: "right" },
    { turns: 2, label: "reverse", sourceName: "reverse" },
    { turns: 3, label: "turn left", sourceName: "left" },
  ].map((group) => ({
    ...group,
    lanes: data.scattering.lanes
      .filter((lane) => lane[4] === group.turns)
      .sort((left, right) => left[0] - right[0]),
  }));
  const holdFrames = 4;
  const slots = Math.max(...groups.map((group) => group.lanes.length));
  const timedPanelLabels = [];
  for (let groupIndex = 0; groupIndex < groups.length; groupIndex += 1) {
    const group = groups[groupIndex];
    const labels = [];
    let frame = 0;
    for (let slot = 0; slot < slots; slot += 1) {
      const [phase] = group.lanes[slot % group.lanes.length];
      const source = path.join(
        scatteringDirectory,
        `phase-${String(phase).padStart(2, "0")}-${group.sourceName}.png`,
      );
      const firstFrame = frame;
      frame = await copyHeldFrame(source, frameDirectories[groupIndex], frame, holdFrames);
      labels.push({
        text: `${group.label}  |  phase P${phase}`,
        firstFrame,
        lastFrame: frame - 1,
      });
    }
    timedPanelLabels.push(labels);
  }
  return { groups, timedPanelLabels };
}

async function exportScatteringOnly(data) {
  await fs.mkdir(outputDirectory, { recursive: true });
  await fs.mkdir(tempParent, { recursive: true });
  const tempRoot = await fs.mkdtemp(path.join(tempParent, "langtons-ant-scattering-"));
  const frameDirectories = ["straight", "right", "reverse", "left"].map(
    (name) => path.join(tempRoot, name),
  );
  const combinedFrames = path.join(tempRoot, "combined");
  await Promise.all(frameDirectories.map((directory) => fs.mkdir(directory)));
  try {
    const { timedPanelLabels } = await prepareScatteringGroupFrames(data, frameDirectories);
    await combineSequences({
      inputs: frameDirectories,
      timedPanelLabels,
      outputDirectory: combinedFrames,
      layout: "grid",
    });
    const output = await encodeGif({
      frameDirectory: combinedFrames,
      outputPath: path.join(outputDirectory, "scattering-all-22.gif"),
      title: "22 pristine scattering phases  |  grouped by outcome",
    });
    console.log(`scattering-all-22.gif: ${output.size} bytes, ${output.width}px, ${output.fps} fps, ${output.colors} colors`);
  } finally {
    await fs.rm(tempRoot, { recursive: true, force: true });
  }
}

function affinePoint(baseRow, depth) {
  const offset = depth - baseRow[3];
  return [baseRow[1] - 2 * offset, baseRow[2] - 2 * offset];
}

function affineLabels(data) {
  const baseDepth = data.reverseHighway.twoWayBaseDepth;
  return affineDepths.map((depth) => {
    const hitStep = data.reverseHighway.historicalHitStep
      + 2 * data.blank.period * (depth - baseDepth);
    return `depth ${depth}  |  hit ${hitStep.toLocaleString("en-US")}`;
  });
}

function affineClockSteps(data) {
  const base = data.reverseHighway.cases.find((row) => row[6] === 1);
  const deepest = affineDepths.at(-1);
  const terminalStep = base[4]
    + 2 * data.blank.period * (deepest - base[3])
    + data.blank.period * 20;
  const startStep = 50000;
  const frameCount = 110;
  return Array.from({ length: frameCount }, (_, index) => (
    startStep + Math.floor((terminalStep - startStep) * index / (frameCount - 1))
  ));
}

function mergeBounds(boundsList) {
  return boundsList.reduce((merged, bounds) => ({
    minX: Math.min(merged.minX, bounds.minX),
    maxX: Math.max(merged.maxX, bounds.maxX),
    minY: Math.min(merged.minY, bounds.minY),
    maxY: Math.max(merged.maxY, bounds.maxY),
  }), { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity });
}

async function exportAffineOnly(data) {
  const reverseRow = data.reverseHighway.cases.find((row) => row[6] === 1);
  if (!reverseRow) throw new Error("The reverse-highway induction base is missing");
  await fs.mkdir(outputDirectory, { recursive: true });
  await fs.mkdir(tempParent, { recursive: true });
  const tempRoot = await fs.mkdtemp(path.join(tempParent, "langtons-ant-affine-"));
  const frameDirectories = affineDepths.map((depth) => path.join(tempRoot, `depth-${depth}`));
  const combinedFrames = path.join(tempRoot, "combined");
  await Promise.all(frameDirectories.map((directory) => fs.mkdir(directory)));
  let browser;
  try {
    browser = await getChromium().launch({ headless: true, args: ["--no-sandbox"] });
    const context = await browser.newContext({
      viewport: { width: 1440, height: 1100 },
      deviceScaleFactor: 1,
      reducedMotion: "no-preference",
    });
    const { page, canvas, pageErrors } = await createCapturePage(context);
    const framePoints = affineDepths.map((depth) => affinePoint(reverseRow, depth));
    const steps = affineClockSteps(data);
    const boundsList = [];
    for (const point of framePoints) {
      boundsList.push(await computeAffineBounds(page, point, steps.at(-1)));
    }
    const bounds = mergeBounds(boundsList);
    for (let index = 0; index < affineDepths.length; index += 1) {
      await captureAffineClock({
        page,
        canvas,
        frameDirectory: frameDirectories[index],
        point: framePoints[index],
        bounds,
        steps,
      });
    }
    if (pageErrors.length > 0) throw pageErrors[0];
    await combineSequences({
      inputs: frameDirectories,
      labels: affineLabels(data),
      outputDirectory: combinedFrames,
      layout: "grid",
    });
    const output = await encodeGif({
      frameDirectory: combinedFrames,
      outputPath: path.join(outputDirectory, "affine-hit-law-depth-15-16-20-30.gif"),
      title: "shared clock from t = 50,000  |  P104 entry aligned",
    });
    console.log(`affine-hit-law-depth-15-16-20-30.gif: ${output.size} bytes, ${output.width}px, ${output.fps} fps, ${output.colors} colors`);
  } finally {
    await browser?.close();
    await fs.rm(tempRoot, { recursive: true, force: true });
  }
}

async function main() {
  run("ffmpeg", ["-version"]);
  await fs.access(fontPath);
  const data = JSON.parse(await fs.readFile(proofMapPath, "utf8"));
  if (process.argv.includes("--scattering-only")) {
    await exportScatteringOnly(data);
    return;
  }
  if (process.argv.includes("--affine-only")) {
    await exportAffineOnly(data);
    return;
  }
  const prefixRow = data.prefixCases.find(([x, y]) => x === 7 && y === 7);
  const reverseRow = data.reverseHighway.cases.find((row) => row[6] === 1);
  const p61Rows = data.finiteHistory.ordinaryCases
    .filter(([phase]) => phase === 61)
    .sort((left, right) => left[3] - right[3]);
  if (!prefixRow || !reverseRow || p61Rows.length !== 15) {
    throw new Error("Required certified GIF cases are missing");
  }

  await fs.mkdir(outputDirectory, { recursive: true });
  await fs.mkdir(tempParent, { recursive: true });
  const tempRoot = await fs.mkdtemp(path.join(tempParent, "langtons-ant-x-gifs-"));
  const prefixFrames = path.join(tempRoot, "prefix");
  const reverseFrames = path.join(tempRoot, "reverse");
  const scatteringGroupFrames = ["straight", "right", "reverse", "left"].map(
    (name) => path.join(tempRoot, `scattering-${name}`),
  );
  const scatteringCombinedFrames = path.join(tempRoot, "scattering-combined");
  const blankFrames = path.join(tempRoot, "blank");
  const couplingBlankFrames = path.join(tempRoot, "coupling-blank");
  const couplingBlackFrames = path.join(tempRoot, "coupling-black");
  const couplingFrames = path.join(tempRoot, "coupling");
  const p61Frames = path.join(tempRoot, "p61");
  const p61BoundaryFrames = path.join(tempRoot, "p61-boundary");
  const overviewFrames = path.join(tempRoot, "overview");
  const affineFrames = affineDepths.map((depth) => path.join(tempRoot, `affine-${depth}`));
  const affineCombinedFrames = path.join(tempRoot, "affine-combined");
  const stillDirectory = path.join(tempRoot, "stills");
  await Promise.all([
    fs.mkdir(prefixFrames),
    fs.mkdir(reverseFrames),
    ...scatteringGroupFrames.map((directory) => fs.mkdir(directory)),
    fs.mkdir(blankFrames),
    fs.mkdir(couplingBlankFrames),
    fs.mkdir(couplingBlackFrames),
    fs.mkdir(p61Frames),
    fs.mkdir(p61BoundaryFrames),
    fs.mkdir(overviewFrames),
    fs.mkdir(stillDirectory),
    ...affineFrames.map((directory) => fs.mkdir(directory)),
  ]);

  const browser = await getChromium().launch({ headless: true, args: ["--no-sandbox"] });
  const p61Stills = new Map();
  try {
    const context = await browser.newContext({
      viewport: { width: 1440, height: 1100 },
      deviceScaleFactor: 1,
      reducedMotion: "no-preference",
    });
    const primary = await createCapturePage(context);
    const { page, canvas, pageErrors } = primary;

    await captureEvolution({
      page,
      canvas,
      frameDirectory: prefixFrames,
      stage: "prefix",
      caption: "1,376 blue cells",
      point: [7, 7],
      seconds: 17.5,
    });
    await captureEvolution({
      page,
      canvas,
      frameDirectory: reverseFrames,
      stage: "reverseHighway",
      caption: "depths 1–14",
      point: [reverseRow[1], reverseRow[2]],
      seconds: 22,
    });

    const blankSteps = piecewiseSteps(70, [
      { until: 0.68, from: 0, to: data.blank.entryStep },
      { until: 1, from: data.blank.entryStep, to: data.blank.entryStep + 20 * data.blank.period },
    ]);
    await captureManualEvolution({
      page,
      canvas,
      frameDirectory: blankFrames,
      initialBlack: [],
      marker: [10000, 10000],
      steps: blankSteps,
    });

    const contactStep = 9971;
    const couplingSteps = piecewiseSteps(75, [
      { until: 0.64, from: 0, to: contactStep },
      { until: 0.76, from: contactStep, to: contactStep },
      { until: 1, from: contactStep, to: 11600 },
    ]);
    await captureManualEvolution({
      page,
      canvas,
      frameDirectory: couplingBlankFrames,
      initialBlack: [],
      marker: [10000, 10000],
      steps: couplingSteps,
    });
    await captureManualEvolution({
      page,
      canvas,
      frameDirectory: couplingBlackFrames,
      initialBlack: [[-16, 9]],
      marker: [-16, 9],
      steps: couplingSteps,
    });

    const p61Depths = [1, 5, 10, 14, 15, 16];
    for (const depth of p61Depths) {
      const row = p61Rows.find((candidate) => candidate[3] === depth);
      const point = row
        ? [row[1], row[2]]
        : [p61Rows.at(-1)[1] - 2 * (depth - 15), p61Rows.at(-1)[2] - 2 * (depth - 15)];
      const still = path.join(stillDirectory, `p61-depth-${depth}.png`);
      await captureTerminal(page, canvas, "finiteHistory", point, still);
      p61Stills.set(depth, still);
    }

    const overviewPalette = [
      "rgba(83,116,130,.55)",
      "rgba(62,137,181,.82)",
      "rgba(49,163,106,.88)",
      "rgba(214,138,56,.88)",
      "rgba(143,112,213,.90)",
    ];
    for (let index = 0; index < 24; index += 1) {
      const firstFade = Math.max(0, Math.min(1, (index - 4) / 5));
      const secondFade = Math.max(0, Math.min(1, (index - 10) / 5));
      const colors = [...overviewPalette];
      colors[0] = `rgba(221,228,226,${0.55 * (1 - firstFade) + 0.04 * firstFade})`;
      colors[1] = `rgba(62,137,181,${0.82 * (1 - secondFade) + 0.08 * secondFade})`;
      await page.evaluate((palette) => window.__xCapture.overview(palette), colors);
      await canvas.screenshot({
        path: path.join(overviewFrames, `frame-${String(index).padStart(4, "0")}.png`),
      });
    }

    const affineFramePoints = affineDepths.map((depth) => affinePoint(reverseRow, depth));
    const affineSteps = affineClockSteps(data);
    const affineBoundsList = [];
    for (const point of affineFramePoints) {
      affineBoundsList.push(await computeAffineBounds(page, point, affineSteps.at(-1)));
    }
    const affineBounds = mergeBounds(affineBoundsList);
    for (let index = 0; index < affineFrames.length; index += 1) {
      await captureAffineClock({
        page,
        canvas,
        frameDirectory: affineFrames[index],
        point: affineFramePoints[index],
        bounds: affineBounds,
        steps: affineSteps,
      });
      if (index === affineFrames.length - 1 && pageErrors.length > 0) throw pageErrors[0];
    }
    if (pageErrors.length > 0) throw pageErrors[0];
  } finally {
    await browser.close();
  }

  const { timedPanelLabels: scatteringPanelLabels } = await prepareScatteringGroupFrames(
    data, scatteringGroupFrames,
  );

  await combineSequences({
    inputs: scatteringGroupFrames,
    timedPanelLabels: scatteringPanelLabels,
    outputDirectory: scatteringCombinedFrames,
    layout: "grid",
  });

  await combineSequences({
    inputs: [couplingBlankFrames, couplingBlackFrames],
    labels: ["blank plane", "one black  q = (-16, 9)"],
    outputDirectory: couplingFrames,
    layout: "side",
  });
  await combineSequences({
    inputs: affineFrames,
    labels: affineLabels(data),
    outputDirectory: affineCombinedFrames,
    layout: "grid",
  });

  const p61Labels = [];
  let p61Frame = 0;
  for (const depth of [1, 5, 10, 14, 15, 16]) {
    const firstFrame = p61Frame;
    p61Frame = await copyHeldFrame(p61Stills.get(depth), p61Frames, p61Frame, 5);
    p61Labels.push({
      text: `P61  |  depth ${depth}  |  ${depth < 15 ? "direct finite replay" : "stable induction"}`,
      firstFrame,
      lastFrame: p61Frame - 1,
    });
  }

  const boundaryLabels = [];
  let boundaryFrame = 0;
  for (let cycle = 0; cycle < 4; cycle += 1) {
    for (const depth of [14, 15]) {
      const firstFrame = boundaryFrame;
      boundaryFrame = await copyHeldFrame(
        p61Stills.get(depth), p61BoundaryFrames, boundaryFrame, 7,
      );
      boundaryLabels.push({
        text: depth === 14
          ? "P61 depth 14  |  Stage 04: history intersects"
          : "P61 depth 15  |  Stage 03: separated stable lane",
        firstFrame,
        lastFrame: boundaryFrame - 1,
      });
    }
  }
  const outputs = [];
  outputs.push(await encodeGif({
    frameDirectory: prefixFrames,
    outputPath: path.join(outputDirectory, "one-black-q-7-7.gif"),
    title: "q = (7, 7)  |  106,258-step prefix transient",
  }));
  outputs.push(await encodeGif({
    frameDirectory: scatteringCombinedFrames,
    outputPath: path.join(outputDirectory, "scattering-all-22.gif"),
    title: "22 pristine scattering phases  |  grouped by outcome",
  }));
  outputs.push(await encodeGif({
    frameDirectory: reverseFrames,
    outputPath: path.join(outputDirectory, "reverse-highway-phase-72.gif"),
    title: "P72  |  reverse highway  |  physical depth 15",
  }));
  outputs.push(await encodeGif({
    frameDirectory: blankFrames,
    outputPath: path.join(outputDirectory, "blank-plane-to-p104.gif"),
    title: "blank plane  |  P104 at t = 9,977  |  v = (-2, -2)",
  }));
  outputs.push(await encodeGif({
    frameDirectory: couplingFrames,
    outputPath: path.join(outputDirectory, "first-contact-coupling.gif"),
    title: "same path until first read  |  t = 9,971",
  }));
  outputs.push(await encodeGif({
    frameDirectory: p61Frames,
    outputPath: path.join(outputDirectory, "ordinary-p61-depth-induction.gif"),
    timedLabels: p61Labels,
  }));
  outputs.push(await encodeGif({
    frameDirectory: p61BoundaryFrames,
    outputPath: path.join(outputDirectory, "stage-03-04-boundary-p61.gif"),
    timedLabels: boundaryLabels,
  }));
  outputs.push(await encodeGif({
    frameDirectory: affineCombinedFrames,
    outputPath: path.join(outputDirectory, "affine-hit-law-depth-15-16-20-30.gif"),
    title: "shared clock from t = 50,000  |  P104 entry aligned",
  }));
  outputs.push(await encodeGif({
    frameDirectory: overviewFrames,
    outputPath: path.join(outputDirectory, "global-map-to-22-rays.gif"),
    title: "global partition to 22 rays  |  21 + 1",
  }));

  await fs.rm(tempRoot, { recursive: true, force: true });
  const names = [
    "one-black-q-7-7.gif",
    "scattering-all-22.gif",
    "reverse-highway-phase-72.gif",
    "blank-plane-to-p104.gif",
    "first-contact-coupling.gif",
    "ordinary-p61-depth-induction.gif",
    "stage-03-04-boundary-p61.gif",
    "affine-hit-law-depth-15-16-20-30.gif",
    "global-map-to-22-rays.gif",
  ];
  for (let index = 0; index < outputs.length; index += 1) {
    const output = outputs[index];
    console.log(`${names[index]}: ${output.size} bytes, ${output.width}px, ${output.fps} fps, ${output.colors} colors`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
