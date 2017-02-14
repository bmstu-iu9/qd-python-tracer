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

# signum
def sign(z):
    if z < 0:
        return -1
    elif z > 0:
        return +1
    else:
        return 0

gcd(20, 35)

sign(-10)
sign(0)
sign(+100)