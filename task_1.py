#!/usr/bin/env python3

# vim: shiftwidth=4

import contextlib
import os
import preproc
import sys

def exec_preproc(input_name):
    lines = preproc.preproc_file(input_name)
    lines = '\n'.join(lines)
    with open('~output.tmp', 'w') as fout, \
         contextlib.redirect_stdout(fout):
        if lines:
            context = {}
            exec(lines, context)
            for k in context:
                print(k)
            (x, y) = (3684468, 17354368)
            gcd = context['gcd'](x, y)
            print('gcd({x}, {y}) = {gcd}'.format(**locals()))
        else:
            return []
    with open('~output.tmp') as fin:
        stdout = [line.rstrip() for line in fin]
    os.remove('~output.tmp')
    return stdout

if __name__=='__main__':
    if len (sys.argv) > 1:
        print('\n'.join(exec_preproc(sys.argv[1])))
    else:
        print('Bad command line')
