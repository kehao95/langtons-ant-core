"""Uniform next-stale-black-read decisions for complete finite-support LR states.

White -> right; black -> left; flip then move. State is observed BEFORE update.
A stale-D read means the current cell is black and none of the preceding D
pre-update positions equals the current position. The preceding D positions
are recovered by the exact inverse, not guessed from a truncated forward log.

This decides ONE family of local target predicates. It does not decide arbitrary
local HALT predicates, eventual periodicity, HIGHWAY, or finite-support universality.
"""
from __future__ import annotations
from functools import lru_cache
from hashlib import sha256
import json
from typing import Any

from baseline.memory_delay import State, DIRS, geometry, verify_period, simulate


def _check_D(D: int) -> None:
    if type(D) is not int or D < 1:
        raise ValueError('D must be a positive integer')


def radius(state: State) -> int:
    x, y = state.pos
    return max((max(abs(u-x), abs(v-y)) for u, v in state.black), default=0)


def input_digest(state: State) -> str:
    data = {'black': sorted(state.black), 'pos': state.pos, 'heading': state.heading}
    return sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()


def predecessor(state: State) -> tuple[State, str]:
    """Unique predecessor and its turn; the destination is not flipped."""
    dx, dy = DIRS[state.heading]
    q = (state.pos[0]-dx, state.pos[1]-dy)
    post_black = q in state.black
    # Black now at q means the preceding read there was white/right.
    turn = 'R' if post_black else 'L'
    old_h = (state.heading + (-1 if post_black else 1)) % 4
    black = state.black.symmetric_difference((q,))
    return State(frozenset(black), q, old_h), turn


def preceding_turns(state: State, D: int) -> str:
    _check_D(D)
    chars = []
    here = state
    for _ in range(D):
        here, ch = predecessor(here)
        chars.append(ch)
    return ''.join(reversed(chars))


@lru_cache(maxsize=200_000)
def suffix_details(word: str) -> tuple[str, int | None]:
    """Next turn of the recency-D rule; latest return index, or None."""
    if not word or set(word)-{'R','L'}:
        raise ValueError('expected nonempty R/L word')
    p, h = (0,0), 0
    last = {}
    for i, ch in enumerate(word):
        last[p] = i
        h = (h + (1 if ch == 'R' else -1)) % 4
        dx, dy = DIRS[h]
        p = p[0]+dx, p[1]+dy
    j = last.get(p)
    return ('R' if j is None else ('L' if word[j]=='R' else 'R')), j


def is_stale(state: State, D: int) -> bool:
    """A radius-D predicate on the PRESENT state (implemented using inversion)."""
    _check_D(D)
    if state.pos not in state.black:
        return False
    return suffix_details(preceding_turns(state, D))[1] is None


def waiting_bound(state: State, D: int) -> int:
    """If a stale-D read will ever occur, its offset is STRICTLY below this."""
    _check_D(D)
    Q = 1 << D
    return Q * (radius(state) + 2*Q + 10)


def event_count_deadline(D: int, n: int, R: int) -> int:
    """If an nth stale-D event exists, its offset is below this deadline.

    A nonperiodic orbit must have all n such events. This bound does NOT
    prove the existence of a nonperiodic orbit or of a future event.
    """
    _check_D(D)
    if type(n) is not int or n < 1 or type(R) is not int or R < 0:
        raise ValueError('n>=1 and R>=0 must be integers')
    Q = 1 << D
    C = R + 2*Q + 10
    return C * ((Q+1)**n - 1)


def _recent_at(initial: str, prefix: str, cycle: str, t: int) -> str:
    D, j = len(initial), len(prefix)
    def char(k: int) -> str:
        if k < 0:
            return initial[k+D]
        if k < j:
            return prefix[k]
        return cycle[(k-j) % len(cycle)]
    return ''.join(char(k) for k in range(t-D,t))


def first_stale_read(start: State, D: int,
                     max_suffix_states: int | None = None) -> dict[str, Any]:
    """Total next-event-or-permanent-no-event classifier, unless capped by caller.

    A permanent_no_stale result also supplies an exact translating trace lasso.
    A stale_read is NOT a HIGHWAY NO, a nonperiodicity proof, or a universal
    computation witness. A true periodic tail may have infinitely many stale-D
    reads when D is too small.
    """
    _check_D(D)
    if max_suffix_states is not None and (type(max_suffix_states) is not int or max_suffix_states < 0):
        raise ValueError('max_suffix_states must be nonnegative or None')
    initial = preceding_turns(start,D)
    w = initial
    black, pos, heading = set(start.black), start.pos, start.heading
    seen: dict[str,int] = {}
    turns: list[str] = []
    H = waiting_bound(start,D)
    common = {'schema':'langtons-ant-stale-memory-v1','D':D,
              'input_sha256':input_digest(start),'initial_suffix':initial,
              'radius':radius(start),'strict_waiting_bound':H}
    while w not in seen:
        t = len(turns)
        if max_suffix_states is not None and len(seen) >= max_suffix_states:
            return dict(common,kind='inconclusive',reason='caller resource cap',
                        updates_executed=t,suffix_states=len(seen))
        want, latest = suffix_details(w)
        actual = 'L' if pos in black else 'R'
        if want != actual:
            if want != 'R' or actual != 'L' or latest is not None:
                raise AssertionError('the exact stale-event identity failed')
            if not t < H:
                raise AssertionError('waiting bound failed')
            return dict(common,kind='stale_read',event_time=t,point=list(pos),
                        prefix=''.join(turns),witness_mode='literal_prefix',
                        updates_executed=t,suffix_states=len(seen),
                        event_recent_suffix=w)
        seen[w]=t
        turns.append(actual)
        black.symmetric_difference_update((pos,))
        heading=(heading+(1 if actual=='R' else -1))%4
        dx,dy=DIRS[heading]
        pos=(pos[0]+dx,pos[1]+dy)
        w=w[1:]+actual
    j=len(turns)
    i=seen[w]
    prefix=''.join(turns)
    cycle=''.join(turns[i:j])
    here=State(frozenset(black),pos,heading)
    points, final_h, drift=geometry(here,cycle)
    rotation=(final_h-heading)%4
    repeats=1 if rotation==0 else (2 if rotation==2 else 4)
    block=cycle*repeats
    points2, final_h2, drift2=geometry(here,block)
    if final_h2!=heading:
        raise AssertionError('heading period normalization failed')
    if drift2==(0,0):
        # Two closed geometric cycles suffice to witness an impossible periodic
        # read word: if both were compatible, the complete state would repeat.
        bp=set(black); pp=pos; hh=heading
        for k in range(2*len(block)):
            actual='L' if pp in bp else 'R'
            if actual != block[k%len(block)]:
                t=j+k
                recent=_recent_at(initial,prefix,cycle,t)
                if actual!='L' or block[k%len(block)]!='R' or suffix_details(recent)[1] is not None:
                    raise AssertionError('first mismatch must be stale black')
                if not t < H:
                    raise AssertionError('waiting bound failed')
                return dict(common,kind='stale_read',event_time=t,point=list(pp),
                            prefix=prefix,cycle=cycle,entry=j,
                            witness_mode='closed_geometry_finite_check',
                            updates_executed=j+k,suffix_states=j,
                            event_recent_suffix=recent)
            bp.symmetric_difference_update((pp,))
            hh=(hh+(1 if actual=='R' else -1))%4
            dx,dy=DIRS[hh];pp=(pp[0]+dx,pp[1]+dy)
        raise AssertionError('a literal bounded periodic orbit would result')
    if rotation:
        raise AssertionError('nonzero quarter rotation cannot have nonzero normalized drift')
    check=verify_period(here,cycle)
    if check['valid']:
        return dict(common,kind='permanent_no_stale',prefix=prefix,cycle=cycle,
                    entry=j,certificate=check,updates_executed=j,suffix_states=j)
    k=check['first_bad_offset']
    t=j+k
    epoch,phase=divmod(k,len(cycle))
    q=points[phase]
    point=(q[0]+epoch*drift[0],q[1]+epoch*drift[1])
    recent=_recent_at(initial,prefix,cycle,t)
    if cycle[phase]!='R' or suffix_details(recent)[1] is not None:
        raise AssertionError('earliest arithmetic mismatch must be stale black')
    if not t < H:
        raise AssertionError('waiting bound failed')
    return dict(common,kind='stale_read',event_time=t,point=list(point),
                prefix=prefix,cycle=cycle,entry=j,certificate=check,
                witness_mode='exact_periodic_ray_mismatch',updates_executed=j,
                suffix_states=j,event_recent_suffix=recent)
