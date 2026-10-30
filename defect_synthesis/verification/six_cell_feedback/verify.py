"""Exact finite certificate for a six-cell, all-parameter positive family.

No simulator is imported from the existing project. The infinite parameter is
covered by the complete XOR recurrence and integer half-ray guards below, not by
finite controls. Standard-library Python and a separately written C++17 replay.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile
from typing import Iterable

ROOT = Path(__file__).resolve().parent
Point = tuple[int, int]
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))
BASE_COMMIT = '16b9b465a291933d0229f8febf180fcc3be7fddc'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pairs(v):
    return {tuple(map(int, q)) for q in v}


def add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def scale(k: int, a: Point) -> Point:
    return k * a[0], k * a[1]


def move(points: Iterable[Point], displacement: Point):
    return {add(q, displacement) for q in points}


def rotate(q: Point, k: int = 1) -> Point:
    x, y = q
    for _ in range(k % 4):
        x, y = y, -x
    return x, y


def geometry(word: str, heading: int = 0, head: Point = (0, 0)):
    require(set(word) <= {'L', 'R'}, 'invalid turn alphabet')
    require(heading in range(4), 'invalid heading')
    reads = []
    p, h = head, heading
    for c in word:
        reads.append(p)
        h = (h + (1 if c == 'R' else -1)) % 4
        p = add(p, DIR[h])
    return reads, p, h


def literal(black: Iterable[Point], steps: int, head=(0, 0), heading=0):
    require(type(steps) is int and steps >= 0, 'invalid literal horizon')
    B = set(black)
    p, h = head, heading
    turns, reads = [], []
    for _ in range(steps):
        reads.append(p)
        c = 'L' if p in B else 'R'
        turns.append(c)
        B.symmetric_difference_update({p})
        h = (h + (1 if c == 'R' else -1)) % 4
        p = add(p, DIR[h])
    return B, p, h, ''.join(turns), reads


def inverse_history(black, head=(0, 0), heading=0, count=9):
    B, p, h, letters, reads = set(black), head, heading, [], []
    for _ in range(count):
        p = add(p, scale(-1, DIR[h]))
        reads.append(p)
        c = 'R' if p in B else 'L'
        letters.append(c)
        B.symmetric_difference_update({p})
        h = (h - (1 if c == 'R' else -1)) % 4
    return ''.join(reversed(letters)), reads


def xor_reads(reads):
    result = set()
    for q in reads:
        result.symmetric_difference_update({q})
    return result


def multiple(q: Point, d: Point):
    require(d != (0, 0), 'zero ray stride')
    a = 0 if d[0] else 1
    if q[a] % d[a]:
        return None
    k = q[a] // d[a]
    return k if q == scale(k, d) else None


def point_ray_hit(p: Point, q: Point, d: Point, lower=0):
    k = multiple((p[0] - q[0], p[1] - q[1]), d)
    return k if k is not None and k >= lower else None


def rays_intersect(p: Point, a: Point, q: Point, b: Point):
    """Exact for the equal-magnitude diagonal strides used by this certificate."""
    require(a in ((2, 2), (2, -2), (-2, 2), (-2, -2)), 'unsupported ray')
    require(b in ((2, 2), (2, -2), (-2, 2), (-2, -2)), 'unsupported ray')
    det = lambda x, y: x[0] * y[1] - x[1] * y[0]
    delta = q[0] - p[0], q[1] - p[1]
    den = det(a, b)
    if den:
        un, vn = det(delta, b), det(delta, a)
        if un % den or vn % den:
            return None
        u, v = un // den, vn // den
        return (u, v) if u >= 0 and v >= 0 else None
    s = multiple((p[0] - q[0], p[1] - q[1]), b)
    if s is None:
        return None
    if a == b:
        return max(0, -s), max(0, s)
    return (0, s) if s >= 0 else None


def avoid_points(points, starts, stride, lower, label):
    points, starts = set(points), set(starts)
    for p in points:
        for q in starts:
            require(point_ray_hit(p, q, stride, lower) is None,
                    f'{label}: physical guard hit at {p}, ray {q}')
    return len(points) * len(starts)


def permanent(black, head, heading, word):
    """All-time periodic ray-parity check, including the last infinite interval."""
    qs, end, hh = geometry(word, heading, head)
    d = end[0] - head[0], end[1] - head[1]
    require(hh == heading and d != (0, 0), 'nontranslating periodic proposal')
    checked = 0
    for i, q in enumerate(qs):
        changes = {0: int(word[i] == 'L')}
        def toggle(k):
            changes[k] = changes.get(k, 0) ^ 1
        for j, z in enumerate(qs):
            s = multiple((z[0] - q[0], z[1] - q[1]), d)
            if s is not None and (s > 0 or (s == 0 and j < i)):
                toggle(s)
        for z in black:
            s = point_ray_hit(z, q, d)
            if s is not None:
                toggle(s)
                toggle(s + 1)
        value = 0
        for k in sorted(changes):
            value ^= changes[k]
            checked += 1
            if value:
                return False, checked, (i, k)
    return True, checked, None


def scan(history, word, legal):
    n, bad_at = 0, []
    for i, c in enumerate(word):
        history += c
        if len(history) >= 10:
            if history[-10:] not in legal:
                n += 1
                bad_at.append(i)
        history = history[-9:]
    return history, n, bad_at


def field_digest(B):
    return sha(''.join(f'{x},{y}\n' for x, y in sorted(B)).encode())


def motif_scan(history,word):
    count=0
    for ch in word:
        window=history+ch; count+=window=='RLRLR'; history=window[-4:]
    return history,count

def verify_basis(c):
    require(c['initial_head']==[0,0] and c['initial_heading']==0 and c['canonical_heading']==2,
            'initial-pose metadata')
    require(c['blank_steps']==9977 and c['seed_stride']==[-2,-2], 'source/time metadata')
    for key,value in {'first_standard':[18743,220], 'certificate_time':[18921,220],
                      'contained_defects':[6702,47], 'intrinsic_defects':[6706,47],
                      'last_defect':[18751,220]}.items():
        require(c[key]==value, 'inconsistent formula metadata: '+key)
    require(c['lifetime']=={'V_phase':35,'D_site':[1,-4],'D_epoch_offset':3,
                           'W_birth_phase':29,'age_base':1528,'age_slope':220},
            'lifetime metadata')
    W, U, V, Z, O = (c[k] for k in ('canonical_W', 'prefix_U', 'reverse_V', 'recovery_Z', 'out_word'))
    require((len(W), len(U), len(V), len(Z), len(O)) == (104, 1210, 116, 4406, 104), 'word lengths')
    require(all(W[i:] + W[:i] != W for i in range(1, 104)), 'W not primitive')
    require(all(V[i:] + V[:i] != V for i in range(1, 116)), 'V not primitive')
    legal = {(W * 2)[i:i+10] for i in range(104)}
    require(len(legal) == 84 and O in {(W * 2)[i:i+104] for i in range(104)}, 'standard phase')
    P, D, M, d, N0 = pairs(c['canonical_P']), pairs(c['deposit_D']), pairs(c['markers_M']), tuple(c['canonical_drift']), c['age_base']
    require((len(P), len(D), len(M), d, N0) == (13, 12, 6, (2, -2), 32), 'source data')
    # Independently generate the blank reference, not a supplied chaotic trace.
    Bblank, pref, href, C, cr = literal([], c['blank_steps'])
    require(sha(C.encode()) == c['blank_word_sha256'], 'blank-prefix hash')
    require([list(pref), href] == c['blank_endpoint'] and len(Bblank) == 715, 'blank reference endpoint')
    norm = {rotate((x-pref[0], y-pref[1]), 2-href) for x, y in Bblank}
    require(P <= norm, 'canonical core missing from blank orbit')
    E = norm ^ P
    require(len(E) == 702, 'blank debris count')
    Dgot, pg, hg, wg, wr = literal(P, 104, heading=2)
    require(wg == W and pg == d and hg == 2, 'canonical one-period word')
    require(Dgot == move(P, d) ^ D, 'complete deposited-tail identity')
    require(permanent(P, (0, 0), 2, W)[0], 'minimal standard ray guard')
    require(permanent(norm, (0, 0), 2, W)[0], 'complete blank standard ray guard')
    # The complete old debris is never read by the blank reference's future.
    eq = avoid_points(E, wr, d, 0, 'canonical debris')
    # No source marker is read before the collision frame, for ANY N>=32.
    rho = href - 2
    global_marker_rays = {add(pref, rotate(q, rho)) for q in M}
    dg = rotate(d, rho)
    pre_guard = avoid_points(cr, global_marker_rays, dg, N0, 'time-zero source guard')
    pre_guard += avoid_points(wr, M, d, 1, 'all earlier standard epochs')
    past0, invreads = inverse_history([])
    pre_guard += avoid_points(invreads, global_marker_rays, dg, N0, 'inverse-history guard')
    seedbase = {add(q, scale(N0, dg)) for q in global_marker_rays}
    require(seedbase == pairs(c['seed_base']), 'six-cell world coordinates')
    require(len(seedbase) == 6 and max(max(x for x,y in seedbase)-min(x for x,y in seedbase), max(y for x,y in seedbase)-min(y for x,y in seedbase)) == 9, 'fixed source diameter')
    # Source after the unmodified blank prefix and N0 standard periods.
    def before_U(N):
        out = P ^ M ^ move(E, scale(-N, d))
        for j in range(1, N+1):
            out.symmetric_difference_update(move(D, scale(-j, d)))
        return out
    Y0 = before_U(N0)
    S0, a, h, ugot, ur = literal(Y0, len(U), heading=2)
    require(ugot == U and [list(a),h] == c['post_U'], 'base collision prefix')
    K = P ^ M ^ xor_reads(ur)
    require(S0 == K ^ (Y0 ^ P ^ M), 'complete post-U field')
    Sv, av, hv, vgot, vr = literal(S0, len(V), a, h)
    require(vgot == V and av == add(a, scale(-1,d)) and hv == h, 'backward period')
    R = xor_reads(vr)
    Q = K ^ move(K,d) ^ D ^ move(R,d)
    require(Q == pairs(c['pump_archive_Q']) and len(Q) == 140, 'complete pump archive identity')
    input_guard = avoid_points(ur + vr, D, scale(-1,d), N0+1, 'old-tail source guard')
    input_guard += avoid_points(ur + vr, E, scale(-1,d), N0, 'old-debris source guard')
    # Fresh direct check of the complete one-pump identity at N0+1.
    S1, a1, h1, u1, _ = literal(before_U(N0+1),len(U),heading=2)
    S1v, a1v, h1v, v1, _ = literal(S1,len(V),a1,h1)
    require(u1 == U and v1 == V and move(S1v,d) == S0 ^ Q, 'one-pump complete state identity')
    output_guard = avoid_points(vr,Q,d,0,'archive versus next pump')
    # Finite recovery and its WHOLE infinite standard future.
    H, ep, eh, zgot, zr = literal(S0,len(Z),a,h)
    require(zgot == Z and [list(ep),eh] == c['normalized_base_endpoint'], 'base full recovery')
    output_guard += avoid_points(zr,Q,d,0,'archive versus recovery')
    ok, breaks, mismatch = permanent(H,ep,eh,O)
    require(ok, f'base permanent suffix {mismatch}')
    oq, oe, oh = geometry(O,eh,ep)
    od = oe[0]-ep[0], oe[1]-ep[1]
    require(od == (-2,-2) and oh == eh, 'outgoing orientation')
    for v in oq:
        for q in Q:
            require(rays_intersect(v,od,q,d) is None, 'future recovery ray meets pump archive')
    output_ray_pairs = len(oq)*len(Q)
    # Defect-count dependence on the repetition count, including both seams.
    hc, dc, _ = scan('', C, legal)
    hw, dw, _ = scan(hc,W,legal)
    hw2, dw2, _ = scan(hw,W,legal)
    require(hw2 == hw and dw2 == 0, 'standard-prefix suffix register')
    hu, du, _ = scan(hw,U,legal)
    hv1, dv1, _ = scan(hu,V,legal)
    hv2, dv2, _ = scan(hv1,V,legal)
    hz0, dz0, bz0 = scan(hu,Z,legal)
    hz1, dz1, bz1 = scan(hv1,Z,legal)
    require(hv2 == hv1 and dv2 == 47 and dv1+dz1-dz0 == 47, 'all-k defect seam identity')
    require(hz0 == hz1 and scan(hz0,O,legal)[1] == 0, 'permanent standard seam')
    require(V.count('R')-V.count('L') == 12, 'return wave mass increment')
    dbase = dc + dw + du + dz0
    require(dbase == c['contained_defects'][0] == 6702, 'total finite-forward defects')
    globalword = C + W*N0 + U + Z
    global_T = len(globalword)
    tail = global_T
    while tail > 0 and globalword[tail-1] == O[(tail-1-global_T)%104]:
        tail -= 1
    require(tail == c['first_standard'][0] == 18743, 'earliest standard suffix')
    require(tail > len(C)+104*N0+len(U)+9, 'earliest seam not in variable part')
    require(max(bz0) == max(bz1), 'last defect unaffected by seam')
    last = len(C)+104*N0+len(U)+max(bz0)
    require(last == c['last_defect'][0] == 18751, 'last defect')
    early = scan(past0,C[:9],legal)[1]
    require(early == 4 and dbase+early == c['intrinsic_defects'][0] == 6706, 'intrinsic initial-boundary correction')
    require(c['certificate_time'] == [global_T,220] and global_T == 18921, 'time formula')
    # Each of the six ORIGINAL black lifetimes ends in U, before the long replay.
    original_ends=[]
    for q in M:
        t=ur.index(q)
        require(U[t]=='L','source marker first read was not black')
        original_ends.append([q[0],q[1],t])
    require(sorted(original_ends)==sorted(c['six_first_reads_U']), 'original black lifetime table')
    require(min(t for _,_,t in original_ends)==13 and max(t for _,_,t in original_ends)==908, 'first-impact and exhaustion offsets')
    require(U[:13]==W[:13] and U[13]!=W[13], 'first divergence from the blank highway')
    require(len(C)+104*N0+13==13318, 'first-impact time constant')
    require(6+sum(x.count('R')-x.count('L') for x in (C,W*N0,U,Z))==1645, 'terminal mass constant')
    # One explicit newborn lifetime consumed at a defect in EVERY V copy.
    vp, _, _ = geometry(V,h,a)
    i,delta,offset,birthphase = 35,(1,-4),3,29
    require(vp[i] == add(delta,scale(-offset,d)) and V[i]=='L','lifetime spatial identity')
    require(wr[birthphase]==delta and W[birthphase]=='R','lifetime birth phase')
    require(delta not in wr[birthphase+1:],'later same-period read after claimed birth')
    avoid_points([delta],wr,d,1,'no later forward-period read of deposited lifetime')
    avoid_points(ur,[vp[i]],scale(-1,d),0,'no U interruption of selected lifetime')
    for ell,z in enumerate(vp):
        s=multiple((z[0]-vp[i][0],z[1]-vp[i][1]),d)
        require(s is None or 116*s+ell>=i,'earlier V occurrence interrupts lifetime')
    require(V[i-9:i+1] not in legal,'selected consumption is not a defect')
    age_const=len(U)+i+104*offset-birthphase
    require(age_const==1528,'lifetime age formula')
    # Recover the global complete terminal field and infinite archive.
    anchor = add(pref,scale(N0,dg))
    Hglobal={add(anchor,rotate(q,rho))for q in H}
    Qglobal={add(anchor,rotate(q,rho))for q in Q}
    epglobal=add(anchor,rotate(ep,rho));ehglobal=(eh+rho)%4
    require([list(epglobal),ehglobal]==c['global_endpoint'], 'common world endpoint')
    return {
        'summary': {'blank_mass':len(Bblank),'blank_debris':len(E),'P':len(P),'D':len(D),'M':len(M),'K':len(K),'R':len(R),'Q':len(Q),'recovery_mass':len(H),'input_guard_pairs':input_guard,'initial_guard_pairs':pre_guard,'canonical_debris_pairs':eq,'output_point_guard_pairs':output_guard,'output_ray_guard_pairs':output_ray_pairs,'base_suffix_parity_breakpoints':breaks,'blank_contained_defects':dc,'first_W_seam_defects':dw,'U_defects':du,'first_V_defects':dv1,'cyclic_V_defects':dv2,'Z_from_U_defects':dz0,'Z_from_V_defects':dz1,'original_lifetimes_consumed_by_U':sorted(original_ends),'world_endpoint':[list(epglobal),ehglobal],'base_endpoint_sha256':field_digest(Hglobal),'pump_archive_sha256':field_digest(Qglobal)},
        'C':C,'W':W,'U':U,'V':V,'Z':Z,'O':O,'legal':legal,'H':Hglobal,'Q':Qglobal,'stride':dg,'seed':seedbase,'pose':(epglobal,ehglobal),'past':past0,
    }


def concrete_controls(c,basis):
    # Literal, complete-field controls. No cutoff is used for all-k coverage.
    ks=list(range(12))+[16,31,32,63,100,257,512,1000]
    controls=[];total=0
    for k in ks:
        seed=move(basis['seed'],scale(k,basis['stride']))
        T=18921+220*k
        B,p,h,w,reads=literal(seed,T)
        expected=basis['C']+basis['W']*(32+k)+basis['U']+basis['V']*k+basis['Z']
        require(w==expected, f'word mismatch at k={k}')
        want=set(basis['H'])
        for j in range(k):
            want.symmetric_difference_update(move(basis['Q'],scale(j,basis['stride'])))
        require(B==want and (p,h)==basis['pose'],f'complete terminal field mismatch k={k}')
        n=scan('',w,basis['legal'])[1]
        require(n==6702+47*k,'literal count formula')
        require(motif_scan('',w)[1]==259+k,'literal five-factor count')
        require(len(B)==1645+24*k,'literal endpoint mass')
        # Track actual births and first later reads of the designated new memories.
        births={}; verified_lifetimes=0
        first_consume=14550+104*k
        for t,(q,letter) in enumerate(zip(reads,w)):
            if letter=='R':
                births[q]=t
            else:
                born=births.pop(q,None)
                gap=t-first_consume
                if gap>=0 and gap%116==0 and gap//116<k:
                    j=gap//116
                    require(born==13022+104*(k-j) and t-born==1528+220*j, 'literal newborn lifetime')
                    verified_lifetimes+=1
        require(verified_lifetimes==k,'missing selected lifetimes')
        # Locate all original markers' first reads in the complete physical run.
        require(all(w[reads.index(q)]=='L'for q in seed),'initial source lifetime')
        controls.append({'k':k,'time':T,'contained_defects':n,'black_count':len(B),'newborn_lifetimes_checked':verified_lifetimes,'full_field_sha256':field_digest(B)})
        total+=T
    return controls,total


def negative_controls(c,basis):
    failures=[]
    damaged=copy.deepcopy(c);s=damaged['reverse_V'];damaged['reverse_V']=('R'if s[0]=='L'else'L')+s[1:]
    for label,case in [('turn',damaged)]:
        try:verify_basis(case)
        except ValueError:failures.append(label)
        else:raise AssertionError('damaged word accepted')
    damaged=copy.deepcopy(c);damaged['seed_base'][0][0]+=1
    try:verify_basis(damaged)
    except ValueError:failures.append('source coordinate')
    else:raise AssertionError('damaged seed accepted')
    damaged=copy.deepcopy(c);damaged['pump_archive_Q'].pop()
    try:verify_basis(damaged)
    except ValueError:failures.append('archive identity')
    else:raise AssertionError('damaged archive accepted')
    damaged=copy.deepcopy(c);damaged['contained_defects'][0]+=1
    try:verify_basis(damaged)
    except ValueError:failures.append('defect total')
    else:raise AssertionError('damaged count accepted')
    p,h=basis['pose'];points,end,hh=geometry(basis['O'],h,p);outd=(end[0]-p[0],end[1]-p[1])
    far=add(points[0],scale(10**60,outd));B=basis['H']^{far}
    require(not permanent(B,p,h,basis['O'])[0],'remote blocker silently erased')
    failures.append('10^60-period outgoing blocker')
    try:avoid_points([p],[p],(2,-2),0,'damaged guard')
    except ValueError:failures.append('archive at recovery head')
    else:raise AssertionError('damaged guard accepted')
    # Direct ray formula cross-checks; all integer intersections in this range
    # have a witness with indices <=12, so exhaustive finite comparison is exact.
    strides=((2,2),(2,-2),(-2,2),(-2,-2));rng=random.Random(20261021);cases=0
    for _ in range(800):
        p=(rng.randrange(-8,9),rng.randrange(-8,9));q=(rng.randrange(-8,9),rng.randrange(-8,9));a=rng.choice(strides);b=rng.choice(strides)
        hit=rays_intersect(p,a,q,b)
        brute=any(add(p,scale(u,a))==add(q,scale(v,b))for u in range(17)for v in range(17))
        require((hit is not None)==brute,'integer ray intersection control')
        if hit is not None:require(add(p,scale(hit[0],a))==add(q,scale(hit[1],b)),'bad ray witness')
        cases+=1
    return {'rejected':failures,'ray_controls':cases,'resource_limits_are_not_NO':True}


def run(with_cpp=True):
    raw=(ROOT/'witness.json').read_bytes();c=json.loads(raw)
    basis=verify_basis(c)
    finite,total=concrete_controls(c,basis)
    negatives=negative_controls(c,basis)
    cpp=None
    if with_cpp:
        with tempfile.TemporaryDirectory(prefix='six-cell-native-') as td:
            td=Path(td);binary=td/'check'
            subprocess.run(['g++','-std=c++17','-O2',str(ROOT/'independent.cpp'),'-o',str(binary)],check=True)
            inp='\n'.join([basis['W'],basis['U'],basis['V'],basis['Z'],basis['O']])+'\n'+str(len(finite))+'\n'+'\n'.join(str(x['k'])for x in finite)+'\n'
            result=subprocess.run([str(binary)],input=inp,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
            lines=iter(result.stdout.splitlines());rows=[]
            guardline=next(lines).split();bs=basis['summary']
            require(guardline[0]=='GUARDS' and list(map(int,guardline[1:]))==[bs['initial_guard_pairs'],bs['input_guard_pairs'],bs['output_point_guard_pairs'],bs['output_ray_guard_pairs'],bs['Q']], 'independent all-parameter guards')
            for row in finite:
                header=next(lines).split();require(header[0]=='CASE','native output header')
                k,t,df,x,y,h,mass=map(int,header[1:]);B=set()
                for _ in range(mass):
                    xx,yy=map(int,next(lines).split());B.add((xx,yy))
                require((k,t,df)==(row['k'],row['time'],row['contained_defects']),'native time/count')
                require(field_digest(B)==row['full_field_sha256'],'native complete field mismatch')
                require(((x,y),h)==basis['pose'],'native pose')
                rows.append(k)
            footer=next(lines)
            require(footer=='PASS independent complete fields, turn words and source lifetimes','native footer')
            require(next(lines,None)is None,'unexpected native data')
            cpp={'cases':len(rows),'updates':sum(x['time']for x in finite),'complete_endpoint_equalities':len(rows),'all_parameter_ray_guards_independent':True,'algorithm':'ordered-set state, direct string-window count and signed-vector rotations'}
    return {'schema':'six-cell-feedback-check-v1','status':'passed','base_commit':BASE_COMMIT,'scope':'all-parameter XOR pumping and all-future positive family; no HC proof or negative seed','witness_sha256':sha(raw),'basis':basis['summary'],'formulas':{'first_permanent_P104':'18743+220*k','certificate_boundary':'18921+220*k','contained_defects':'6702+47*k','intrinsic_defects':'6706+47*k','newborn_lifetime_age':'1528+220*j, 0<=j<k','first_source_impact':'13318+104*k','endpoint_black_mass':'1645+24*k','initial_black_mass':6,'initial_black_diameter':9,'all_k_nonnegative':True},'literal_controls':finite,'literal_updates':total,'independent_cpp':cpp,'negative_controls':negatives,'sources_sha256':{p:sha((ROOT/p).read_bytes())for p in ('verify.py','independent.cpp')}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',type=Path);ap.add_argument('--no-cpp',action='store_true');a=ap.parse_args()
    report=run(not a.no_cpp)
    if a.write:
        a.write.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print('WROTE exact fresh report',a.write)
    else:
        want=json.loads((ROOT/'report.json').read_text())
        require(report==want,'frozen report mismatch; no file has been rewritten')
        print('PASS six-cell all-parameter certificate and independent complete replay')

if __name__=='__main__':main()
