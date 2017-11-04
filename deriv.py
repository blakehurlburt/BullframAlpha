from AST import *


def identityRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Var) and expr.expr == expr.sym:
            return Num(1)
    return expr

def constantRule(expr):
    if isinstance(expr, Deriv):
        if not expr.expr.contains(expr.sym):
            return Num(0)
    return expr

def constMultRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Mul):
            consts = []
            notconsts = []
            for e in expr.expr.children:
                if isinstance(e, Num) or isinstance(e, Var) and e != expr.sym:
                    consts.append(e)
                else:
                    notconsts.append(e)
            if notconsts == []:
                return Num(0)
            if consts == []:
                return expr
            c = consts[0] if len(consts) == 1 else Mul(consts)
            nc = notconsts[0] if len(notconsts) == 1 else Mul(notconsts)

            return Mul([c, takeDeriv(Deriv(nc, expr.sym))])
    return expr

def sumRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Add):
            return Add([takeDeriv(Deriv(c, expr.sym)) for c in expr.expr.children])
    return expr

def differenceRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Sub):
            return Sub(takeDeriv(Deriv(expr.expr.left, expr.sym)), takeDeriv(Deriv(expr.expr.right, expr.sym)))
    return expr

def powerRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Pow) \
            and isinstance(expr.expr.base, Var) and expr.expr.base == expr.sym \
            and not expr.expr.exp.contains(expr.sym):
                return Mul([expr.expr.exp, Pow(expr.expr.base, Sub(expr.expr.exp, Num(1)))])
    return expr

def productRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Mul):
            if len(expr.expr.children) == 2:
                return Add([Mul([expr.expr.children[0], takeDeriv(Deriv(expr.expr.children[1], expr.sym))]),
                            Mul([expr.expr.children[1], takeDeriv(Deriv(expr.expr.children[0], expr.sym))])])
            else:
                return Add([Mul([expr.expr.children[0], takeDeriv(Deriv(Mul(expr.expr.children[1:]), expr.sym))])
                       ,Mul([Mul(expr.expr.children[1:]), takeDeriv(Deriv(expr.expr.children[0], expr.sym))])])
    return expr

def quotientRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Div):
            return Div(Sub(Mul([takeDeriv(Deriv(expr.expr.top, expr.sym)), expr.expr.bottom]),
                           Mul([takeDeriv(Deriv(expr.expr.bottom, expr.sym)), expr.expr.top])),
                       Pow(expr.expr.bottom, Num(2)))
    return expr

def exponentRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Pow) and expr.expr.exp.contains(expr.sym)\
            and not expr.expr.base.contains(expr.sym):

            return Mul([Mul([expr.expr.base, expr.expr.exp]), Apply(Fun("ln"), expr.expr.exp)])
    return expr

def funExponentRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Pow) and expr.expr.exp.contains(expr.sym)\
            and expr.expr.base.contains(expr.sym):

            return Mul([expr.expr,
                       Add([Div(Mul([expr.expr.exp, takeDeriv(Deriv(expr.expr.base, expr.sym))]),
                                expr.expr.base),
                            Mul([Apply(Fun("ln"), expr.expr.base),
                                 takeDeriv(Deriv(expr.expr.exp, expr.sym))])])])
    return expr

def sinRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "sin"\
        and expr.expr.expr == expr.sym:
            return Apply(Fun("cos"), expr.expr.expr)
    return expr

def cosRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "cos"\
        and expr.expr.expr == expr.sym:
            return Mul([Apply(Fun("sin"), expr.expr.expr), Num(-1)])
    return expr

def tanRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "tan"\
        and expr.expr.expr == expr.sym:
            return Pow(Apply(Fun("sec"), expr.expr.expr), Num(2))
    return expr

def secRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "sec"\
        and expr.expr.expr == expr.sym:
            return Mul([Apply(Fun("sec"), expr.expr.expr), Apply(Fun("tan"), expr.expr.expr)])
    return expr

def cscRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "csc"\
        and expr.expr.expr == expr.sym:
            return Mul([Num(-1), Mul([Apply(Fun("csc"), expr.expr.expr), Apply(Fun("cot"), expr.expr.expr)])])
    return expr

def cotRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "cot"\
        and expr.expr.expr == expr.sym:
            return Mul([Num(-1), Pow(Apply(Fun("csc"), expr.expr.expr), Num(2))])
    return expr

def arcsinRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "arcsin"\
        and expr.expr.expr == expr.sym:
            return Div(Num(1), Pow(Sub(Num(1), Pow(expr.expr.expr, Num(2))), Div(Num(1),Num(2))))
    return expr

def chainRule(expr):
    if isinstance(expr, Deriv) and isinstance(expr.expr, Apply) and expr.expr.expr != expr.sym:
        return Mul([takeDeriv(Deriv(Apply(expr.expr.fun, expr.sym), expr.sym)).sub(expr.sym, expr.expr.expr),\
                    takeDeriv(Deriv(expr.expr.expr, expr.sym))])
    return expr

def arccosRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "arccos"\
        and expr.expr.expr == expr.sym:
            return Div(Num(-1), Pow(Sub(Num(1), Pow(expr.expr.expr, Num(2))), Div(Num(1),Num(2))))
    return expr

def arctanRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "arctan"\
        and expr.expr.expr == expr.sym:
            return Div(Num(1), Add([Num(1), Pow(expr.expr.expr, Num(2))]))
    return expr

def arcsecRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "arcsec"\
        and expr.expr.expr == expr.sym:
            return Div(Num(1), Mul([Apply(Fun("abs"), expr.expr.expr),\
                   (Pow(Sub(Pow(expr.expr.expr, Num(2)), Num(1)), Div(Num(1),Num(2))))]))
    return expr

def arccscRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "arccsc"\
        and expr.expr.expr == expr.sym:
            return Div(Num(-1), Mul([Apply(Fun("abs"), expr.expr.expr),\
                   (Pow(Sub(Pow(expr.expr.expr, Num(2)), Num(1)), Div(Num(1),Num(2))))]))
    return expr

def arccotRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "arccot"\
        and expr.expr.expr == expr.sym:
            return Div(Num(-1), Add([Num(1), Pow(expr.expr.expr, Num(2))]))
    return expr

def lnRule(expr):
    if isinstance(expr, Deriv):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == "ln"\
        and expr.expr.expr == expr.sym:
            return Div(Num(1), expr.sym)
    return expr

def takeDeriv(expr):
    expr = identityRule(expr)
    expr = constantRule(expr)
    expr = constMultRule(expr)
    expr = sumRule(expr)
    expr = differenceRule(expr)
    expr = powerRule(expr)
    expr = productRule(expr)
    expr = quotientRule(expr)
    expr = exponentRule(expr)
    expr = lnRule(expr)
    expr = sinRule(expr)
    expr = cosRule(expr)
    expr = tanRule(expr)
    expr = secRule(expr)
    expr = cscRule(expr)
    expr = cotRule(expr)
    expr = arcsinRule(expr)
    expr = arccosRule(expr)
    expr = arctanRule(expr)
    expr = arcsecRule(expr)
    expr = arccscRule(expr)
    expr = arccotRule(expr)
    expr = chainRule(expr)
    expr = funExponentRule(expr)
    return expr

print(takeDeriv(Deriv(Apply(Fun("ln"), Apply(Fun("sin"), Mul([Num(2), Var("x")]))), Var("x"))))
