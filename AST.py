class Expr:
    pass

class Add(Expr):
    def __init__(self, addends):
        self.children = addends

    def __str__(self):
        return "(+, " + ", ".join(map(str, self.children)) + ")"

class Sub(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(-, " +  str(self.left) + ", " + str(self.right) + ")"

class Mul(Expr):
    def __init__(self, factors):
        self.children = factors

    def __str__(self):
        return "(*, " + ", ".join(map(str, self.children)) + ")"

class Div(Expr):
    def __init__(self, top, bottom):
        self.left = top
        self.right = bottom

    def __str__(self):
        return "(/, " +  str(self.left) + ", " + str(self.right) + ")"

class Pow(Expr):
        def __init__(self, base, expr):
            self.left = base
            self.right = exp

        def __str__(self):
            return "(^, " +  str(self.left) + ", " + str(self.right) + ")"

class Num(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

class Var(Expr):
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return self.sym

class Deriv(Expr):
    def __init__(self, expr, sym):
        self.sym = sym
        self.expr = expr

    def __str__(self):
        return "(D, " + str(self.expr) + ", " + str(self.sym) + ")"

class Apply(Expr):
    def __init__(self, fun, expr):
        self.fun = fun
        self.expr = expr

    def __str__(self):
        return "(" + str(self.fun) + ", " + str(self.expr) + ")"
