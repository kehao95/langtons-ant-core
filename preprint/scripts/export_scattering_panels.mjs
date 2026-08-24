#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const playwrightModule = process.env.PLAYWRIGHT_MODULE ?? "playwright";
const { chromium } = require(playwrightModule);

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(scriptDirectory, "../..");
const proofMapPath = path.join(repositoryRoot, "docs/proof-map.json");
const outputDirectory = path.join(repositoryRoot, "preprint/figures/scattering");
const exceptionalDirectory = path.join(repositoryRoot, "preprint/figures/exceptional");
const stageDirectory = path.join(repositoryRoot, "preprint/figures/stages");
const baseUrl = process.argv[2] ?? "http://127.0.0.1:4173";

const PRISTINE_REFERENCE_AFTER_HIT_CYCLES = 15;
const VIEW_PADDING_CELLS = 3;
const CANVAS_WIDTH = 1100;
const CANVAS_HEIGHT = 760;
const CANVAS_MARGIN = 28;
const VISIBLE_REVERSE_DEPTH = 20;

function addCycle([x, y], [dx, dy], cycle) {
  return [x + dx * cycle, y + dy * cycle];
}

function transformFromPoints(points) {
  const xs = points.map(([x]) => x);
  const ys = points.map(([, y]) => y);
  const minX = Math.min(...xs) - VIEW_PADDING_CELLS;
  const maxX = Math.max(...xs) + VIEW_PADDING_CELLS;
  const minY = Math.min(...ys) - VIEW_PADDING_CELLS;
  const maxY = Math.max(...ys) + VIEW_PADDING_CELLS;
  const scale = Math.min(
    (CANVAS_WIDTH - CANVAS_MARGIN * 2) / (maxX - minX + 1),
    (CANVAS_HEIGHT - CANVAS_MARGIN * 2) / (maxY - minY + 1),
  );
  const left = (CANVAS_WIDTH - (maxX - minX + 1) * scale) / 2;
  const top = (CANVAS_HEIGHT - (maxY - minY + 1) * scale) / 2;
  return {
    point([x, y]) {
      return [
        left + (x - minX + 0.5) * scale,
        top + (maxY - y + 0.5) * scale,
      ];
    },
  };
}

function pristineTransform(data) {
  const lanePoints = data.scattering.lanes.map(([, x, y]) => [x, y]);
  const support = [];
  const finalReferenceCycle = data.scattering.cyclesBeforeHit
    + PRISTINE_REFERENCE_AFTER_HIT_CYCLES;
  for (let cycle = 0; cycle <= finalReferenceCycle; cycle += 1) {
    for (const point of data.blank.supportRelative) {
      support.push(addCycle(point, data.blank.drift, cycle));
    }
  }
  return transformFromPoints([...support, ...lanePoints, [0, 0]]);
}

function exceptionalTransform(data) {
  const reverseRows = data.reverseHighway.cases;
  const reversePoints = reverseRows.map(([, x, y]) => [x, y]);
  const reverseBase = reverseRows.find((row) => row[6] === 1);
  if (!reverseBase) throw new Error("reverse-highway base row is missing");
  const reverseBasePoint = [reverseBase[1], reverseBase[2]];
  const stableTail = [];
  for (
    let depth = data.reverseHighway.twoWayBaseDepth;
    depth <= VISIBLE_REVERSE_DEPTH;
    depth += 1
  ) {
    stableTail.push(addCycle(
      reverseBasePoint,
      data.blank.drift,
      depth - data.reverseHighway.twoWayBaseDepth,
    ));
  }
  return transformFromPoints([
    ...data.finiteHistory.historicalWakeRelative,
    ...data.blank.supportRelative,
    ...reversePoints,
    ...stableTail,
    data.reverseHighway.historicalHit,
    [0, 0],
  ]);
}

function applyPaperTheme(source) {
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
    ['overview: ["#31586b", "#63b8ed", "#70cfa7", "#e89b55", "#b798f5"]',
      'overview: ["#d7e1e3", "#63a8cf", "#70cfa7", "#e89b55", "#a88fd2"]'],
    ['strokeCell(selectedPoint, "#f2f6f5")', 'strokeCell(selectedPoint, "#25373d")'],
    ['"rgba(244, 249, 248, .72)"', '"rgba(42, 63, 68, .62)"'],
  ]);
  let themed = source;
  for (const [before, after] of replacements) {
    if (!themed.includes(before)) {
      throw new Error(`paper-theme source marker not found: ${before}`);
    }
    themed = themed.replace(before, after);
  }
  return themed;
}

async function main() {
  const data = JSON.parse(await fs.readFile(proofMapPath, "utf8"));
  if (data?.scattering?.lanes?.length !== 22) {
    throw new Error("proof-map.json does not contain exactly 22 scattering lanes");
  }
  await fs.mkdir(outputDirectory, { recursive: true });
  await fs.mkdir(exceptionalDirectory, { recursive: true });
  await fs.mkdir(stageDirectory, { recursive: true });

  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  try {
    const context = await browser.newContext({
      viewport: { width: 1440, height: 1100 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    const page = await context.newPage();
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(error));

    await page.route("**/app.js*", async (route) => {
      const response = await route.fetch();
      const source = await response.text();
      await route.fulfill({
        response,
        body: applyPaperTheme(source),
        contentType: "text/javascript",
      });
    });

    await page.goto(baseUrl, { waitUntil: "networkidle" });
    const canvas = page.locator("#proof-map");
    const displayStages = [
      ["outside", "complete blank-orbit footprint", "stage-01-untouched.png"],
      ["prefix", "1,376 blue cells", "stage-02-prefix.png"],
      ["finiteHistory", "Orange marks direct depths", "stage-04-finite-history.png"],
      ["overview", "Every visible cell has one class", "stage-06-global-map.png"],
    ];
    for (const [stage, captionText, filename] of displayStages) {
      await page.locator(`[data-proof-stage="${stage}"]`).click();
      await page.waitForFunction(
        (expected) => document.querySelector("#map-caption")?.textContent?.includes(expected),
        captionText,
      );
      await page.mouse.move(1, 1);
      await page.waitForTimeout(100);
      await canvas.screenshot({ path: path.join(stageDirectory, filename) });
    }

    await page.locator('[data-proof-stage="pristine"]').click();
    await page.waitForFunction(() => (
      document.querySelector("#map-caption")?.textContent?.includes("first read in cycle")
    ));

    const transform = pristineTransform(data);
    const directionNames = ["straight", "right", "reverse", "left"];

    for (const [phase, x, y, , turns] of data.scattering.lanes) {
      const reset = page.locator("#return-selection");
      if (await reset.isEnabled()) await reset.click();

      const box = await canvas.boundingBox();
      if (!box) throw new Error("canvas is not visible");
      const [internalX, internalY] = transform.point([x, y]);
      const screenX = box.x + internalX * box.width / CANVAS_WIDTH;
      const screenY = box.y + internalY * box.height / CANVAS_HEIGHT;
      await page.mouse.move(screenX, screenY);

      await page.waitForFunction(
        ({ phaseValue, coordinate }) => {
          const readout = document.querySelector("#cell-readout")?.textContent ?? "";
          return readout.includes(coordinate)
            && readout.includes(`P104 phase ${phaseValue}`);
        },
        { phaseValue: phase, coordinate: `${x},${y}` },
      );
      await page.waitForTimeout(1100);
      await page.waitForFunction(() => (
        document.querySelector("#map-caption")?.textContent
          ?.includes("complete disturbed footprint")
      ), undefined, { timeout: 10000 });
      await page.waitForTimeout(100);

      const filename = `phase-${String(phase).padStart(2, "0")}-${directionNames[turns]}.png`;
      await canvas.screenshot({ path: path.join(outputDirectory, filename) });
    }

    await page.locator('[data-proof-stage="reverseHighway"]').click();
    await page.waitForFunction(() => (
      document.querySelector("#map-caption")?.textContent?.includes("depths 1–14")
    ));
    const reverseBase = data.reverseHighway.cases.find((row) => row[6] === 1);
    if (!reverseBase) throw new Error("reverse-highway base row is missing");
    const [, reverseX, reverseY, reverseDepth] = reverseBase;
    const reverseTransform = exceptionalTransform(data);
    await canvas.scrollIntoViewIfNeeded();
    const reverseBox = await canvas.boundingBox();
    if (!reverseBox) throw new Error("canvas is not visible");
    const [reverseInternalX, reverseInternalY] = reverseTransform.point([reverseX, reverseY]);
    await page.mouse.move(
      reverseBox.x + reverseInternalX * reverseBox.width / CANVAS_WIDTH,
      reverseBox.y + reverseInternalY * reverseBox.height / CANVAS_HEIGHT,
    );
    await page.waitForFunction(
      ({ coordinate, depth }) => {
        const readout = document.querySelector("#cell-readout")?.textContent ?? "";
        return readout.includes(coordinate)
          && readout.includes(`phase 72 · depth ${depth}`);
      },
      { coordinate: `${reverseX},${reverseY}`, depth: reverseDepth },
    );
    await page.waitForTimeout(1100);
    await page.waitForFunction(() => (
      document.querySelector("#map-caption")?.textContent
        ?.includes("complete disturbed footprint")
    ), undefined, { timeout: 10000 });
    await page.waitForTimeout(100);
    await canvas.screenshot({
      path: path.join(exceptionalDirectory, "phase-72-depth-15-history.png"),
    });

    if (pageErrors.length > 0) throw pageErrors[0];
  } finally {
    await browser.close();
  }
  console.log(`Exported 22 scattering panels to ${outputDirectory}`);
  console.log(`Exported the phase-72 history panel to ${exceptionalDirectory}`);
  console.log(`Exported four proof-stage maps to ${stageDirectory}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
