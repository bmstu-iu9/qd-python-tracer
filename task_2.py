#!/usr/bin/env python3

# vim: shiftwidth=4

import math
import os
import random
import re
import sys
import taskgen
import task_1

def gen_variants(varprefix = '2-1'):
    tasklist = [gen_gcd(True),
                gen_gcd(False),
                task_1.gen_hex,
                gen_square_equal(True),
                gen_square_equal(False),
                gen_findmax_normal,
                gen_unique]

    varset = set()
    with open('task_2_tasks.txt', 'w') as ftasks, \
         open('task_2_answers.txt', 'w') as fanswers:
        for i in range(1, 5):
            print(i, end='\r')
            var = '{varprefix}-{i}'.format(**locals())
            taskgen.gen_variant(tasklist, var, varset, ftasks, fanswers)

def gen_gcd(no_zero):
    def genargs():
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        return (x, y)

    def gen_no_zero():
        return ('task_2_gcd.py', 'gcd', genargs,
                lambda args, result, stdout: result >= 3 and 30 <= len(stdout) <= 40)

    def gen_zero():
        return ('task_2_gcd.py', 'gcd', genargs,
                lambda args, result, stdout: 0 in args)

    return gen_no_zero if no_zero else gen_zero

def gen_square_equal(roots):
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
                return (roots and sqrtD
                        and 100 * (-b - sqrtD) % (2*a) == 0
                        and 100 * (-b + sqrtD) % (2*a) == 0)
            elif D == 0:
                return (roots and 100 * (-b) % (2*a) == 0)
            else:
                return not roots
        else:
            if b != 0:
                return (roots and 100 * (-c) % b == 0)
            else:
                return not roots
    return lambda: ('task_1_square_equal.py', 'square_equal', genargs, validargs)

def int_sqrt(x):
    for i in range (1, 99):
        if i*i == x:
            return i
    return None

def gen_findmax_normal():
    def genargs():
        items_len = random.randint(1, 20)
        items = []
        while items_len > 0:
            items += [random.randint(-99, 99)]
            items_len -= 1
        return ((list, tuple(items)),)

    def valid(args, result, stdout):
        return 20 <= len(stdout) <= 30

    return ('task_2_findmax.py', 'findmax', genargs, valid)

def gen_unique():
    def genargs():
        items_len = random.randint(0, 20)
        randint = lambda: random.randint(-99, 99)
        items = [randint()]
        while items_len > 0:
            items += [random.choice([randint(), random.choice(items)])]
            items_len -= 1
        return ((list, tuple(items)),)

    def valid(args, result, stdout):
        arg = taskgen.real_args(args)[0]
        return (20 <= len(stdout) <= 30
                and 1.1 <= len(arg) / len(result) <= 1.5)

    return ('task_2_uniq.py', 'unique', genargs, valid)

if __name__=='__main__':
    if len(sys.argv) > 2:
        gen_variants(os.argv[1])
    else:
        gen_variants()
