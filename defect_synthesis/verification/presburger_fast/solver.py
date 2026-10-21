"""Minimal libz3 command bridge. UNKNOWN/errors are never UNSAT.

No binary or Python binding is bundled. SMT-LIB files can be run with any
compatible solver. Numeric witnesses are independently checked by callers.
"""
from __future__ import annotations
import ctypes as C
import ctypes.util
import re

_path=C.util.find_library('z3')
if not _path: raise ImportError('system libz3 required for these optional solver checks')
_lib=C.CDLL(_path); P=C.c_void_p

def bind(name,args,out):
    f=getattr(_lib,name); f.argtypes=args; f.restype=out; return f
_mkcfg=bind('Z3_mk_config',[],P)
_delcfg=bind('Z3_del_config',[P],None)
_mkctx=bind('Z3_mk_context',[P],P)
_delctx=bind('Z3_del_context',[P],None)
_eval=bind('Z3_eval_smtlib2_string',[P,C.c_char_p],C.c_char_p)
_error=bind('Z3_get_error_code',[P],C.c_uint)
_message=bind('Z3_get_error_msg',[P,C.c_uint],C.c_char_p)
_HANDLER=C.CFUNCTYPE(None,P,C.c_uint)
_set_handler=bind('Z3_set_error_handler',[P,_HANDLER],None)
_version=bind('Z3_get_full_version',[],C.c_char_p)

@_HANDLER
def _ignore(ctx,code): pass  # checked immediately after each call, not ignored semantically

class Session:
    def __init__(self, timeout_ms=10000):
        if type(timeout_ms) is not int or timeout_ms<0:raise ValueError('nonnegative timeout required')
        cfg=_mkcfg();self.ptr=_mkctx(cfg);_delcfg(cfg)
        if not self.ptr:raise MemoryError('Z3 context')
        _set_handler(self.ptr,_ignore)
        self.run(f'(set-option :timeout {timeout_ms})\n(set-option :produce-models true)\n(set-logic QF_LIA)')
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
    def close(self):
        if self.ptr:_delctx(self.ptr);self.ptr=None
    def run(self,text):
        if not self.ptr:raise RuntimeError('closed context')
        out=_eval(self.ptr,text.encode());code=_error(self.ptr)
        if code:raise ArithmeticError(_message(self.ptr,code).decode())
        if out is None:raise ArithmeticError('empty Z3 response')
        text=out.decode().strip()
        if '(error ' in text:raise ArithmeticError(text)
        return text
    def check(self, assertion=None):
        prefix='' if assertion is None else '(push 1)\n(assert '+assertion+')\n'
        answer=self.run(prefix+'(check-sat)')
        if assertion is not None:self.run('(pop 1)')
        if answer not in ('sat','unsat','unknown'):raise ArithmeticError(answer)
        return answer
    def values(self,names):
        raw=self.run('(get-value ('+' '.join(names)+'))')
        tokens=re.findall(r'\(|\)|[^\s()]+',raw);it=iter(tokens)
        def parse(tok):
            if tok!='(':return tok
            out=[]
            for t in it:
                if t==')':return out
                out.append(parse(t))
            raise ValueError('bad solver output')
        tree=parse(next(it))
        def integer(x):
            if isinstance(x,str):return int(x)
            if len(x)==2 and x[0]=='-':return -integer(x[1])
            raise ValueError('noninteger solver value')
        return {k:integer(v) for k,v in tree}

def version():return _version().decode()
