"""All-length axis-strip geometry via complete finite covering certificates.

No ant input is assumed to occupy a strip. This proves a conditional geometric
statement about every physically feasible ten-legal FINITE word, and its
cross-event localization corollary. It does not prove HC or bounded-J10 termination.
"""
from __future__ import annotations
from collections import defaultdict, deque, Counter
import argparse, hashlib, json, random, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE='53f98d2e93614a8eea5424b0bb967c7311bb97f7'
W=('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
   'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')
A='LLRRRRLRRLRRRRLLLLRLRRRRLRLL'
B=('RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR'
   'LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL')
T='RRRRLLRLLRRRRLLRRRRLLRLL'
DIR=((0,1),(1,0),(0,-1),(-1,0))
NORMALS=((1,0),(0,1),(-1,0),(0,-1))
LEGAL={(W*2)[i:i+10] for i in range(104)}
EXPECTED_WORD_HASH='6b76e51621e15d2304f1c0baa28790cc267cabafca3fc03250dea8721b2b4794'

def sha(raw:bytes)->str:return hashlib.sha256(raw).hexdigest()
def geom(w,h=0):
 p=(0,0);positions=[]
 for c in w:
  positions.append(p);h=(h+(1 if c=='R' else -1))%4
  d=DIR[h];p=(p[0]+d[0],p[1]+d[1])
 return positions,p,h

def realization(w):
 ps,p,h=geom(w);last={};seed=set()
 for q,c in zip(ps,w):
  if q not in last:
   if c=='L':seed.add(q)
  elif last[q]==c:return None
  last[q]=c
 return seed

def enumerate_words():
 # Start at zero so EVERY physically feasible short word is also covered.
 states=[('',(0,0),0,{})];counts=[1];short_radius=0
 for depth in range(1,151):
  out=[]
  for w,p,h,last in states:
   for c in 'RL':
    if depth>=10 and w[-9:]+c not in LEGAL:continue
    if last.get(p)==c:continue
    ll=last.copy();ll[p]=c;hh=(h+(1 if c=='R' else -1))%4
    dx,dy=DIR[hh];q=(p[0]+dx,p[1]+dy)
    out.append((w+c,q,hh,ll))
    if depth<=149:short_radius=max(short_radius,abs(q[0]),abs(q[1]))
  states=out;counts.append(len(states))
 return sorted(v[0] for v in states),counts,short_radius

def sccs(adj):
 rev={v:set() for v in adj}
 for v in adj:
  for u in adj[v]:rev[u].add(v)
 visited=set();order=[]
 for v in sorted(adj):
  if v in visited:continue
  visited.add(v);stack=[(v,iter(sorted(adj[v])))]
  while stack:
   x,it=stack[-1];y=next(it,None)
   if y is None:order.append(x);stack.pop()
   elif y not in visited:visited.add(y);stack.append((y,iter(sorted(adj[y]))))
 visited=set();comps=[]
 for v in reversed(order):
  if v in visited:continue
  visited.add(v);comp={v};stack=[v]
  while stack:
   for u in rev[stack.pop()]:
    if u not in visited:visited.add(u);comp.add(u);stack.append(u)
  comps.append(comp)
 return comps

def make_graph(words):
 adj=defaultdict(set)
 for w in words:adj[w[:-1]].add(w[1:]);adj[w[1:]]
 components=sccs(adj)
 assert sorted(len(c) for c in components if len(c)>1)==[24,104,366]
 H=next(c for c in components if len(c)==366);mapping={}
 for v in sorted(H):
  states=set(range(102))
  for c in v:
   states={(q+1)%102 for q in states if B[q]==c}|({75} if 0 in states and c=='L' else set())
  if len(states)!=1:raise AssertionError('nonunique inherited quotient')
  mapping[v]=states.pop()
 qtext=''.join(v+'\t'+str(mapping[v])+'\n' for v in sorted(mapping))
 assert sha(qtext.encode())=='f6d5502737c0ce931c1f9ca62a62ad8307157b4133c8f087f7ac0268b0d05682'
 model={(j,B[j]):(j+1)%102 for j in range(102)};model[0,'L']=75
 for v in H:
  for u in adj[v]&H:assert model[mapping[v],u[-1]]==mapping[u]
 lift={}
 for v in sorted(adj):
  for count in range(4) if v in H else [0]:
   if count==3 and mapping[v]==0:continue
   lift[v,count]=set()
   for u in adj[v]:
    n=count+int(mapping[v]==0 and u[-1]=='R') if v in H and u in H else 0
    if u in H and (n>3 or n==3 and mapping[u]==0):continue
    lift[v,count].add((u,n))
 assert (len(adj),len(lift),sum(map(len,lift.values())))==(6501,7595,7763)
 G={(v,c,h):{(u,n,(h+(1 if u[-1]=='R' else -1))%4) for u,n in out}
    for (v,c),out in lift.items() for h in range(4)}
 return dict(adj),G,mapping

def classify(G):
 comps=sccs(G);cid={v:i for i,c in enumerate(comps) for v in c}
 cyclic={i for i,c in enumerate(comps) if len(c)>1 or any(v in G[v] for v in c)}
 masks={};cycles=[]
 for i in sorted(cyclic):
  start=min(comps[i]);v=start;word=''
  while True:
   out=G[v]&comps[i];assert len(out)==1
   v=next(iter(out));word+=v[0][-1]
   if v==start:break
  _,d,h=geom(word,start[2]);assert h==start[2] and d!=(0,0)
  masks[i]=sum(1<<b for b,n in enumerate(NORMALS) if n[0]*d[0]+n[1]*d[1]>=0)
  cycles.append((len(word),d,masks[i]))
 dag={i:set() for i in range(len(comps))};degree={i:0 for i in dag}
 for v in G:
  for u in G[v]:
   if cid[v]!=cid[u]:dag[cid[v]].add(cid[u])
 for i in dag:
  for j in dag[i]:degree[j]+=1
 queue=deque(sorted(i for i in dag if not degree[i]));top=[]
 while queue:
  i=queue.popleft();top.append(i)
  for j in sorted(dag[i]):
   degree[j]-=1
   if not degree[j]:queue.append(j)
 assert len(top)==len(dag)
 return comps,cid,cyclic,masks,cycles,dag,top

def mask_certificate(G,comps,cid,masks,dag,top):
 # Finite DAG certificate for ALL paths, not a collection of sampled paths.
 seen={i:{masks.get(i,15)} for i in dag}
 for i in top:
  for j in dag[i]:seen[j]|={m&masks.get(j,15) for m in seen[i]}
 assert all(0 not in v for v in seen.values())
 for i in dag:
  assert masks.get(i,15) in seen[i]
  for j in dag[i]:assert {m&masks.get(j,15) for m in seen[i]}<=seen[j]
 # Independent full-node fixed point; no condensation order is used here.
 node_masks={v:masks.get(cid[v],15) for v in G}
 reached={v:{node_masks[v]} for v in G};queue=deque((v,node_masks[v]) for v in sorted(G))
 while queue:
  v,m=queue.popleft()
  for u in G[v]:
   mm=m&node_masks[u]
   assert mm!=0
   if mm not in reached[u]:reached[u].add(mm);queue.append((u,mm))
 assert all(reached[v]==seen[cid[v]] for v in G)
 return {'condensation_mask_states':sum(map(len,seen.values())),
         'node_mask_states':sum(map(len,reached.values())),
         'zero_mask_reachable':False,'independent_fixed_point_equal':True}

def potentials(adj,G,cid,masks):
 reports=[];all_prelude=[];damaged_rejected=False
 for bit,norm in enumerate(NORMALS):
  allowed={v for v in G if masks.get(cid[v],15)&(1<<bit)}
  rev={v:[] for v in allowed}
  for v in allowed:
   for u in G[v]:
    if u in allowed:
     dx,dy=DIR[u[2]];cost=-(norm[0]*dx+norm[1]*dy);rev[u].append((v,cost))
  h={v:0 for v in allowed};queue=deque(sorted(allowed));inq=set(allowed)
  while queue:
   u=queue.popleft();inq.remove(u)
   for v,cost in rev[u]:
    val=h[u]+cost
    if val>h[v]:
     h[v]=val
     if val>10000:raise RuntimeError('certificate generator cap; no theorem inferred')
     if v not in inq:queue.append(v);inq.add(v)
  assert min(h.values())==0 and max(h.values())==33
  for u in rev:
   for v,cost in rev[u]:assert h[v]>=h[u]+cost
  low=high=absolute=0;prelude_count=0
  for w in sorted(adj):
   ps,p,hh=geom(w);v=(w,0,hh)
   if v not in allowed:continue
   z=[norm[0]*q[0]+norm[1]*q[1] for q in ps+[p]]
   low=max(low,-min(z),h[v]-z[-1])
   high=max(high,max(z)-z[-1]+h[v])
   absolute=max(absolute,max(map(abs,z)));prelude_count+=1
  assert max(low,high)<=43
  blob=''.join(f'{v[0]}\t{v[1]}\t{v[2]}\t{h[v]}\n' for v in sorted(allowed))
  reports.append({'normal':norm,'vertices':len(allowed),'edges':sum(map(len,rev.values())),
                  'max_potential':33,'potential_sha256':sha(blob.encode()),
                  'prelude_states':prelude_count,'lower_allowance':low,'upper_allowance':high})
  # All-zero potential must fail at an actual negative-coordinate edge.
  if not damaged_rejected:
   damaged_rejected=any(cost>0 for incoming in rev.values() for v,cost in incoming)
 assert damaged_rejected
 return reports,damaged_rejected

def count_defects(w):return sum(w[i-9:i+1] not in LEGAL for i in range(9,len(w)))
def in_tube(ps,p,q,radius=43):
 return any(all(min(p[c],q[c])-radius<=z[c]<=max(p[c],q[c])+radius for z in ps) for c in (0,1))
def direction_property(positions):
 # Linear-time direct check of the oriented conclusion; no finite graph used.
 p=positions[0];q=positions[-1]
 for n in NORMALS:
  z=[n[0]*(r[0]-p[0])+n[1]*(r[1]-p[1]) for r in positions]
  if min(z)<-43 or max(z)>z[-1]+43:continue
  record=-10**9;retreat=0
  for a in z[149:]:record=max(record,a);retreat=max(retreat,record-a)
  if retreat<=33:return True
 return False

def simulate(seed,steps,p=(0,0),h=0):
 black=set(seed);word=[];poses=[p]
 for _ in range(steps):
  c='L' if p in black else 'R';word.append(c)
  if p in black:black.remove(p)
  else:black.add(p)
  h=(h+(1 if c=='R' else -1))%4;d=DIR[h];p=(p[0]+d[0],p[1]+d[1]);poses.append(p)
 return ''.join(word),poses,black,h

def controls():
 # Imported silent fold family: used only as an exact scope control.
 C='RLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLL'
 D='LLRRRRLRRLRRRRLLLLRLRRRRLRL'
 assert (len(C),len(D))==(44,27)
 folds=[];updates=0
 for n in (0,1,2,5,20,100,1000):
  w=C+A*(n+6)+B+A*(n+2)+D;seed=realization(w)
  assert seed is not None and len(seed)==10*n+76 and count_defects(w)==0
  got,ps,out,h=simulate(seed,len(w));updates+=len(w)
  assert got==w and in_tube(ps,ps[0],ps[-1]) and direction_property(ps)
  folds.append({'n':n,'length':len(w),'black':len(seed),'end':ps[-1],
                'x_range':[min(x for x,y in ps),max(x for x,y in ps)],
                'y_range':[min(y for x,y in ps),max(y for x,y in ps)]})
 # An ACTUAL interval with defects that leaves both return strips.
 port={(0,-1),(1,1),(1,3),(2,2)};n=40
 starts=[((0,0),1),((n-1,n),0),((-n,3*n-4),3),((-5*n+5,-n),2),((-3*n,-3*n+8),1)]
 def rot(q,k):
  x,y=q
  for _ in range(k%4):x,y=y,-x
  return x,y
 seed=set()
 for p,h in starts:
  for z in port:
   x,y=rot(z,h-1);seed.add((p[0]+x,p[1]+y))
 assert len(seed)==20
 word,ps,out,h=simulate(seed,624*n-1516,h=1)
 assert ps[-1]==(0,2) and not in_tube(ps,ps[0],ps[-1]) and count_defects(word)>0
 # Further independent tests on real complete inputs: split at each bad ending letter.
 rng=random.Random(1576);pieces=0;literal_updates=0
 for _ in range(48):
  seed={(rng.randrange(-5,6),rng.randrange(-5,6)) for j in range(rng.randrange(24))}
  w,ps,_,_=simulate(seed,1800,h=rng.randrange(4));literal_updates+=len(w);start=0
  for i in range(len(w)):
   if i>=9 and w[i-9:i+1] not in LEGAL:
    assert count_defects(w[start:i])==0 and in_tube(ps[start:i+1],ps[start],ps[i]) and direction_property(ps[start:i+1]);pieces+=1;start=i+1
  assert in_tube(ps[start:],ps[start],ps[-1]) and direction_property(ps[start:]);pieces+=1
 return {'silent_fold_family':folds,'silent_fold_literal_updates':updates,
         'defect_required_control':{'initial_black':20,'length':len(word),'defects':count_defects(word),'violates_both_tubes':True},
         'random_complete_inputs':48,'random_literal_updates':literal_updates,'silent_subwords_checked':pieces}

def run():
 words,counts,radius=enumerate_words();raw='\n'.join(words)+'\n'
 assert sha(raw.encode())==EXPECTED_WORD_HASH and len(words)==6605
 with tempfile.TemporaryDirectory(prefix='ant-axis-') as td:
  td=Path(td);exe=td/'independent';cpp=ROOT/'independent.cpp'
  subprocess.run(['g++','-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True,timeout=30)
  subprocess.run([str(exe),str(td/'words.txt'),str(td/'stats.json')],check=True,timeout=40)
  ns=json.loads((td/'stats.json').read_text())
  assert (td/'words.txt').read_text()==raw and ns['counts']==counts and ns['short_radius']==radius
 assert radius==24
 adj,G,mapping=make_graph(words);comps,cid,cyclic,masks,cycles,dag,top=classify(G)
 mask_report=mask_certificate(G,comps,cid,masks,dag,top)
 certs,damaged=potentials(adj,G,cid,masks)
 result={'schema':'silent-axis-geometry-v1','base_commit':BASE,'status':'passed',
  'word_count':len(words),'word_sha256':sha(raw.encode()),'short_word_counts_sha256':sha(json.dumps(counts,separators=(',',':')).encode()),
  'short_word_max_radius':radius,'independent_cpp_words_and_all_levels_equal':True,
  'oriented_vertices':len(G),'oriented_edges':sum(map(len,G.values())),
  'oriented_cyclic_components':sorted(cycles),'mask_certificate':mask_report,
  'potentials':certs,'damaged_zero_potential_rejected':damaged,
  'return_tube_radius':43,'event_cross_padding':44,'controls':controls(),
  'scope':'Analytic all-length coverage plus exact finite certificates; no HC proof, no global J10 budget, no bounded-J10 termination.',
  'sources_sha256':{p:sha((ROOT/p).read_bytes()) for p in ['check.py','independent.cpp']}}
 return json.loads(json.dumps(result))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');parser.add_argument('--report',default=str(ROOT/'report.json'))
 args=parser.parse_args();data=run();path=Path(args.report)
 if args.generate:path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 else:
  expected=json.loads(path.read_text());assert data==expected,'frozen report mismatch'
 print(json.dumps({'status':'passed','oriented_vertices':data['oriented_vertices'],'radius':data['return_tube_radius'],
                   'independent_words':data['word_count'],'edge_checks':sum(p['edges'] for p in data['potentials'])}))
