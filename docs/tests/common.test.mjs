import test from 'node:test';
import assert from 'node:assert/strict';
import {createState, cloneState, step, inverse, trueHistory} from '../labs/common.mjs';
const sorted = s => ({...s, black:[...s.black].sort()});
test('forward and inverse preserve the complete state in both directions', () => {
  for(let mask=0;mask<16;mask++) for(let heading=0;heading<4;heading++) {
    const points=[[-2,-1],[-1,-1],[-2,0],[-1,0]].filter((_,i)=>mask&(1<<i));
    const start=createState(points,[-2,-1],heading);
    const forward=cloneState(start); step(forward);
    assert.deepEqual(sorted(inverse(forward)),sorted(start));
    const backward=inverse(start); step(backward);
    assert.deepEqual(sorted(backward),sorted(start));
    assert.deepEqual([...start.black].sort(),points.map(p=>p.join(',')).sort());
  }
});
test('true prehistory replays into exactly the input state, including remote cells', () => {
  const initial=createState([[0,0],[3,-2],[1000000,-1000000]],[-3,2],3);
  const events=trueHistory(initial,200);
  let past=cloneState(initial);
  for(let i=0;i<200;i++) past=inverse(past);
  assert.deepEqual(Array.from({length:200},()=>step(past)),events);
  assert.deepEqual(sorted(past),sorted(initial));
  assert.equal(events[0].t,-200); assert.equal(events.at(-1).t,-1);
});
