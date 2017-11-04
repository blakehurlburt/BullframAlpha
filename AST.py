class Expr:
    def __repr__(self):
        return str(self)

class Add(Expr):
    def __init__(self, addends):
        self.children = addends

    def __str__(self):
        return "(+, " + ", ".join(map(str, self.children)) + ")"

    def __eq__(self, other):
        return isinstance(other, Add) and self.children == other.children

    def contains(self, expr):
        return self == expr or any(map(lambda e: e.contains(expr), self.children))


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

class Mul(Expr):
    def __init__(self, factors):
        self.children = factors

    def __str__(self):
        return "(*, " + ", ".join(map(str, self.children)) + ")"

    def __eq__(self, other):
        return isinstance(other, Mul) and self.children == other.children

    def contains(self, expr):
        return self == expr or any(map(lambda e: e.contains(expr), self.children))

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

class Neg(Expr):
        def __init__(self, exp):
            self.exp = exp

        def __str__(self):
            return "(-, " + str(self.exp) + ")"

        def __eq__(self, other):
            return isinstance(other, Neg) and self.exp == other.exp

        def contains(self, expr):
            return self == expr or self.exp.contains(expr)


class Num(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return isinstance(other, Num) and self.val == other.val

    def contains(self, expr):
        return False

class Var(Expr):
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return self.sym

    def __eq__(self, other):
        return isinstance(other, Var) and self.sym == other.sym

    def contains(self, expr):
        return self == expr

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

class Fun:
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return self.sym

    def __eq__(self, other):
        return self.sym == self.other
