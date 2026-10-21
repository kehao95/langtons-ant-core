"""Exact contour-surgery pilot. No HC theorem or permanent sealing claim.

Frozen routing is not the physical time evolution. The physical update uses
its old successor and then swaps the two incoming ports at the updated site.
Run with --write only when intentionally producing a new report. Default
execution regenerates and compares the immutable deterministic report.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random

DIR=((0,1),(1,0),(0,-1),(-1,0))
Edge=tuple[int,int,int]
Point=tuple[int,int]

def default_successor(e: Edge)->Edge:
    x,y,h=e; h=(h+1)%4; dx,dy=DIR[h]
    return x+dx,y+dy,h

def frozen_successor(e: Edge, black: set[Point])->Edge:
    x,y,h=e; h=(h+(-1 if (x,y) in black else 1))%4
    dx,dy=DIR[h]
    return x+dx,y+dy,h

def opposite(e: Edge)->Edge:
    return e[0],e[1],(e[2]+2)%4

def frozen_cycle(e: Edge, black: set[Point])->tuple[Edge,...]:
    # Exact finite-modification bound, explained in the accompanying note.
    cap=8*len(black)+4
    cur=e; result=[]; seen=set()
    for _ in range(cap):
        if cur in seen:
            raise AssertionError('non-root recurrence contradicts permutation')
        seen.add(cur); result.append(cur)
        cur=frozen_successor(cur,black)
        if cur==e: return tuple(result)
    raise AssertionError('finite-modification cycle bound violated')

def surgery_check(black: set[Point], root: Edge)->dict:
    old=set(frozen_cycle(root,black)); other=opposite(root)
    old_other=set(frozen_cycle(other,black))
    following=frozen_successor(root,black)
    updated=black ^ {root[:2]}
    # P_(B xor {q}) = P_B o tau_q, including both ports.
    assert frozen_successor(root,updated)==frozen_successor(other,black)
    assert frozen_successor(other,updated)==following
    active=set(frozen_cycle(following,updated))
    if other in old:
        detached=set(frozen_cycle(root,updated))
        assert active and detached and active.isdisjoint(detached)
        assert active|detached==old
        assert other in active and root in detached
        assert root[:2] in {e[:2] for e in active}&{e[:2] for e in detached}
        kind='split'
    else:
        assert old.isdisjoint(old_other)
        assert active==old|old_other
        detached=set();kind='merge'
    return dict(kind=kind,active_before=len(old),other_before=len(old_other),
                active_after=len(active),detached_after=len(detached))

class PermutationAnt:
    """Sparse finite deviation of the all-right successor permutation."""
    def __init__(self, black: set[Point], root: Edge):
        self.root=root
        self.sector=(root[2]-root[0]-root[1])%2
        self.overrides={}
        for x,y in black:
            h=(x+y+self.sector)%2
            for hh in (h,h+2):
                e=(x,y,hh)
                self.overrides[e]=default_successor(opposite(e))
    def image(self,e: Edge)->Edge:
        return self.overrides.get(e,default_successor(e))
    def step(self)->None:
        e=self.root; z=opposite(e)
        a,b=self.image(e),self.image(z)
        for key,value in ((e,b),(z,a)):
            if value==default_successor(key): self.overrides.pop(key,None)
            else: self.overrides[key]=value
        self.root=a
    def complete_black(self)->set[Point]:
        result={e[:2] for e in self.overrides}
        assert len(self.overrides)==2*len(result)
        return result

def vector_step(black: set[Point], position: Point, vector: Point):
    # An independent physical representation: no heading-index turn table.
    dx,dy=vector
    if position in black:
        vector=(-dy,dx); black.remove(position);letter='L'
    else:
        vector=(dy,-dx); black.add(position);letter='R'
    return (position[0]+vector[0],position[1]+vector[1]),vector,letter

def run()->dict:
    cells=[(x,y) for x in range(-1,2) for y in range(-1,2)]
    kinds=Counter()
    for mask in range(1<<len(cells)):
        black={p for i,p in enumerate(cells) if mask>>i&1}
        for h in range(4):
            r=surgery_check(black,(0,0,h)); kinds[r['kind']]+=1
    rng=random.Random(20261020)
    updates=0; full_checks=0; digest=sha256()
    for case in range(33):
        initial=set() if case==0 else {(rng.randrange(-6,7),rng.randrange(-6,7))
                                      for _ in range(rng.randrange(25))}
        if case%7==0 and case:
            initial.add((10**60+case,-10**60))
        h=0 if case==0 else rng.randrange(4)
        model=PermutationAnt(initial,(0,0,h))
        physical=set(initial);p=(0,0);v=DIR[h]
        duration=12000 if case==0 else 512
        for t in range(duration):
            model.step();p,v,c=vector_step(physical,p,v)
            assert model.root==(p[0],p[1],DIR.index(v))
            assert model.complete_black()==physical
            digest.update(f'{case},{t},{p},{v},{c}\n'.encode())
            updates+=1;full_checks+=1
    # Frozen contours separated at update 4 rejoin at update 8 on ONE blank orbit.
    black=set();e=(0,0,0);detached=None;witness=[];word=[]
    for t in range(9):
        r=surgery_check(black,e)
        if t==4:
            assert r==dict(kind='split',active_before=20,other_before=20,
                           active_after=4,detached_after=16)
            detached=set(frozen_cycle(e,black^{e[:2]}))
        if 5<=t<=8:
            assert detached is not None
            assert set(frozen_cycle(min(detached),black))==detached
        if t==8:
            assert set(frozen_cycle(opposite(e),black))==detached
            assert r==dict(kind='merge',active_before=16,other_before=16,
                           active_after=32,detached_after=0)
        witness.append(dict(update=t,root=list(e),initial_field=[list(q) for q in sorted(black)],**r))
        word.append('L' if e[:2] in black else 'R')
        following=frozen_successor(e,black);black.symmetric_difference_update({e[:2]});e=following
    assert ''.join(word)=='RRRRLRRRR'
    return dict(schema='contour-surgery-pivot-v1',status='passed',
                scope='exact representation and finite controls only; no HC advance claimed',
                local_fields=512,headings=4,one_step_surgeries=dict(kinds),
                complete_orbit_inputs=33,physical_updates=updates,
                complete_field_equalities=full_checks,orbit_trace_sha256=digest.hexdigest(),
                separated_cycle_rejoins=dict(split_update=4,rejoin_update=8,
                    detached_directed_arcs=16,prefix=''.join(word)),
                prefix_witness=witness,
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    args=parser.parse_args(); path=Path(__file__).with_name('report.json')
    result=run()
    if args.write:
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    else:
        expected=json.loads(path.read_text())
        if result!=expected:raise AssertionError('frozen report differs')
    print(json.dumps({k:v for k,v in result.items() if k!='prefix_witness'},indent=2))
if __name__=='__main__': main()
