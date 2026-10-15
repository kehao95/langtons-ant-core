"""Reconstruct omitted large witnesses, checking their frozen original hashes.

An existing different file is rejected, never overwritten. Regeneration is
not proof: run check.py and independent.cpp afterwards, or reproduce.py.
"""
from pathlib import Path
import hashlib
import kernel as k
ROOT=Path(__file__).resolve().parent
EXPECTED={'windows10.txt':'6b76e51621e15d2304f1c0baa28790cc267cabafca3fc03250dea8721b2b4794',
          'quotient.tsv':'f6d5502737c0ce931c1f9ca62a62ad8307157b4133c8f087f7ac0268b0d05682'}
def save(name,data):
    if hashlib.sha256(data).hexdigest()!=EXPECTED[name]:raise RuntimeError('wrong regenerated '+name)
    p=ROOT/'certificates'/name
    if p.exists():
        if p.read_bytes()!=data:raise RuntimeError('existing certificate differs: '+name)
    else:p.write_bytes(data)
def main():
    words,_=k.enumerate_words(10,150)
    adj,rev=k.graph(words);H=next(c for c in k.sccs(adj,rev) if len(c)==366)
    B=k.load_witness(ROOT/'certificates')['B'];mapping={}
    for word in sorted(H):
        states=set(range(102))
        for c in word:
            states={((q+1)%102)for q in states if B[q]==c}|({75}if 0 in states and c=='L'else set())
        if len(states)!=1:raise RuntimeError('quotient state not uniquely reconstructed')
        mapping[word]=states.pop()
    save('windows10.txt',('\n'.join(words)+'\n').encode())
    save('quotient.tsv',''.join(w+'\t'+str(mapping[w])+'\n'for w in sorted(mapping)).encode())
    print('Restored and hash-checked both original finite witnesses.')
if __name__=='__main__':main()
