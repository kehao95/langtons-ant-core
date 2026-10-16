import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {familyTimes, growingScale, isqrt, buildTrace, atTime, selectedEvents, isStale, outsideSquare} from '../labs/memory.mjs';
const fixtures=JSON.parse(readFileSync(new URL('../data/memory.json',import.meta.url),'utf8'));
const canonical=value=>JSON.stringify(value,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);

for(const [name,row] of [['blank',fixtures.blank],['reborn',fixtures.reborn],...fixtures.families.map(r=>[`family n=${r.n}`,r])]) {
  test(`${name}: complete field, pose and every intrinsic S128 event match Python`,()=>{
    const trace=buildTrace(row.seed,row.heading,row.length);
    assert.deepEqual(selectedEvents(trace,128,-1).map(e=>({t:e.t,point:e.point,birth:e.birth})),row.events128);
    const final={black:[...trace.final.black].map(p=>p.split(',').map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]),heading:trace.final.h,position:[trace.final.x,trace.final.y]};
    assert.deepEqual(final,row.final);
    assert.equal(createHash('sha256').update(canonical(final)).digest('hex'),row.final_sha256);
    const restored=atTime(trace,Math.min(257,row.length));
    assert.equal(restored.t,257);
    if(row.n){
      const ev=trace.records[row.death];
      assert.equal(ev.birth,60);assert.deepEqual(ev.point,[0,2]);
      assert.equal(selectedEvents(trace,128,-1).filter(e=>60<e.t&&e.t<row.death).length,31);
      assert.deepEqual(familyTimes(row.n),{n:BigInt(row.n),birth:60n,death:BigInt(row.death),age:BigInt(row.death-60),entry:BigInt(row.entry)});
    }
  });
}

test('a selected lifetime changes colour at birth and death, and has a strict D threshold',()=>{
  const trace=buildTrace(fixtures.blank.seed,fixtures.blank.heading,800), e=trace.records[197];
  assert.equal(e.birth,21);assert.deepEqual(e.point,[-3,-2]);
  assert.equal(isStale(e,175),true);assert.equal(isStale(e,176),false);
  assert.equal(atTime(trace,21).black.has('-3,-2'),false);
  assert.equal(atTime(trace,22).black.has('-3,-2'),true);
  assert.equal(atTime(trace,197).black.has('-3,-2'),true);
  assert.equal(atTime(trace,198).black.has('-3,-2'),false);
  assert.equal(outsideSquare(e.point,2),true);assert.equal(outsideSquare(e.point,3),false);
  assert.equal(selectedEvents(trace,128,3,true).some(r=>r.t===197),false);
});

test('an initially black coordinate can acquire a new qualifying lifetime',()=>{
  const trace=buildTrace(fixtures.reborn.seed,fixtures.reborn.heading,800);
  const e=trace.records[fixtures.reborn.rebirth.t];
  assert.equal(e.initialCoordinate,true);assert.equal(e.birth,4);assert.equal(e.t,16);
  assert.equal(isStale(e,4),true);
  assert.equal(selectedEvents(trace,4,-1,true).some(r=>r.t===16),true);
});

test('true inverse prehistory is part of a time-zero event test',()=>{
  const trace=buildTrace([[0,0]],0,1);
  assert.equal(trace.records[0].previous,-4);
  assert.equal(isStale(trace.records[0],3),true);
  assert.equal(isStale(trace.records[0],4),false);
  // D is limited to the amount of genuine inverse prehistory the page retains.
  assert.throws(()=>isStale(trace.records[0],257),RangeError);
});

test('family arithmetic stays exact beyond floating-point coordinates',()=>{
  const n=10n**60n, result=familyTimes(n);
  assert.equal(result.death,624n*n-1516n);assert.equal(result.entry-result.death,774n);
  assert.throws(()=>familyTimes(21));assert.throws(()=>familyTimes(18));
});

test('fixed huge first-feedback certificate retains exact birth, death and all segments',()=>{
  const h=fixtures.huge,N=BigInt(h.N);
  assert.equal(BigInt(h.birth),104n*N-102n);assert.equal(BigInt(h.death),104n*N+46n);
  assert.equal(BigInt(h.death)-BigInt(h.birth),148n);
  assert.equal(h.post_terms.length,379);
  assert.equal(BigInt(h.total_written_reads),BigInt(h.death)+1n);
  assert.equal(createHash('sha256').update(canonical(h.post_terms)).digest('hex'),h.post_terms_sha256);
});

test('growing-scale exact integers match all original Python fixtures and maximal cutoff',()=>{
  for(const row of fixtures.scales){
    const result=growingScale(row.exponent);
    for(const [k,v] of Object.entries(row)) if(k!=='exponent') assert.equal(String(result[k]),v,`${row.exponent}: ${k}`);
    const {n,quadratic_coefficient:a,linear_coefficient:c,H}=result;
    assert.ok(a*n*n+c*n<=H);assert.ok(a*(n+1n)**2n+c*(n+1n)>H);
  }
  for(const n of [0n,1n,2n,3n,4n,10n**120n-1n,10n**120n]){
    const s=isqrt(n);assert.ok(s*s<=n&&(s+1n)*(s+1n)>n);
  }
});
