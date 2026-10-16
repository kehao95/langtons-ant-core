"""Exact opt-in fixed-schema optimizations; no change to global schema coverage.

Unary cardinality thresholds use powers of the strict order on read times,
not (bound+1)-fold Cartesian products. Whitelist matching shares Boolean
subexpressions in a reduced decision DAG. libisl failures remain exceptions.
"""
from __future__ import annotations
import ctypes as C
from functools import lru_cache
import hashlib
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1] / 'defect_resource_spectrum' / 'code'
PINS = {
    'isl_bridge.py': '7b58e0a9b97c6cdc3277bc9053e3c905b3fe242b970573bb31d7f7851503d949',
    'trace_arithmetic.py': '7b53fa550bbc60b167610eeb5955dc2812c37f193a1b9804b8078d7761eaf356',
}
for name, digest in PINS.items():
    path = BASE / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise RuntimeError('Changed baseline requires a new equivalence audit: ' + name)
    loaded = sys.modules.get(path.stem)
    if loaded is not None and Path(loaded.__file__).resolve() != path.resolve():
        raise RuntimeError('Conflicting imported baseline: ' + name)
sys.path.insert(0, str(BASE))
from isl_bridge import Context, Obj, ArithmeticFailure  # noqa: E402
from trace_arithmetic import Aff, Block, Schema  # noqa: E402


def _unary(schema: Schema, times: Obj) -> None:
    if times.ctx is not schema.ctx or times.kind != 'set':
        raise ValueError('A time set in the schema context is required')
    schema.ctx._bind('isl_set_dim', [C.c_void_p, C.c_int], C.c_int)
    dimension = schema.ctx.lib.isl_set_dim(times.ptr, 3)  # isl_dim_set
    if dimension < 0:
        raise ArithmeticFailure('Cannot inspect set dimensions')
    if dimension != 1:
        raise ValueError('Cardinality optimization requires ONE time dimension')


class CountQuery:
    """Reuse squared strict-order relations for several INTEGER threshold queries.

    For any parameter fibre F, (a,b) in order**m witnesses m+1 DISTINCT
    elements of F. It follows that |F|>m iff order**m is nonempty (m>=1).
    This also correctly rejects finite thresholds on infinite integer fibres.
    No transitive-closure approximation or parametric multiplication is used.
    """
    def __init__(self, schema: Schema, times: Obj):
        _unary(schema, times)
        self.schema = schema
        self.times = times.restrict(schema.domain)
        self.powers: list[Obj] = []
        self.total_compositions = 0
        self.last_stats: dict[str, int] = {}

    def _power(self, bit: int) -> Obj:
        if not self.powers:
            order = self.schema.ctx.map(self.schema.prefix + '{ [t] -> [u] : t<u }')
            self.powers.append(order.on_domain(self.times).on_range(self.times).coalesce())
        while len(self.powers) <= bit:
            last = self.powers[-1]
            self.powers.append(last.then(last).coalesce())
            self.total_compositions += 1
        return self.powers[bit]

    def at_most(self, bound: int) -> Obj:
        if type(bound) is not int or bound < 0:
            raise ValueError('A nonnegative integer threshold is required')
        before = self.total_compositions
        if bound == 0:
            too_many = self.times.params()
        else:
            result = None
            rest, bit = bound, 0
            while rest:
                if rest & 1:
                    power = self._power(bit)
                    if result is None:
                        result = power
                    else:
                        result = result.then(power).coalesce()
                        self.total_compositions += 1
                rest >>= 1
                bit += 1
            assert result is not None
            too_many = result.params()
        answer = self.schema.domain.subtract(too_many).coalesce()
        self.last_stats = {
            'threshold_bits': bound.bit_length(),
            'new_compositions': self.total_compositions - before,
            'cached_powers': len(self.powers),
            'explicit_time_dimensions': 2 if bound else 1,
        }
        return answer


@lru_cache(maxsize=128)
def _decision_dag(words: tuple[str, ...]):
    """Immutable Boolean DAG; nodes 0/1 reject/accept, R=0 and L=1."""
    if not words:
        raise ValueError('Nonempty factor whitelist required')
    width = len(words[0])
    if not width or any(len(w) != width or set(w) - {'R', 'L'} for w in words):
        raise ValueError('Uniform nonempty R/L words required')
    nodes = [None, None]
    unique = {}

    def build(offset, suffixes):
        if not suffixes:
            return 0
        if offset == width:
            return 1
        r = build(offset + 1, tuple(w[1:] for w in suffixes if w[0] == 'R'))
        l = build(offset + 1, tuple(w[1:] for w in suffixes if w[0] == 'L'))
        if r == l:
            return r  # R/L form a partition at every complete schema window.
        key = (offset, r, l)
        if key not in unique:
            unique[key] = len(nodes)
            nodes.append(key)
        return unique[key]

    root = build(0, words)
    return width, tuple(nodes), root


def dag_defect_times(schema: Schema, legal_factors: set[str], stats=None) -> Obj:
    """Exact forbidden-window END times, sharing equivalent whitelist suffixes.

    The schema defines exactly one R/L letter at each consecutive time from
    zero to its length. Thus shifted R/L masks partition every complete window.
    This is necessary for the identical-branch reduction in _decision_dag.
    """
    words = tuple(sorted(legal_factors))
    width, nodes, root = _decision_dag(words)
    possible = schema.times.intersect(schema.ctx.set(
        schema.prefix + f'{{ [t] : t>={width-1} }}'))
    empty = schema.ctx.set(schema.prefix + '{ [t] : false }')
    values = {0: empty, 1: possible}
    letter_times = (schema.right.domain(), schema.left.domain())
    masks = {}
    intersections = unions = shifts = 0
    for node_id in range(2, len(nodes)):
        offset, r, l = nodes[node_id]
        terms = []
        for letter, child in enumerate((r, l)):
            if child == 0:
                continue
            key = (offset, letter)
            if key not in masks:
                move = schema.ctx.map(schema.prefix +
                    f'{{ [t] -> [u] : u=t+{width-1-offset} }}')
                masks[key] = letter_times[letter].apply(move)
                shifts += 1
            terms.append(masks[key].intersect(values[child]))
            intersections += 1
        if len(terms) == 2:
            values[node_id] = terms[0].union(terms[1]).coalesce()
            unions += 1
        else:
            values[node_id] = terms[0].coalesce()
    answer = possible.subtract(values[root]).coalesce()
    if stats is not None:
        stats.update({'dag_nodes': len(nodes)-2, 'mask_intersections': intersections,
                      'mask_unions': unions, 'shifts': shifts,
                      'baseline_mask_intersections': width*len(words),
                      'baseline_mask_unions': len(words)})
    return answer


class FastSchema(Schema):
    """Drop-in opt-in class for the two optimized queries; other methods unchanged."""
    def cardinality_at_most(self, times: Obj, bound: int):
        query = CountQuery(self, times)
        answer = query.at_most(bound)
        self.last_count_stats = query.last_stats
        return answer

    def defect_times(self, legal_factors: set[str]):
        self.last_factor_stats = {}
        return dag_defect_times(self, legal_factors, self.last_factor_stats)
