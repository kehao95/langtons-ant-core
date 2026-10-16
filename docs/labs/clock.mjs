import { createState, step, key, renderGrid, setupPage, formatInt } from './common.mjs';

const parity = (x, y) => (x + y) % 2 === 0 ? 1n : -1n;
export function integerClock(state, center = 0) {
  const sigma = parity(state.x, state.y) * (state.h % 2 === 0 ? 1n : -1n);
  const s = state.x + state.y - center;
  const f = 3n ** BigInt(Math.abs(s)) - 1n;
  const e = state.h < 2 ? 1 : -1;
  let field = 0n;
  for (const cell of state.black) {
    const [x, y] = cell.split(',').map(Number);
    field += parity(x, y) * (3n ** BigInt(Math.abs(x + y - center)) - 1n);
  }
  return -sigma * field + (e * s >= 0 ? f / 2n : -3n * (f / 2n));
}
export function squareBound(n) {
  if (!Number.isInteger(n) || n < 1) throw new RangeError('Side length must be a positive integer');
  const m = BigInt(n);
  return (13n * 3n ** (m - 1n) - 2n * m * m - 4n * m - 5n) / 2n;
}
export function expectedGain(before, after, center = 0) {
  const e = before.h < 2 ? 1 : -1;
  const next = after.h < 2 ? 1 : -1;
  const s = before.x + before.y - center;
  return 1n + (e !== next && e * s < 0 ? 4n * (3n ** BigInt(Math.abs(s)) - 1n) : 0n);
}

if (typeof document !== 'undefined') {
  setupPage('clock');
  const $ = id => document.getElementById(`clock-${id}`);
  let n = 7, seed = [], pose = [3, 3], heading = 0, state, path, viewport;
  let playing = false, fast = false, gain = null, branch = '', timer, initialClock = 0n;
  const inside = () => state.x >= 0 && state.x < n && state.y >= 0 && state.y < n;
  function stop() { playing = false; clearTimeout(timer); $('play').textContent = 'Play'; }
  function draw() {
    viewport = renderGrid($('grid'), state, {path, bounds: [-1, n, -1, n]});
    $('time').textContent = formatInt(state.t);
    $('value').textContent = integerClock(state, n - 1).toString();
    $('gain').textContent = gain === null ? '—' : `+${gain}`;
    $('bound').textContent = squareBound(n).toString();
    const spent = integerClock(state, n - 1) - initialClock;
    $('spent').textContent = spent.toString();
    $('remaining').textContent = inside() ? (squareBound(n) - spent).toString() : 'Exited';
    $('branch').textContent = branch || 'Take one step to inspect its algebraic branch.';
    $('status').textContent = !inside() ? `First exit at update ${state.t}. Verified ${state.t} ≤ ${squareBound(n)}.` : state.t ? 'Clock increasing. Reset to edit the initial field.' : 'Ready. Edit cells or move the ant before running.';
    $('step').disabled = !inside(); $('finish').disabled = !inside(); $('play').disabled = !inside();
    $('apply').disabled = state.t !== 0;
    $('heading').disabled = state.t !== 0;
  }
  function reset() { stop(); state = createState(seed, pose, heading); initialClock = integerClock(state, n - 1); path = [[state.x,state.y]]; gain = null; branch = ''; draw(); }
  function advance() {
    if (!inside()) return false;
    const before = {x: state.x, y: state.y, h: state.h};
    const initial = integerClock(state, n - 1);
    const event = step(state);
    gain = integerClock(state, n - 1) - initial;
    const expected = expectedGain(before, state, n - 1);
    if (gain !== expected || gain < 1n) throw new Error('Clock identity failed');
    branch = `Read ${event.black ? 'black → left' : 'white → right'} at (${before.x}, ${before.y}); s = ${before.x + before.y - n + 1}. Full-field gain ${gain} = local prediction ${expected}.`;
    path.push([state.x, state.y]);
    if (!inside()) stop();
    return inside();
  }
  function tick() {
    if (!playing) return;
    const count = fast ? 200 : 1;
    for (let i = 0; i < count; ++i) if (!advance()) break;
    draw(); if (playing) timer = setTimeout(tick, fast ? 16 : 160);
  }
  function preset() {
    seed = [];
    for (let x = 0; x < n; ++x) for (let y = 0; y < n; ++y) {
      if ($('preset').value === 'checker' && (x+y)%2 === 0 || $('preset').value === 'corners' && (x===0 || x===n-1) && (y===0 || y===n-1)) seed.push([x,y]);
    }
    reset();
  }
  function edit(x, y) {
    if (state.t || !Number.isInteger(x) || !Number.isInteger(y) || x<0 || x>=n || y<0 || y>=n) return;
    if ($('edit').value === 'ant') pose = [x,y];
    else { const cells = new Set(seed.map(p=>key(...p))); const k = key(x,y); if(cells.has(k)) cells.delete(k); else cells.add(k); seed = [...cells].map(v=>v.split(',').map(Number)); }
    reset();
  }
  $('grid').addEventListener('click', event => { const rect = $('grid').getBoundingClientRect(); const p = viewport?.toCell(event.clientX-rect.left,event.clientY-rect.top); if(p) edit(...p); });
  $('apply').onclick = () => edit(Number($('x').value), Number($('y').value));
  $('size').oninput = () => { n = Number($('size').value); $('size-value').value = n; pose = [Math.floor(n/2),Math.floor(n/2)]; for(const id of ['x','y']) {$(id).max = n-1; $(id).value = pose[0];} preset(); };
  $('preset').onchange = preset;
  $('heading').onchange = () => { heading = Number($('heading').value); reset(); };
  $('reset').onclick = reset;
  $('step').onclick = () => { stop(); advance(); draw(); };
  $('play').onclick = () => { if(playing) stop(); else {playing=true;fast=false;$('play').textContent='Pause';tick();} };
  $('finish').onclick = () => { stop();playing=true;fast=true;$('play').textContent='Pause';tick(); };
  $('height').oninput = () => { const h=Number($('height').value);$('height-value').value=h;$('degree').textContent=`Degree ${Math.floor(h/2)+1} in the long side N (height ${h} fixed).`; };
  document.addEventListener('visibilitychange', () => { if(document.hidden) stop(); });
  reset();
}
