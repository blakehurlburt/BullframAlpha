from AST import *
import math

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

def addConsts(expr):
    if isinstance(expr, Add):
        sum = 0
        nonconsts = []
        for t in expr.terms:
            if isinstance(t, Num):
                sum += t.val
            else:
                nonconsts.append(t)
        if len(nonconsts) == 0:
            return Num(sum)
        if sum != 0:
            return Add([Num(sum)]+nonconsts)
        if len(nonconsts) == 1:
            return nonconsts[0]
        return Add(nonconsts)
    return expr

def subConsts(expr):
    if isinstance(expr, Sub) and isinstance(expr.left, Num) and isinstance(expr.right, Num):
        return Num(expr.left.val - expr.right.val)
    return expr

def mulConsts(expr):
    if isinstance(expr, Mul):
        prod = 1
        nonconsts = []
        for f in expr.factors:
            if isinstance(f, Num):
                prod *= f.val
            else:
                nonconsts.append(f)
        if len(nonconsts) == 0:
            return Num(prod)
        if prod != 1:
            return Mul([Num(prod)]+nonconsts)
        if len(nonconsts) == 1:
            return nonconsts[0]
        return Mul(nonconsts)
    return expr

def divConsts(expr):
    if isinstance(expr, Div) and isinstance(expr.top, Num) and isinstance(expr.bottom, Num):
        return Num(expr.top.val / expr.bottom.val)
    return expr

def powConsts(expr):
    if isinstance(expr, Pow) and isinstance(expr.base, Num) and isinstance(expr.exp, Num):
        return Num(expr.base.val ** expr.exp.val)
    return expr

def lnConst(expr):
    if isinstance(expr, Apply) and expr.fun == Fun("ln") and isinstance(expr.expr, Num):
        return Num(math.log(expr.expr.val))
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

def onePow(expr):
    if isinstance(expr, Pow) and expr.base == Num(1):
        return Num(1)
    return expr

def removeSub(expr):
    if isinstance(expr, Sub):
        if isinstance(expr.right, Add):
            return Add([expr.left]+[Mul([Num(-1), t]) for t in expr.right.terms])
        return Add([expr.left, Mul([Num(-1), expr.right])])
    return expr

def removeDiv(expr):
    if isinstance(expr, Div):
        if isinstance(expr.bottom, Mul):
            return Mul([expr.top]+[Pow(t, Num(-1)) for t in expr.bottom.factors])
        return Mul([expr.top, Pow(expr.bottom, Num(-1))])
    return expr

def mulPows(expr):
    if isinstance(expr, Pow) and isinstance(expr.base, Pow):
        return Pow(expr.base.base, Mul([expr.base.exp, expr.exp]))
    return expr

def extractFactor(term):
    if isinstance(term, Mul):
        nums = [x for x in term.factors if isinstance(x, Num)]
        factors = [x for x in term.factors if not isinstance(x, Num)]

        if not nums:
            num = Num(1)
        elif len(nums) == 1:
            num = nums[0]
        else:
            num = Mul(nums)

        if not factors:
            fact = Num(1)
        elif len(factors) == 1:
            fact = factors[0]
        else:
            fact = Mul(factors)

        return (num, fact)

    if isinstance(term, Num):
        return (term, Num(1))
    return (Num(1), term)

def combineLikeTerms(expr):
    if isinstance(expr, Add):

        tuples = map(extractFactor, expr.terms)

        result = []

        def merge(num1, num2):
            if isinstance(num1, Add):
                return Add(num1.terms + [num2])
            else:
                return Add([num1, num2])

        for (num, expr) in tuples:

            newResult = []

            for i in range(0, len(result)):
                (n, e) = result[i]
                if e == expr:
                    newResult.append((merge(n, num), e))
                    newResult += result[i+1:]
                    break
                else:
                    newResult.append((n, e))
            else:
                newResult.append((num, expr))

            result = newResult

        result = [Mul([n, e]) for (n, e) in result]

        return result[0] if len(result) == 1 else Add(result)

    return expr

def extractPow(factor):
    if isinstance(factor, Pow):
        return (factor.exp, factor.base)

    return (Num(1), factor)

def combineLikeFactors(expr):
    if isinstance(expr, Mul):

        tuples = map(extractPow, expr.factors)

        result = []

        def merge(num1, num2):
            if isinstance(num1, Add):
                return Add(num1.terms + [num2])
            else:
                return Add([num1, num2])

        for (num, expr) in tuples:

            newResult = []

            for i in range(0, len(result)):
                (n, e) = result[i]
                if e == expr:
                    newResult.append((merge(n, num), e))
                    newResult += result[i+1:]
                    break
                else:
                    newResult.append((n, e))
            else:
                newResult.append((num, expr))

            result = newResult

        result = [Pow(e, n) for (n, e) in result]

        return result[0] if len(result) == 1 else Mul(result)

    return expr

def eSub(expr):
    expr = expr.sub(Num(math.e), Var("e"))
    return expr


def simplify(expr):
    exprOld = 0
    exprNew = expr
    while exprOld != exprNew:
        exprOld = exprNew
        #print("A: " + str(exprNew) + "\n")
        exprNew = exprNew.map(addConsts)
        exprNew = exprNew.map(subConsts)
        exprNew = exprNew.map(mulConsts)
        exprNew = exprNew.map(divConsts)
        exprNew = exprNew.map(powConsts)
        exprNew = exprNew.map(lnConst)
        #print("B: " + str(exprNew) + "\n")
        exprNew = exprNew.map(flattenMul)
        exprNew = exprNew.map(flattenAdd)
        #print("C: " + str(exprNew) + "\n")
        exprNew = exprNew.map(removeSub)
        exprNew = exprNew.map(removeDiv)
        exprNew = exprNew.map(mulPows)
        #print("D: " + str(exprNew) + "\n")
        exprNew = exprNew.map(combineLikeTerms)
        #print("E: " + str(exprNew) + "\n")
        exprNew = exprNew.map(combineLikeFactors)
        #print("F: " + str(exprNew) + "\n")
        exprNew = exprNew.map(powZero)
        exprNew = exprNew.map(powOne)
        exprNew = exprNew.map(onePow)
        #print("G: " + str(exprNew) + "\n")
        exprNew = exprNew.map(mulZero)
        exprNew = exprNew.map(mulOne)
        #print("H: " + str(exprNew) + "\n")
        exprNew = exprNew.map(addZero)
        exprNew = exprNew.map(eSub)
        #print("I: " + str(exprNew) + "\n")
    return exprNew

if __name__ == "__main__":
    expr = Div(Mul([Num(2), Var("x"), Apply(Fun("cos"), Var("u"))]), Mul([Num(2), Var("x")]))
    print("Expression: " + str(expr))
    print("Simplified: " + str(simplify(expr)))
