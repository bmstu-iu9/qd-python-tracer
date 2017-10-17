#!/usr/bin/env python3

# vim: shiftwidth=4

import math
import os
import random
import re
import sys
import taskgen
import task_1

def gen_variants(varprefix = '1-1'):
    tasklist = [gen_gcd(True),
                gen_gcd(False),
                gen_hex(),
                gen_square_equal([1, 2]),
                gen_square_equal([0, 1]),
                gen_factorize(),
                gen_remove_digit()]
    taskgen.gen_variants(tasklist, varprefix, 51,
                        'fall_mod1_tasks.txt', 'fall_mod1_answers.txt')

def gen_gcd(no_zero):
    def genargs():
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        return (x, y)

    if no_zero:
        return ('fall_mod1_gcd.py', 'gcd', genargs,
                lambda args, result, stdout: (result >= 3
                                              and 20 <= len(stdout) <= 30))
    else:
        return ('fall_mod1_gcd.py', 'gcd', genargs,
                lambda args, result, stdout: 0 in args)

def gen_hex():
    return ('fall_mod1_hex.py', 'hex',
            lambda: (random.randint(20, 1000),),
            lambda args, result, stdout: re.match('[A-F]', result))

def gen_square_equal(roots_count):
    def genargs():
        a = random.randint(-100, 100)
        b = random.randint(-100, 100)
        c = random.randint(-100, 100)
        return (a, b, c)

    def validargs(args, result, stdout):
        (a, b, c) = args
        if a != 0:
            D = b*b - 4*a*c
            if D > 0:
                sqrtD = int_sqrt(D)
                return (2 in roots_count and sqrtD
                        and 100 * (-b - sqrtD) % (2*a) == 0
                        and 100 * (-b + sqrtD) % (2*a) == 0)
            elif D == 0:
                return (1 in roots_count and 100 * (-b) % (2*a) == 0)
            else:
                return 0 in roots_count and D > -10000
        else:
            if b != 0:
                return (1 in roots_count and 100 * (-c) % b == 0)
            else:
                return 0 in roots_count
    return ('fall_mod1_square_equal.py', 'square_equal', genargs, validargs)

def int_sqrt(x):
    for i in range (1, 100):
        if i*i == x:
            return i
    return None

def gen_factorize():
    def genargs():
        n = random.randint(0, 2000)
        return (n,)

    def validargs(args, result, stdout):
        return len(stdout) < 35

    return ('fall_mod1_factorize.py', 'factorize', genargs, validargs)

def gen_remove_digit():
    def genargs():
        return (random.randint(0, 100000), random.randint(0, 9))

    def validargs(args, result, stdout):
        first_digit = args[0]
        while first_digit > 9:
            first_digit //= 10

        diflen = random.choice([1, 1, 2, 1, 3, 1])
        ls = lambda n: len(str(n))

        return (ls(args[0]) - ls(result) >= diflen
                and first_digit != args[1] and len(stdout) < 35)

    return ('fall_mod1_remove_digit.py', 'remove_digit', genargs, validargs)

if __name__=='__main__':
    if len(sys.argv) > 2:
        gen_variants(os.argv[1])
    else:
        gen_variants()
