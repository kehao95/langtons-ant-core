"""Independent coordinate-vector dynamics and exact infinite-phase verification."""
from __future__ import annotations
from collections import defaultdict

DIRECTIONS=((0,1),(1,0),(0,-1),(-1,0))

class State:
    def __init__(self,black,pose):
        self.black=set(black);self.x,self.y,h=pose
        self.dx,self.dy=DIRECTIONS[h]
    @property
    def pose(self):return self.x,self.y,DIRECTIONS.index((self.dx,self.dy))
    def step(self):
        p=self.x,self.y
        if p in self.black:
            self.black.remove(p);self.dx,self.dy=-self.dy,self.dx;c='L'
        else:
            self.black.add(p);self.dx,self.dy=self.dy,-self.dx;c='R'
        self.x+=self.dx;self.y+=self.dy
        return c


def geometry(word,pose):
    x,y,h=pose;dx,dy=DIRECTIONS[h];ps=[]
    for c in word:
        if c not in 'RL':raise ValueError('LR word required')
        ps.append((x,y));dx,dy=(dy,-dx)if c=='R'else(-dy,dx);x+=dx;y+=dy
    return ps,(x,y,DIRECTIONS.index((dx,dy)))


def permanent(black,pose,word):
    """Full initial-field translation-class grouping, then exact event epochs.

    This does not call the affine source/chronology code. It is a concrete-state
    infinite-future theorem, not a repeat-length detector.
    """
    ps,end=geometry(word,pose);d=end[0]-pose[0],end[1]-pose[1]
    if end[2]!=pose[2]or d==(0,0):return False
    axis=0 if d[0]else 1;den=d[axis]
    def key(p):return(p[0]*d[1]-p[1]*d[0],p[axis]%abs(den))
    def level(p):return p[axis]//den
    classes=defaultdict(set)
    for p in black:classes[key(p)].add(level(p))
    phases=defaultdict(list)
    for i,p in enumerate(ps):phases[key(p)].append((i,level(p)))
    for i,(p,c)in enumerate(zip(ps,word)):
        height=level(p)
        previous=[jlevel-height for j,jlevel in phases[key(p)]
                  if jlevel>height or jlevel==height and j<i]
        hits={z-height for z in classes[key(p)]if z>=height}
        points={0,*previous,*hits,*(n+1 for n in hits)};points.add(max(points)+1)
        for n in points:
            actual=(n in hits)^bool(sum(q<=n for q in previous)%2)
            if actual!=(c=='L'):return False
    return True


def finite_halfstrip_guard(path,pose,word,width,side):
    """The whole supplied finite path and infinite tail avoid extra columns."""
    def valid(p):
        x,y=p
        return not 0<=y<5 or (x>=0 if side=='left'else x<width)
    if any(not valid(p)for p in path):return False
    ps,end=geometry(word,pose);d=end[0]-pose[0],end[1]-pose[1]
    if d[1]==0:raise ValueError('diagonal tail required')
    for x,y in ps:
        for row in range(5):
            delta=row-y
            if delta%d[1]==0 and delta//d[1]>=0:
                n=delta//d[1]
                if not valid((x+n*d[0],row)):return False
    return True
