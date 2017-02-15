#!/usr/bin/env python3

from math import *

def gcd(x, y):
    if x == 0:
        return y
    while y != 0:
        rem = x % y
        x = y
        y = rem
    return x

# x1 = p/r, x2 = q/r
# r2x2 - (p+q)·rx + pq = 0
# D = r2(p-q)2
equals = []
for p in range(-100, 100):
    for q in range(-100, 100):
        for r in range(1, 100):
            D = r*r*(p-q)*(p-q)
            a = r*r
            b = -(p+q)*r
            c = p*q
            x1 = p/r
            x2 = q/r
            if (0 <= D <= 9999 and (b != 0 or c != 0)
                and 100 * p % r == 0 and 100 * q % r == 0
                and 0 <= b*b <= 9999 and fabs(4*a*c) <= 9999
                and 1 <= c <= 99):
                equals += [(a, b, c, D, x1, x2)]

equals.sort()

for eq in equals:
  print("%.2fx2%+.2fx%+.2f = 0, D = %.2f, x1 = %.2f, x2=%.2f" % eq)
