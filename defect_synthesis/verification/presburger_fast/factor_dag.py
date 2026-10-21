"""Linear-size DAG for exact forward-contained ten-factor counts.

No zero/nonzero Cartesian case expansion. Fixed-size suffix state is passed
through each part once. The relation is word-syntactic; physical feasibility
is separately enforced by the stream parity encoder.
"""
from __future__ import annotations
import _paths  # Pin and load the unchanged sibling schema syntax.
from dataclasses import dataclass
from compiler import Power, Schema, L10, scan_factors
from stream_qf import Circuit, Expr

@dataclass(frozen=True)
class Suffix:
    bits:tuple[Expr,...]
    length:Expr
    last_bad:Expr

_ALLOWED=tuple(tuple(ch=='L' for ch in word) for word in sorted(L10))

def _advance(c:Circuit,state:Suffix,word:str):
    bits=state.bits;length=state.length;last=state.last_bad;delta=0
    for index,ch in enumerate(word):
        if length==9 and all(type(v) is bool for v in bits):
            hist=''.join('L' if v else 'R' for v in bits)
            hist,inc,last=scan_factors(hist,word[index:])
            delta=c.add(delta,inc);bits=tuple(ch=='L' for ch in hist);length=9
            break
        bit=ch=='L'
        allowed=c.or_(*(c.and_(*(b if w else c.not_(b) for b,w in zip((*bits,bit),row)))
                         for row in _ALLOWED if row[-1]==bit))
        last=c.and_(c.eq(length,9),c.not_(allowed))
        delta=c.add(delta,c.ite(last,1,0))
        bits=(*bits[1:],bit)
        length=9 if index>=8 else c.ite(c.lt(length,9),c.add(length,1),9)
    # Once >=9 letters have actually been appended, these registers no longer
    # depend on the incoming history. This is an exact transfer identity.
    if len(word)>=9:
        bits=tuple(ch=='L' for ch in word[-9:]);length=9
    return Suffix(bits,length,last),delta


def count_circuit(schema:Schema,c:Circuit):
    if tuple(schema.parameters)!=c.parameters:raise ValueError('parameter spaces differ')
    state=Suffix((False,)*9,0,False);total=0
    for part in schema.parts:
        if isinstance(part,str):
            state,inc=_advance(c,state,part);total=c.add(total,inc);continue
        q=(9+len(part.word)-1)//len(part.word)
        partial=[(state,0)];z=state;count=0
        for _ in range(q):
            z,inc=_advance(c,z,part.word);count=c.add(count,inc);partial.append((z,count))
        if len(part.word*q)<9:raise AssertionError('insufficient stabilization')
        z=Suffix(tuple(ch=='L' for ch in (part.word*q)[-9:]),9,z.last_bad)
        partial[-1]=(z,count)
        stable,rate=_advance(c,z,part.word)
        if type(rate) is not int or type(stable.last_bad) is not bool:
            raise AssertionError('cycle count did not become constant')
        k=c.affine(part.exponent)
        inc=c.add(count,c.mul(rate,c.add(k,-q)))
        new=Suffix(z.bits,9,c.ite(c.eq(k,q),z.last_bad,stable.last_bad,'Bool'))
        for i in reversed(range(q)):
            alt,n=partial[i];condition=c.eq(k,i)
            inc=c.ite(condition,n,inc)
            new=Suffix(tuple(c.ite(condition,a,b,'Bool') for a,b in zip(alt.bits,new.bits)),
                       c.ite(condition,alt.length,new.length),
                       c.ite(condition,alt.last_bad,new.last_bad,'Bool'))
        total=c.add(total,inc);state=new
    return total,state
