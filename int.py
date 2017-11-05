from AST import *
from simplify import simplify
from deriv import takeDeriv
from parser import parse
from time import sleep
import math

def constantRule(expr):
    if isinstance(expr, Int):
        if not expr.expr.contains(expr.sym):
            return Mul([expr.expr,expr.sym])
    return expr

def constantmultipleRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Mul):
            consts = []
            notconsts = []
            for e in expr.expr.factors:
                if isinstance(e, Num) or isinstance(e, Var) and e != expr.sym: #TODO check for containment of variable
                    consts.append(e)
                else:
                    notconsts.append(e)
            if notconsts == []:
                return Num(0)
            if consts == []:
                return expr
            c = consts[0] if len(consts) == 1 else Mul(consts)
            nc = notconsts[0] if len(notconsts) == 1 else Mul(notconsts)
            return Mul([c, takeInt(Int(nc, expr.sym))])
    return expr


def identityRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Var) and expr.expr == expr.sym:
            return Mul([Div(Num(1),Num(2)), Pow(expr.expr,Num(2))])
    return expr

def negationRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Neg):
            return Mul([Num(-1),takeInt(Int(expr.expr.exp, expr.sym))])
    return expr

def sumRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Add):
            return Add([takeInt(Int(c, expr.sym)) for c in expr.expr.terms])
    return expr

def differenceRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Sub):
            return Sub(takeInt(Int(expr.expr.left, expr.sym)), takeInt(Int(expr.expr.right, expr.sym)))
    return expr


def overxRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div) and expr.expr.bottom == expr.sym:
            return Apply(Fun("ln"), Apply(Fun("abs"), expr.sym))

        if isinstance(expr.expr, Pow):
            if expr.expr.base == expr.sym and expr.expr.exp == Num(-1):
                return Apply(Fun("ln"), Apply(Fun("abs"), expr.sym))
    return expr

def lnRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Apply) and expr.expr.fun == Fun("ln")\
        and expr.expr.expr == expr.sym:
            return Sub(Mul([expr.sym, Apply(Fun("ln"), expr.sym)]), expr.sym)
    return expr

def exponentRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow) and expr.expr.exp.contains(expr.sym)\
                    and not expr.expr.base.contains(expr.sym):
                return Div(expr.expr, Apply(Fun("ln"), expr.expr.base))
    return expr


def powerRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow) \
            and isinstance(expr.expr.base, Var) and expr.expr.base == expr.sym \
            and not expr.expr.exp.contains(expr.sym):
                return Mul([Div(Num(1), Add([expr.expr.exp, Num(1)])), Pow(expr.expr.base, Add([expr.expr.exp, Num(1)]))])

    return expr

def sinRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Apply) and expr.expr.fun == Fun("sin")\
        and expr.expr.expr == expr.sym:
            return Mul([Num(-1),Apply(Fun("cos"), expr.expr.expr)])
    return expr

def cosRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Apply) and expr.expr.fun == Fun("cos")\
        and expr.expr.expr == expr.sym:
            return Apply(Fun("sin"), expr.expr.expr)
    return expr

def sec2Rule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow)\
            and expr.expr.base == Apply(Fun("sec"), expr.sym) and expr.expr.exp == Num(2):
            return Apply(Fun("tan"), expr.sym )
    return expr

def csc2Rule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Pow)\
            and expr.expr.base == Apply(Fun("csc"), expr.sym) and expr.expr.exp == Num(2):
            return Mul([Num(-1),Apply(Fun("cot"), expr.sym )])
    return expr

def sectanRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Mul):
            if expr.expr.factors[0] == Apply(Fun("sec"), expr.sym) and expr.expr.factors[1] == Apply(Fun("tan"), expr.sym):
                return Apply(Fun("sec"), expr.sym )

            if expr.expr.factors[1] == Apply(Fun("sec"), expr.sym) and expr.expr.factors[0] == Apply(Fun("tan"), expr.sym):
                return Apply(Fun("sec"), expr.sym)
    return expr

def csccotRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Mul):
            if expr.expr.factors[0] == Apply(Fun("csc"), expr.sym) and expr.expr.factors[1] == Apply(Fun("cot"), expr.sym):
                return Mul([Num(-1),Apply(Fun("csc"), expr.sym )])

            if expr.expr.factors[1] == Apply(Fun("csc"), expr.sym) and expr.expr.factors[0] == Apply(Fun("cot"), expr.sym):
                return Mul([Num(-1),Apply(Fun("csc"), expr.sym )])
    return expr

def arcsinRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            if isinstance(expr.expr.bottom, Pow):
                if isinstance(expr.expr.bottom.base, Sub):
                    if expr.expr.top == Num(1) and expr.expr.bottom.exp == Div(Num(1), Num(2))\
                    and expr.expr.bottom.base.right == Pow(expr.sym, Num(2)) and expr.expr.bottom.base.left == Num(1):
                        return Apply(Fun("arcsin"), expr.sym)
    return expr

def arctanRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            if isinstance(expr.expr.bottom, Add):
                if expr.expr.top == Num(1) and ((expr.expr.bottom == Add([Num(1),Pow(Var("x"), Num(2))]))\
                or (expr.expr.bottom == Add([Pow(Var("x"), Num(2)), Num(1)]))):
                    return Apply(Fun("arctan"), expr.sym)
    return expr

def arcsecRule(expr):
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            if isinstance(expr.expr.bottom, Mul) and expr.expr.top == Num(1):
                if isinstance(expr.expr.bottom.factors[0], Apply) and isinstance(expr.expr.bottom.factors[1], Pow):
                    if expr.expr.bottom.factors[0].fun == "abs" and expr.expr.bottom.factors[1].exp == Div(Num(1), Num (2)):
                        if isinstance(expr.expr.bottom.factors[1].base, Sub):
                            if isinstance(expr.expr.bottom.factors[1].base.left, Pow) and\
                            expr.expr.bottom.factors[1].base.right == Num(1) and\
                            expr.expr.bottom.factors[1].base.left.base == expr.sym and\
                            expr.expr.bottom.factors[1].base.left.exp == Num(2):
                                return Apply(Fun("arcsec"), expr.sym)
    return expr


def usubRule(expr):
    apply_funcs=[Fun("sin"), Fun("cos"), Fun("tan"), Fun("sec"), Fun("csc"), Fun("cot"), Fun("ln")]
    if isinstance(expr, Int):
        if isinstance(expr.expr, Div):
            u = expr.expr.bottom
            sub_var = str(expr.sym)+("u")
            new_integrand = simplify(Div(expr.expr.top, Mul([takeDeriv(Deriv(u, expr.sym)), Var(sub_var)])))
            if  not new_integrand.contains(expr.sym):
                usubintegral = takeInt(Int(new_integrand, Var(sub_var)))
                usubintegral = usubintegral.sub(Var(sub_var),u)
                return usubintegral

        new_expr = simplify(expr.expr)

        if not isinstance(new_expr, Mul):
            new_expr = Mul([Num(1), new_expr])

        if isinstance(new_expr.factors[1], Pow) and new_expr.factors[1].base.contains(expr.sym):
            u = new_expr.factors[1].base
            sub_var = str(expr.sym)+("u")
            new_integrand = simplify(Div(Mul([new_expr.factors[0], Pow(Var(sub_var), new_expr.factors[1].exp)]),\
                                takeDeriv(Deriv(u, expr.sym))))

            if  not new_integrand.contains(expr.sym):
                usubintegral = takeInt(Int(new_integrand, Var(sub_var)))
                usubintegral = usubintegral.sub(Var(sub_var),u)
                return usubintegral

        if isinstance(new_expr.factors[0], Pow):
            u = new_expr.factors[0].base
            sub_var = str(expr.sym)+("u")

            new_integrand = simplify(Div(Mul([new_expr.factors[1], Pow(Var(sub_var), new_expr.factors[0].exp)]),\
                             takeDeriv(Deriv(u, expr.sym))))

            if  not new_integrand.contains(expr.sym):
                usubintegral = takeInt(Int(new_integrand, Var(sub_var)))
                usubintegral = usubintegral.sub(Var(sub_var),u)
                return usubintegral

        if isinstance(new_expr.factors[1], Apply):
            for apply_func in apply_funcs:
                if new_expr.factors[1].fun == apply_func:
                    u = new_expr.factors[1].expr
                    sub_var = str(expr.sym)+("u")

                    new_integrand = simplify(Div(Mul([new_expr.factors[0], Apply(apply_func, Var(sub_var))]),\
                                    takeDeriv(Deriv(u, expr.sym))))

                    if  not new_integrand.contains(expr.sym):
                        usubintegral = takeInt(Int(new_integrand,Var(sub_var)))
                        usubintegral = usubintegral.sub(Var(sub_var),u)
                        return usubintegral

            if isinstance(new_expr.factors[0], Apply):
                for apply_func in apply_funcs:
                    if new_expr.factors[0].fun == apply_func:
                        u = new_expr.factors[0].expr
                        sub_var = str(expr.sym)+("u")

                        new_integrand = simplify(Div(Mul([new_expr.factors[1], Apply(apply_func, Var(sub_var))]),\
                                        takeDeriv(Deriv(u, expr.sym))))

                        if  not new_integrand.contains(expr.sym):
                                usubintegral = takeInt(Int(new_integrand, Var(sub_var)))
                                usubintegral = usubintegral.sub(Var(sub_var),u)
                                return usubintegral


    return (expr)

def bypartsRule(expr):
    arc_trigs = [Fun("arcsin"), Fun("arccos"), Fun("arctan"), Fun("arcsec"), Fun("arcsec"),\
               Fun("arccot"), Fun("arcsec"), Fun("arccsc")]

    trigs = [Fun("sin"), Fun("cos"), Fun("tan"), Fun("sec"), Fun("csc"), Fun("cot")]
    if isinstance(expr, Int):
        u = expr.expr
        dv = Num(1)
        if isinstance(expr.expr, Mul):
            for n in range(len(expr.expr.factors)):
                if isinstance(expr.expr.factors[n], Apply) and expr.expr.factors[n].fun == Fun("ln"):
                    u = expr.expr.factors[n]
                    if len(expr.expr.factors) == 2:
                        dv = (expr.expr.factors[:n] + expr.expr.factors[n+1:])[0]
                    else:
                        dv = Mul(expr.expr.factors[:n] + expr.expr.factors[n+1:])
                    break

            else:
                for n in range(len(expr.expr.factors)):
                    if isinstance(expr.expr.factors[n], Apply) and expr.expr.factors[n].fun in arc_trigs:
                        u = expr.expr.factors[n]
                        if len(expr.expr.factors) == 2:
                            dv = (expr.expr.factors[:n] + expr.expr.factors[n+1:])[0]
                        else:
                            dv = Mul(expr.expr.factors[:n] + expr.expr.factors[n+1:])
                        break
                else:
                    for n in range(len(expr.expr.factors)):
                        if not isinstance(expr.expr.factors[n], Apply):
                            if isinstance(expr.expr.factors[n], Pow) and not expr.expr.factors[n].exp.contains(expr.sym)\
                            and expr.expr.factors[n].base == expr.sym or expr.expr.factors[n] == expr.sym:
                                u = expr.expr.factors[n]
                                if len(expr.expr.factors) == 2:
                                    dv = (expr.expr.factors[:n] + expr.expr.factors[n+1:])[0]
                                else:
                                    dv = Mul(expr.expr.factors[:n] + expr.expr.factors[n+1:])
                                break
                    else:
                        for n in range(len(expr.expr.factors)):
                            if isinstance(expr.expr.factors[n], Apply) and expr.expr.factors[n].fun in trigs:
                                    u = expr.expr.factors[n]
                                    if len(expr.expr.factors) == 2:
                                        dv = (expr.expr.factors[:n] + expr.expr.factors[n+1:])[0]
                                    else:
                                        dv = Mul(expr.expr.factors[:n] + expr.expr.factors[n+1:])
                                    break
                        else:
                            for n in range(len(expr.expr.factors)):
                                if isinstance(expr.expr.factors[n], Pow) and expr.expr.factors[n].exp.contains(expr.sym):
                                    u = expr.expr.factors[n]

                                    if len(expr.expr.factors) == 2:
                                        dv = (expr.expr.factors[:n] + expr.expr.factors[n+1:])[0]
                                    else:
                                        dv = Mul(expr.expr.factors[:n] + expr.expr.factors[n+1:])
                                    break

        v = simplify(takeInt(Int(dv, expr.sym)))
        du = takeDeriv(Deriv(u, expr.sym))
        print("u: " + str(u))
        print("du: " + str(du))
        print("v: " + str(v))
        print("dv: " + str(dv))

        return Sub(Mul([u, v]), takeInt(Int(simplify(Mul([v, du])), expr.sym)))

    return expr


def takeInt(expr):
    expr = expr.sub(Var("e"), Num(math.e))
    expr = negationRule(expr)
    expr = constantRule(expr)
    expr = identityRule(expr)
    expr = sumRule(expr)
    expr = differenceRule(expr)
    expr = constantmultipleRule(expr)
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
    expr = bypartsRule(expr)
    #expr = expr.sub(Num(math.e), Var("e"))
    return expr

test = "int(x*e^x, x)"
print("test: " + test)
expr = parse(test)
print("expr: " + str(expr))
print(takeInt(expr))
print(simplify(takeInt(expr)))
