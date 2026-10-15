#!/usr/bin/env python3
"""Independent controls: complex-coordinate transitions and online colour-tree.
Does not import check.py or its recursion/list-of-given-seeds.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
TARGET={(0,-1),(1,1),(1,3),(2,2)}
SHARP={(0,-1),(2,1),(3,3)}

def require(test,msg):
    if not test:raise AssertionError(msg)

def complex_run(seed,n,start_heading=1+0j):
    board={complex(*q) for q in seed}
    p=0j;h=start_heading;minx=0;word=[]
    for t in range(n):
        minx=min(minx,int(p.real))
        b=p in board
        if b:board.remove(p);h*=1j
        else:board.add(p);h*=-1j
        word.append('L' if b else 'R')
        p+=h
    return ({(int(z.real),int(z.imag)) for z in board},
            (int(p.real),int(p.imag)),h,minx,''.join(word))

def online_escape_tree(k=3):
    """At every *first* read independently branch WHITE or BLACK initial bit.
    The second implementation branches in time, not over known seed sets.
    """
    stats=Counter();peak=-1;winner=None
    import sys
    sys.setrecursionlimit(3000)
    def walk(p,h,board,visited,chosen,t):
        nonlocal peak,winner
        require(t<=920, 'counterexample to 918 uniform exit')
        if p.real<0:
            stats[len(chosen)]+=1
            if t>peak:peak=t;winner=tuple(sorted(chosen))
            return
        first=p not in visited
        options=(False,True) if first and len(chosen)<k else (False,)
        for newblack in options:
            if newblack:
                require(first,'cannot choose an old cell')
                nxtchosen=chosen+( (int(p.real),int(p.imag)), )
            else:nxtchosen=chosen
            nb=set(board);nv=set(visited)
            if first:nv.add(p)
            readblack= (p in nb) or newblack
            if readblack:
                if p in nb:nb.remove(p)
                # A virgin cell chosen initially BLACK turns white.
                nh=h*1j
            else:
                nb.add(p)
                nh=h*(-1j)
            walk(p+nh,nh,nb,nv,nxtchosen,t+1)
    walk(0j,1+0j,set(),set(),tuple(),0)
    return stats,peak,winner

if __name__=='__main__':
    stats,m,winner_seed=online_escape_tree()
    require(m==918,f'wrong independent bound {m}')
    require(set(winner_seed)==SHARP,f'wrong sharp example {winner_seed}')
    b,p,h,mini,turns=complex_run(TARGET,182)
    evidence=json.loads((HERE/'witness.json').read_text())
    require(len(b)==36 and p==(5,1) and h==1+0j and mini==0,
            'independent gate prefix mismatch')
    require(sorted(b)==[tuple(p) for p in evidence['gate']['black_after_182']],
            'complete gate black field mismatch')
    can=evidence['reference']['word']
    b2,p2,h2,mini2,blank_prefix=complex_run(set(),9977,start_heading=1j)
    require(p2==(-15,10) and h2==-1+0j, 'blank entry mismatch')
    # Next cycle must be the canonical word independently.
    bb={complex(*q) for q in b2};a=complex(*p2);head=h2;read=[]
    for i in range(104):
        isblack=a in bb
        if isblack:bb.remove(a);head*=1j
        else:bb.add(a);head*=-1j
        read.append('L' if isblack else 'R');a+=head
    require(''.join(read)==can,'canonical reference mismatch')
    require(a==complex(-17,8) and head==-1+0j,'reference drift mismatch')
    print(json.dumps({'status':'PASS','independent_online_leaf_counts':dict(stats),
        'max_first_exit':m,'sharp_seed':winner_seed,'gate_prefix_steps':182,
        'gate_black_cells':len(b),'reference_entry':9977},ensure_ascii=False))
