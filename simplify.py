from AST import *

def contains(expr, token):
    

def identityRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Var) and expr.expr.sym == expr.sym:
            return Num(1)
    return expr

def constantRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Num): #TODO add support for other vars
            return Num(0)
    return expr

def constMultRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Mul):
            consts = []
            notconsts = []
            for e in expr.expr.children:
                if isinstance(e, Num) or isinstance(e, Var) and e.sym != expr.sym:
                    consts.append(e)
                else:
                    notconsts.append(e)
            if notconsts == []:
                return Num(0)
            if consts == []:
                return expr
            c = consts[0] if len(consts) == 1 else Mul(consts)
            nc = nonconsts[0] if len(nonconsts) == 1 else Mul(nonconsts)

            return Mul(c, takeDeriv(Deriv(nc, expr.sym)))
    return expr

def sumRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Add):
            return Add([takeDeriv(Deriv(c, expr.sym)) for c in expr.expr.children])
    return expr

def powerRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Pow) \
            and isinstance(expr.expr.base, Var) and expr.expr.base.sym == expr.sym \
            and takeDeriv(Deriv(expr.expr.exp, expr.sym)) == Num(0):
                return Mul(expr.expr.exp, Pow(expr.expr.base, Sub(expr.expr.exp, Num(1))))
    return expr

def differenceRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Sub):
            return Sub(takeDeriv(Deriv(expr.expr.left, expr.sym), Deriv(expr.expr.right, expr.sym)))
    return expr

def productRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Mul):
            return Add(Mul(expr.expr.children[0], takeDeriv(Deriv(Mul(expr.expr.children[1:]), expr.sym))
                      ,Mul(Mul(expr.expr.children[1:]), takeDeriv(Deriv(expr.expr.children[0]), expr.sym))))
    return expr

def quotientRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Div):
            return Div(Sub(Mul(Deriv(expr.expr.top, expr.sym), expr.expr.bottom),
                           Mul(Deriv(expr.expr.bottom, expr.sym), expr.expr.top)),
                       Pow(expr.expr.bottom, Num(2)))
    return expr

def takeDeriv(expr):
    expr = identityRule(expr)
    expr = constMultRule(expr)
    expr = sumRule(expr)
    expr = differenceRule(expr)
    expr = powerRule(expr)
    expr = productRule(expr)
    expr = quotientRule(expr)
    return expr

print(takeDeriv(Deriv(Pow(Var("x"), Num(2)), "x")))
