#!/usr/bin/env python3

# vim: shiftwidth=4

import contextlib
import os
import preproc
import random
import re
import sys

def gen_variant():
    gen_task_1_gcd()
    gen_task_1_hex()

def gen_task_1_gcd():
    def genargs():
        valid_args = False
        while not valid_args:
            x = random.randint(2, 100)
            y = random.randint(2, 100)
            valid_args = x != y
        return (x, y)

    gen_task('task_1_gcd.py', 'gcd', genargs,
             lambda result, stdout: result > 3 and 40 <= len(stdout) <= 50)

def gen_task_1_hex():
    gen_task('task_1_hex.py', 'hex',
             lambda: [random.randint(20, 1000)],
             lambda result, stdout: re.match('[A-F]', result))

def gen_task(source, funcname, genargsfunc, validfunc):
    valid_task = False
    while not valid_task:
        args = genargsfunc()
        (result, stdout) = exec_function_from(source, funcname, args)
        valid_task = validfunc(result, stdout)

    print('=' * 80)
    args = ', '.join(repr(arg) for arg in args)
    print('{funcname}({args}) = {result}'.format(**locals()))
    print('\n'.join(stdout))

def exec_function_from(source, funcname, args):
    code = preproc_code_for_source(source)
    context = {}
    exec_text(code, context)

    code = 'trace_res = ' + funcname + '(*trace_args)'
    context['trace_args'] = args
    stdout = unique_lines(exec_text(code, context))

    return (context['trace_res'], stdout)

memoized_source = None
memoized_code = None
def preproc_code_for_source(source):
    global memoized_source
    global memoized_code

    if memoized_source == source:
        return memoized_code

    code_lines = preproc.preproc_file(source)
    code = compile(code_lines, source + '[preproc]', 'exec')

    memoized_source = source
    memoized_code = code
    return code

def exec_text(text, context):
    with open('~output.tmp', 'w') as fout, \
         contextlib.redirect_stdout(fout):
        exec(text, context)
    with open('~output.tmp') as fin:
        stdout = [line.rstrip() for line in fin]
    os.remove('~output.tmp')
    return stdout

def unique_lines(lines):
    res = []
    for line in lines:
        if not res or res[-1] != line:
            res += [line]
    return res

if __name__=='__main__':
    gen_variant()
