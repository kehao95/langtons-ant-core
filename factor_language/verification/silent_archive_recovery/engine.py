"""Exact affine-cell verifier for complete autonomous recovery, k >= 0.

All geometry and time labels are derived from words. Endpoint arrangements cover
all integer parameters, not just the representatives used to inspect each slab.
No shared ant simulator or external solver is imported.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json

D = ((0, 1), (1, 0), (0, -1), (-1, 0))
MOD = 8


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def at(f, k):
    return f[0]*k+f[1]


def nn(f, lo, hi):
    return at(f, lo) >= 0 and (f[0] >= 0 if hi is None else at(f, hi) >= 0)


@dataclass(frozen=True)
class Record:
    x: int
    res: int
    lo: tuple[int, int]
    end: tuple[int, int]
    block: int = -1
    order: int = 0
    turn: str = ''
    time: tuple[int, int, int] = (0, 0, 0)  # a*k+b*r+c

    def active(self, k, r):
        return at(self.lo, k) <= r < at(self.end, k)


def trace(word, heading):
    need(bool(word) and set(word) <= {'L','R'}, 'invalid literal word')
    x=y=0
    rows=[]
    for i,ch in enumerate(word):
        rows.append((x,y,ch,i))
        heading=(heading+(1 if ch=='R' else -1))%4
        dx,dy=D[heading];x+=dx;y+=dy
    return rows,x,y,heading


def source_records(profile,n0):
    out=[]
    for part in ('low','bulk','high'):
        need(len(profile[part])==len({tuple(q) for q in profile[part]}),'duplicate source point')
        for x,y in profile[part]:
            need(type(x) is int and type(y) is int,'noninteger source')
            if part=='low':
                need(y<8,'bad low cap')
                res=y%MOD;r=(y-res)//MOD
                out.append(Record(x,res,(0,r),(0,r+1)))
            elif part=='high':
                need(y>=8,'bad high cap')
                y+=4*n0;res=y%MOD;r=(y-res)//MOD
                out.append(Record(x,res,(1,r),(1,r+1)))
            else:
                need(8<=y<12,'bad bulk tile')
                for z in (0,1):
                    count=(n0-1-z)//2+1
                    yy=y+4*z;res=yy%MOD;r=(yy-res)//MOD
                    out.append(Record(x,res,(0,r),(1,r+count)))
    return out


def blocks_for(c,reg):
    n0=reg['n_offset']
    prefix=[{'word':b['word'],'count':[2*b['count'][0],n0*b['count'][0]+b['count'][1]]}
            for b in c['producer_blocks']]
    return prefix+reg['blocks']


def read_records(blocks,pose):
    x,y0,h=pose;y=(0,y0);tm=(0,0);out=[];ends=[]
    for bi,b in enumerate(blocks):
        word=b['word'];a,b0=b['count']
        need(type(a) is int and type(b0) is int and a>=0 and b0>=0,'negative/noninteger count')
        rows,dx,dy,eh=trace(word,h)
        single=(a,b0)==(0,1)
        need(single or (dx==0 and abs(dy) in (4,8) and eh==h),'unsupported loop geometry')
        need(y[0]%MOD==0,'nonintegral anchor residue')
        alpha=y[0]//MOD
        for xx,yy,ch,i in rows:
            if single:
                r0=(y[1]+yy)//MOD;res=(y[1]+yy)%MOD
                out.append(Record(x+xx,res,(alpha,r0),(alpha,r0+1),bi,i,ch,(tm[0],0,tm[1]+i)))
                continue
            split=MOD//abs(dy);s=1 if dy>0 else -1
            need(a%split==0,'non-affine repeat residue')
            for z in range(split):
                ca=a//split;cb=(b0-1-z)//split+1
                need(ca>=0 and cb>=0,'negative split count')
                yy0=y[1]+yy+dy*z;res=yy0%MOD;beta=(yy0-res)//MOD
                if s==1:
                    lo=(alpha,beta);end=(alpha+ca,beta+cb)
                else:
                    lo=(alpha-ca,beta-cb+1);end=(alpha,beta+1)
                order=i+len(word)*z-len(word)*split*s*beta
                tt=(tm[0]-len(word)*split*s*alpha,len(word)*split*s,tm[1]+order)
                out.append(Record(x+xx,res,lo,end,bi,order,ch,tt))
        x+=dx*b0;y=(y[0]+dy*a,y[1]+dy*b0);tm=(tm[0]+len(word)*a,tm[1]+len(word)*b0);h=eh
        ends.append({'x':x,'y':list(y),'h':h,'time':list(tm)})
    return out,ends


def slabs(groups):
    starts={0};pairs=0
    for ts in groups.values():
        fs=sorted({f for t in ts for f in (t.lo,t.end)})
        for i,f in enumerate(fs):
            for g in fs[:i]:
                if f[0]==g[0]:continue
                pairs+=1
                q=Fraction(g[1]-f[1],f[0]-g[0])
                if q>=0:
                    k=q.numerator//q.denominator;starts.update((k,k+1))
    ss=sorted(starts)
    return [(s,ss[i+1]-1 if i+1<len(ss) else None) for i,s in enumerate(ss)],pairs


def tri_nonnegative(f,left,right,klo,khi):
    for r in (left,(right[0],right[1]-1)):
        need(nn((f[0]+f[1]*r[0],f[2]+f[1]*r[1]),klo,khi),'chronological ordering failed')


def physical_coverage(source,reads):
    groups=defaultdict(list)
    for t in source+reads:groups[t.x,t.res].append(t)
    domains,pairs=slabs(groups);bands=checks=orders=0;digest=hashlib.sha256()
    for klo,khi in domains:
        for cls,ts in sorted(groups.items()):
            fs=sorted({f for t in ts for f in (t.lo,t.end)},key=lambda f:(at(f,klo),f))
            for f,g in zip(fs,fs[1:]):
                need(nn((g[0]-f[0],g[1]-f[1]),klo,khi),'endpoint order failed')
                if at(f,klo)==at(g,klo) and f!=g:need(khi==klo,'unisolated crossing')
            unique=[]
            for f in fs:
                if not unique or at(unique[-1],klo)!=at(f,klo):unique.append(f)
            for l,r in zip(unique,unique[1:]):
                need(nn((r[0]-l[0],r[1]-l[1]-1),klo,khi),'empty/changing cell band')
                active=[t for t in ts if t.active(klo,at(l,klo))]
                bit=sum(t.block==-1 for t in active)
                need(bit<=1,'overlapping complete source parts')
                seq=sorted((t for t in active if t.block>=0),key=lambda t:(t.block,t.order))
                for t,u in zip(seq,seq[1:]):
                    tri_nonnegative((u.time[0]-t.time[0],u.time[1]-t.time[1],u.time[2]-t.time[2]-1),l,r,klo,khi)
                    orders+=1
                for t in seq:
                    need(bit==(t.turn=='L'),f'physical read conflict at {cls}, k={klo}, r={at(l,klo)}, block={t.block}')
                    bit^=1;checks+=1
                bands+=1
                digest.update(json.dumps([klo,khi,cls,l,r,bit,[t.turn for t in seq]],separators=(',',':')).encode())
    return {'parameter_slabs':domains,'cross_slope_pairs':pairs,'spatial_bands':bands,
            'alternation_checks':checks,'chronology_checks':orders,'arrangement_sha256':digest.hexdigest()}


def field_index(records):
    index=defaultdict(list)
    for t in records:index[t.x,t.res].append(t)
    return index


def fixed_point_parities(index,p):
    x,y=p;r=y//MOD;ts=index.get((x,y%MOD),[])
    starts={0}
    for t in ts:
        for a,b in (t.lo,t.end):
            if not a:continue
            q=Fraction(r-b,a)
            if q>=0:
                k=q.numerator//q.denominator;starts.update((k,k+1))
    ss=sorted(starts);answer=[]
    for i,klo in enumerate(ss):
        khi=ss[i+1]-1 if i+1<len(ss) else None
        bit=0
        for t in ts:
            active=t.active(klo,r)
            f=( -t.lo[0],r-t.lo[1]);g=(t.end[0],t.end[1]-r-1)
            if active:need(nn(f,klo,khi) and nn(g,klo,khi),'membership changes in slab')
            else:
                if at(t.lo,klo)>r:need(nn((t.lo[0],t.lo[1]-r-1),klo,khi),'inactive lower changes')
                else:need(nn((-t.end[0],r-t.end[1]),klo,khi),'inactive upper changes')
            bit^=active
        answer.append((klo,khi,bit))
    return answer


def certify_tail(records,p,h,word):
    rows,dx,dy,eh=trace(word,h);period=len(word)
    need(period==104 and eh==h and abs(dx)==abs(dy)==2,'not a standard-shaped tail')
    q=[(p[0]+x,p[1]+y) for x,y,_,_ in rows]
    index=field_index(records);xmin=min(t.x for t in records);xmax=max(t.x for t in records)
    checks=0;epochs_total=0
    for i,(qx,qy) in enumerate(q):
        thresholds=[]
        for j,(rx,ry) in enumerate(q):
            if (rx-qx)%dx:continue
            z=(rx-qx)//dx
            if (ry-qy)!=z*dy:continue
            if z>0 or (z==0 and j<i):thresholds.append(z)
        epochs={0}|set(thresholds)
        # Every epoch potentially meeting the complete input/XOR support is explicit.
        for xx in range(xmin,xmax+1):
            if (xx-qx)%dx==0:
                e=(xx-qx)//dx
                if e>=0:epochs.update((e,e+1))
        epochs.add(max(epochs)+1)
        for e in sorted(epochs):
            before=sum(z<=e for z in thresholds)%2
            for klo,khi,bit in fixed_point_parities(index,(qx+e*dx,qy+e*dy)):
                need((bit^before)==(word[i]=='L'),f'tail colour conflict phase={i}, epoch={e}, k={klo}')
                checks+=1
            epochs_total+=1
    return {'drift':[dx,dy],'epochs_by_phase':epochs_total,'all_parameter_parity_checks':checks,
            'complete_field_x_bounds':[xmin,xmax]}


def certify_past(source,pose,past):
    index=field_index(source);p=tuple(pose[:2]);h=pose[2];toggled=set();rev=[]
    for _ in range(9):
        dx,dy=D[h];p=(p[0]-dx,p[1]-dy)
        vals={bit for _,_,bit in fixed_point_parities(index,p)}
        need(len(vals)==1,'inverse branch depends on parameter')
        bit=next(iter(vals))^(p in toggled)^1
        toggled.symmetric_difference_update((p,))
        rev.append('L' if bit else 'R');h=(h+(1 if bit else -1))%4
    need(''.join(reversed(rev))==past,'true nine-turn history mismatch')


def count_defects(blocks,past,standard):
    legal={(standard*2)[i:i+10] for i in range(104)}
    def consume(s,u):
        bad=0
        for ch in u:
            v=s+ch;bad+=v not in legal;s=v[1:]
        return s,bad
    a=b=0
    # For k>=2 every nonconstant loop here has at least two copies.
    for spec in blocks:
        u=spec['word'];ca,cb=spec['count']
        if ca:
            need(2*ca+cb>=2 and len(u)>=8,'unstabilized repetition')
            past,v=consume(past,u*2)
            stable,rate=consume(past,u)
            need(stable==past,'history not stationary after two copies')
            a+=ca*rate;b+=v+(cb-2)*rate
        else:
            past,v=consume(past,u*cb);b+=v
    return (a,b),past,consume


def verify_regime(c,reg):
    n0=reg['n_offset'];need(n0 in (10,17),'unexpected domain')
    blocks=blocks_for(c,reg);source=source_records(c['source'],n0)
    reads,ends=read_records(blocks,c['pose'])
    certify_past(source,c['pose'],c['past9'])
    coverage=physical_coverage(source,reads)
    tail=reg['tail'];standard=c['standard']
    need(len(standard)==104 and len({(standard*2)[i:i+104] for i in range(104)})==104,'nonprimitive standard')
    need(len(tail)==104 and tail in standard*2,'tail not a standard phase')
    endpoint=ends[-1];need(endpoint['y'][0]==0,'parameter-dependent endpoint')
    p=(endpoint['x'],endpoint['y'][1]);h=endpoint['h']
    tc=certify_tail(source+reads,p,h,tail)
    need(blocks[-1]['count']==[0,1] and blocks[-1]['word'][-1]!=tail[-1],'entry minimality not established')
    total,past,consume=count_defects(blocks,c['past9'],standard)
    _,extra=consume(past,tail[:9]);total=(total[0],total[1]+extra)
    # Cover the two small parameter values outside the stabilized counting formula.
    for k in (0,1):
        s=c['past9'];value=0
        for b0 in blocks:
            s,v=consume(s,b0['word']*at(b0['count'],k));value+=v
        s,v=consume(s,tail[:9]);value+=v
        need(value==at(total,k),'small parameter defect-count exception')
    ds=[];s=past
    for i,ch in enumerate(tail[:9]):
        s,v=consume(s,ch)
        if v:ds.append(i)
    need(bool(ds),'last event is not in the checked suffix')
    mass=[20,10*n0+41]
    for b0 in blocks:
        growth=b0['word'].count('R')-b0['word'].count('L')
        mass[0]+=growth*b0['count'][0];mass[1]+=growth*b0['count'][1]
    return {'n_equals':'2k+'+str(n0),'block_count':len(blocks),'recovery_variable_loops':sum(b['count'][0]>0 for b in reg['blocks']),
            'source_records':len(source),'read_records':len(reads),'coverage':coverage,
            'entry':endpoint,'entry_mass_k':mass,'all_future_J10_k':list(total),
            'last_J10_minus_entry':max(ds),'tail':tc,'block_endpoints':ends}


def first_read(c,reg,k,point):
    """Exact first future read of a point in an infinite certified regime.

    None means no read, not a statement about arbitrary ant trajectories.
    This evaluates finitely many affine read records and 104 future rays.
    """
    need(type(k) is int and k>=0,'parameter outside the certified regime')
    need(len(point)==2 and all(type(v) is int for v in point),'noninteger query')
    blocks=blocks_for(c,reg);reads,ends=read_records(blocks,c['pose'])
    x,y=point;r=y//MOD;best=None
    for t in reads:
        if t.x==x and t.res==y%MOD and t.active(k,r):
            time=t.time[0]*k+t.time[1]*r+t.time[2]
            best=time if best is None else min(best,time)
    e=ends[-1];rows,dx,dy,_=trace(reg['tail'],e['h']);p=(e['x'],at(e['y'],k));tau=at(e['time'],k)
    for qx,qy,_,i in rows:
        ux=x-p[0]-qx;uy=y-p[1]-qy
        if ux%dx==0:
            epoch=ux//dx
            if epoch>=0 and uy==epoch*dy:
                time=tau+104*epoch+i
                best=time if best is None else min(best,time)
    return best
