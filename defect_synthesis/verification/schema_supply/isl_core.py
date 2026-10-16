"""Small owning wrapper around the system ISL C API; every error is fatal."""
import ctypes as C
import ctypes.util
lib = C.CDLL(ctypes.util.find_library('isl') or 'libisl.so.23')
libc = C.CDLL(None)
libc.free.argtypes=[C.c_void_p]
def fn(name,args,restype=C.c_void_p):
    f=getattr(lib,name);f.argtypes=args;f.restype=restype;return f
P=C.c_void_p; S=C.c_char_p; I=C.c_int; U=C.c_uint
fn('isl_ctx_alloc',[]);fn('isl_ctx_free',[P],None)
fn('isl_options_set_on_error',[P,I],I)
fn('isl_ctx_last_error',[P],I);fn('isl_ctx_last_error_msg',[P],S)
for typ in ('set','map'):
    for name in ('copy','free','coalesce','lexmin','lexmax','compute_divs','make_disjoint'):
        fn(f'isl_{typ}_{name}',[P], None if name=='free' else P)
    fn(f'isl_{typ}_to_str',[P]);fn(f'isl_{typ}_read_from_str',[P,S])
    for name in ('union','intersect','subtract','intersect_params'):
        fn(f'isl_{typ}_{name}',[P,P])
    for name in ('is_empty','is_bounded') if typ=='set' else ('is_empty',):
        fn(f'isl_{typ}_{name}',[P],I)
    fn(f'isl_{typ}_is_equal',[P,P],I)
    fn(f'isl_{typ}_params',[P])
    fn(f'isl_{typ}_project_out',[P,I,U,U])
fn('isl_map_domain',[P]);fn('isl_map_range',[P]);fn('isl_map_reverse',[P])
fn('isl_map_apply_range',[P,P]);fn('isl_map_intersect_domain',[P,P]);fn('isl_map_intersect_range',[P,P])
fn('isl_set_apply',[P,P]);fn('isl_set_count_val',[P]);fn('isl_val_to_str',[P]);fn('isl_val_free',[P],None)
fn('isl_map_is_single_valued',[P],I);fn('isl_map_is_injective',[P],I)
fn('isl_set_dim_min',[P,I]);fn('isl_set_dim_max',[P,I]);fn('isl_pw_aff_as_map',[P])
fn('isl_set_get_basic_set_list',[P]);fn('isl_basic_set_list_n_basic_set',[P],I)
fn('isl_basic_set_list_get_at',[P,I]);fn('isl_basic_set_list_free',[P],None)
fn('isl_set_from_basic_set',[P]);fn('isl_set_get_stride',[P,I]);fn('isl_val_get_num_si',[P],C.c_long)
class Context:
    def __init__(self):
        self.p=lib.isl_ctx_alloc();lib.isl_options_set_on_error(self.p,1)
    def error(self):
        msg=lib.isl_ctx_last_error_msg(self.p)
        return msg.decode() if msg else 'ISL failure'
    def obj(self,typ,text):
        return Obj(self,typ,getattr(lib,f'isl_{typ}_read_from_str')(self.p,text.encode()))
    def set(self,text):return self.obj('set',text)
    def map(self,text):return self.obj('map',text)
class Obj:
    def __init__(self,ctx,typ,p):
        if not p:raise RuntimeError(ctx.error())
        self.ctx,self.typ,self.p=ctx,typ,p
    def __del__(self):
        if getattr(self,'p',None):getattr(lib,f'isl_{self.typ}_free')(self.p);self.p=None
    def cp(self):return getattr(lib,f'isl_{self.typ}_copy')(self.p)
    def __str__(self):
        p=getattr(lib,f'isl_{self.typ}_to_str')(self.p)
        if not p:raise RuntimeError(self.ctx.error())
        try:return C.string_at(p).decode()
        finally:libc.free(p)
    def unary(self,name,out=None):return Obj(self.ctx,out or self.typ,getattr(lib,f'isl_{self.typ}_{name}')(self.cp()))
    def binary(self,name,other,out=None):return Obj(self.ctx,out or self.typ,getattr(lib,f'isl_{self.typ}_{name}')(self.cp(),other.cp()))
    def coalesce(self):return self.unary('coalesce')
    def lexmin(self):return self.unary('lexmin')
    def lexmax(self):return self.unary('lexmax')
    def reverse(self):return self.unary('reverse')
    def domain(self):return self.unary('domain','set')
    def range(self):return self.unary('range','set')
    def params(self):return self.unary('params','set')
    def union(self,o):return self.binary('union',o)
    def intersect(self,o):return self.binary('intersect',o)
    def subtract(self,o):return self.binary('subtract',o)
    def intersect_params(self,o):return self.binary('intersect_params',o)
    def apply_range(self,o):return self.binary('apply_range',o)
    def intersect_domain(self,o):return self.binary('intersect_domain',o)
    def intersect_range(self,o):return self.binary('intersect_range',o)
    def apply(self,o):return self.binary('apply',o)
    def equal(self,o):
        z=getattr(lib,f'isl_{self.typ}_is_equal')(self.p,o.p)
        if z<0:raise RuntimeError(self.ctx.error())
        return bool(z)
    def empty(self):
        z=getattr(lib,f'isl_{self.typ}_is_empty')(self.p)
        if z<0:raise RuntimeError(self.ctx.error())
        return bool(z)
    def single(self):
        z=lib.isl_map_is_single_valued(self.p)
        if z<0:raise RuntimeError(self.ctx.error())
        return bool(z)
    def project(self,dim,first,n):return Obj(self.ctx,self.typ,getattr(lib,f'isl_{self.typ}_project_out')(self.cp(),dim,first,n))
    def basic_sets(self):
        p=lib.isl_set_get_basic_set_list(self.p)
        if not p:raise RuntimeError(self.ctx.error())
        try:
            count=lib.isl_basic_set_list_n_basic_set(p)
            if count<0:raise RuntimeError(self.ctx.error())
            for i in range(count):
                yield Obj(self.ctx,'set',lib.isl_set_from_basic_set(lib.isl_basic_set_list_get_at(p,i)))
        finally:lib.isl_basic_set_list_free(p)
    def count(self):
        p=lib.isl_set_count_val(self.p)
        if not p:raise RuntimeError(self.ctx.error())
        s=lib.isl_val_to_str(p)
        try:return int(C.string_at(s).decode())
        finally:libc.free(s);lib.isl_val_free(p)
    def stride(self):
        p=lib.isl_set_get_stride(self.p,0)
        if not p:raise RuntimeError(self.ctx.error())
        s=lib.isl_val_to_str(p)
        if not s:
            lib.isl_val_free(p);raise RuntimeError(self.ctx.error())
        try:return int(C.string_at(s).decode())
        finally:libc.free(s);lib.isl_val_free(p)
fn('isl_set_flat_product',[P,P])
Obj.flat_product = lambda self,o: self.binary('flat_product',o)
