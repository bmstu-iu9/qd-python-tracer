#!/usr/bin/env python3

# vim: shiftwidth=4

import contextlib
import os
import preproc
import sys

def exec_text(text, context):
    with open('~output.tmp', 'w') as fout, \
         contextlib.redirect_stdout(fout):
        exec(text, context)
    with open('~output.tmp') as fin:
        stdout = [line.rstrip() for line in fin]
    os.remove('~output.tmp')
    return stdout

def exec_function_from(code, funcname, args):
    context = {'trace_args' : args}
    code += '\ntrace_res = ' + funcname + '(*trace_args)'
    stdout = exec_text(code, context)
    return (context['trace_res'], stdout)

def exec_preproc(input_name):
    lines = preproc.preproc_file(input_name)
    (result, stdout) = exec_function_from(lines, 'gcd', [3684468, 17354368])
    return [repr(result)] + stdout

if __name__=='__main__':
    if len (sys.argv) > 1:
        print('\n'.join(exec_preproc(sys.argv[1])))
    else:
        print('Bad command line')
