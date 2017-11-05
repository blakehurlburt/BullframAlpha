assert(__name__ == '__main__')

import deriv
import parser
import simplify

test = "deriv(sin(2*x) * cos(1 / x), x)"

print(test)
res = parser.parse(test)
print(res)
res = deriv.takeDeriv(res)
print(res)
res = simplify.simplify(res)
print(res)
