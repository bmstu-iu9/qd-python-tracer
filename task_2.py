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
                task_1.gen_hex(),
                gen_square_equal(True),
                gen_square_equal(False),
                gen_findmax_normal(),
                gen_unique(),
                gen_join()]
    taskgen.gen_variants(tasklist, varprefix, 30,
                        'task_2_tasks.txt', 'task_2_answers.txt')

def gen_gcd(no_zero):
    def genargs():
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        return (x, y)

    if no_zero:
        return ('task_2_gcd.py', 'gcd', genargs,
                lambda args, result, stdout: (result >= 3
                                              and 20 <= len(stdout) <= 30))
    else:
        return ('task_2_gcd.py', 'gcd', genargs,
                lambda args, result, stdout: 0 in args)

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
    return ('task_1_square_equal.py', 'square_equal', genargs, validargs)

def int_sqrt(x):
    for i in range (1, 99):
        if i*i == x:
            return i
    return None

def gen_findmax_normal():
    def genargs():
        items_len = random.randint(1, 10)
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
        items_len = random.randint(0, 10)
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

def gen_join():
    def genargs():
        sep = random.choice(',+:;')
        items_len = random.randint(1, 10)
        items = []
        while items_len > 0:
            items += [random.randint(0, 99)]
            items_len -= 1
        return (sep, (list, tuple(items)))

    def valid(args, result, stdout):
        return 15 <= len(stdout) <= 25

    return ('task_2_join.py', 'join', genargs, valid)

if __name__=='__main__':
    if len(sys.argv) >= 2:
        gen_variants(sys.argv[1])
    else:
        gen_variants()
