from AST import *

def flattenMul(expr):
    if isinstance(expr, Mul):
        newFactors = []
        for f in expr.factors:
            if isinstance(f, Mul):
                newFactors.extend(f.factors)
            else:
                newFactors.append(f)
        return Mul(newFactors)
    return expr

def flattenAdd(expr):
    if isinstance(expr, Add):
        newTerms = []
        for t in expr.terms:
            if isinstance(t, Add):
                newTerms.extend(t.terms)
            else:
                newTerms.append(t)
        return Add(newTerms)
    return expr

def mulZero(expr):
    if isinstance(expr, Mul):
        if any(map(lambda x: x == Num(0), expr.factors)):
            return Num(0)
    return expr

def mulOne(expr):
    if isinstance(expr, Mul):
        newFactors = [f for f in expr.factors if f != Num(1)]
        if len(newFactors) == 0:
            return Num(1)
        elif len(newFactors) == 1:
            return newFactors[0]
        else:
            return Mul(newFactors)
    return expr

def addZero(expr):
    if isinstance(expr, Add):
        newTerms = [t for t in expr.terms if t != Num(0)]
        if len(newTerms) == 0:
            return Num(0)
        elif len(newTerms) == 1:
            return newTerms[0]
        else:
            return Add(newTerms)
    return expr

def powZero(expr):
    if isinstance(expr, Pow) and expr.exp == Num(0):
        return Num(1)
    return expr

def powOne(expr):
    if isinstance(expr, Pow) and expr.exp == Num(1):
        return expr.base
    return expr

def addConsts(expr):
    if isinstance(expr, Add):
        sum = 0
        for t in expr.terms:
            if not isinstance(t, Num):
                return expr
            sum += t.val
        return Num(sum)
    return expr

def subConsts(expr):
    if isinstance(expr, Sub) and isinstance(expr.left, Num) and isinstance(expr.right, Num):
        return Num(expr.left.val - expr.right.val)
    return expr

def mulConsts(expr):
    if isinstance(expr, Mul):
        prod = 1
        for f in expr.factors:
            if not isinstance(f, Num):
                return expr
            prod *= f.val
        return Num(prod)
    return expr

def divConsts(expr):
    if isinstance(expr, Sub) and isinstance(expr.top, Num) and isinstance(expr.bottom, Num):
        return Num(expr.top.val / expr.bottom.val)
    return expr

def powConsts(expr):
    if isinstance(expr, Pow) and isinstance(expr.base, Num) and isinstance(expr.exp, Num):
        return Num(expr.base.val ** expr.exp.val)
    return expr

def removeSub(expr):
    if isinstance(expr, Sub):
        return Add([expr.left, Mul([Num(-1), expr.right])])
    return expr

def removeDiv(expr):
    if isinstance(expr, Div):
        return Mul([expr.top, Pow(expr.bottom, Num(-1))])
    return expr

def mulPows(expr):
    if isinstance(expr, Pow) and isinstance(expr.base, Pow):
        return Pow(expr.base.base, Mul([expr.base.exp, expr.exp]))
    return expr

def simplify(expr):
    exprOld = 0
    exprNew = expr
    while exprOld != exprNew:
        exprOld = exprNew
        exprNew = exprNew.map(flattenMul)
        exprNew = exprNew.map(flattenAdd)
        exprNew = exprNew.map(mulZero)
        exprNew = exprNew.map(mulOne)
        exprNew = exprNew.map(addZero)
        exprNew = exprNew.map(powZero)
        exprNew = exprNew.map(powOne)
        exprNew = exprNew.map(addConsts)
        exprNew = exprNew.map(subConsts)
        exprNew = exprNew.map(mulConsts)
        exprNew = exprNew.map(divConsts)
        exprNew = exprNew.map(powConsts)
        exprNew = exprNew.map(removeSub)
        exprNew = exprNew.map(removeDiv)
        exprNew = exprNew.map(mulPows)
    return exprNew

if __name__ == "__main__":
    print(simplify(Div(Var("x"), Pow(Var("x"), Num(2)))))
