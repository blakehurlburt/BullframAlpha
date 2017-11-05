from fractions import Fraction

class Expr:
    def __repr__(self):
        return str(self)

class Add(Expr):
    def __init__(self, addends):
        self.terms = addends

    def __str__(self):
        return "(+, " + ", ".join(map(str, self.terms)) + ")"

    def __eq__(self, other):
        return isinstance(other, Add) and self.terms == other.terms

    def contains(self, expr):
        return self == expr or any(map(lambda e: e.contains(expr), self.terms))

    def sub(self, find, replace):
        return replace if self == find else Add([c.sub(find, replace) for c in self.terms])

    def map(self, fun):
        return fun(Add([x.map(fun) for x in self.terms]))


class Sub(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(-, " +  str(self.left) + ", " + str(self.right) + ")"

    def __eq__(self, other):
        return isinstance(other, Sub) and self.left == other.left and self.right == other.right

    def contains(self, expr):
        return self == expr or self.left.contains(expr) or self.right.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Sub(self.left.sub(find, replace), self.right.sub(find, replace))

    def map(self, fun):
        return fun(Sub(self.left.map(fun), self.right.map(fun)))

class Mul(Expr):
    def __init__(self, factors):
        self.factors = factors

    def __str__(self):
        return "(*, " + ", ".join(map(str, self.factors)) + ")"

    def __eq__(self, other):
        return isinstance(other, Mul) and self.factors == other.factors

    def contains(self, expr):
        return self == expr or any(map(lambda e: e.contains(expr), self.factors))

    def sub(self, find, replace):
        return replace if self == find else Mul([c.sub(find, replace) for c in self.factors])

    def map(self, fun):
        return fun(Mul([x.map(fun) for x in self.factors]))

class Div(Expr):
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom

    def __str__(self):
        return "(/, " +  str(self.top) + ", " + str(self.bottom) + ")"

    def __eq__(self, other):
        return isinstance(other, Div) and self.top == other.top and self.bottom == other.bottom

    def contains(self, expr):
        return self == expr or self.top.contains(expr) or self.bottom.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Div(self.top.sub(find, replace), self.bottom.sub(find, replace))

    def map(self, fun):
        return fun(Div(self.top.map(fun), self.bottom.map(fun)))


class Pow(Expr):
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp

    def __str__(self):
        return "(^, " +  str(self.base) + ", " + str(self.exp) + ")"

    def __eq__(self, other):
        return isinstance(other, Pow) and self.base == other.base and self.exp == other.exp

    def contains(self, expr):
        return self == expr or self.base.contains(expr) or self.exp.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Pow(self.base.sub(find, replace), self.exp.sub(find, replace))

    def map(self, fun):
        return fun(Pow(self.base.map(fun), self.exp.map(fun)))


class Neg(Expr):
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "(-, " + str(self.exp) + ")"

    def __eq__(self, other):
        return isinstance(other, Neg) and self.exp == other.exp

    def contains(self, expr):
        return self == expr or self.exp.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Neg(self.exp.sub(find, replace))

    def map(self, fun):
        return fun(Neg(self.exp.map(fun)))

class Num(Expr):
    def __init__(self, val):
        self.val = Fraction(val)

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return isinstance(other, Num) and self.val == other.val

    def contains(self, expr):
        return False

    def sub(self, find, replace):
        return replace if self == find else self

    def map(self, fun):
        return fun(self)

class Var(Expr):
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return self.sym

    def __eq__(self, other):
        return isinstance(other, Var) and self.sym == other.sym

    def contains(self, expr):
        return self == expr

    def sub(self, find, replace):
        return replace if self == find else self

    def map(self, fun):
        return fun(self)

class Deriv(Expr):
    def __init__(self, expr, sym):
        self.sym = sym
        self.expr = expr

    def __str__(self):
        return "(D, " + str(self.expr) + ", " + str(self.sym) + ")"

    def __eq__(self, other):
        return isinstance(other, Deriv) and self.expr == other.expr and self.sym == other.sym

    def contains(self, expr):
        return self == expr or self.sym.contains(expr) or self.expr.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Deriv(self.expr.sub(find, replace), self.sym.sub(find, replace))

    def map(self, fun):
        # should we modify the sym?
        return fun(Deriv(self.expr.map(fun), self.sym.map(fun)))

class Int(Expr):
    def __init__(self, expr, sym):
        self.sym = sym
        self.expr = expr

    def __str__(self):
        return "(I, " + str(self.expr) + ", " + str(self.sym) + ")"

    def __eq__(self, other):
        return isinstance(other, Int) and self.expr == other.expr and self.sym == other.sym

    def contains(self, expr):
        return self == expr or self.sym.contains(expr) or self.expr.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Int(self.expr.sub(find, replace), self.sym.sub(find, replace))

    def map(self, fun):
        # should we modify the sym?
        return fun(Int(self.expr.map(fun), self.sym.map(fun)))

class DefInt(Expr):
    def __init__(self, expr, sym, lower, upper):
        self.sym = sym
        self.expr = expr
        self.lower = lower
        self.upper = upper

    def __str__(self):
        return "(I, " + ", ".join(map(str, [self.expr, self.sym, self.lower, self.upper])) + ")"

    def __eq__(self, other):
        return isinstance(other, DefInt) and [self.expr, self.sym, self.lower, self.upper] == [other.expr, other.sym, other.lower, other.upper]

    def contains(self, expr):
        return self == expr or self.sym.contains(expr) or self.expr.contains(expr)

    def sub(self, find, replace):
        # TODO: handle when subbing in something involving the variable we're integrating wrt
        return replace if self == find else DefInt(self.expr.sub(find, replace), self.sym.sub(find, replace), \
                                                self.lower.sub(find, replace), self.upper.sub(find, replace))

    def map(self, fun):
        # should we modify the sym?
        return fun(DefInt(self.expr.map(fun), self.sym.map(fun)), self.lower.map(fun), self.upper.map(fun))

class Apply(Expr):
    def __init__(self, fun, expr):
        self.fun = fun
        self.expr = expr

    def __str__(self):
        return "(" + str(self.fun) + ", " + str(self.expr) + ")"

    def __eq__(self, other):
        return isinstance(other, Apply) and self.expr == other.expr and self.fun == other.fun

    def contains(self, expr):
        return self == expr or self.expr.contains(expr)

    def sub(self, find, replace):
        return replace if self == find else Apply(self.fun, self.expr.sub(find, replace))

    def map(self, fun):
        return fun(Apply(self.fun.map(fun), self.expr.map(fun)))

class Fun:
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return self.sym

    def __eq__(self, other):
        return self.sym == other.sym

    def map(self, fun):
        return fun(self)
