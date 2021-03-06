def gcd(x, y):
    if x < 0:
        x = -x
    if y < 0:
        y = -y
    if x == 0:
        return y
    while y != 0:
        rem = x % y
        x = y
        y = rem
    return x
