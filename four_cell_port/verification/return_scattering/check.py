#!/usr/bin/env python3
"""Unbounded-return scattering packets: exact, scoped certificate checker.

The all-parameter bridge is in proof/results/return-scattering-closure.md.
This checks a restricted constructive family, NOT HC. Standard library only.
Run without -O. Existing guarded_scattering/check.py is imported, hash pinned.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path

if sys.flags.optimize:
    raise RuntimeError('certificate assertions require Python without -O')
DEP = Path(__file__).resolve().parents[1] / 'guarded_scattering' / 'check.py'
DEP_SHA = '7b199ee5d2f291eb5450c3f232d2bbf91e469de2bd9eb416a753393886d3da14'
assert hashlib.sha256(DEP.read_bytes()).hexdigest() == DEP_SHA
spec = importlib.util.spec_from_file_location('guarded_scattering_dependency', DEP)
g = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g
spec.loader.exec_module(g)
G = -160
NMIN = 100
V_A = (-12, 12)
V_C = (-24, -44)
HIT = (-38, -32)
MARK3 = (177, -260)
V_OUT = (203, -244)
WORD = g.WORD
s = lambda p: p[0] + p[1]
r = lambda p: p[0] - p[1]
ell = lambda p: p[1] - p[0]
phase = lambda a: (WORD * 2)[a:a+104]
q2 = lambda n: (-2*n-15, 2*n+11)
inside = lambda p: s(p) >= G and r(p) >= G


def xor(B, points):
    for p in points:
        B.symmetric_difference_update((p,))


def mature(j, k, form, bound):
    d = g.rot(g.D, k)
    assert form(d) > 0
    B = set()
    for i, p in enumerate(g.P):
        p = g.rot(g.sub(p, g.P[j]), k)
        lo = -((form(p)-bound)//form(d))
        hi = 0 if i < j else -1
        for a in range(lo, hi+1):
            xor(B, (g.add(p, g.mul(a, d)),))
    assert (0, 0) not in B
    return B


def footprint_plan(a, k, p):
    Q, h, end, hh = g.plan(phase(a), p, (g.H[a]+k)%4)
    assert g.sub(end, p) == g.rot(g.D, k)
    return Q


class Checks:
    def __init__(self):
        self.inequalities = []
        self.blocks = {}
        self.clock_steps = 0

    def affine(self, a, b, label):
        """a*n+b >= 0 for every integer n>=NMIN, not sampled interpolation."""
        assert isinstance(a, int) and isinstance(b, int)
        assert a >= 0 and a*NMIN+b >= 0, (label, a, b)
        self.inequalities.append((label, a, b))

    def block(self, name, S, steps, endpoint, heading):
        other, word, path = g.independent_replay(S, steps)
        assert other.p == endpoint and other.h == heading
        real = S.copy()
        clock = g.LocalClock(path+[other.p], real)
        initial_fuel = clock.fuel()
        for c in word:
            p, h = real.p, real.h
            black = p in real.B
            assert real.step() == c
            clock.advance(p, h, black, real)
        assert real.B == other.B and real.p == other.p and real.h == other.h
        assert clock.value == clock.full(real)
        self.clock_steps += steps
        self.blocks[name] = {
            'steps_per_simulator': steps,
            'initial_black': len(S.B), 'final_black': len(real.B),
            'initial_field_sha256': g.digest(S.B),
            'final_field_sha256': g.digest(real.B),
            'word_sha256': hashlib.sha256(''.join(word).encode()).hexdigest(),
            'min_s': min(map(s, path)), 'max_s': max(map(s, path)),
            'min_r': min(map(r, path)), 'max_r': max(map(r, path)),
            'endpoint': list(real.p), 'heading': real.h,
            'clock_initial_fuel_bits': initial_fuel.bit_length(),
            'clock_final_fuel_bits': clock.fuel().bit_length(),
        }
        return real, path, ''.join(word)

    def tails(self, S, a):
        assert g.tail_breakpoints(S, phase(a))
        assert g.tail_classes(S, phase(a))


def certify_packets(C):
    M1 = mature(57, 0, s, G)
    A, pathA, wa = C.block('A_first_turn', g.State(M1|{(0,0)}, (0,0), g.H[57]),
                          832, V_A, 2)
    C.tails(A, 58)
    QB = footprint_plan(58, 3, V_A)
    assert min(map(s, pathA+QB)) >= G
    # Both later markers are absent from all A reads. MARK3 misses all B rays.
    C.affine(2, min(p[0] for p in pathA)+14, 'q2_left_of_A')
    assert MARK3 not in pathA
    assert all((z:=g.ray(g.sub(MARK3,p),(-2,2))) is None or z<0 for p in QB)
    hitsB = []
    for i,p in enumerate(QB):
        z = g.ray(g.sub(q2(0),p),(-2,2))
        if z is not None:
            C.affine(1,z,'B_first_contact_epoch')
            hitsB.append((104*z+i,i))
    assert min(hitsB)==(14,14) and phase(58)[14]=='R'
    # The entire field in the next incoming half-plane is the mature NW kernel.
    M2 = mature(72,3,ell,G)
    for p in sorted(A.B|{MARK3}):
        C.affine(4,ell(q2(0))+G-1-ell(p),'old_endpoint_outside_C_guard')
    for i,p in enumerate(g.P):
        v = g.add(V_A,g.rot(g.sub(p,g.P[58]),3))
        v = g.add(v,g.mul(0 if i<58 else -1,(-2,2)))
        C.affine(4,ell(q2(0))+G-1-ell(v),'omitted_NW_past_outside_C_guard')
    assert min(s(g.add(q2(0),p)) for p in M2) >= G
    CC, pathC, wc = C.block('C_reverse_turn',g.State(M2|{(0,0)},(0,0),(g.H[72]+3)%4),
                             51272,V_C,0)
    assert min(map(ell,pathC+[CC.p])) >= G
    assert min(s(p)+s(q2(0)) for p in pathC+[CC.p]) >= G
    C.tails(CC,18)
    QD0 = footprint_plan(18,1,g.add(q2(0),V_C))
    assert min(map(s,QD0)) >= G
    # Returning SE rays and the entire outgoing NW write stream are disjoint.
    assert max(map(s,QD0)) < min(map(s,QB))
    assert max(map(s,QD0)) < min(s(p)+s(q2(0)) for p in M2)
    candidates=[]
    for b in sorted(A.B|{MARK3}):
        for i,p in enumerate(QD0):
            z=g.ray(g.sub(b,p),(2,-2))
            if z is not None:
                C.affine(1,z,'D_static_hit_epoch')
                candidates.append((104*z+i,i,b))
    assert min(candidates)==(-170,38,HIT)
    assert phase(18)[38]=='R' and HIT in A.B
    assert all(b!=MARK3 for _,_,b in candidates)
    # The distant reversal changes nothing in the fixed return region Omega.
    for p in sorted(set(pathC)|{(0,0)}):
        C.affine(4,G-1-r(g.add(q2(0),p)),'C_writes_outside_return_region')
    # Build the EXACT stabilized full field inside Omega at the old black read.
    B_return=set(A.B)|{MARK3}
    b_terms=0
    for p in QB:
        hi=(r(p)-G)//4
        C.affine(1,-hi-1,'B_all_visible_epochs_present')
        if s(p)>=G:
            for j in range(max(0,hi+1)):
                xor(B_return,(g.add(p,g.mul(j,(-2,2))),));b_terms+=1
    for p in QB[:14]:
        C.affine(4,G-1-r(p),'B_last_partial_outside_return_region')
    d_terms=0
    for p in QD0:
        lo=-((r(p)-G)//4)
        C.affine(1,lo,'D_all_visible_epochs_present')
        if s(p)>=G:
            for j in range(lo,-2):
                xor(B_return,(g.add(p,g.mul(j,(2,-2))),));d_terms+=1
    for p in QD0[:38]:
        v=g.add(p,(-4,4))
        if inside(v):xor(B_return,(v,));d_terms+=1
    B_return={p for p in B_return if inside(p)}
    assert HIT in B_return and MARK3 in B_return
    # Without the third INPUT marker, the return still converges, but to SE.
    E0,pathE0,we0=C.block('E0_two_marker_return_without_reset',
                          g.State(B_return-{MARK3},HIT,2),9308,(-22,-60),2)
    C.tails(E0,14)
    QE0=footprint_plan(14,1,E0.p)
    assert all(inside(p) for p in pathE0+QE0+[E0.p])
    assert MARK3 not in pathE0
    reset_hits=[]
    for i,p in enumerate(QE0):
        z=g.ray(g.sub(MARK3,p),(2,-2))
        if z is not None and z>=0:reset_hits.append(104*z+i)
    assert min(reset_hits)==10401 and phase(14)[1]=='R'
    E,pathE,we=C.block('E_old_wake_recovery_and_reset',g.State(B_return.copy(),HIT,2),
                       23661,V_OUT,1)
    C.tails(E,94)
    Qout=footprint_plan(94,0,V_OUT)
    assert all(inside(p) for p in pathE+Qout+[E.p])
    # Genuine old lifetime, created in the incoming NE flight, not an input marker.
    births=[]
    for i,p in enumerate(g.P):
        z=g.ray(g.sub(HIT,g.sub(p,g.P[57])),g.D)
        if z is not None and 104*z+i-57<0:
            births.append((104*z+i-57,i,z,WORD[i]))
    assert max(births)==(-1736,89,-17,'R')
    assert HIT not in pathA and s(HIT)<min(map(s,QB))
    # The packet itself stays in one diagonal half-plane, despite unbounded x retreat.
    packet_s_max=max(max(map(s,pathA)),max(map(s,QB)),
                     s(q2(0))+max(map(s,pathC)),max(map(s,QD0)),
                     max(map(s,pathE)),max(map(s,M1|{(0,0),MARK3})))
    packet_s_min=min(min(map(s,pathA)),min(map(s,QB)),
                     s(q2(0))+min(map(s,pathC)),min(map(s,QD0)),min(map(s,pathE)))
    assert packet_s_max==59 and packet_s_min==-109
    # Capture exact stage words for independent complete-state train replay.
    info={'M1':M1,'M2':M2,'A':A,'C':CC,'return_field':B_return,'E':E,
          'wa':wa,'wc':wc,'we':we,'QB':QB,'QD0':QD0,
          'packet_s_max':packet_s_max,'packet_s_min':packet_s_min}
    report={
        'first_marker_phase':57,'reverse_marker_phase':72,'reset_marker_relative':MARK3,
        'parameter_domain':'every integer n>=100',
        'packet_updates':'208*n+75609','old_read_updates':'208*n+51948',
        'old_birth_relative_to_primary':-1736,'old_lifetime_age':'208*n+53684',
        'old_read_position':HIT,'output_position':V_OUT,'output_phase':94,
        'packet_read_s_range':[packet_s_min,packet_s_max],
        'two_marker_updates':'208*n+61256',
        'two_marker_output_position':[-22,-60], 'two_marker_output_phase':14,
        'reset_marker_first_read_after_two_marker_boundary':10401,
        'old_return_field_black':len(B_return),
        'old_return_field_sha256':g.digest(B_return),
        'stable_B_xor_terms':b_terms,'stable_D_xor_terms':d_terms,
        'first_D_contact_candidates':len(candidates),
        'western_reversal_endpoint':'(-2*n-39, 2*n-33)',
    }
    return info,report


def certify_connectors(C, info):
    # q_next from phase 94 after m full periods plus phase adjustment to 57.
    delta0=g.add(V_OUT,g.add(g.D,g.sub(g.P[57],g.P[94])))
    delta=lambda m:g.add(delta0,g.mul(m,g.D))
    assert delta(100)==(408,-42)
    max_s=info['packet_s_max']
    C.affine(4,s(delta0)+G-1-max_s,'next_guard_beyond_all_packet_writes')
    for i,p in enumerate(g.P):
        v=g.add(V_OUT,g.add(g.sub(p,g.P[94]),g.mul(0 if i<94 else -1,g.D)))
        C.affine(4,s(delta0)+G-1-s(v),'next_guard_beyond_synthetic_output_past')
    # Initial canonical field and its omitted periodic past also lie behind first guard.
    first0=g.P[57]
    for p in sorted(g.BASE):
        C.affine(4,s(first0)+G-1-s(p),'initial_guard_beyond_BASE')
    for i,p in enumerate(g.P):
        v=g.sub(p,g.D)
        C.affine(4,s(first0)+G-1-s(v),'initial_guard_beyond_synthetic_past')
    assert min(map(s,g.P))==0
    # Off-rail secondary markers miss the entire incoming NE line, not just a prefix.
    rrail=[r(g.sub(p,g.P[57])) for p in g.P]
    C.affine(4,min(rrail)-1-r(q2(0)),'q2_outside_incoming_NE_rail')
    assert r(MARK3)>max(rrail)
    # Later packets' earliest marker cannot interrupt current packet or incoming flight.
    premax=max(s(g.add(g.sub(p,g.P[57]),g.mul(0 if i<57 else -1,g.D)))
               for i,p in enumerate(g.P))
    C.affine(4,s(delta0)-83-1-max(max_s,premax),'future_markers_after_current_reads')
    return {'minimum_primary_sum_increment':s(delta(100)),
            'minimum_guard_slack':s(delta(100))+G-max_s,
            'primary_spacing_domain':'every integer m>=100',
            'arbitrary_initial_debris_guard':'x+y<0',
            'minimum_initial_guard_slack':s(first0)+400+G-max(map(s,g.BASE)),
            'incoming_read_overshoot':premax}


def make_train(gaps, excursions, debris=()):
    if len(gaps)!=len(excursions):raise ValueError('length mismatch')
    if any(not isinstance(v,int) or isinstance(v,bool) for v in (*gaps,*excursions)):
        raise ValueError('parameters must be exact integers')
    if any(m<100 for m in gaps) or any(n<100 for n in excursions):
        raise ValueError('parameters outside certified class; not an HC negative')
    debris=set(debris)
    if any(s(p)>=0 for p in debris):raise ValueError('debris outside initial guard')
    B=set(g.BASE)|debris
    pose=(0,0);a=0;data=[];elapsed=0
    for m,n in zip(gaps,excursions):
        primary=g.add(pose,g.add(g.mul(m+(57<a),g.D),g.sub(g.P[57],g.P[a])))
        markers=[primary,g.add(primary,q2(n)),g.add(primary,MARK3)]
        assert len(set(markers))==3 and B.isdisjoint(markers)
        B.update(markers)
        flight=104*m+(57-a)%104
        elapsed+=flight
        data.append({'primary':primary,'n':n,'a':a,'flight':flight,'time':elapsed})
        elapsed+=208*n+75609
        pose=g.add(primary,V_OUT);a=94
    assert len(B)==13+3*len(data)+len(debris)
    return g.State(B,(0,0),1),data,elapsed


def expected_parts(row,info):
    n=row['n']
    yield (phase(row['a']),row['flight'])
    yield (info['wa'],832)
    yield (phase(58),104*n+14)
    yield (info['wc'],51272)
    yield (phase(18),104*n-170)
    yield (info['we'],23661)


def replay_train(gaps, excursions, debris, info):
    S,data,T=make_train(gaps,excursions,debris)
    original=S.copy();last={};born={};deaths=[];t=0
    checkpoints={}
    for row in data:
        primary=row['primary'];n=row['n'];base=row['time']
        checkpoints[base+104*n+846]=(g.add(primary,q2(n)),(g.H[72]+3)%4,None)
        checkpoints[base+208*n+51948]=(g.add(primary,HIT),2,'old')
        for w,length in expected_parts(row,info):
            for i in range(length):
                if t in checkpoints:
                    p,h,kind=checkpoints[t]
                    assert S.p==p and S.h==h
                    if kind=='old':
                        assert S.p in S.B and last[S.p]==base-1736
                        assert born[S.p]==base-1736
                        # Full field in the protected return region, excluding future markers.
                        local={g.sub(p,primary) for p in S.B if inside(g.sub(p,primary))}
                        future=set()
                        for later in data:
                            if later['time']>base:
                                future.update((later['primary'],g.add(later['primary'],q2(later['n'])),
                                               g.add(later['primary'],MARK3)))
                        local.difference_update(g.sub(p,primary) for p in future)
                        assert local==info['return_field']
                        deaths.append(t-born[S.p])
                p=S.p;black=p in S.B
                if not black:born[p]=t
                last[p]=t
                assert S.step()==w[i%len(w)],(t,S.p)
                t+=1
    assert t==T
    w=phase(94) if data else WORD
    assert g.tail_breakpoints(S,w) and g.tail_classes(S,w)
    # Entire input, not only pose/mass, agrees with an independently written simulator.
    other,_,_=g.independent_replay(original,T)
    assert S.B==other.B and S.p==other.p and S.h==other.h
    assert set(debris)<=S.B
    return {'packets':len(data),'updates':T,'initial_black':len(original.B),
            'final_black':len(S.B),'final_position':S.p,'final_heading':S.h,
            'final_field_sha256':g.digest(S.B),'old_lifetime_ages':deaths}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--compare',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    C=Checks();info,packet=certify_packets(C);connectors=certify_connectors(C,info)
    cases=[([],[],set()),([100],[100],set()),([100],[101],set()),([101],[137],{(-1000,0),(5,-9)}),
           ([100],[500],set()),([100,100],[100,173],{(-10,-10)}),
           ([101,103,100],[100,111,127],{(-999999,1)}),
           ([100]*6,[100,101,150,103,211,100],set())]
    trains=[replay_train(*x,info) for x in cases]
    huge=10**60
    big,rows,T=make_train([huge,100],[100,huge],{(-huge,-1)})
    assert len(big.B)==20
    for label,a,b in C.inequalities:assert a*huge+b>=0
    bad=info['E'].copy();bad.B.symmetric_difference_update((bad.p,))
    assert not g.tail_breakpoints(bad,phase(94)) and not g.tail_classes(bad,phase(94))
    # A remote black cell on a certified R first-visit ray is not erased as invisible.
    far=info['E'].copy();Q=footprint_plan(94,0,far.p)
    # Standard phase 57, future epoch adjusted from phase 94.
    marker=g.add(far.p,g.add(g.mul(huge+1,g.D),g.sub(g.P[57],g.P[94])))
    far.B.add(marker)
    assert not g.tail_breakpoints(far,phase(94)) and not g.tail_classes(far,phase(94))
    for bad_gap,bad_exc in ((100,99),(99,100),(100,100.0),(100,True)):
        try:make_train([bad_gap],[bad_exc])
        except ValueError:pass
        else:raise AssertionError('unsupported domain was accepted')
    report={'schema':1,'status':'restricted analytic closure with exact certificates; not HC',
            'dependency_sha256':DEP_SHA,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'packet':packet,'connectors':connectors,'blocks':C.blocks,
            'affine_inequalities':len(C.inequalities),
            'affine_certificate_sha256':hashlib.sha256(json.dumps(C.inequalities,separators=(',',':')).encode()).hexdigest(),
            'clock_step_checks':C.clock_steps,'complete_train_cases':len(trains),
            'train_packets':sum(t['packets'] for t in trains),'train_updates_per_simulator':sum(t['updates'] for t in trains),
            'trains':trains,'huge_parameter':str(huge),'huge_train_updates':str(T),
            'negative_controls':{'wrong_tail_colour':1,'remote_tail_blocker':1,'unsupported_parameters':4}}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.compare:assert args.compare.read_text()==text,'regenerated report differs'
    if args.output:args.output.write_text(text)
    print(text)

if __name__=='__main__':main()
