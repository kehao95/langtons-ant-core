"""Literal full-field controls; not a substitute for all-word coverage."""
import json, random
from pathlib import Path
from audit import W, L10, D

def trajectory(B,p,h,n):
    B=set(B);m=[len(B)];a=[]
    for _ in range(n):
        c='L' if p in B else 'R';a.append(c)
        B.symmetric_difference_update({p});h=(h+(1 if c=='R' else -1))%4
        p=(p[0]+D[h][0],p[1]+D[h][1]);m.append(len(B))
    return ''.join(a),m,B,p,h

def main():
    root=Path(__file__).resolve().parent;wit=json.loads((root/'witness.json').read_text())
    B=set(map(tuple,wit['short_seed']))
    a,m,_,_,_=trajectory(B,(0,0),0,90)
    assert a==wit['short_witness'] and (m[0],m[-1])==(28,26)
    assert all(a[i:i+10] in L10 for i in range(81))
    assert 3*90-26*(m[-1]-m[0])==322
    randoms=random.Random(20261015);intervals=prefixes=0
    for case in range(128):
        B={(randoms.randint(-8,8),randoms.randint(-8,8)) for _ in range(randoms.randrange(70))}
        if case%8==0:B.add((10**60+case,-10**60))
        p=(randoms.randint(-3,3),randoms.randint(-3,3));h=case%4
        a,m,_,_,_=trajectory(B,p,h,1500)
        end=[int(j>=9 and a[j-9:j+1] not in L10) for j in range(len(a))]
        cumulative=[0]
        for bit in end:cumulative.append(cumulative[-1]+bit)
        for t in range(1501):
            assert 3*t-26*(m[t]-m[0])<=351*cumulative[t]+322
            prefixes+=1
        for _ in range(128):
            s=randoms.randrange(1501);t=randoms.randrange(s,1501)
            N=0 if t-s<10 else cumulative[t]-cumulative[s+9]
            g=m[t]-m[s]
            assert 3*(t-s)-26*g<=351*N+322
            if N==0:assert 3*(t-s)-26*g<=322
            intervals+=1
    report={'status':'passed','complete_finite_seeds':128,'prefixes':prefixes,
      'arbitrary_intervals':intervals,'remote_cells_retained':16,
      'sharp_word_length':90,'sharp_initial_mass':28,'sharp_final_mass':26,
      'sharp_deficit':322,'scope':'finite controls, not all-input extrapolation',
      'HC_proved':False}
    (root/'orbit_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Do not disable assertions')
    main()
