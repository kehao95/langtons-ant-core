"""Complete but deliberately enormous finite schema cover for a fixed J10 budget.

The bound is an imported analytic coverage obligation, not established by running
this generator. A cutoff NEVER establishes exhaustion or an all-coordinate NO.
The supplied-schema compiler is the useful operational component. No full N>=1
cover traversal is included in the retained validation report.
"""
from __future__ import annotations
from itertools import product
from math import comb
from compiler import Schema, Power, var, W, T, A, geometry, compile_schema, defect_domain, exact_seed_formula
from isl_exact import Context, sample_parameters

MODES=(W,T,A)
LOOPS=tuple(sorted({w[i:]+w[:i] for w in MODES for i in range(len(w))}))


def cover_bounds(N: int):
    if type(N) is not int or N<0: raise ValueError('N must be a nonnegative integer')
    # Each of N+1 ten-legal runs: <=5 loops, <=1322 nonpowered letters;
    # 2048 is a deliberately conservative cap. Add the <=N removed bad letters.
    return 5*(N+1),2048*(N+1)+N


def compositions(total: int, slots: int):
    if slots==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,slots-1):
                yield (first,)+tail


def descriptions(max_powers: int, max_fixed: int, loops=LOOPS):
    """All shapes within supplied bounds, finite but NOT generally tractable.

    Deterministic order by sum(power slots, fixed letters). Zero powers are
    allowed by the later arithmetic, so this collection contains duplicates.
    """
    if any(type(v) is not int or v<0 for v in (max_powers,max_fixed)):
        raise ValueError('nonnegative bounds required')
    for u in loops:
        if not u or geometry(u)[2]!=0: raise ValueError('non-resetting loop')
    for size in range(max_powers+max_fixed+1):
        for powers in range(max(0,size-max_fixed),min(max_powers,size)+1):
            fixed=size-powers
            for cuts in compositions(fixed,powers+1):
                for letters in product('LR',repeat=fixed):
                    w=''.join(letters);start=0;pieces=[]
                    for length in cuts:
                        pieces.append(w[start:start+length]);start+=length
                    for words in product(loops,repeat=powers):
                        yield tuple(pieces),tuple(words)


def descriptor_count(max_powers: int,max_fixed: int,loop_count: int):
    return sum((2**length)*comb(length+s,s)*(loop_count**s)
               for s in range(max_powers+1) for length in range(max_fixed+1))


def make_schema(parameters,pieces,words,domain='1=1'):
    exponent_names=tuple(f'rep{i}' for i in range(len(words)))
    if set(parameters)&set(exponent_names): raise ValueError('reserved repetition parameter')
    parts=[]
    for i,w in enumerate(words):
        parts += [pieces[i],Power(w,var(exponent_names[i]))]
    parts += [pieces[-1]]
    return Schema((*parameters,*exponent_names),parts,domain=domain)


def all_coordinate_existence(m: int,N: int,*,max_schemas: int|None=None,max_operations: int=0):
    """Theoretical total E_(m,N) decision with explicit optional resource guards.

    SAT includes a complete integer seed and a bounded-power word. It is not an
    HC-negative answer. UNSAT is permitted ONLY on exhaustion of the full cover.
    Driver is intentionally not advertised as practical for a large N.
    """
    if type(m) is not int or m<0 or type(N) is not int or N<1:
        raise ValueError('m>=0 and N>=1 must be integers')
    if max_schemas is not None and (type(max_schemas) is not int or max_schemas<0):
        raise ValueError('invalid schema limit')
    params=tuple(v for i in range(m) for v in (f'z{i}x',f'z{i}y'))
    black,distinct=exact_seed_formula([(f'z{i}x',f'z{i}y') for i in range(m)])
    ctx=Context(max_operations); visited=0
    try:
        for pieces,words in descriptions(*cover_bounds(N)):
            if max_schemas is not None and visited>=max_schemas:
                return dict(status='UNKNOWN',reason='incomplete schema cover',schemas=visited)
            visited+=1;ctx.reset_operations()
            s=make_schema(params,pieces,words)  # keep distinctness out of read-map geometry
            target=defect_domain(s,ctx,N,exact=True,ends_bad=True)
            if target.is_empty(): continue
            c=compile_schema(s,ctx,s.black_set(ctx,black))
            good=c.feasible.intersect(target).intersect(s.param_set(ctx,distinct))
            if good.is_empty():continue
            sample=sample_parameters(good,len(s.parameters))
            assignment=dict(zip(s.parameters,sample))
            return dict(status='SAT',schemas=visited,
                        seed=[[assignment[f'z{i}x'],assignment[f'z{i}y']] for i in range(m)],
                        pieces=list(pieces),powers=[{'word':u,'exponent':assignment[f'rep{i}']}
                                                   for i,u in enumerate(words)],
                        post_time=s.length.evaluate(assignment),scope='finite N-defect witness only')
        return dict(status='UNSAT',schemas=visited,scope='complete all-coordinate finite-budget exclusion')
    except (ArithmeticError, MemoryError, RecursionError) as exc:
        return dict(status='UNKNOWN',reason=str(exc),schemas=visited)
