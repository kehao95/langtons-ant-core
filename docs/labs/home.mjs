import {createState,step,renderGrid,setupPage} from './common.mjs';
setupPage('home');
const buttons=[...document.querySelectorAll('[data-filter]')];
for(const button of buttons)button.addEventListener('click',()=>{
  const chosen=button.dataset.filter;
  for(const b of buttons)b.setAttribute('aria-pressed',String(b===button));
  let count=0;
  for(const card of document.querySelectorAll('[data-topics]')){card.hidden=chosen!=='all'&&!card.dataset.topics.split(' ').includes(chosen);if(!card.hidden)count++;}
  document.querySelector('#filter-status').textContent=chosen==='all'?'Showing all six laboratories.':`Showing ${count} laboratories · ${button.textContent}.`;
});
try{
  const response=await fetch('./data/wake.json');if(!response.ok)throw new Error('Could not load the highway witness.');
  const data=await response.json();let state=createState(data.seed,[0,0],data.heading);let cycles=0;
  const canvas=document.querySelector('#hero-ant');const button=document.querySelector('#hero-step');
  const draw=()=>{const next=createState(state.black,[state.x,state.y],state.h),path=[];for(let i=0;i<208;i++){path.push([next.x,next.y]);step(next);}
    renderGrid(canvas,state,{path});document.querySelector('#hero-caption').textContent=`Period 104 · ${cycles} cycles · ${state.black.size} black cells`;};
  button.addEventListener('click',()=>{if(cycles===8){state=createState(data.seed,[0,0],data.heading);cycles=0;}else{for(let i=0;i<104;i++)step(state);cycles++;}button.textContent=cycles===8?'Reset the seed ↺':'Advance 104 steps ↗';draw();});draw();
}catch(error){const node=document.querySelector('#hero-error');node.hidden=false;node.textContent=error.message;document.querySelector('#hero-step').disabled=true;}
