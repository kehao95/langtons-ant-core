"""Independent all-parameter affine-order oracle.

Unlike affine.zero_on_epochs (interior-jump/collision coverage), this checker
partitions the entire parameter ray by EVERY pairwise affine-order change.
A single integer representative proves each complete order cell, including the
last infinite cell. It uses only integers and the displayed affine expressions.
"""
from affine import Aff

def zero_on_epochs(edges,count,kmin):
    if count.a<0 or count(kmin)<1:raise AssertionError('empty parameterized domain')
    functions=sorted(set(edges)|{Aff(),count});starts={kmin}
    for i,f in enumerate(functions):
        for g in functions[:i]:
            a,b=f.a-g.a,f.b-g.b
            if a:
                q=(-b)//a
                starts.update(k for k in (q,q+1)if k>=kmin)
    jumps=0
    for k in sorted(starts):
        n=count(k);values=sorted(f(k)for f in edges)
        if sum(v<=0 for v in values)%2:raise AssertionError(('origin',k))
        at=0
        while at<len(values):
            end=at+1
            while end<len(values)and values[end]==values[at]:end+=1
            if 0<values[at]<n and(end-at)%2:
                raise AssertionError(('interior',k,values[at]))
            jumps+=1;at=end
    return {'all_order_regions':len(starts),'ordered_jump_groups':jumps}
