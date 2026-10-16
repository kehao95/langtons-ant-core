"""Complete but deliberately conservative fixed-defect schema construction.

A finite schema cap is INCONCLUSIVE. This is a reference construction proving
uniform effectivity; it is not a claim that the enormous disjunction is practical.
"""
from __future__ import annotations
from itertools import product
import ctypes as C
from trace_arithmetic import Aff,Block,Schema
from flat_cover import A,T,STANDARD,L10

def compositions(total,parts):
    if parts==1:yield(total,);return
    for first in range(total+1):
        for tail in compositions(total-first,parts-1):yield(first,)+tail

def templates(events:int):
    if type(events) is not int or events<1:raise ValueError('positive event budget')
    powers=sorted({w[k:]+w[:k] for w in (A,T,STANDARD) for k in range(len(w))})
    bound=9+2000*events
    # Every loop is finite: without a resource cap this generator terminates.
    for s in range(5*events+1):
        for literal_length in range(bound+1):
            for cuts in compositions(literal_length,s+1):
                for bits in product('RL',repeat=literal_length):
                    text=''.join(bits);offset=0;pieces=[]
                    for n in cuts:pieces.append(text[offset:offset+n]);offset+=n
                    for loops in product(powers,repeat=s):
                        blocks=[]
                        for i,piece in enumerate(pieces):
                            if piece:blocks.append(Block(piece))
                            if i<s:blocks.append(Block(loops[i],Aff.var(f'K{i}')))
                        yield s,blocks

def compile_all_coordinates(m:int,N:int,*,max_schemas:int|None=None):
    """Return an exact union only on COMPLETE; a capped union is an underapproximation.
    No nontrivial full run is claimed in the retained evidence.
    """
    if type(m) is not int or m<0 or type(N) is not int or N<1:raise ValueError('invalid m,N')
    if max_schemas is not None and (type(max_schemas) is not int or max_schemas<0):raise ValueError('invalid cap')
    from isl_bridge import Context
    ctx=Context();coords=[z for i in range(m) for z in (f'X{i}',f'Y{i}')]
    base='['+','.join(coords)+'] -> '
    union=ctx.set(base+'{ : false }');count=0
    for s,blocks in templates(N):
        if max_schemas is not None and count>=max_schemas:
            return {'status':'INCONCLUSIVE','schemas':count,'partial_formula':str(union)}
        pars=coords+[f'K{i}' for i in range(s)]
        distinct=' and '.join(f'(X{i}!=X{j} or Y{i}!=Y{j})' for i in range(m) for j in range(i)) or 'true'
        plan=Schema(pars,blocks,domain=distinct,ctx=ctx)
        initial=plan.point_field([(Aff.var(f'X{i}'),Aff.var(f'Y{i}')) for i in range(m)])
        physical=plan.analyze(initial,method='lexmin',want_endpoint=False)['good']
        bad=plan.defect_times(L10)
        exact=plan.cardinality_at_most(bad,N).subtract(plan.cardinality_at_most(bad,N-1))
        finish=plan.ctx.set(plan.prefix+f'{{ [t] : t={plan.endpoint[3]}-1 }}')
        valid=physical.intersect(exact).intersect(bad.intersect(finish).params())
        if s:
            ctx._bind('isl_set_project_out',[C.c_void_p,C.c_int,C.c_uint,C.c_uint],C.c_void_p)
            valid=type(valid)(ctx,'set',ctx.checked(ctx.lib.isl_set_project_out(valid.copy_ptr(),1,2*m,s)))
        union=union.union(valid);count+=1
    return {'status':'COMPLETE','schemas':count,'formula':str(union.coalesce())}
