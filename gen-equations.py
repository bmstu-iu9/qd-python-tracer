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

# x1 = a/q, x2 = b/q
# q²x² - (a+b)·qx + ab = 0
# D = q²(a-b)²
equals = []
for a in range(-100, 100):
    for b in range(-100, 100):
        for q in range(1, 100):
            D = q*q*(a-b)*(a-b)
            A = q*q
            B = -(a+b)*q
            C = a*b
            x1 = a/q
            x2 = b/q
            if (0 <= D <= 9999 and (B != 0 or C != 0)
                and 100 * a % q == 0 and 100 * b % q == 0
                and 0 <= B*B <= 9999 and fabs(4*A*C) <= 9999
                and 1 <= C <= 99):
                equals += [(A, B, C, D, x1, x2)]

equals.sort()

for eq in equals:
  print("%.2fx2%+.2fx%+.2f = 0, D = %.2f, x1 = %.2f, x2=%.2f" % eq)
