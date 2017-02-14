def gcd(x, y):
    if x == 0:
        return y
    if y == 0:
        return x
    while y != 0:
        rem = x % y
        x = y
        y = rem
    return x
