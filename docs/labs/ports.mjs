import {createState, step, key, renderGrid, setupPage, formatInt} from './common.mjs';
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]], sub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const rot=(p,k)=>k===0?[...p]:[p[1],-p[0]];
const dir=k=>k===0?[2,2]:[2,-2];
export function constructTrain(data, firstId, secondId, gap=100) {
  if (!Number.isInteger(gap) || gap<100) throw new RangeError('The separation certificate requires an integer gap of at least 100 periods.');
  const rows=[firstId,secondId].map(id=>data.rules.find(r=>r.id===id));
  if(rows.some(r=>!r)) throw new Error('Unknown collision rule.');
  if(rows[0].orientation!==0) throw new Error('This seed starts on an NE highway. Choose an NE incoming first rule.');
  if(rows[0].outputOrientation!==rows[1].orientation) throw new Error(`Orientation mismatch: the first rule leaves ${rows[0].outputOrientation===0?'NE':'SE'}, but the second expects ${rows[1].orientation===0?'NE':'SE'}.`);
  let point=[0,0], orientation=0, phase=0, time=0;
  const markers=[],events=[];
  for(const row of rows) {
    const d=dir(orientation), cycles=gap+Number(row.phase<phase);
    const offset=rot(sub(data.phasePositions[row.phase],data.phasePositions[phase]),orientation);
    const marker=add(point,add(d.map(v=>cycles*v),offset));
    time+=104*gap+(row.phase-phase+104)%104;
    events.push({time,point:marker,guard:marker[0]+row.guard,label:`Collision ${events.length+1}: phase ${row.phase}`});
    markers.push(marker);point=add(marker,row.endpoint.position);time+=row.updates;
    events.push({time,point,guard:marker[0]+row.guard,label:`Recovery ${markers.length} complete`});
    phase=row.outputPhase;orientation=row.outputOrientation;
  }
  const witness=data.trains.find(t=>t.spec[0][0]===rows[0].phase && t.spec[1][0]===rows[1].phase && t.spec.every(s=>s[1]===gap));
  return {seed:{black:[...data.base,...markers],position:[0,0],heading:1},updates:time,markers,events,
    endpoint:witness?.endpoint || {position:point,heading:rows[1].endpoint.heading},
    guard:-1, title:'A two-collision train', description:`Both markers are installed at time zero. Each gap is ${gap} full P104 periods. The second interface faces ${rows[1].orientation===0?'NE':'SE'}.`};
}
export async function fieldDigest(state) {
  const cells=[...state.black].map(v=>v.split(',').map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const bytes=new TextEncoder().encode(JSON.stringify(cells));
  const buffer=await globalThis.crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(buffer)].map(v=>v.toString(16).padStart(2,'0')).join('');
}
if(typeof document!=='undefined') {
  setupPage('ports');
  const $=id=>document.getElementById(`ports-${id}`);
  let data, config, state, path=[],playing=false, timer, target=0, generation=0,checked=false,fastPlayback=false;
  const option=(value,text)=>{const o=document.createElement('option');o.value=value;o.textContent=text;return o;};
  function stop(){playing=false;clearTimeout(timer);$('play').textContent='Play';}
  function draw(){
    const bounds=$('view').value==='near'?[state.x-20,state.x+20,state.y-16,state.y+16]:undefined;
    const view = renderGrid($('grid'),state,{path,highlight:config.markers||[],bounds});
    const guarded = [...(config.events||[])].reverse().find(e=>e.time<=state.t && e.guard!==undefined);
    const guard = guarded?.guard ?? config.guard;
    if (guard!==undefined && guard>=view.bounds[0] && guard<=view.bounds[1]) {
      const canvas=$('grid'), ctx=canvas.getContext('2d'), x=view.xy([guard-.5,0])[0];
      ctx.save();ctx.strokeStyle='#bb713f';ctx.lineWidth=2;ctx.setLineDash([7,5]);ctx.beginPath();ctx.moveTo(x,20);ctx.lineTo(x,canvas.height-30);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#80502e';ctx.font='13px "Proof Mono", ui-monospace, monospace';ctx.fillText(`protected x ≥ ${guard}`,Math.min(x+8,canvas.width-170),20);ctx.restore();
    }
    $('time').textContent=formatInt(state.t);$('mass').textContent=formatInt(state.black.size);
    $('endpoint').textContent=formatInt(config.updates);$('progress').max=config.updates;$('progress').value=state.t;
    const next=(config.events||[]).find(e=>e.time>state.t);
    const current=[...(config.events||[])].reverse().find(e=>e.time<=state.t);
    $('stage').textContent=state.t===config.updates?'Endpoint':current?.label || 'Approach';
    $('status').textContent=state.t===config.updates?'Finite endpoint reached. See the endpoint check.':next?`Next milestone: ${next.label}, at update ${formatInt(next.time)}.`:'Literal updates in progress.';
    const done=state.t>=config.updates;for(const id of ['step','play','next','end']) $(id).disabled=done;
    if(config.oldReadTime!==undefined) $('lifetime').textContent=state.t<config.birthTime?`The highlighted old-wake cell will be born at update ${config.birthTime}.`:state.t<=config.oldReadTime?`Old-wake cell age: ${state.t-config.birthTime} updates. First readback: ${config.oldReadTime}; exact lifetime ${config.lifetime}.`:`Old wake read back at update ${config.oldReadTime}, age ${config.lifetime} = 208 × ${config.n} + 53,684.`;
    else $('lifetime').textContent='';
    if(done&&!checked){checked=true;const g=generation;const ep=config.endpoint;const ok=state.x===ep.position[0]&&state.y===ep.position[1]&&state.h===ep.heading&&(ep.mass===undefined||state.black.size===ep.mass);$('check').textContent=ok?'Endpoint position, heading and available mass certificate agree.':'Endpoint comparison FAILED.';if(!ok)throw new Error('Endpoint mismatch');if(ep.fieldSha256)fieldDigest(state).then(hash=>{if(g!==generation)return;if(hash!==ep.fieldSha256)throw new Error('Full-field mismatch');$('check').textContent='PASS: complete final black field SHA-256, position, heading and mass match the Python certificate.';}).catch(error=>{if(g===generation)$('check').textContent=`Full-field hash check unavailable or failed: ${error.message}`;});}
  }
  function reset(){if(!config)return;stop();generation++;checked=false;state=createState(config.seed.black,config.seed.position,config.seed.heading);path=[[state.x,state.y]];$('heading').textContent=config.title;$('description').textContent=config.description;$('check').textContent=config.turns?'Every turn is compared with the Python replay; the final complete field is hash-checked.':'Literal full-field replay; endpoint pose checked against the construction. Exported presets also check the complete field hash.';$('seed-summary').textContent=`${config.seed.black.length} black cells; ant at (${config.seed.position}), heading ${['N','E','S','W'][config.seed.heading]}.`;$('seed').textContent=JSON.stringify(config.seed.black);$('milestones').replaceChildren(...(config.events||[]).map(e=>{const li=document.createElement('li');li.textContent=`${e.time}: ${e.label}`;return li;}));draw();}
  function advance(){if(state.t>=config.updates)return false;const i=state.t;const result=step(state);if(config.turns&&result.turn!==config.turns[i])throw new Error(`Replay turn mismatch at ${i}`);if(state.t%Math.max(1,Math.floor(config.updates/8000))===0||state.t===config.updates)path.push([state.x,state.y]);return state.t<config.updates;}
  function tick(){if(!playing)return;const batch=fastPlayback?2000:config.updates<1000?1:60;for(let i=0;i<batch&&state.t<target;i++)advance();draw();if(state.t>=target)stop();else timer=setTimeout(tick,fastPlayback?16:config.updates<1000?50:40);}
  function run(to,fast=false){stop();fastPlayback=fast;target=to;playing=true;$('play').textContent='Pause';tick();}
  function validate(){try{constructTrain(data,$('first').value,$('second').value,Number($('gap').value));if(Number($('gap').value)>300)throw new Error('The browser caps gaps at 300 for responsive replay; the theorem permits every integer gap ≥100.');$('compatibility').textContent='Interfaces match and the certified gap condition holds.';$('build').disabled=false;return true;}catch(e){$('compatibility').textContent=e.message;$('build').disabled=true;return false;}}
  function load(){
    stop();const mode=$('mode').value;
    for(const name of ['kernel','train','return']) $(`${name}-controls`).hidden=mode!==name;
    $('compatibility').textContent='';$('compatibility').hidden=mode!=='train';
    const proofIndex={gate:0,sharp:0,kernel:1,train:2,return:3}[mode];for(let i=0;i<4;i++) $(`proof-${i}`).open=i===proofIndex;
    if(mode==='gate'||mode==='sharp'){const c=data.basic.find(x=>x.id===mode);config={...c,guard:0,title:mode==='gate'?'Four cells open a permanent port':'Three cells attain the sharp exit bound',description:mode==='gate'?'Complete four-cell seed, ant facing east. The first 182 updates stay in x ≥ 0 and reach the certified permanent highway interface.':'Complete three-cell seed in x ≥ 0. Its first visit to x < 0 is exactly update 918.',markers:c.seed.black,events:[{time:c.updates,label:mode==='gate'?'Permanent P104 interface':'First half-plane exit'}]};}
    else if(mode==='kernel'){const c=data.rules.find(r=>r.id===$('rule').value);config={...c,title:`Phase ${c.phase}: ${c.orientation===0?'NE':'SE'} → ${c.outputOrientation===0?'NE':'SE'}`,description:`A complete finite mature-wake kernel at its collision. The protected boundary is x = ${c.guard}; recovery takes ${formatInt(c.updates)} literal updates.`,markers:[[0,0]],events:[{time:0,label:'Collision read'},{time:c.updates,label:'Recovered highway interface'}]};}
    else if(mode==='train'){if(!validate())return;config=constructTrain(data,$('first').value,$('second').value,Number($('gap').value));}
    else {const c=data.returns.find(r=>r.n===Number($('excursion').value));config={...c,title:'An excursion that reads its own old wake',description:`A complete 16-cell input: 13 cells of the standard base plus three preinstalled markers. Excursion parameter n = ${c.n}; the final interface is NE.`,markers:[...c.seed.black.filter(p=>!data.base.some(q=>p[0]===q[0]&&p[1]===q[1])),c.oldPoint],events:[{time:c.birthTime,label:'Old-wake cell written black'},{time:c.primaryTime,label:'Primary marker collision'},{time:c.primaryTime+104*c.n+846,label:'Distant reversal marker'},{time:c.oldReadTime,label:'Old black cell read back'},{time:c.updates,label:'NE interface restored'}]};}
    reset();
  }
  async function init(){try{const response=await fetch('./data/ports.json');if(!response.ok)throw new Error(`HTTP ${response.status}`);data=await response.json();for(const r of data.rules){const label=`${r.orientation===0?'NE':'SE'} phase ${r.phase} → ${r.outputOrientation===0?'NE':'SE'}`;$('rule').append(option(r.id,label));$('second').append(option(r.id,label));if(r.orientation===0)$('first').append(option(r.id,label));}$('first').value='0-29';$('second').value='1-15';$('rule').value='0-29';for(const id of ['mode','rule','excursion'])$(id).onchange=load;for(const id of ['first','second','gap'])$(id).onchange=validate;$('gap').oninput=validate;$('build').onclick=load;$('view').onchange=draw;$('reset').onclick=reset;$('step').onclick=()=>{stop();advance();draw();};$('play').onclick=()=>playing?stop():run(config.updates);$('end').onclick=()=>run(config.updates,true);$('next').onclick=()=>run((config.events||[]).find(e=>e.time>state.t)?.time||config.updates,true);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});load();}catch(e){$('status').textContent=`Could not load the proof witnesses: ${e.message}`;}}
  init();
}
