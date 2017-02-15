from math import *

def square_equal(a, b, c):
    if a != 0:
        D = b*b - 4*a*c
        if D > 0:
            x1 = (-b - sqrt(D)) / (2*a)
            x2 = (-b + sqrt(D)) / (2*a)
            return [x1, x2]
        elif D == 0:
            return [-b / (2*a)]
        else:
            return []
    else:
        if b != 0:
            return [-c / b]
        else:
            return []
