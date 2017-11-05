import AST
from simplify import simplify

import itertools as it

def foil(expr):
    if not isinstance(expr, AST.Mul):
        return (expr, AST.Num(1))

    numerator = []
    denominator = []
    for factor in expr.factors:
        if isinstance(factor, AST.Pow):
            exp = int(factor.exp.val)
            if exp > 0:
                if isinstance(factor.base, AST.Add):
                    numerator.extend([factor.base] * exp)
                else:
                    numerator.extend([AST.Add([factor.base])] * exp)
            else:
                if isinstance(factor.base, AST.Add):
                    denominator.extend([factor.base] * -exp)
                else:
                    denominator.extend([AST.Add([factor.base])] * -exp)
        else:
            if isinstance(factor, AST.Add):
                numerator.append(factor)
            else:
                numerator.append(AST.Add([factor]))

    top = AST.Add([AST.Mul(p) for p in it.product(*[factor.terms for factor in numerator])])
    bot = AST.Add([AST.Mul(p) for p in it.product(*[factor.terms for factor in denominator])])
    return (top, bot)

def distribute(node):
    if isinstance(node, AST.Mul):
        (top, bot) = foil(node)
        if bot == AST.Num(1):
            return top
        return AST.Div(top, bot)
    return node

def degreeSort(sumNode):
    if not isinstance(sumNode, AST.Add):
        return sumNode
    degrees = []
    for product in sumNode.terms:
        if isinstance(product, AST.Mul):
            exponential = product.factors[1]
            if isinstance(exponential, AST.Pow):
                degrees.append(exponential.exp.val)
            else:
                degrees.append(1)
        elif isinstance(product, AST.Pow):
            degrees.append(product.exp.val)
        else:
            degrees.append(0)

    zipped = zip(degrees, sumNode.terms)
    res = [t[1] for t in sorted(zipped, key=lambda t:-t[0])]
    return AST.Add(res)

def divide(numer, denom, var):
    def degree(polynomial):
        if not isinstance(polynomial, AST.Add):
            return 0
        terms = polynomial.terms
        if isinstance(terms[0], AST.Pow):
            return terms[0].exp.val
        if isinstance(terms[0], AST.Mul):
            exponential = terms[0].factors[1]
            if isinstance(exponential, AST.Var):
                return 1
            return terms[0].factors[1].exp.val

        return 1

    def getCoefficient(polynomial, power):
        if not isinstance(polynomial, AST.Add):
            polynomial = AST.Add([polynomial])
        # print("P:", power)
        for term in polynomial.terms:
            if isinstance(term, AST.Num):
                coeff = term.val
                exp = 0
            elif isinstance(term, AST.Pow):
                coeff = 1
                exp = term.exp.val
            elif isinstance(term, AST.Mul):
                coeff = term.factors[0].val
                if isinstance(term.factors[1], AST.Var):
                    exp = 1
                else:
                    exp = term.factors[1].exp.val
            elif isinstance(term, AST.Var):
                return 1
            else:
                print("Error:", term)
                print(type(term))

            # print("E:", exp)

            # print(power, exp)
            # print(type(power), type(exp))
            # print()
            if power == exp:
                return coeff

        return 1

    res = AST.Add([])

    topDeg = degree(numer)
    botDeg = degree(denom)
    while topDeg >= botDeg:
        diff = topDeg - botDeg
        coeff = AST.Num(getCoefficient(numer, topDeg) / getCoefficient(denom, botDeg))
        xPow = AST.Pow(var, AST.Num(diff))
        res.terms.append(simplify(AST.Mul([coeff, xPow])))
        numer = AST.Sub(numer, AST.Mul([coeff, denom, xPow]))

        newNumer = simplify(numer.map(distribute))
        while numer != newNumer:
            numer = newNumer
            newNumer = simplify(numer.map(distribute))

        numer = degreeSort(numer)
        topDeg = degree(numer)

    res.terms.append(AST.Div(numer, denom))
    return simplify(res)

def polydiv(expr, var):
    newExpr = simplify(expr.map(distribute))
    while expr != newExpr:
        expr = newExpr
        newExpr = simplify(expr.map(distribute))

    (numer, denom) = map(simplify, foil(expr))

    (numer, denom) = map(degreeSort, (numer, denom))

    quotient = divide(numer, denom, var)
    return quotient

if __name__ == "__main__":
    from parser import parse
    from simplify import simplify
    # test = "(3*x+2)*(4*x+7) / (2*x+3)"
    test = "(3*x^4 - 2*x^3 + x^2 - 7) / (x^2 + 3*x - 4)"
    print(test)
    #test = "(x^4 - x^3 + x^2 - x) / (x-1)"
    expr = parse(test)
    expr = polydiv(expr, AST.Var("x"))
    print(expr)

    """
    print("orig:", expr)
    newExpr = simplify(expr.map(distribute))
    while expr != newExpr:
        expr = newExpr
        newExpr = simplify(expr.map(distribute))
    print(expr)
    (numer, denom) = map(simplify, foil(expr))
    print(numer, "/", denom)
    (numer, denom) = map(degreeSort, (numer, denom))
    print("sorted:", numer, "/", denom)
    quotient = divide(numer, denom, AST.Var("x"))
    print(quotient)
    """
