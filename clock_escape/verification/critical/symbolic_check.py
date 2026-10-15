"""Optional exact polynomial identity check; requires SymPy, no numerical fits."""
import json
import sympy as s
from critical import REWARD_SIGNS, MOVES

a,b,U,V=s.symbols('a b U V',positive=True)
def head(u,v,h):
 if h==0:return 2/(b+1)*(u+1/u)*(v-b/v)
 if h==1:return 2/(a+1)*(u-a/u)*(v+1/v)
 if h==2:return 2/(b+1)*(u+1/u)*(1/v-b*v)
 return 2/(a+1)*(1/u-a*u)*(v+1/v)
rows=[]
for h in range(4):
 for black in (False,True):
  delta=-1 if black else 1
  hh=(h+delta)%4;dx,dy=MOVES[hh]
  ax=1 if h%2==0 else -1
  inc=-ax*delta*(U-1/U)*(V-1/V)+head(U*a**dx,V*b**dy,hh)-head(U,V,h)
  sx,sy=REWARD_SIGNS[h][black]
  residual=s.factor(inc-4*U**sx*V**sy)
  check=s.cancel(residual.subs(b,(a+3)/(a-1)))
  assert check==0
  rows.append({'heading':h,'black':black,'residual_before_critical_substitution':str(residual),'critical_residual':str(check)})
print(json.dumps({'status':'passed','identities':rows},indent=2))
