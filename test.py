assert(__name__ == "__main__")

from simplify import simplify
from parser import parse
from integral import takeInt
from deriv import takeDeriv

tests = []
# tests.append("deriv(x, x)")
# tests.append("deriv(x^2, x)")
# tests.append("deriv(x^3 + 3*x + 2, x)")
# tests.append("deriv(4*sin(x^2), x)")
# tests.append("deriv((x+1)/(x+2), x)")
# tests.append("deriv(deriv(x^3 + 4*x^2 + 5x + 8, x), x)")
# tests.append("deriv(tan(x), x)")
# tests.append("deriv(e^x + ln(x), x)")
# tests.append("deriv(sin(x^2^x - cos(4+3*x)) / 4*(-2 +x), x)")
tests.append("int((6*x^4+23*x^2+4*x+15)/(x^2+3), x)")

#tests.append("int(x*e^(6*x), x)")


for t in tests:
    print("---------------------------------------------------------")
    print("Trying to evaluate: " + t)
    expr = parse(t)
    print("Parses to: " + str(expr))
    expr = simplify(expr)
    print("Which simplifies to: " + str(expr))
    #expr = simplify(expr)
    #print("Which simplifies to: " + str(expr))
    print("---------------------------------------------------------")
