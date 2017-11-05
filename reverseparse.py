
def toString(expr):
    if isinstance(expr, Deriv):
        return str(0x25) + expr.expr + str(0x2B) + expr.sym + str(0x11)
    if isinstance(expr, Int):
        return str(0x24) + expr.expr + str(0x2B) + expr.sym + str(0x11)
    if isinstance(expr, Add):
        return str(0x10) + [toString(t) + str(0x70) for t in expr.terms][:-1] + str(0x11)
    if isinstance(expr, Sub):
        return toString(expr.left) + str(0x71) + toString(expr.right)
    if isinstance(expr, Neg):
        return str(0xB0) + toString(expr.exp)
    if isinstance(expr, Mul):
        return str(0x10) + [toString(f) + str(0x82) for f in expr.factors][:-1] + str(0x11)
    if isinstance(expr, Div):
        return toString(expr.top) + str(0x83) + toString(expr.bottom)
    if isinstance(expr, Pow):
        return str(0x10) + toString(expr.base) str(0x11) + str(0xF0) + str(0x10) + toString(expr.exp) str(0x11)
    if isinstance(expr, Apply):
        s = toString(expr.fun) + toString(expr.sym)
        if expr.fun.sym == "sec" or expr.fun.sym == "csc" or expr.fun.sym == "cot":
            s += str(0x11) + str(0x0C)
        if expr.fun.sym == "arcsec" or expr.fun.sym == "arccsc" or expr.fun.sym == "arccot":
            s += str(0x11) + str(0x0C) + str(0x11)
    if isinstance(expr, Fun):
        if expr.sym == "sin":
            return str(0xC2)
        if expr.sym == "cos":
            return str(0xC4)
        if expr.sym == "tan":
            return str(0xC6)
        if expr.sym == "sec":
            return str(0xC4)
        if expr.sym == "csc":
            return str(0xC2)
        if expr.sym == "cot":
            return str(0xC6)
        if expr.sym == "ln":
            return str(0xBE)
        if expr.sym == "abs":
            return str(0xB2)
        if expr.sym == "arcsin":
            return str(0xC3)
        if expr.sym == "arccos":
            return str(0xC5)
        if expr.sym == "arctan":
            return str(0xC7)
        if expr.sym == "arcsec":
            return str(0xC5) + str(0x10)
        if expr.sym == "arccsc":
            return str(0xC3) + str(0x10)
        if expr.sym == "arccot":
            return str(0xC7) + str(0x10)
    if isinstance(expr, Var):
        return expr.sym
    if isinstance(expr, Num):
        s=""
        for char in str(expr):
            if  ord(char) <= 0x30 and <= 0x39:
                s += char
            elif char == ".":
                s += str(0x3A)
            elif char == "-":
                s += str(0xB0)
            elif char == '/':
                s += str(83)
        return s
