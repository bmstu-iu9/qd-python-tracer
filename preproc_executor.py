#!/usr/bin/env python3

# vim: shiftwidth=4

import contextlib
import os
import preproc

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
        if not res or '    ' + res[-1][4:] != line:
            res += [line]
    return res
