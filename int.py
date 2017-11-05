from AST import *
from simplify import simplify
from deriv import takeDeriv

def constantRule(expr):
    if isinstance(expr, Int):
        if not expr.expr.contains(expr.sym):
            return Add([Mul([expr.expr,expr.sym]), Var("C")])
    return expr

def identityRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Var) and expr.expr == expr.sym:
            return Add([Mul([Div(Num(1),Num(2)), Pow(expr.expr,Num(2))]),Var("C")])
    return expr

def negationRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Neg):
            return Mul([Num(-1),takeInt(Int(expr.expr.exp, expr.sym))])
    return expr

def sumRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Add):
            return Add([takeInt(Int(c, expr.sym)) for c in expr.expr.factors])
    return expr

def differenceRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Sub):
            return Sub(takeInt(Int(expr.expr.left, expr.sym)), takeInt(Int(expr.expr.right, expr.sym)))
    return expr


def overxRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div) and expr.expr.bottom == expr.sym:
            return Add([Apply(Fun("ln"), Apply(Fun("abs"), expr.sym)), Var("C")])
    return expr

def lnRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == Fun("ln")\
        and expr.expr.expr == expr.sym:
            return Add([Sub(Mul([expr.sym, Apply(Fun("ln"), expr.sym)]), expr.sym),Var("C")])
    return expr

def exponentRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow) and expr.expr.exp.contains(expr.sym)\
                    and not expr.expr.base.contains(expr.sym):
                return Add([Div(expr.expr, Apply(Fun("ln"), expr.expr.base)), Var("C")])
    return expr


def powerRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow) \
            and isinstance(expr.expr.base, Var) and expr.expr.base == expr.sym \
            and not expr.expr.exp.contains(expr.sym):
                return Add([Mul([Div(Num(1), Add([expr.expr.exp, Num(1)])), Pow(expr.expr.base, Add([expr.expr.exp, Num(1)]))]),\
                       Var("C")])
    return expr

def sinRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == Fun("sin")\
        and expr.expr.expr == expr.sym:
            return Add([Mul([Num(-1),Apply(Fun("cos"), expr.expr.expr)]),Var("C")])
    return expr

def cosRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Apply) and expr.expr.fun.sym == Fun("cos")\
        and expr.expr.expr == expr.sym:
            return Add([Apply(Fun("sin"), expr.expr.expr),Var("C")])
    return expr

def sec2Rule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow)\
            and expr.expr.base == Apply(Fun("sec"), expr.sym) and expr.expr.exp == Num(2):
            return Add([Apply(Fun("tan"), expr.sym ),Var("C")])
    return expr

def csc2Rule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow)\
            and expr.expr.base == Apply(Fun("csc"), expr.sym) and expr.expr.exp == Num(2):
            return Add([Mul([Num(-1),Apply(Fun("cot"), expr.sym )]),Var("C")])
    return expr

def sectanRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Mul):
            if expr.expr.factors[0] == Apply(Fun("sec"), expr.sym) and expr.expr.factors[1] == Apply(Fun("tan"), expr.sym):
                return Add([Apply(Fun("sec"), expr.sym ),Var("C")])

            if expr.expr.factors[1] == Apply(Fun("sec"), expr.sym) and expr.expr.factors[0] == Apply(Fun("tan"), expr.sym):
                return Add([Apply(Fun("sec"), expr.sym ),Var("C")])
    return expr

def csccotRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Mul):
            if expr.expr.factors[0] == Apply(Fun("csc"), expr.sym) and expr.expr.factors[1] == Apply(Fun("cot"), expr.sym):
                return Add([Mul([Num(-1),Apply(Fun("csc"), expr.sym )]),Var("C")])

            if expr.expr.factors[1] == Apply(Fun("csc"), expr.sym) and expr.expr.factors[0] == Apply(Fun("cot"), expr.sym):
                return Add([Mul([Num(-1),Apply(Fun("csc"), expr.sym )]),Var("C")])
    return expr

def arcsinRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            if isinstance(expr.expr.bottom, Pow):
                if isinstance(expr.expr.bottom.base, Sub):
                    if expr.expr.top == Num(1) and expr.expr.bottom.exp == Div(Num(1), Num(2))\
                    and expr.expr.bottom.base.right == Pow(expr.sym, Num(2)) and expr.expr.bottom.base.left == Num(1):
                        return Add([Apply(Fun("arcsin"), expr.sym), Var("C")])
    return expr

# def arccosRule(expr):
#     if isinstance(expr, Int):
#         if isinstance(expr.expr, Div):
#             if isinstance(expr.expr.bottom, Pow):
#                 if isinstance(expr.expr.bottom.base, Sub):
#                     if expr.expr.top == Num(-1) and expr.expr.bottom.exp == Div(Num(1), Num(2))\
#                     and expr.expr.bottom.base.right == Pow(expr.sym, Num(2)) and expr.expr.bottom.base.left == Num(1):
#                         return Add([Apply(Fun("arccsc"), expr.sym), Var("C")])
#     return expr

def arctanRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            if isinstance(expr.expr.bottom, Add):
                if expr.expr.top == Num(1) and ((expr.expr.bottom == Add([Num(1),Pow(Var("x"), Num(2))]))\
                or (expr.expr.bottom == Add([Pow(Var("x"), Num(2)), Num(1)]))):
                    return Add([Apply(Fun("arctan"), expr.sym), Var("C")])
    return expr

def arcsecRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            if isinstance(expr.expr.bottom, Mul) and expr.expr.top == Num(1):
                if isinstance(expr.expr.bottom.factors[0], Apply) and isinstance(expr.expr.bottom.factors[1], Pow):
                    if expr.expr.bottom.factors[0].fun.sym== "abs" and expr.expr.bottom.factors[1].exp == Div(Num(1), Num (2)):
                        if isinstance(expr.expr.bottom.factors[1].base, Sub):
                            if isinstance(expr.expr.bottom.factors[1].base.left, Pow) and\
                            expr.expr.bottom.factors[1].base.right == Num(1) and\
                            expr.expr.bottom.factors[1].base.left.base == expr.sym and\
                            expr.expr.bottom.factors[1].base.left.exp == Num(2):
                                return Add([Apply(Fun("arcsec"), expr.sym), Var("C")])
    return expr


def usubRule(expr):
    apply_funcs=[Fun("sin"), Fun("cos"), Fun("tan"), Fun("sec"), Fun("csc"), Fun("cot"), Fun("ln")]
    if isinstance(expr, Int):
        if not isinstance(expr.expr, Mul):
            new_expr = Mul([Num(1), expr.expr])
        else:
            new_expr = expr.expr

        if isinstance(new_expr.factors[1], Pow):
            u =new_expr.factors[1].base
            if  not divSimp(Div(Mul([new_expr.factors[0], Pow(Var("u"), new_expr.factors[1].exp)]),\
                    takeDeriv(Deriv(u, expr.sym)))).contains(exrp.sym):

                usubintegral = takeInt(Int(Pow(Var("u"), new_expr.factors[1].exp), Var("u")))
                usubintegral = usubintegral.sub(Var("u"),u)

            return usubintegral

        if isinstance(new_expr.factors[0], Pow):
            u =new_expr.factors[0].base
            if  not divSimp(Div(Mul([new_expr.factors[1], Pow(Var("u"), new_expr.factors[0].exp)]),\
                    takeDeriv(Deriv(u, expr.sym)))).contains(expr.sym):

                usubintegral = takeInt(Int(Pow(Var("u"), new_expr.factors[0].exp), Var("u")))
                usubintegral = usubintegral.sub(Var("u"),u)

            return usubintegral

        if isinstance(new_expr.factors[1], Apply):
            for apply_func in apply_funcs:
                if new_expr.factors[1].fun == apply_func:
                    u= new_expr.factors[1].expr
                    if  not simplify(Div(Mul([new_expr.factors[0], Apply(Fun(apply_func), Var("u"))]),\
                            takeDeriv(Deriv(u, expr.sym)))).contains(expr.sym):
                        usubintegral = takeInt(Int(Apply(Fun(apply_func),Var("u")), Var("u")))
                        usubintegral = usubintegral.sub(Var("u"),u)

                    return usubintegral

            if isinstance(new_expr.factors[0], Apply):
                for apply_func in appy_funcs:
                    if new_expr.factors[0].fun == apply_func:
                        u= new_expr.factors[0].expr
                        if  not simplify(Div(Mul([new_expr.factors[1], Apply(Fun(apply_func), Var("u"))]),\
                                    takeDeriv(Deriv(u, expr.sym)))).contains(expr.sym):
                                usubintegral = takeInt(Int(Apply(Fun(apply_func),Var("u")), Var("u")))
                                usubintegral = usubintegral.sub(Var("u"),u)

                        return usubintegral

    return (expr)

def takeInt(expr):
    expr = negationRule(expr)
    expr = constantRule(expr)
    expr = identityRule(expr)
    expr = sumRule(expr)
    expr = differenceRule(expr)
    expr = lnRule(expr)
    expr = overxRule(expr)
    expr = powerRule(expr)
    expr = exponentRule(expr)
    expr = sinRule(expr)
    expr = cosRule(expr)
    expr = sec2Rule(expr)
    expr = csc2Rule(expr)
    expr = sectanRule(expr)
    expr = csccotRule(expr)
    expr = arcsinRule(expr)
    expr = arctanRule(expr)
    expr = arcsecRule(expr)
    expr = usubRule(expr)
    return expr

print(takeInt(Int(Mul([Var("x"), Apply(Fun("sin"), Pow(Var("x"), Num(2)))]), Var("x"))))
