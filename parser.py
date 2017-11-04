import pyparsing as pp

var = pp.Word(pp.alphas)
number = pp.Word(pp.nums) + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))

plus  = pp.Literal("+")
minus = pp.Literal("-")
mult  = pp.Literal("*")
div   = pp.Literal("/")
pwr   = pp.Literal("^")

lpar  = pp.Literal("(").suppress()
rpar  = pp.Literal(")").suppress()

addop = plus | minus
mulop = mult | div
pwrop = pwr

"""
expr = pp.Forward()
atom = var | number | (lpar + expr + rpar)

factor = pp.Forward()
factor << atom + pp.ZeroOrMore(pwrop + factor)

term = factor + pp.ZeroOrMore(mulop + factor)

expr << term + pp.ZeroOrMore(addop + term)

bnf = expr

pattern =  bnf + pp.StringEnd()
"""

expr = pp.Forward()

func = var + lpar + expr + rpar

operand = func | number | var

expr << pp.Or(pp.operatorPrecedence(operand, [
    (pwrop, 2, pp.opAssoc.RIGHT),
    (mulop, 2, pp.opAssoc.LEFT),
    (addop, 2, pp.opAssoc.LEFT),
]), func)

pattern = expr + pp.StringEnd()

if __name__ == "__main__":
    test = "sin(x^2^x - cos(4+3*x)) / 2"
    #test = "sin / 2"
    #test = "sin(x^2^x - 3*x+4)"
    #test = "(x^2^x - 3*x + 4) / 2"
    print(test)
    res = pattern.parseString(test)
    print(res)
