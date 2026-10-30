"""Minimal owning wrapper for the system ISL exact integer-set API.
Errors are exceptions; they are never interpreted as empty sets.
"""
from __future__ import annotations
import ctypes as C
import ctypes.util

P=C.c_void_p
_path=ctypes.util.find_library('isl')
if not _path: raise ImportError('The system libisl library is required.')
lib=C.CDLL(_path); libc=C.CDLL(None)
libc.free.argtypes=[P];libc.free.restype=None

def bind(name,args,result=P):
    f=getattr(lib,name);f.argtypes=args;f.restype=result;return f

bind('isl_ctx_alloc',[]);bind('isl_ctx_free',[P],None)
bind('isl_options_set_on_error',[P,C.c_int],C.c_int)
bind('isl_ctx_last_error_msg',[P],C.c_char_p)
bind('isl_ctx_reset_error',[P],None)
bind('isl_version',[],C.c_char_p)
for kind in ('set','map'):
    bind('isl_'+kind+'_read_from_str',[P,C.c_char_p])
    for name in ('copy','coalesce','params'):
        bind('isl_'+kind+'_'+name,[P])
    bind('isl_'+kind+'_free',[P],None)
    bind('isl_'+kind+'_to_str',[P])
    for name in ('union','intersect','subtract','intersect_params'):
        bind('isl_'+kind+'_'+name,[P,P])
    bind('isl_'+kind+'_is_empty',[P],C.c_int)
    bind('isl_'+kind+'_is_equal',[P,P],C.c_int)
for name in ('domain','range'):
    bind('isl_map_'+name,[P])
bind('isl_map_intersect_range',[P,P])

class Context:
    def __init__(self):
        self.p=lib.isl_ctx_alloc()
        if not self.p:raise MemoryError('isl_ctx_alloc failed')
        lib.isl_options_set_on_error(self.p,1)
    def __del__(self):
        if getattr(self,'p',None):lib.isl_ctx_free(self.p);self.p=None
    def fail(self):
        m=lib.isl_ctx_last_error_msg(self.p)
        message=m.decode() if m else 'ISL operation failed'
        lib.isl_ctx_reset_error(self.p)
        raise ArithmeticError(message)
    def set(self,s):return Obj(self,'set',lib.isl_set_read_from_str(self.p,s.encode()))
    def map(self,s):return Obj(self,'map',lib.isl_map_read_from_str(self.p,s.encode()))
    @property
    def version(self):return lib.isl_version().decode().strip()

class Obj:
    def __init__(self,ctx,kind,p):
        self.ctx,self.kind,self.p=ctx,kind,p
        if not p:ctx.fail()
    def __del__(self):
        if getattr(self,'p',None):getattr(lib,'isl_'+self.kind+'_free')(self.p);self.p=None
    def copy(self):
        p=getattr(lib,'isl_'+self.kind+'_copy')(self.p)
        if not p:self.ctx.fail()
        return p
    def unary(self,name,out=None):
        return Obj(self.ctx,out or self.kind,getattr(lib,'isl_'+self.kind+'_'+name)(self.copy()))
    def binary(self,name,other):
        if self.ctx is not other.ctx:raise ValueError('Different ISL contexts')
        return Obj(self.ctx,self.kind,getattr(lib,'isl_'+self.kind+'_'+name)(self.copy(),other.copy()))
    def union(self,o):return self.binary('union',o)
    def intersect(self,o):return self.binary('intersect',o)
    def subtract(self,o):return self.binary('subtract',o)
    def intersect_params(self,o):return self.binary('intersect_params',o)
    def intersect_range(self,o):return self.binary('intersect_range',o)
    def domain(self):return self.unary('domain','set')
    def coalesce(self):return self.unary('coalesce')
    def empty(self):
        z=getattr(lib,'isl_'+self.kind+'_is_empty')(self.p)
        if z<0:self.ctx.fail()
        return bool(z)
    def equal(self,o):
        if self.ctx is not o.ctx or self.kind!=o.kind:raise ValueError('Incompatible ISL objects')
        z=getattr(lib,'isl_'+self.kind+'_is_equal')(self.p,o.p)
        if z<0:self.ctx.fail()
        return bool(z)
    def __str__(self):
        p=getattr(lib,'isl_'+self.kind+'_to_str')(self.p)
        if not p:self.ctx.fail()
        try:return C.string_at(p).decode()
        finally:libc.free(p)

def xor(a,b):return a.subtract(b).union(b.subtract(a))
