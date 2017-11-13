from AST import *

def toString(expr):
    if isinstance(expr, Deriv):
        return bytes([0x25]) + toString(expr.expr) + bytes([0x2B]) + toString(expr.sym) + bytes([0x11])
    if isinstance(expr, Int):
        return bytes([0x24]) + toString(expr.expr) + bytes([0x2B]) + toString(expr.sym) + bytes([0x11])
    if isinstance(expr, Add):
        return bytes([0x10]) + "".join([toString(t) + bytes([0x70]) for t in expr.terms][:-1]) + bytes([0x11])
    if isinstance(expr, Sub):
        return toString(expr.left) + bytes([0x71]) + toString(expr.right)
    if isinstance(expr, Neg):
        return bytes([0xB0]) + toString(expr.exp)
    if isinstance(expr, Mul):
        return bytes([0x10]) + "".join([toString(f) + bytes([0x82]) for f in expr.factors][:-1]) + bytes([0x11])
    if isinstance(expr, Div):
        return toString(expr.top) + bytes([0x83]) + toString(expr.bottom)
    if isinstance(expr, Pow):
        return bytes([0x10]) + toString(expr.base) + bytes([0x11]) + bytes([0xF0]) + bytes([0x10]) + toString(expr.exp) + bytes([0x11])
    if isinstance(expr, Apply):
        s = toString(expr.fun) + toString(expr.sym)
        if expr.fun.sym == "sec" or expr.fun.sym == "csc" or expr.fun.sym == "cot":
            s += bytes([0x11]) + bytes([0x0C])
        if expr.fun.sym == "arcsec" or expr.fun.sym == "arccsc" or expr.fun.sym == "arccot":
            s += bytes([0x11]) + bytes([0x0C]) + bytes([0x11])
        return s
    if isinstance(expr, Fun):
        if expr.sym == "sin":
            return bytes([0xC2])
        if expr.sym == "cos":
            return bytes([0xC4])
        if expr.sym == "tan":
            return bytes([0xC6])
        if expr.sym == "sec":
            return bytes([0xC4])
        if expr.sym == "csc":
            return bytes([0xC2])
        if expr.sym == "cot":
            return bytes([0xC6])
        if expr.sym == "ln":
            return bytes([0xBE])
        if expr.sym == "abs":
            return bytes([0xB2])
        if expr.sym == "arcsin":
            return bytes([0xC3])
        if expr.sym == "arccos":
            return bytes([0xC5])
        if expr.sym == "arctan":
            return bytes([0xC7])
        if expr.sym == "arcsec":
            return bytes([0xC5]) + bytes([0x10])
        if expr.sym == "arccsc":
            return bytes([0xC3]) + bytes([0x10])
        if expr.sym == "arccot":
            return bytes([0xC7]) + bytes([0x10])
    if isinstance(expr, Var):
        return expr.sym
    if isinstance(expr, Num):
        s=""
        for char in expr:
            if  0x30 <= ord(char) <= 0x39:
                s += bytes([char])
            elif char == ".":
                s += bytes([0x3A])
            elif char == "-":
                s += bytes([0xB0])
            elif char == '/':
                s += bytes([83])
        return s
