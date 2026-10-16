"""Check a complete semilinear supply/defect certificate, then classify its rays."""
from fractions import Fraction

def need(ok,msg):
    if not ok:raise ValueError(msg)

def relation(ctx,components):
    rows=[]
    for comp in components:
        base=comp['base'];gs=comp['generators']
        need(len(base)==2 and all(type(x) is int and x>=0 for x in base),'invalid base')
        need(all(len(g)==2 and all(type(x) is int and x>=0 for x in g) for g in gs),'invalid generator')
        names=[f'q{i}' for i in range(len(gs))]
        eqs=[]
        for d,name in enumerate(('c','d')):
            eqs.append(name+'='+str(base[d])+''.join(f'+{g[d]}*{n}' for g,n in zip(gs,names)))
        if names:
            eqs=[f'exists ({",".join(names)}: '+ ' and '.join([*(f'{n}>=0' for n in names),*eqs])+')']
        rows.append('[c,d]: '+' and '.join(eqs))
    return ctx.set('{ '+'; '.join(rows or ['[c,d]:false'])+' }')

def verify(ctx,actual,components):
    supplied=relation(ctx,components)
    need(supplied.equal(actual),'semilinear certificate does not equal the complete computed relation')
    for comp in components:
        for dc,dd in comp['generators']:
            if dc==0 and dd>0:
                return {'kind':'fixed_mass_unbounded','mass':comp['base'][0],
                        'base_defects':comp['base'][1],'defect_stride':dd}
    alpha=max([Fraction(0)]+[Fraction(dd,dc) for comp in components for dc,dd in comp['generators'] if dc>0])
    beta=max([Fraction(comp['base'][1])-alpha*comp['base'][0] for comp in components],default=Fraction(0))
    # Verify again as an exact set inclusion, not only by arithmetic on generators.
    den=alpha.denominator*beta.denominator
    aa=int(alpha*den);bb=int(beta*den)
    need(actual.intersect(ctx.set(f'{{[c,d]:{den}*d>{aa}*c+({bb})}}')).empty(),'derived upper bound fails')
    return {'kind':'affine_budget','alpha':[alpha.numerator,alpha.denominator],
            'beta':[beta.numerator,beta.denominator]}
