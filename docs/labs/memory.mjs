import {createState, step, inverse, key, renderGrid, setupPage, formatInt} from './common.mjs';

export function familyTimes(value) {
  const n = BigInt(value);
  if (n < 20n || n % 2n) throw new RangeError('Choose an even integer n ≥ 20.');
  return {n, birth:60n, death:624n*n-1516n, age:624n*n-1576n, entry:624n*n-742n};
}

export function isqrt(n) {
  if (n < 0n) throw new RangeError('A square root needs a nonnegative integer.');
  if (n < 2n) return n;
  let a = 1n << BigInt(Math.ceil(n.toString(2).length / 2));
  while (true) { const b = (a + n/a)/2n; if (b >= a) return a; a = b; }
}

export function growingScale(exponent, mass=20n, width=100n) {
  if (!Number.isInteger(exponent) || exponent < 64 || exponent > 1024) throw new RangeError('Use an integer exponent from 64 to 1024.');
  const H = 3n ** BigInt(exponent), L = BigInt(exponent);
  const D = L.toString(2).length - 6, Q = 1n << BigInt(D), radius = L/16n;
  const ell = 2n*radius + 6n*Q + 5n, burst = 8n*ell*3n**ell+1n;
  const a = 18n*Q*Q, c = 2n*Q*(width+2n*radius)+20n*Q*Q+burst-a;
  let lo = 0n, hi = isqrt(H/a)+1n;
  while (lo+1n < hi) { const m=(lo+hi)/2n; if (a*m*m+c*m <= H) lo=m; else hi=m; }
  const late = isqrt(isqrt(H)), count = lo-mass-2n*late;
  return {H,L,D:BigInt(D),Q,radius,ell,burst,n:lo,late_birth:late,count:count>0n?count:0n,quadratic_coefficient:a,linear_coefficient:c};
}

function copyState(s) { return {...s, black:new Set(s.black)}; }

/** The first 256 past positions come from the unique inverse of the FULL input. */
export function buildTrace(seed, heading, length, maxMemory=256) {
  const state = createState(seed,[0,0],heading), initial = new Set(state.black);
  const last = new Map(), births = new Map([...state.black].map(p => [p,null]));
  let past = copyState(state);
  for (let age=1; age<=maxMemory; age++) {
    past=inverse(past); const p=key(past.x,past.y);
    if (!last.has(p)) last.set(p,-age);
  }
  const records=[], snapshots=new Map([[0,copyState(state)]]);
  for (let t=0;t<length;t++) {
    const p=key(state.x,state.y), black=state.black.has(p), previous=last.get(p);
    records.push({t,point:[state.x,state.y],black,birth:black?births.get(p):null,
      previous:previous??null, initialCoordinate:initial.has(p), mass:state.black.size});
    if (black) births.delete(p); else births.set(p,t);
    last.set(p,t); step(state);
    if (state.t%256===0) snapshots.set(state.t,copyState(state));
  }
  snapshots.set(length,copyState(state));
  return {records,snapshots,length,maxMemory,final:copyState(state)};
}

export function atTime(trace,t) {
  t=Math.max(0,Math.min(trace.length,Math.trunc(t)));
  const base=trace.snapshots.has(t)?t:Math.floor(t/256)*256;
  const state=copyState(trace.snapshots.get(base));
  while(state.t<t) step(state);
  return state;
}

export function isStale(record,D) {
  if (!Number.isInteger(D) || D<1 || D>256) throw new RangeError('Replay memory D must be 1…256.');
  return record.black && (record.previous===null || record.t-record.previous>D);
}

export function outsideSquare(point,radius) {
  return radius<0 || Math.max(Math.abs(point[0]),Math.abs(point[1]))>radius;
}

export function selectedEvents(trace,D,radius,freshOnly=false) {
  return trace.records.filter(r => isStale(r,D) && (!freshOnly || (r.birth!==null && outsideSquare(r.point,radius))));
}

async function init() {
  setupPage('memory');
  const $=id=>document.getElementById(id);
  const response=await fetch('./data/memory.json');
  if(!response.ok) throw new Error(`Memory data could not load (${response.status}).`);
  const data=await response.json();
  let fixture=data.blank, trace, events=[], selected=null, playing=null;
  const canvas=$('memory-canvas');
  const fmt=n=>formatInt(n);
  const radius=()=>Number($('region').value);
  const memory=()=>Number($('memory').value);

  function describe(event) {
    if (!event) return 'No matching read in this finite replay window. Change D, the region, or the input to explore another window.';
    const gap=event.previous===null?`more than ${trace.maxMemory}`:String(event.t-event.previous);
    const lifetime=event.birth===null?'This black lifetime was already present at the source checkpoint.':`This lifetime was written at update ${fmt(event.birth)} and consumed at update ${fmt(event.t)}, an age of ${fmt(event.t-event.birth)}.`;
    const reborn=event.birth!==null&&event.initialCoordinate?' The coordinate was initially black, then erased and rewritten. Its new lifetime qualifies as newly generated memory.':'';
    const exterior=outsideSquare(event.point,radius());
    return `Cell (${event.point.join(', ')}): previous read ${gap} updates earlier. ${lifetime}${reborn} ${exterior?'It lies outside the selected K.':'It lies inside the selected K.'}`;
  }

  function draw() {
    const t=Number($('time').value), state=atTime(trace,t);
    const path=trace.records.slice(Math.max(0,t-208),t).map(r=>r.point);
    let bounds;
    if($('view').value==='local') bounds=[state.x-16,state.x+16,state.y-16,state.y+16];
    const grid=renderGrid(canvas,state,{path,highlight:selected?[selected.point]:[],bounds});
    if(radius()>=0) {
      const r=radius(), ctx=canvas.getContext('2d'), a=grid.xy([-r,r]);
      const side=(2*r+1)*grid.scale;
      ctx.save();ctx.strokeStyle='#146e75';ctx.lineWidth=2;ctx.setLineDash([6,4]);
      ctx.strokeRect(a[0]-grid.scale/2,a[1]-grid.scale/2,side,side);ctx.restore();
    }
    $('time-output').textContent=fmt(t);
    $('mass-output').textContent=fmt(state.black.size);
    $('pose-output').textContent=`(${state.x}, ${state.y}) · ${['N','E','S','W'][state.h]}`;
    $('event-description').textContent=describe(selected);
    if(selected) {
      const present=state.black.has(key(...selected.point));
      $('cell-status').textContent=`Selected cell is ${present?'black':'white'} before update ${fmt(t)}. ${t===selected.t?'This update reads and erases it.':selected.birth!==null&&t===selected.birth?'This update writes its new lifetime.':''}`;
    } else $('cell-status').textContent='Select an event to follow one physical cell through its lifetime.';
    $('birth-button').disabled=!selected||selected.birth===null;
    $('read-button').disabled=!selected;
    $('after-button').disabled=!selected;
    const idx=events.indexOf(selected);
    $('previous-event').disabled=idx<=0;
    $('next-event').disabled=idx<0||idx>=events.length-1;
  }

  function choose(index,jump=true) {
    selected=events[index]??null;
    $('event-select').value=selected?String(index):'';
    if(selected&&jump) $('time').value=selected.t;
    draw();
  }

  function classify(preferredTime=null) {
    const D=memory(); $('memory-output').textContent=D;
    $('region-output').textContent=radius()<0?'K is empty':`K = [−${radius()}, ${radius()}]²`;
    events=selectedEvents(trace,D,radius(),$('fresh-only').checked);
    $('event-count').textContent=fmt(events.length);
    $('event-select').replaceChildren(...events.map((event,index)=>{
      const option=document.createElement('option'); option.value=index;
      const kind=event.birth===null?'source lifetime':event.initialCoordinate?'reborn coordinate':'new lifetime';
      option.textContent=`t = ${event.t} · (${event.point.join(', ')}) · ${kind}`;
      return option;
    }));
    $('event-select').disabled=!events.length;
    if(!events.length) { const option=document.createElement('option'); option.textContent='No event in this replay window'; $('event-select').append(option); }
    const wanted=preferredTime??selected?.t;
    const index=events.findIndex(e=>e.t===wanted);
    choose(index>=0?index:0);
  }

  function load() {
    if(playing){clearInterval(playing);playing=null;$('play-button').textContent='Play';}
    const mode=$('input-case').value;
    fixture=mode==='family'?data.families.find(r=>r.n===Number($('literal-n').value)):data[mode];
    $('literal-n').disabled=mode!=='family';
    trace=buildTrace(fixture.seed,fixture.heading,fixture.length);
    $('time').max=trace.length; $('time').value=0;
    $('window-length').textContent=fmt(trace.length);
    $('initial-mass').textContent=fixture.seed.length;
    if(mode==='reborn') $('memory').value=4;
    else $('memory').value=128;
    const preferred=mode==='blank'?197:mode==='reborn'?fixture.rebirth.t:fixture.death;
    classify(preferred);
  }

  $('input-case').addEventListener('change',load);
  $('literal-n').addEventListener('change',load);
  $('memory').addEventListener('input',()=>classify());
  $('region').addEventListener('input',()=>classify());
  $('fresh-only').addEventListener('change',()=>classify());
  $('event-select').addEventListener('change',()=>choose(Number($('event-select').value)));
  $('time').addEventListener('input',draw);
  $('view').addEventListener('change',draw);
  $('previous-event').addEventListener('click',()=>choose(events.indexOf(selected)-1));
  $('next-event').addEventListener('click',()=>choose(events.indexOf(selected)+1));
  $('birth-button').addEventListener('click',()=>{$('time').value=selected.birth;draw();});
  $('read-button').addEventListener('click',()=>{$('time').value=selected.t;draw();});
  $('after-button').addEventListener('click',()=>{$('time').value=selected.t+1;draw();});
  $('play-button').addEventListener('click',()=>{
    if(playing){clearInterval(playing);playing=null;$('play-button').textContent='Play';return;}
    $('play-button').textContent='Pause';
    playing=setInterval(()=>{
      const t=Number($('time').value);
      if(t>=trace.length){clearInterval(playing);playing=null;$('play-button').textContent='Play';return;}
      $('time').value=Math.min(trace.length,t+(fixture.length>1000?16:1));draw();
    },60);
  });
  $('step-button').addEventListener('click',()=>{$('time').value=Math.min(trace.length,Number($('time').value)+1);draw();});

  function updateFamily() {
    try {
      const value=$('family-n').value.trim();
      if(!/^\d{1,100}$/.test(value)) throw new Error('Enter an even integer from 20 upwards (at most 100 digits).');
      const result=familyTimes(value);
      $('family-error').textContent='';
      $('family-death').textContent=fmt(result.death);
      $('family-age').textContent=fmt(result.age);
      $('family-entry').textContent=fmt(result.entry);
      $('family-caption').textContent=`For n = ${fmt(result.n)}, the same cell (0, 2) is created at update 60 and returns after ${fmt(result.age)} updates. The seed still contains exactly 20 black cells, and exactly 31 S₁₂₈ reads occur strictly between birth and consumption.`;
    } catch(error) { $('family-error').textContent=error.message; }
  }
  $('family-n').addEventListener('input',updateFamily);
  $('huge-family').addEventListener('click',()=>{$('family-n').value='1'+'0'.repeat(60);updateFamily();});
  $('small-family').addEventListener('click',()=>{$('family-n').value='20';updateFamily();});
  $('replay-family').addEventListener('click',()=>{$('input-case').value='family';$('literal-n').value='20';load();$('explorer').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});});

  $('huge-birth').textContent=fmt(BigInt(data.huge.birth));
  $('huge-death').textContent=fmt(BigInt(data.huge.death));
  $('huge-terms').textContent=data.huge.post_terms.length;
  $('huge-point').textContent=`(${data.huge.point.join(', ')})`;
  $('huge-reads').textContent=fmt(BigInt(data.huge.total_written_reads));

  function updateScale() {
    const exponent=Number($('scale').value), result=growingScale(exponent);
    $('scale-output').textContent=exponent;
    $('scale-D').textContent=fmt(result.D);$('scale-radius').textContent=fmt(result.radius);
    $('scale-late').textContent=fmt(result.late_birth);$('scale-count').textContent=fmt(result.count);
    $('scale-horizon').textContent=fmt(result.H);
  }
  $('scale').addEventListener('input',updateScale);
  window.addEventListener('resize',draw);
  load();updateFamily();updateScale();
  document.body.dataset.ready='true';
}

if(typeof document!=='undefined') init().catch(error=>{
  const target=document.getElementById('load-status');
  if(target) {target.textContent=error.message;target.setAttribute('role','alert');}
  console.error(error);
});
