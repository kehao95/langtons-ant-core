"""Small owning ctypes bridge to exact integer-set operations in libisl.
No private API, numerical optimizer, or Python package is required.
An operation-limit or library error raises an exception; it is never UNSAT.
"""
from __future__ import annotations
import ctypes as C
import ctypes.util

class ArithmeticFailure(RuntimeError):
    pass

class Context:
    def __init__(self, max_operations: int = 0):
        name=ctypes.util.find_library('isl')
        if not name: raise ArithmeticFailure('libisl is required')
        self.lib=C.CDLL(name)
        self.libc=C.CDLL(None)
        self.libc.free.argtypes=[C.c_void_p]; self.libc.free.restype=None
        self._bind('isl_ctx_alloc',[],C.c_void_p)
        self._bind('isl_ctx_free',[C.c_void_p],None)
        self._bind('isl_ctx_set_max_operations',[C.c_void_p,C.c_ulong],None)
        self._bind('isl_ctx_last_error_msg',[C.c_void_p],C.c_char_p)
        self._bind('isl_options_set_on_error',[C.c_void_p,C.c_int],C.c_int)
        self._bind('isl_version',[],C.c_char_p)
        self.ptr=self.lib.isl_ctx_alloc()
        self.lib.isl_options_set_on_error(self.ptr,1) # CONTINUE: raise, never abort
        self.lib.isl_ctx_set_max_operations(self.ptr,max_operations)
        for kind in ('set','map'):
            self._bind(f'isl_{kind}_read_from_str',[C.c_void_p,C.c_char_p],C.c_void_p)
            self._bind(f'isl_{kind}_copy',[C.c_void_p],C.c_void_p)
            self._bind(f'isl_{kind}_free',[C.c_void_p],None)
            self._bind(f'isl_{kind}_to_str',[C.c_void_p],C.c_void_p)
            for op in ('union','intersect','subtract','intersect_params'):
                self._bind(f'isl_{kind}_{op}',[C.c_void_p,C.c_void_p],C.c_void_p)
            for op in ('coalesce','params'):
                self._bind(f'isl_{kind}_{op}',[C.c_void_p],C.c_void_p)
            for op in ('is_empty',): self._bind(f'isl_{kind}_{op}',[C.c_void_p],C.c_int)
            for op in ('is_equal','is_subset'):
                self._bind(f'isl_{kind}_{op}',[C.c_void_p,C.c_void_p],C.c_int)
        for op in ('reverse','domain','range','wrap'):
            self._bind(f'isl_map_{op}',[C.c_void_p],C.c_void_p)
        for op in ('apply_range','intersect_domain','intersect_range'):
            self._bind(f'isl_map_{op}',[C.c_void_p,C.c_void_p],C.c_void_p)
        self._bind('isl_set_unwrap',[C.c_void_p],C.c_void_p)
        self._bind('isl_set_apply',[C.c_void_p,C.c_void_p],C.c_void_p)
        self._bind('isl_set_complement',[C.c_void_p],C.c_void_p)
        self._bind('isl_set_is_bounded',[C.c_void_p],C.c_int)
    def _bind(self,n,a,r):
        f=getattr(self.lib,n);f.argtypes=a;f.restype=r
    @property
    def version(self): return self.lib.isl_version().decode()
    def checked(self,p):
        if not p:
            msg=self.lib.isl_ctx_last_error_msg(self.ptr)
            raise ArithmeticFailure(msg.decode() if msg else 'isl operation failed')
        return p
    def parse(self,kind,text):
        ptr=getattr(self.lib,f'isl_{kind}_read_from_str')(self.ptr,text.encode())
        return Obj(self,kind,self.checked(ptr))
    def set(self,text): return self.parse('set',text)
    def map(self,text): return self.parse('map',text)
    def __del__(self):
        if getattr(self,'ptr',None):
            self.lib.isl_ctx_free(self.ptr); self.ptr=None

class Obj:
    def __init__(self,ctx,kind,ptr): self.ctx=ctx;self.kind=kind;self.ptr=ptr
    def __del__(self):
        if getattr(self,'ptr',None):
            getattr(self.ctx.lib,f'isl_{self.kind}_free')(self.ptr);self.ptr=None
    def copy_ptr(self):return getattr(self.ctx.lib,f'isl_{self.kind}_copy')(self.ptr)
    def __str__(self):
        p=getattr(self.ctx.lib,f'isl_{self.kind}_to_str')(self.ptr)
        self.ctx.checked(p)
        try:return C.string_at(p).decode()
        finally:self.ctx.libc.free(p)
    def op(self,name,*args,result=None):
        if any(a.ctx is not self.ctx for a in args):raise ValueError('mixed contexts')
        p=getattr(self.ctx.lib,f'isl_{self.kind}_{name}')(self.copy_ptr(),*[a.copy_ptr() for a in args])
        return Obj(self.ctx,result or self.kind,self.ctx.checked(p))
    def pred(self,name,*args):
        n=getattr(self.ctx.lib,f'isl_{self.kind}_{name}')(self.ptr,*[a.ptr for a in args])
        if n<0: raise ArithmeticFailure('isl predicate failed')
        return bool(n)
    def union(self,b):return self.op('union',b)
    def intersect(self,b):return self.op('intersect',b)
    def subtract(self,b):return self.op('subtract',b)
    def coalesce(self):return self.op('coalesce')
    def params(self):return self.op('params',result='set')
    def restrict(self,b):return self.op('intersect_params',b)
    def empty(self):return self.pred('is_empty')
    def equal(self,b):return self.pred('is_equal',b)
    def subset(self,b):return self.pred('is_subset',b)
    def reverse(self):return self.op('reverse')
    def then(self,b):return self.op('apply_range',b)
    def domain(self):return self.op('domain',result='set')
    def range(self):return self.op('range',result='set')
    def on_domain(self,b):return self.op('intersect_domain',b)
    def on_range(self,b):return self.op('intersect_range',b)
    def apply(self,b):return self.op('apply',b,result='set')

def count_fixed(obj: Obj) -> int:
    """Count a bounded set after ALL symbolic parameters have been fixed."""
    c=obj.ctx
    c._bind('isl_set_count_val',[C.c_void_p],C.c_void_p)
    c._bind('isl_val_to_str',[C.c_void_p],C.c_void_p)
    c._bind('isl_val_free',[C.c_void_p],None)
    p=c.checked(c.lib.isl_set_count_val(obj.ptr))
    s=c.checked(c.lib.isl_val_to_str(p))
    try: result=C.string_at(s).decode()
    finally:c.libc.free(s);c.lib.isl_val_free(p)
    try:return int(result)
    except ValueError:raise ArithmeticFailure('set is not a fixed finite integer count: '+result)
