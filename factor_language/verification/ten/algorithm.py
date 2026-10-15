"""Polynomial-bit reachability of the radius-nine ten-factor defect.

This returns whether an event exists, not always its first occurrence time.
A 'forced_future' result is a theorem-certified YES, not an observed event.
No output is a NO-HIGHWAY verdict.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import kernel as k
r = k.r
Point = tuple[int, int]
ALLOWED = r.factors(r.W, 10)
PHASES = {r.W[i:] + r.W[:i]: i for i in range(104)}


def inverse(black: set[Point], p: Point, h: int):
    q = (p[0]-r.DIR[h][0], p[1]-r.DIR[h][1])
    # Supplied B is post-update; undo its one changed cell.
    black.symmetric_difference_update({q})
    old_turn = 'L' if q in black else 'R'
    old_h = (h - (1 if old_turn == 'R' else -1)) % 4
    return q, old_h, old_turn


def intrinsic_history(black: set[Point], p: Point, h: int, length=9):
    b = set(black); turns = []
    for _ in range(length):
        p,h,c = inverse(b,p,h); turns.append(c)
    return ''.join(reversed(turns))


def permanent_phase(black: set[Point], p: Point, h: int):
    """Exact complete-field P104 predicate. Never a repeated-prefix heuristic."""
    trial = set(black); q = p; g = h; word = ''
    for _ in range(104):
        q,g,c = r.step_cells(trial,q,g); word += c
    if word not in PHASES: return None
    rec = r.periodic_recipe(word)
    assert not rec['ray_starts']
    q, d, _, _ = r.geometry(word)
    normalized = {r.rotate((x-p[0],y-p[1]),-h) for x,y in black}
    difference = normalized ^ set(map(tuple,rec['points']))
    for v in difference:
        if any((a := r.multiple((v[0]-u[0],v[1]-u[1]),d)) is not None and a >= 0 for u in q):
            return None
    return PHASES[word]


def decide_future_defect(black: set[Point], p: Point=(0,0), h: int=0, *, intrinsic=True):
    """Decide any future J10 event (or any forward forbidden 10-factor).

    Input is an explicit finite set, not a compressed infinite field. With
    intrinsic=False only forward windows starting at time >=0 are checked.
    Main trajectory advances <=12*m+221 steps; permanence uses 104 additional
    lookahead steps on a copy, and intrinsic history uses 9 inverse steps.
    """
    if h not in range(4): raise ValueError('heading must be 0,1,2,3')
    if any(len(q)!=2 or any(not isinstance(v,int) for v in q) for q in black):
        raise ValueError('integer coordinate pairs required')
    black = set(black); m=len(black); bound=12*m+212
    history = intrinsic_history(black,p,h) if intrinsic else ''
    def is_event(c):
        return len(history)==9 and history+c not in ALLOWED
    for t in range(bound):
        c='L' if p in black else 'R'
        if is_event(c):
            return {'event_exists':True,'kind':'observed','first_event_update':t,
                    'main_updates':t,'mass_bound':bound}
        p,h,c=r.step_cells(black,p,h); history=(history+c)[-9:]
    phase=permanent_phase(black,p,h)
    if phase is None:
        return {'event_exists':True,'kind':'forced_future','first_event_update':None,
                'main_updates':bound,'mass_bound':bound,
                'reason':'No previous defect; failure of P_now at the proved attraction deadline.'}
    for t in range(bound,bound+9):
        c='L' if p in black else 'R'
        if is_event(c):
            return {'event_exists':True,'kind':'observed','first_event_update':t,
                    'main_updates':t,'mass_bound':bound}
        p,h,c=r.step_cells(black,p,h); history=(history+c)[-9:]
    return {'event_exists':False,'kind':'permanent_standard','standard_time':bound,
            'standard_phase':phase,'main_updates':bound+9,'mass_bound':bound}
