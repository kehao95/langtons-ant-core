import {createState,step,renderGrid,setupPage,formatInt} from './common.mjs';
const mod=(a,b)=>((a%b)+b)%b;
export function parityScreen(wake,sigma=1){
  if(![-1,1].includes(sigma))throw Error('sigma must be ±1');
  if(wake.some(p=>p.length!==2||!Number.isSafeInteger(p[0])||![0,1].includes(p[1]))||new Set(wake.map(p=>p.join(','))).size!==wake.length)throw Error('distinct full drift classes required');
  const normalized=wake.map(([t,r])=>[t+(sigma===-1?1:0),r]);
  const counts=[0,0,0,0];for(const[t,r]of normalized)counts[2*mod(t,2)+r]++;
  const[q0,q1,c0,c1]=counts;const residues=[q0-c0,q1-c1,q0-c1,q1-c0].every(x=>mod(x,4)===2);
  const V=q0+q1;let J=0;for(const[t]of normalized.filter(([t])=>mod(t,2)===0))for(const[u]of normalized.filter(([t])=>mod(t,2)===1))if(t<u)J++;
  const preliminary=wake.length>0&&wake.length%4===0&&residues;
  const parity=mod(J+V/2,2);
  return {counts,V,J,parity,preliminary,passes:preliminary&&parity===1};
}
export function profileOf(wake){const map=new Map();for(const[t]of wake)map.set(t,(map.get(t)||0)+1);return map;}
export function theoremScope(wake){
  if(!wake.length)return false;const p=profileOf(wake),lo=Math.min(...p.keys()),hi=Math.max(...p.keys());
  return wake.length===12&&hi-lo===10&&[...p].every(([t,n])=>t===lo||t===hi||n<=1);
}
export function traceWord(word,heading=1,position=[0,0]){let[x,y]=position,h=heading;const points=[];for(const turn of word){points.push([x,y]);h=mod(h+(turn==='R'?1:-1),4);const d=[[0,1],[1,0],[0,-1],[-1,0]][h];x+=d[0];y+=d[1];}return{points,end:[x,y],heading:h};}
export function oddClasses(points){const counts=new Map();for(const[x,y]of points){const k=`${x+y},${mod(x,2)}`;counts.set(k,(counts.get(k)||0)+1);}return [...counts].filter(([,n])=>n%2).map(([k])=>k.split(',').map(Number));}
async function start(){
 setupPage('wake');const data=await fetch('./data/wake.json').then(r=>{if(!r.ok)throw Error('Witness load failed');return r.json();});
 const $=id=>document.getElementById(id);let selected=data.oddClasses.map(p=>[...p]),sigma=data.sigma;
 function drawPeriod(){const phase=+$('phase').value,state=createState(data.seed,[0,0],data.heading);for(let i=0;i<phase;i++)step(state);const word=data.word.slice(phase)+data.word.slice(0,phase),trace=traceWord(word,state.h,[state.x,state.y]);renderGrid($('wake-canvas'),state,{path:trace.points,highlight:[[state.x,state.y]]});$('phase-value').textContent=phase;$('word').textContent=word;$('period-position').textContent=`(${state.x}, ${state.y})`;$('period-drift').textContent=`(${trace.end[0]-state.x}, ${trace.end[1]-state.y})`;
 $('period-classes').textContent=oddClasses(trace.points).length;}
 function drawEditor(){
  $('sigma').value=String(sigma);const cells=new Set(selected.map(p=>p.join(',')));$('layer-grid').replaceChildren();
  const top=Math.max(0,...selected.map(p=>p[0])),bottom=Math.min(-10,...selected.map(p=>p[0]));
  for(let t=top;t>=bottom;t--){const row=document.createElement('div');row.className='layer-row';const label=document.createElement('span');label.textContent=`t = ${t}`;row.append(label);for(let r=0;r<2;r++){const b=document.createElement('button');b.type='button';b.className='lane';b.setAttribute('aria-label',`Layer ${t}, residue ${r}`);b.setAttribute('aria-pressed',String(cells.has(`${t},${r}`)));b.textContent=cells.has(`${t},${r}`)?'●':'○';b.onclick=()=>{const k=`${t},${r}`;selected=cells.has(k)?selected.filter(p=>p.join(',')!==k):[...selected,[t,r]];drawEditor();};row.append(b);} $('layer-grid').append(row);}
  const s=parityScreen(selected,sigma),p=profileOf(selected),levels=[...p.keys()],width=levels.length?Math.max(...levels)-Math.min(...levels):0;
  $('growth').textContent=selected.length;$('width').textContent=width;$('parity-value').textContent=s.preliminary?`${s.J} + ${s.V}/2 ≡ ${s.parity} (mod 2)`:'Growth or signed residue test fails';$('residue-counts').textContent=s.counts.join(', ');
  $('screen-result').textContent=s.passes?'Not excluded by this necessary screen. Realizability needs an ordered-read / infinite-tail certificate; parity alone does not establish it.':'Excluded: these odd classes cannot describe a highway with full drift (2, −2) and this σ.';
  $('scope-checks').replaceChildren();for(const [name,ok] of [['Full drift (2, −2), fixed for this explorer',true],['Growth = 12',selected.length===12],['Transverse width = 10',width===10],['At most one odd class at each strict interior layer',[...p].every(([t,n])=>t===Math.min(...levels)||t===Math.max(...levels)||n<=1)]]){const li=document.createElement('li');li.textContent=`${ok?'✓':'×'} ${name}`;$('scope-checks').append(li);}
  $('scope-result').textContent=theoremScope(selected)?'Within the thin-wake theorem’s geometric assumptions: any realizing finite-support periodic highway must be the standard P104 (up to the theorem’s equivalences).':'Outside the thin-wake theorem’s growth / width / interior-thinness assumptions.';
 }
 $('phase').oninput=drawPeriod;$('sigma').onchange=()=>{sigma=+$('sigma').value;drawEditor();};
 $('wake-preset').onchange=()=>{const choice=$('wake-preset').value;if(choice==='standard'){selected=data.oddClasses.map(p=>[...p]);sigma=data.sigma;}else{const raw=data.examples[choice].wake,top=Math.max(...raw.map(p=>p[0]));selected=raw.map(([t,r])=>[t-top,r]);sigma=top%2?-1:1;}drawEditor();};
 const byCap=new Map();for(const c of data.cases){const old=byCap.get(c.cap)||[0,0];old[0]++;old[1]+=c.jobs;byCap.set(c.cap,old);}
 $('caps').textContent=[...byCap].sort((a,b)=>a[0]-b[0]).map(([cap,[cases,jobs]])=>`P ≤ ${cap}: ${cases} cases / ${jobs} jobs`).join(' · ');
 $('prefixes').textContent=formatInt(data.proof.prefixVisits);drawPeriod();drawEditor();
}
if(typeof document!=='undefined')start().catch(e=>{document.getElementById('load-status').textContent=`Unable to load proof witnesses: ${e.message}`;});
