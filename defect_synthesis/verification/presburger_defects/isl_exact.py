"""Small ownership-safe ctypes bridge to libisl's exact integer set algebra.

No bundled binary and no approximate arithmetic. Each operation copies its input
before calling an __isl_take function. ISL errors, including resource exhaustion,
raise ArithmeticError; they are never interpreted as an empty set.
"""
from __future__ import annotations
import ctypes as C
import ctypes.util

_P = C.c_void_p
_path = ctypes.util.find_library('isl')
if not _path:
    raise ImportError('libisl is required (e.g. the system libisl23 package)')
_lib = C.CDLL(_path)
_libc = C.CDLL(None)
_libc.free.argtypes = [_P]
_libc.free.restype = None

def _bind(name, args, result=_P):
    fn = getattr(_lib, name)
    fn.argtypes, fn.restype = args, result
    return fn

_alloc = _bind('isl_ctx_alloc', [])
_ctx_free = _bind('isl_ctx_free', [_P], None)
_error = _bind('isl_ctx_last_error_msg', [_P], C.c_char_p)
_reset = _bind('isl_ctx_reset_error', [_P], None)
_onerror = _bind('isl_options_set_on_error', [_P, C.c_int], C.c_int)
_maxops = _bind('isl_ctx_set_max_operations', [_P, C.c_ulong], None)
_resetops = _bind('isl_ctx_reset_operations', [_P], None)
_version = _bind('isl_version', [], C.c_char_p)
_FUN = {}
for kind in ('set', 'map'):
    for name in ('copy', 'free', 'coalesce', 'params'):
        _FUN[kind, name] = _bind(f'isl_{kind}_{name}', [_P])
    _FUN[kind, 'read'] = _bind(f'isl_{kind}_read_from_str', [_P, C.c_char_p])
    _FUN[kind, 'str'] = _bind(f'isl_{kind}_to_str', [_P])
    for name in ('union', 'intersect', 'subtract', 'intersect_params'):
        _FUN[kind, name] = _bind(f'isl_{kind}_{name}', [_P, _P])
    for name in ('is_empty',):
        _FUN[kind, name] = _bind(f'isl_{kind}_{name}', [_P], C.c_int)
    _FUN[kind, 'is_equal'] = _bind(f'isl_{kind}_is_equal', [_P, _P], C.c_int)
for name in ('reverse','lexmin','lexmax','domain','range'):
    _FUN['map', name] = _bind(f'isl_map_{name}', [_P])
_FUN['map','apply_range'] = _bind('isl_map_apply_range', [_P,_P])
_FUN['set','project_out'] = _bind('isl_set_project_out', [_P,C.c_int,C.c_uint,C.c_uint])

class Context:
    def __init__(self, max_operations: int = 0):
        if type(max_operations) is not int or max_operations < 0:
            raise ValueError('max_operations must be a nonnegative integer')
        self.ptr = _alloc()
        if not self.ptr:
            raise MemoryError('isl_ctx_alloc')
        _onerror(self.ptr, 1)  # ISL_ON_ERROR_CONTINUE; Python raises instead.
        _maxops(self.ptr, max_operations)
    def __del__(self):
        if getattr(self, 'ptr', None):
            _ctx_free(self.ptr)
            self.ptr = None
    def fail(self):
        msg = _error(self.ptr)
        _reset(self.ptr)
        raise ArithmeticError(msg.decode() if msg else 'libisl operation failed')
    def set(self, text: str):
        return Object(self, 'set', _FUN['set','read'](self.ptr,text.encode()))
    def map(self, text: str):
        return Object(self, 'map', _FUN['map','read'](self.ptr,text.encode()))
    def reset_operations(self):
        _resetops(self.ptr)
    @property
    def version(self):
        return _version().decode().strip()

class Object:
    def __init__(self, ctx: Context, kind: str, ptr):
        self.ctx, self.kind, self.ptr = ctx, kind, ptr
        if not ptr:
            ctx.fail()
    def __del__(self):
        if getattr(self,'ptr',None):
            _FUN[self.kind,'free'](self.ptr)
            self.ptr = None
    def _copy(self):
        ptr = _FUN[self.kind,'copy'](self.ptr)
        if not ptr: self.ctx.fail()
        return ptr
    def unary(self, name: str, out: str | None = None):
        return Object(self.ctx, out or self.kind, _FUN[self.kind,name](self._copy()))
    def binary(self, name: str, other: Object):
        if self.ctx is not other.ctx:
            raise ValueError('cannot combine independent ISL contexts')
        return Object(self.ctx, self.kind, _FUN[self.kind,name](self._copy(),other._copy()))
    def __str__(self):
        p = _FUN[self.kind,'str'](self.ptr)
        if not p: self.ctx.fail()
        try: return C.string_at(p).decode()
        finally: _libc.free(p)
    def coalesce(self): return self.unary('coalesce')
    def params(self): return self.unary('params','set')
    def union(self, other): return self.binary('union',other)
    def intersect(self, other): return self.binary('intersect',other)
    def subtract(self, other): return self.binary('subtract',other)
    def intersect_params(self, other): return self.binary('intersect_params',other)
    def reverse(self): return self.unary('reverse')
    def lexmin(self): return self.unary('lexmin')
    def lexmax(self): return self.unary('lexmax')
    def domain(self): return self.unary('domain','set')
    def range(self): return self.unary('range','set')
    def apply_range(self, other): return self.binary('apply_range',other)
    def project_params(self, first: int, count: int):
        if self.kind != 'set': raise TypeError('project_params expects a set')
        return Object(self.ctx, 'set', _FUN['set','project_out'](self._copy(),1,first,count))
    def is_empty(self):
        result = _FUN[self.kind,'is_empty'](self.ptr)
        if result < 0: self.ctx.fail()
        return bool(result)
    def is_equal(self, other):
        if self.ctx is not other.ctx or self.kind != other.kind:
            raise ValueError('objects must have one kind and context')
        result = _FUN[self.kind,'is_equal'](self.ptr,other.ptr)
        if result < 0: self.ctx.fail()
        return bool(result)

# Map projections and point sampling used by the finite-budget driver.
_FUN['map','project_out'] = _bind('isl_map_project_out', [_P,C.c_int,C.c_uint,C.c_uint])
_FUN['map','intersect_domain'] = _bind('isl_map_intersect_domain', [_P,_P])
_set_move = _bind('isl_set_move_dims', [_P,C.c_int,C.c_uint,C.c_int,C.c_uint,C.c_uint])
_sample = _bind('isl_set_sample_point', [_P])
_point_str = _bind('isl_point_to_str', [_P])
_point_free = _bind('isl_point_free', [_P])

def project_map_params(obj: Object, first: int, count: int):
    if obj.kind!='map': raise TypeError('map required')
    return Object(obj.ctx,'map',_FUN['map','project_out'](obj._copy(),1,first,count))

def sample_parameters(obj: Object, count: int) -> tuple[int,...] | None:
    """One integer parameter assignment; input must have zero set dimensions."""
    import re
    if obj.kind!='set': raise TypeError('set required')
    if obj.is_empty(): return None
    moved=_set_move(obj._copy(),3,0,1,0,count) if count else obj._copy()
    if not moved: obj.ctx.fail()
    point=_sample(moved)
    if not point: obj.ctx.fail()
    text=_point_str(point)
    if not text:
        _point_free(point);obj.ctx.fail()
    try: rendered=C.string_at(text).decode()
    finally:
        _libc.free(text);_point_free(point)
    match=re.fullmatch(r'\{\s*\[([^\]]*)\]\s*\}',rendered)
    if not match: raise ArithmeticError('unexpected exact sample format: '+rendered)
    values=tuple(int(x.strip()) for x in match.group(1).split(',') if x.strip())
    if len(values)!=count: raise ArithmeticError('unexpected sample dimension')
    return values
