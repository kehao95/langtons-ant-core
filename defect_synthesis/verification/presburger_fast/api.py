"""Opt-in supplied-schema decision API; this does not enumerate global covers."""
from __future__ import annotations
import _paths  # Pin and load the unchanged sibling schema syntax.
from typing import Callable, Iterable
from compiler import Schema
from stream_qf import Encoder, Segment, Circuit, Expr, atom
from factor_dag import count_circuit
from solver import Session
import numeric


def solve_schema(schema: Schema, source: Iterable[Segment], *,
                 defects: int | None = None, exact: bool = False,
                 ends_bad: bool = False,
                 where: Callable[[Circuit], Expr] | None = None,
                 timeout_ms: int = 10000) -> dict:
    """Find one parameter assignment, with independent compressed replay.

    `where` constructs additional QF linear constraints using Circuit methods.
    All coordinates/exponents are otherwise unbounded. A supplied-schema UNSAT
    is NEVER an all-schema result. Errors and native limits produce UNKNOWN.
    Unsupported source/loop syntax raises ValueError, rather than weakening it.
    """
    if defects is not None and (type(defects) is not int or defects<0):
        raise ValueError('defects must be a nonnegative integer or None')
    source=tuple(source)
    try:
        enc=Encoder(schema,source);conditions=[enc.valid]
        if where is not None:conditions.append(where(enc.c))
        if defects is not None or ends_bad:
            count,state=count_circuit(schema,enc.c)
            if defects is not None:
                conditions.append(enc.c.eq(count,defects) if exact else enc.c.le(defects,count))
            if ends_bad:conditions.append(state.last_bad)
        condition=enc.c.and_(*conditions)
        with Session(timeout_ms) as solver:
            solver.run(enc.c.text(condition));status=solver.check()
            if status!='sat':
                return {'status':status.upper(),'scope':'supplied schema only',
                        'reason':'native solver resource limit or incomplete decision' if status=='unknown' else None}
            values=solver.values(schema.parameters) if schema.parameters else {}
        replay=numeric.verify(schema,source,values)
        count,last=numeric.factor_count(schema,values)
        if not replay['valid']:raise AssertionError('SAT physical witness failed independent replay')
        if defects is not None and (count!=defects if exact else count<defects):
            raise AssertionError('SAT lexical count failed independent replay')
        if ends_bad and not last:raise AssertionError('SAT final event failed independent replay')
        return {'status':'SAT','scope':'supplied schema only','parameters':values,
                'witness':dict(replay,defects=count,last_bad=last),'encoding':enc.stats()}
    except (ArithmeticError,MemoryError) as exc:
        return {'status':'UNKNOWN','scope':'supplied schema only','reason':str(exc)}
