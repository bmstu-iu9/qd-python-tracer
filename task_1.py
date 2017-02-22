#!/usr/bin/env python3

# vim: shiftwidth=4

import math
import preproc_executor as pex
import os
import random
import re
import sys

def gen_variants(varprefix = '1-1'):
    varset = set()
    with open('task_1_tasks.txt', 'w') as ftasks, \
         open('task_1_answers.txt', 'w') as fanswers:
        for i in range(1, 50):
            print(i, end='\r')
            var = '{varprefix}-{i}'.format(**locals())
            gen_variant(var, varset, ftasks, fanswers)

def gen_variant(var, varset, ftasks, fanswers):
    tasklist = [gen_gcd_no_zero,
                gen_gcd_zero_x,
                gen_gcd_zero_y,
                gen_hex,
                gen_square_equal_d_pos,
                gen_square_equal_d_zero,
                gen_square_equal_d_neg,
                gen_square_equal_linear_valid,
                gen_square_equal_linear_invalid]

    print('Группа: Л4-2__, фамилия, имя ' + '_' * 50, file = ftasks)
    print('Вариант: ' + var, file = ftasks)
    print(file = ftasks)
    print('Выполните трассировку следующих вызовов функций:', file = ftasks)

    print('Вариант: ' + var, file = fanswers)
    for num, task in enumerate(tasklist):
        (filename, funcname, genargsfunc, validfunc) = task()
        (args, result, stdout) = gen_task(filename, funcname,
                                          genargsfunc, validfunc,
                                          num, varset)

        item_no = num + 1
        args = ', '.join(repr(arg) for arg in args)
        print('{item_no}. {funcname}({args})'.format(**locals()), file = ftasks)

        print('{item_no}. {funcname}({args}) = {result!r}'.format(**locals()),
              file = fanswers)
        print('\n'.join(stdout), file = fanswers)

    print('PAGEBREAK', file = ftasks)
    print('PAGEBREAK', file = fanswers)

def gen_gcd_no_zero():
    def genargs():
        valid_args = False
        while not valid_args:
            x = random.randint(2, 100)
            y = random.randint(2, 100)
            valid_args = x != y
        return (x, y)

    return ('task_1_gcd.py', 'gcd', genargs,
            lambda args, result, stdout: result > 3 and 40 <= len(stdout) <= 50)

def gen_gcd_zero_x():
    return ('task_1_gcd.py', 'gcd',
            lambda: (0, random.randint(2, 100)),
            lambda args, result, stdout: True)

def gen_gcd_zero_y():
    return ('task_1_gcd.py', 'gcd',
            lambda: (random.randint(2, 100), 0),
            lambda args, result, stdout: True)

def gen_hex():
    return ('task_1_hex.py', 'hex',
            lambda: (random.randint(20, 1000),),
            lambda args, result, stdout: re.match('[A-F]', result))

def gen_square_equal_d_pos():
    sqr = lambda x: x*x

    # x1 = p/r, x2 = q/r
    # r2x2 - (p+q)·rx + pq = 0
    # D = r2(p-q)2
    def genargs():
        valid_args = False
        while not valid_args:
            p = random.randint(-99, 99)
            q = random.randint(-99, 99)
            r = random.randint(1, 99)
            sgn = random.randint(-1, +1)

            D = sqr(r*(p-q))
            a = r*r*sgn
            b = -(p+q)*r*sgn
            c = p*q*sgn

            valid_args = (a != 0 and 0 <= D <= 9999 and (b != 0 or c != 0)
                          and 100 * p % r == 0 and 100 * q % r == 0
                          and -99 <= b <= 99 and math.fabs(4*a*c) <= 9999
                          and 1 <= c <= 99)
        return (a, b, c)

    return ('task_1_square_equal.py', 'square_equal', genargs,
            lambda args, result, stdout: True)

def gen_square_equal_d_zero():
    # a·x2 + b·x + c = 0
    # (p·x — q) = 0
    # a = p2, b = -2pq, c = q2
    def genargs():
        valid_args = False
        while not valid_args:
            p = random.randint(-99, 99)
            q = random.randint(1, 99)
            sgn = random.randint(-1, +1)

            a = p*p*sgn
            b = -2*p*q*sgn
            c = q*q*sgn

            valid_args = (a != 0 and -99 <= a <= 99 and 100 * q % p == 0
                          and -99 <= b <= 99 and -99 <= c <= 99)
        return (a, b, c)

    return ('task_1_square_equal.py', 'square_equal', genargs,
            lambda args, result, stdout: True)

def gen_square_equal_d_neg():
    def genargs():
        valid_args = False
        while not valid_args:
            a = random.randint(-99, 99)
            b = random.randint(-99, 99)
            c = random.randint(-99, 99)

            D = b*b - 4*a*c
            valid_args = (D < 0 and a != 0 and -99 <= a <= 99
                          and -99 <= b <= 99 and -99 <= c <= 99
                          and 0 <= b*b <= 999 and math.fabs(4*a*c) <= 999)
        return (a, b, c)

    return ('task_1_square_equal.py', 'square_equal', genargs,
            lambda args, result, stdout: True)

def gen_square_equal_linear_valid():
    def genargs():
        valid_args = False
        while not valid_args:
            b = random.randint(-99, 99)
            c = random.randint(-99, 99)

            valid_args = b != 0 and 100 * c % b == 0 and c != 0
        return (0, b, c)

    return ('task_1_square_equal.py', 'square_equal', genargs,
            lambda args, result, stdout: True)

def gen_square_equal_linear_invalid():
    return ('task_1_square_equal.py', 'square_equal',
            lambda: (0, 0, random.randint(-99, 99)),
            lambda args, result, stdout: True)

def gen_findmax_normal():
    def genargs():
        items_len = random.randint(1, 20)
        items = []
        while items_len > 0:
            items += [random.randint(-99, 99)]
            items_len -= 1
        return (tuple(items),)

    def valid(args, result, stdout):
        return 30 <= len(stdout) <= 40

    return ('task_1_findmax.py', 'findmax', genargs, valid)

def gen_task(source, funcname, genargsfunc, validfunc, num, varset):
    valid_task = False
    while not valid_task:
        args = genargsfunc()
        if (args, num) not in varset:
            (result, stdout) = pex.exec_function_from(source, funcname, args)
            valid_task = validfunc(args, result, stdout)

    varset.add((args, num))

    return (args, result, stdout)

if __name__=='__main__':
    if len(sys.argv) > 2:
        gen_variants(os.argv[1])
    else:
        gen_variants()
