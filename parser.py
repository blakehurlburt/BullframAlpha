import pyparsing as pp

import AST

def action(ctor):
    def __action(fullString, index, *args):
        print("fullString = ", fullString)
        print("index =", index)
        print("args =", args)
        return ctor(*args[0])
    return __action

var = pp.Word(pp.alphas)
number = pp.Word(pp.nums) + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))

plus  = pp.Literal("+")
minus = pp.Literal("-")
mult  = pp.Literal("*")
div   = pp.Literal("/")
pwr   = pp.Literal("^")

lpar  = pp.Suppress("(")
rpar  = pp.Suppress(")")

addop = plus | minus
mulop = mult | div
pwrop = pwr

expr = pp.Forward()

func = (var + lpar + expr + rpar).setParseAction(action(AST.Apply))

operand = func | number | var

expr << pp.Or(pp.operatorPrecedence(operand, [
    (pwrop, 2, pp.opAssoc.RIGHT),
    (mulop, 2, pp.opAssoc.LEFT),
    (addop, 2, pp.opAssoc.LEFT),
]), func)

def __exprParseAction(fullString, index, arg):
    if isinstance(arg, AST.Expr):
        # another action has already taken place
        return arg

    arg = arg[0]
    if len(arg) < 3:
        # a literal
        # TODO fix this for unary functions
        return arg

    ops = {
        "+": AST.Add,
        "-": AST.Sub,
        "*": AST.Mul,
        "/": AST.Div,
        "^": AST.Pow,
    }
    op = arg[1]
    args = (arg[0], arg[2])

    if op in "+*":
        return ops[op](args)
    else:
        return ops[op](*args)

expr.setParseAction(__exprParseAction)

pattern = expr + pp.StringEnd()

if __name__ == "__main__":
    test = "sin(x^2^x - cos(4+3*x)) / 2"
    #test = "sin / 2"
    #test = "sin(x^2^x - 3*x+4)"
    #test = "(x^2^x - 3*x + 4) / 2"
    print(test)
    res = pattern.parseString(test)
    print(res)
