import pyparsing as pp

import AST

def action(ctor):
    def __action(fullString, index, *args):
        return ctor(*args[0])
    return __action

var = pp.Word(pp.alphas).setParseAction(action(AST.Var))
number = pp.Word(pp.nums) + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))
number.setParseAction(action(lambda s: AST.Num(int(s))))

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
    (minus, 1, pp.opAssoc.RIGHT),
    (pwrop, 2, pp.opAssoc.RIGHT),
    (mulop, 2, pp.opAssoc.LEFT),
    (addop, 2, pp.opAssoc.LEFT),
]), func)

def __exprParseAction(fullString, index, arg):
    if not isinstance(arg, pp.ParseResults):
        # another action has already taken place
        return arg

    print(arg)
    if len(arg) == 1:
        arg = arg[0]
        if isinstance(arg, AST.Expr):
            # another action has already taken place
            return arg

    ops = {
        "+": AST.Add,
        "-": AST.Sub,
        "*": AST.Mul,
        "/": AST.Div,
        "^": AST.Pow,
    }

    if len(arg) < 3: # unary
        return AST.Neg(arg[1])
        
    op = arg[1]

    args = (__exprParseAction(fullString, index, arg[0]),
            __exprParseAction(fullString, index, arg[2]))

    if op in "+*":
        return ops[op](args)
    else:
        return ops[op](*args)

expr.setParseAction(__exprParseAction)

pattern = expr + pp.StringEnd()

if __name__ == "__main__":
    test = "sin(x^2^x - cos(4+3*x)) / -2"
    #test = "sin / 2"
    #test = "sin(x^2^x - 3*x+4)"
    #test = "(x^2^x - 3*x + 4) / 2"
    print(test)
    res = pattern.parseString(test)
    print(res)
