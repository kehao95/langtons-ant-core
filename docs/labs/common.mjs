/** Literal classical dynamics shared by the new explanatory labs.
 * States include the complete finite black set. Views may crop; states never do.
 * Time t is before update t; white/right, black/left, toggle, then move.
 */
export const MOVES = [[0, 1], [1, 0], [0, -1], [-1, 0]];
export const key = (point, y) => Array.isArray(point) ? `${point[0]},${point[1]}` : `${point},${y}`;
export const point = (value) => typeof value === 'string' ? value.split(',').map(Number) : value;
export function createState(black = [], position = [0, 0], heading = 0) {
  if (!Number.isInteger(heading) || heading < 0 || heading > 3) throw new RangeError('Heading must be 0..3.');
  const cells = [...black].map(point);
  for (const q of [...cells, position]) if (q.length !== 2 || !q.every(Number.isSafeInteger)) throw new RangeError('Grid coordinates must be safe integers.');
  return { black: new Set(cells.map(key)), x: position[0], y: position[1], h: heading, t: 0 };
}
export function cloneState(state) { return { ...state, black: new Set(state.black) }; }
export function step(state) {
  const q = [state.x, state.y], k = key(q), black = state.black.has(k);
  const event = { t: state.t, point: q, black, turn: black ? 'L' : 'R' };
  if (black) state.black.delete(k); else state.black.add(k);
  state.h = (state.h + (black ? 3 : 1)) % 4;
  state.x += MOVES[state.h][0]; state.y += MOVES[state.h][1]; state.t++;
  return event;
}
export function inverse(state) {
  const previous = cloneState(state);
  previous.x -= MOVES[state.h][0]; previous.y -= MOVES[state.h][1];
  const k = key([previous.x, previous.y]);
  const wasBlack = !state.black.has(k);
  if (wasBlack) previous.black.add(k); else previous.black.delete(k);
  previous.h = (state.h + (wasBlack ? 1 : 3)) % 4; previous.t--;
  return previous;
}
export function trueHistory(state, length) {
  if (!Number.isSafeInteger(length) || length < 0) throw new RangeError('Invalid history length');
  let q = cloneState(state); const history = [];
  for (let i = 0; i < length; i++) {
    q = inverse(q);
    history.push({ t: q.t, point: [q.x, q.y], black: q.black.has(key([q.x, q.y])), turn: q.black.has(key([q.x, q.y])) ? 'L' : 'R' });
  }
  return history.reverse();
}
export function formatInt(value) { return typeof value === 'bigint' ? value.toLocaleString('en-US') : Number(value).toLocaleString('en-US'); }

/** Canvas coordinates are illustrative only; full black state remains intact.
 * Returns toCell for canvas-relative CSS pixels (click editing).
 */
export function renderGrid(canvas, state, options = {}) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width || 960, H = canvas.height || 560;
  const path = (options.path || []).map(p => point(p.point || p));
  const highlights = (options.highlight || []).map(p => point(p.point || p));
  const black = [...state.black].map(point);
  let bounds = options.bounds;
  if (!bounds) {
    let minX = state.x, maxX = state.x, minY = state.y, maxY = state.y;
    for (const [x, y] of [...black, ...path, ...highlights]) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y); }
    const pad = 2; bounds = [minX - pad, maxX + pad, minY - pad, maxY + pad];
  }
  const [minX, maxX, minY, maxY] = bounds;
  const padding = 35;
  const scale = Math.min((W - 2 * padding) / Math.max(1, maxX - minX + 1), (H - 2 * padding) / Math.max(1, maxY - minY + 1));
  const left = (W - (maxX - minX + 1) * scale) / 2;
  const top = (H - (maxY - minY + 1) * scale) / 2;
  const xy = ([x, y]) => [left + (x - minX + .5) * scale, top + (maxY - y + .5) * scale];
  ctx.clearRect(0, 0, W, H); ctx.fillStyle = '#f5f5ed'; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.beginPath(); ctx.rect(left, top, (maxX - minX + 1) * scale, (maxY - minY + 1) * scale); ctx.clip();
  if (scale >= 7 && maxX - minX < 300 && maxY - minY < 300) {
    ctx.strokeStyle = '#dbe3dc'; ctx.lineWidth = 1; ctx.beginPath();
    for (let x = minX; x <= maxX + 1; x++) { const px = left + (x - minX) * scale; ctx.moveTo(px, top); ctx.lineTo(px, H - top); }
    for (let y = minY; y <= maxY + 1; y++) { const py = top + (y - minY) * scale; ctx.moveTo(left, py); ctx.lineTo(W - left, py); } ctx.stroke();
  }
  if (path.length) {
    ctx.strokeStyle = '#5e9c99'; ctx.lineWidth = Math.max(1.3, Math.min(3, scale / 7)); ctx.globalAlpha = .62; ctx.beginPath();
    path.forEach((p, i) => { const [x, y] = xy(p); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }); ctx.stroke(); ctx.globalAlpha = 1;
  }
  ctx.fillStyle = '#173b43';
  for (const p of black) {
    if (p[0] < minX || p[0] > maxX || p[1] < minY || p[1] > maxY) continue;
    const [x, y] = xy(p); const size = Math.max(1.3, scale * .72); ctx.fillRect(x - size / 2, y - size / 2, size, size);
  }
  ctx.strokeStyle = '#c66b3f'; ctx.lineWidth = Math.max(2, Math.min(4, scale / 8));
  for (const p of highlights) { const [x, y] = xy(p); const size = Math.max(7, scale * .88); ctx.strokeRect(x - size / 2, y - size / 2, size, size); }
  const [ax, ay] = xy([state.x, state.y]); const size = Math.max(5, Math.min(16, scale * .43));
  ctx.save(); ctx.translate(ax, ay); ctx.rotate(state.h * Math.PI / 2);
  ctx.fillStyle = '#d16a3c'; ctx.strokeStyle = '#fffaf0'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(0, -size); ctx.lineTo(size * .8, size * .8); ctx.lineTo(0, size * .45); ctx.lineTo(-size * .8, size * .8); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); ctx.restore();
  ctx.fillStyle = '#526972'; ctx.font = '12px "Proof Mono", "DejaVu Sans Mono", monospace';
  ctx.fillText(`x ${minX} … ${maxX}   ·   y ${minY} … ${maxY}`, 12, H - 12);
  canvas.dataset.time = String(state.t); canvas.dataset.mass = String(state.black.size);
  return {
    bounds, scale, xy,
    toCell(px, py) {
      const rect = canvas.getBoundingClientRect();
      const ix = px * W / (rect.width || W), iy = py * H / (rect.height || H);
      const x = minX + Math.floor((ix - left) / scale), y = maxY - Math.floor((iy - top) / scale);
      return x < minX || x > maxX || y < minY || y > maxY ? null : [x, y];
    },
  };
}

export const PAGES = [
  { id: 'one-black', title: 'One black cell', file: 'one-black.html', short: '01' },
  { id: 'clock', title: 'Clocks & escape', file: 'clock.html', short: '02' },
  { id: 'wake', title: 'Reading the wake', file: 'wake.html', short: '03' },
  { id: 'factors', title: 'Local language', file: 'factors.html', short: '04' },
  { id: 'memory', title: 'Memory & feedback', file: 'memory.html', short: '05' },
  { id: 'ports', title: 'Ports & scattering', file: 'ports.html', short: '06' },
];
export function setupPage(active = 'home') {
  if (typeof document === 'undefined') return;
  for (const target of document.querySelectorAll('[data-site-nav]')) {
    target.innerHTML = `<div class="site-bar"><a class="site-brand" href="./index.html" ${active === 'home' ? 'aria-current="page"' : ''}><span class="brand-mark" aria-hidden="true">↱</span> LANGTON’S ANT <span class="brand-sub">PROOF LABS</span></a><a class="source-link" href="https://github.com/kehao95/langtons-ant-core">Source ↗</a></div><nav class="site-nav" aria-label="Proof laboratories"><a href="./index.html" ${active === 'home' ? 'aria-current="page"' : ''}>Overview</a>${PAGES.map(p => `<a href="./${p.file}" ${active === p.id ? 'aria-current="page"' : ''}><span>${p.short}</span> ${p.title}</a>`).join('')}</nav>`;
  }
  for (const target of document.querySelectorAll('[data-site-footer]')) {
    target.innerHTML = `<div class="footer-inner"><p><strong>Langton’s Ant · Proof Labs</strong><br>White turns right. Black turns left. The complete field stays with the ant.</p><p><a href="./index.html#proof-and-evidence">How to read these proofs</a><br><a href="https://github.com/kehao95/langtons-ant-core/blob/main/PREPRINTS.md">Papers & versions ↗</a> · Hao Ke</p></div>`;
  }
  renderMath(document.body);
}
export function renderMath(element) {
  if (typeof globalThis.renderMathInElement === 'function') globalThis.renderMathInElement(element, { delimiters: [{ left: '$$', right: '$$', display: true }, { left: '\\[', right: '\\]', display: true }, { left: '\\(', right: '\\)', display: false }], throwOnError: false });
}
