DIGITS = '0123456789ABCDEF'

def hex(number):
    if number == 0:
        return '0'
    res = ''
    while number > 0:
        digit = number % 16
        res = DIGITS[digit] + res
        number = number // 16
    return res