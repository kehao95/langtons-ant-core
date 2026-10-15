#!/usr/bin/env python3
"""Exact guarded-scattering certificates. Python standard library only.

Checks a restricted constructive family, NOT HC or global renewal termination.
No simulator module elsewhere in the repository is changed or imported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path

if sys.flags.optimize:
    raise RuntimeError('Run without -O: certificate assertions must remain enabled')

V = ((0, 1), (1, 0), (0, -1), (-1, 0))
BASE = {(0,6),(1,5),(0,5),(2,4),(0,4),(2,3),(-1,3),
        (1,2),(-1,2),(1,1),(2,0),(1,0),(0,0)}
WORD = ('LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLL'
        'RLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR')
# k, first-visit phase, guard x, recovery updates INCLUDING marker, output phase,
# endpoint x,y,heading. k=0: NE incoming; k=1: clockwise rotated, SE incoming.
TABLE = [
 (0,13,-3,312,97,2,6,2), (0,14,-11,416,102,2,4,1),
 (0,27,-9,520,103,4,6,0), (0,28,-33,6552,34,8,10,3),
 (0,29,-42,12792,100,18,-16,2), (0,32,-13,8528,97,22,-32,3),
 (0,38,-30,5928,27,2,-24,1), (0,55,-31,6656,76,-4,-34,0),
 (0,56,-19,7696,83,22,-24,1), (0,60,-21,2600,90,14,2,1),
 (0,61,-32,32656,51,40,-14,2), (0,62,-33,7488,17,8,-26,1),
 (0,70,-15,8632,70,30,14,3), (0,71,-25,15808,20,8,-20,0),
 (0,75,-18,3848,79,18,12,2), (0,89,-4,312,57,10,4,2),
 (1,13,-3,312,97,6,-2,3), (1,14,0,416,102,4,-2,2),
 (1,15,-14,3952,94,26,16,1), (1,27,-1,520,103,6,-4,1),
 (1,28,-26,6552,34,10,-8,0), (1,45,-25,2184,76,6,14,3),
 (1,46,-11,832,47,12,14,2), (1,47,-10,832,4,10,12,3),
 (1,57,-7,832,58,12,12,3), (1,60,-26,2600,90,2,-14,2),
 (1,61,-36,32656,51,-14,-40,3), (1,70,-13,8632,70,14,-30,0),
 (1,75,-15,3848,79,12,-18,3), (1,89,-6,312,57,4,-10,3),
]

def rot(p, k):
    x, y = p
    return ((x,y),(y,-x),(-x,-y),(-y,x))[k % 4]

def add(p, q): return (p[0]+q[0], p[1]+q[1])
def sub(p, q): return (p[0]-q[0], p[1]-q[1])
def mul(n, p): return (n*p[0], n*p[1])
def digest(B):
    return hashlib.sha256(json.dumps(sorted(B),separators=(',',':')).encode()).hexdigest()

@dataclass
class State:
    B: set[tuple[int, int]]
    p: tuple[int, int] = (0, 0)
    h: int = 1
    def copy(self): return State(self.B.copy(), self.p, self.h)
    def step(self):
        black = self.p in self.B
        self.B.symmetric_difference_update((self.p,))
        self.h = (self.h + (-1 if black else 1)) % 4
        self.p = add(self.p, V[self.h])
        return 'L' if black else 'R'

def plan(word, p=(0,0), h=1):
    positions, headings = [], []
    for c in word:
        if c not in 'LR': raise ValueError('invalid turn')
        positions.append(p); headings.append(h)
        h = (h + (1 if c == 'R' else -1)) % 4
        p = add(p, V[h])
    return positions, headings, p, h

P, H, D, _ = plan(WORD)
assert len(WORD) == 104 and D == (2,2)

def ray(v, d):
    axis = 0 if d[0] else 1
    if not d[axis] or v[axis] % d[axis]: return None
    n = v[axis] // d[axis]
    return n if mul(n,d) == v else None

def tail_breakpoints(S, word):
    """All future reads, via write-onset thresholds and finite input exceptions."""
    Q, _, end, h = plan(word, S.p, S.h); d = sub(end,S.p)
    if d == (0,0) or h != S.h: return False
    for i, p in enumerate(Q):
        thresholds, exceptions = [], set()
        for j, q in enumerate(Q):
            a = ray(sub(p,q),d)
            if a is not None and (a < 0 or (a == 0 and j < i)):
                thresholds.append(-a)
        for q in S.B:
            k = ray(sub(q,p),d)
            if k is not None and k >= 0: exceptions.add(k)
        tests = {0, *thresholds}
        for k in exceptions: tests.update((k,k+1))
        for k in tests:
            black = (k in exceptions) ^ bool(sum(t <= k for t in thresholds) % 2)
            if black != (word[i] == 'L'): return False
    return True

def tail_classes(S, word):
    """Independent all-future formulation: ordered visits to each spatial cell."""
    Q, _, end, h = plan(word,S.p,S.h); d = sub(end,S.p)
    if d == (0,0) or h != S.h: return False
    groups = []
    for i,p in enumerate(Q):
        for rep, entries in groups:
            z = ray(sub(p,rep),d)
            if z is not None:
                entries.append((i,z)); break
        else: groups.append((p,[(i,0)]))
    for rep, entries in groups:
        floor = min(z for i,z in entries)
        exceptions = set()
        for p in S.B:
            z = ray(sub(p,rep),d)
            if z is not None and z >= floor: exceptions.add(z)
        tests = {z for i,z in entries}
        for z in exceptions: tests.update((z,z+1))
        order = sorted(entries,key=lambda iz: iz[0]-len(word)*iz[1])
        for z in tests:
            colour = z in exceptions
            for i,zi in order:
                if zi <= z:
                    if colour != (word[i] == 'L'): return False
                    colour = not colour
    return True

def kernel(row):
    """Mature incoming wake in x>=guard, computed without a simulation cutoff."""
    k,j,g,*_ = row
    d = rot(D,k); Q = [rot(sub(p,P[j]),k) for p in P]
    B = set()
    for i,p in enumerate(Q):
        lo = -((p[0]-g)//d[0]); hi = 0 if i < j else -1
        for a in range(lo,hi+1): B.symmetric_difference_update((add(p,mul(a,d)),))
    assert (0,0) not in B
    B.add((0,0))
    return State(B,(0,0),(H[j]+k)%4)

def independent_replay(S, n):
    B = S.B.copy(); x,y = S.p; vx,vy = V[S.h]; word=[]; path=[]
    for _ in range(n):
        path.append((x,y))
        if (x,y) in B:
            B.remove((x,y)); vx,vy = -vy,vx; word.append('L')
        else:
            B.add((x,y)); vx,vy = vy,-vx; word.append('R')
        x += vx; y += vy
    return State(B,(x,y),V.index((vx,vy))),word,path

class LocalClock:
    """Integer-scaled r=4 clock of proof/results/clock.md, internal field only."""
    def __init__(self, points, S):
        self.x0=min(x for x,y in points); self.x1=max(x for x,y in points)
        self.y0=min(y for x,y in points); self.y1=max(y for x,y in points)
        self.c=(self.x0+self.x1+self.y0+self.y1)//2
        self.M=max(abs(self.x0+self.y0-self.c),abs(self.x1+self.y1-self.c))
        self.den=2*4**self.M
        self.sigma=(-1 if sum(S.p)%2 else 1)*(1 if S.h%2==0 else -1)
        cells=[(x,y) for x in range(self.x0,self.x1+1) for y in range(self.y0,self.y1+1)]
        self.upper=5*sum(self.f(p) for p in cells)+max(abs(self.g(p,h)) for p in cells for h in (0,2))
        self.value=self.full(S)
    def inside(self,p): return self.x0<=p[0]<=self.x1 and self.y0<=p[1]<=self.y1
    def uv(self,p):
        s=sum(p)-self.c
        return 4**(self.M+s),4**(self.M-s)
    def f(self,p):
        u,v=self.uv(p); return u+v
    def g(self,p,h):
        u,v=self.uv(p)
        return 2*(u-4*v) if h in (0,1) else 2*(v-4*u)
    def field(self,p): return -5*self.sigma*(-1 if sum(p)%2 else 1)*self.f(p)
    def full(self,S): return sum(self.field(p) for p in S.B if self.inside(p))+self.g(S.p,S.h)
    def fuel(self): return (self.upper-self.value+self.den-1)//self.den
    def advance(self,p,h,black,S):
        assert self.inside(p) and self.inside(S.p)
        before=self.fuel()
        delta=(-1 if black else 1)*self.field(p)+self.g(S.p,S.h)-self.g(p,h)
        assert delta>=self.den
        self.value+=delta
        assert 0<=self.fuel()<before

def check_kernels():
    reports=[]; outputs={}
    assert tail_breakpoints(State(BASE.copy()),WORD)
    assert tail_classes(State(BASE.copy()),WORD)
    fresh=[]
    for i,p in enumerate(P):
        if all(not ((a:=ray(sub(p,q),D)) is not None and (a<0 or (a==0 and j<i))) for j,q in enumerate(P)):
            fresh.append(i)
    assert len(fresh)==22
    for row in TABLE:
        k,j,g,t,a,x,y,h=row
        assert j in fresh
        S=kernel(row); other,words,path=independent_replay(S,t)
        assert other.p==(x,y) and other.h==h
        w=(WORD*2)[a:a+104]; Q,_,end,fh=plan(w,other.p,other.h)
        d=sub(end,other.p); kout=0 if d==(2,2) else 1 if d==(2,-2) else None
        assert kout is not None and fh==h and h==(H[a]+kout)%4
        assert min(p[0] for p in path+Q)>=g
        assert tail_breakpoints(other,w) and tail_classes(other,w)
        C=LocalClock(path+[other.p],S); fuel=C.fuel(); real=S.copy()
        for c in words:
            p,h0=real.p,real.h; black=p in real.B
            assert real.step()==c
            C.advance(p,h0,black,real)
        assert real==other and C.value==C.full(real)
        # A wrong colour at the next read must fail both infinite tests.
        bad=real.copy();bad.B.symmetric_difference_update((bad.p,))
        assert not tail_breakpoints(bad,w) and not tail_classes(bad,w)
        report={'k':k,'phase':j,'guard':g,'updates':t,'out_k':kout,'out_phase':a,
                'end':list(other.p),'heading':other.h,'black_in':len(S.B),'black_out':len(other.B),
                'input_sha256':digest(S.B),'output_sha256':digest(other.B),
                'max_prefix_x':max(p[0] for p in path),'max_end_x':max(p[0] for p in other.B),
                'tail_min_x':min(p[0] for p in Q),'clock_initial_fuel':str(fuel),
                'clock_final_fuel':str(C.fuel())}
        reports.append(report); outputs[k,j]=(row,other,report)
    return fresh,reports,outputs

def connector_checks(outputs, gap=100):
    slacks=[]; displacements=[]; initial_slacks=[]
    for row,S,r in outputs.values():
        k,a=r['out_k'],r['out_phase']; pa=rot(P[a],k)
        # The entire synthetic pre-output standard past has this maximum x.
        synthetic=max(rot(p,k)[0]-pa[0]+(0 if i<a else -2) for i,p in enumerate(P))
        oldmax=max(r['max_prefix_x'],r['max_end_x'],S.p[0]+synthetic,r['guard'])
        for row2,_,rr in outputs.values():
            if row2[0]!=k:continue
            j,g=row2[1:3]
            dx=S.p[0]+2*(gap+int(j<a))+rot(P[j],k)[0]-pa[0]
            slack=dx+g-oldmax
            assert slack>0
            # Earlier flight reads lie at most 2 canonical spans beyond their target.
            span=max(max(rot(p,kk)[0] for p in P)-min(rot(p,kk)[0] for p in P) for kk in (0,1))
            assert dx>2*span+2
            slacks.append(slack);displacements.append(dx)
    for row,_,r in outputs.values():
        if row[0]!=0: continue
        j,g=row[1:3]; qx=2*gap+P[j][0]
        synthetic=max(p[0]-2 for p in P)
        slack=qx+g-max(max(x for x,y in BASE),synthetic)
        assert slack>0
        initial_slacks.append(slack)
    assert len(slacks)==448
    return {'pairs':len(slacks),'min_guard_slack':min(slacks),
            'min_marker_dx':min(displacements),'initial_cases':len(initial_slacks),
            'min_initial_slack':min(initial_slacks)}

def construct(spec):
    """All markers are placed at time zero. spec contains (phase, gap>=100)."""
    rows={(r[0],r[1]):r for r in TABLE}
    p=(0,0); k=a=t=0; markers=[]; events=[]
    for j,n in spec:
        if not isinstance(n,int) or isinstance(n,bool) or n<100: raise ValueError('gap must be an integer >=100')
        if (k,j) not in rows: raise ValueError('unsupported scattering phase')
        row=rows[k,j]; delta=(j-a)%104
        q=add(p,add(mul(n+int(j<a),rot(D,k)),rot(sub(P[j],P[a]),k)))
        t+=104*n+delta
        markers.append(q);events.append((t,q,row))
        p=add(q,(row[5],row[6])); t+=row[3];a=row[4]
        _,_,end,_=plan((WORD*2)[a:a+104],p,row[7]);d=sub(end,p)
        k=0 if d==(2,2) else 1
    assert len(set(markers))==len(markers)
    return State(BASE|set(markers)),events,t,p,k,a

def replay_train(spec, west=()):
    S,events,T,endpoint,k,a=construct(spec)
    if any(x>=-1 for x,y in west): raise ValueError('unprotected debris')
    S.B.update(west);pending={q for _,q,_ in events}
    indexed={t:(i,q,row) for i,(t,q,row) in enumerate(events)}
    guard=-1;turns=0;contact_checks=0
    for t in range(T):
        if t in indexed:
            i,q,row=indexed[t];assert S.p==q and q in S.B
            guard=q[0]+row[2]
            expected={add(q,v) for v in kernel(row).B}|{z for _,z,_ in events[i+1:]}
            assert {v for v in S.B if v[0]>=guard}==expected
            pending.remove(q);contact_checks+=1
        else: assert S.p not in pending
        assert S.p[0]>=guard
        S.step();turns+=1
    assert S.p==endpoint and not pending
    w=(WORD*2)[a:a+104]
    assert S.h==(H[a]+k)%4
    assert tail_breakpoints(S,w) and tail_classes(S,w)
    return {'markers':len(spec),'updates':turns,'contacts':contact_checks,'final_black':len(S.B),
            'final_field_sha256':digest(S.B)}

def make_spec(length, rng, gap=100):
    k=0; spec=[]
    for _ in range(length):
        row=rng.choice([r for r in TABLE if r[0]==k]);j=row[1]
        spec.append((j,gap+rng.randrange(4)))
        _,_,end,_=plan((WORD*2)[row[4]:row[4]+104],(row[5],row[6]),row[7])
        d=sub(end,(row[5],row[6]));k=0 if d==(2,2) else 1
    return spec

def check_all():
    fresh,reports,outputs=check_kernels()
    composition=connector_checks(outputs)
    huge=connector_checks(outputs,10**60)
    rng=random.Random(230315)
    runs=[]
    # Every initial type, all output types through random long strings, and both turns.
    for row in TABLE:
        if row[0]==0:runs.append(replay_train([(row[1],100)],west=[(-2,17),(-100,-500)]))
    for length in (2,2,3,3,5,8,13,21,34,55):
        runs.append(replay_train(make_spec(length,rng),west=[(-2,10**8),(-3,-10**8),(-17,0)]))
    # Directed zigzag repeats NE->SE phase29 and SE->NE phase15.
    zigzag=[(29,100),(15,100)]*12
    runs.append(replay_train(zigzag))
    astronomical=construct([(29,10**60),(15,10**60),(13,10**60)])
    assert len(astronomical[0].B)==16
    for spec in ([(72,100)],[(13,99)]):
        try: construct(spec)
        except ValueError: pass
        else: raise AssertionError('scope rejection missing')
    bad=State(BASE.copy());bad.B.add(add(P[13],mul(10**60,D)))
    assert not tail_breakpoints(bad,WORD) and not tail_classes(bad,WORD)
    return {'schema':1,'status':'restricted analytic theorem with exact certificates; not HC',
            'fresh_phases':fresh,'kernel_count':len(reports),'composition':composition,
            'kernel_certificate_sha256':hashlib.sha256(json.dumps(reports,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'train_certificate_sha256':hashlib.sha256(json.dumps(runs,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'largest_kernel_output_black':max(r['black_out'] for r in reports),
            'huge_gap_pairs':huge['pairs'],'huge_gap':str(10**60),
            'literal_kernel_updates_per_simulator':sum(r[3] for r in TABLE),
            'clock_step_checks':sum(r[3] for r in TABLE),
            'train_cases':len(runs),'train_markers':sum(r['markers'] for r in runs),
            'train_updates':sum(r['updates'] for r in runs),'zigzag_24':runs[-1],
            'negative_controls':{'wrong_tail_current_colour':30,'remote_tail_blocker':1,
                                 'unsupported_phase':1,'insufficient_gap':1},
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-report',type=Path)
    parser.add_argument('--compare',type=Path)
    args=parser.parse_args();report=check_all()
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.compare:
        assert json.loads(args.compare.read_text())==report,'retained report differs'
    if args.write_report: args.write_report.write_text(text)
    print(json.dumps({k:v for k,v in report.items() if k not in ('kernels','trains')},indent=2))

if __name__=='__main__': main()
