import pyparsing as pp

import AST

def action(ctor):
    def __action(fullString, index, *args):
        return ctor(*args[0])
    return __action

var = pp.Word(pp.alphas).setParseAction(action(AST.Var))
number = pp.Word(pp.nums) + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))
number.setParseAction(action(lambda s: AST.Num(float(s))))

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

func = (var + lpar + expr + pp.ZeroOrMore(pp.Suppress(",") + expr) + rpar)
def __funcParseAction(fullString, index, arg):
    #TODO rewrite to handle multivariate functions
    if arg[0].sym == "deriv":
        return AST.Deriv(*arg[1:])
    elif arg[0].sym == "int":
        if len(arg) < 4: #indefinite
            return AST.Int(arg[1:])
        else:
            return AST.DefInt(*arg[1:])
    else:
        return AST.Apply(AST.Fun(arg[0].sym), arg[1])

func.setParseAction(__funcParseAction)

operand = func | number | var

class LeftBinOp:
    def __init__(self, tokens):
        self.operators = tokens[0][1::2]
        self.operands = tokens[0][0::2]

    def map(self, func):
        res = LeftBinOp([[]])
        res.operators = self.operators[:]
        res.operands = [opr.map(func) for opr in self.operands]
        return func(res)

expr << pp.Or(pp.operatorPrecedence(operand, [
    (minus, 1, pp.opAssoc.RIGHT, lambda t: AST.Neg(t[0][1])),
    (pwrop, 2, pp.opAssoc.RIGHT, lambda t: AST.Pow(t[0][0], t[0][2])),
    (mulop, 2, pp.opAssoc.LEFT, LeftBinOp),
    (addop, 2, pp.opAssoc.LEFT, LeftBinOp),
]), func)

pattern = expr + pp.StringEnd()

def parse(string):
    res = expr.parseString(string)[0]
    def convertLeftBinOp(obj):
        if not isinstance(obj, LeftBinOp):
            return obj

        ops = {
            '+': AST.Add,
            '-': AST.Sub,
            '*': AST.Mul,
            '/': AST.Div
        }
        def makeNode(op, left, right):
            if op in '+*':
                return ops[op]([left, right])
            else:
                return ops[op](left, right)

        root = makeNode(obj.operators[0], obj.operands[0], obj.operands[1])
        cur = root

        for rhs, operator in zip(obj.operands[2:], obj.operators[1:]):
            print(rhs)
            if isinstance(cur, AST.Add):
                lhs = cur.terms[-1]
            elif isinstance(cur, AST.Sub):
                lhs = cur.right
            elif isinstance(cur, AST.Mul):
                lhs = cur.factors[-1]
            elif isinstance(cur, AST.Div):
                lhs = cur.bottom

            newNode = makeNode(operator, lhs, rhs)

            if isinstance(cur, AST.Add):
                cur.terms[-1] = newNode
            elif isinstance(cur, AST.Sub):
                cur.right = newNode
            elif isinstance(cur, AST.Mul):
                cur.factors[-1] = newNode
            elif isinstance(cur, AST.Div):
                cur.bottom = newNode

            cur = newNode

        return root

    return res.map(convertLeftBinOp)


if __name__ == "__main__":
    test = "deriv(sin(x^2^x - cos(4+3*x)) / 4*(-2 +x + 3 - 1), x)"
    #test = "int(sin(x^2^x - cos(4+3*x)) / 4*(-2 +x), x, -sin(x), sin(x))"
    #test = "sin / 2"
    #test = "sin(x^2^x - 3*x+4)"
    #test = "(x^2^x - 3*x + 4) / 2"
    #test = "1 * 2 + 3 - 4 / 5 + 6"
    # test = "1 + 2 + 3 - 4 * 5 + 6"
    #test = "1+2"
    # test = "deriv(x + 2 * x + 3 + 4 + 5 * x, x)"
    test = "(x+1)*(x+2)*(2*x+3)"
    print("Input:", test)
    res = parse(test)
    print("Result:", res)
