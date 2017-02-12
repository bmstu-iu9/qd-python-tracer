#!/usr/bin/env python3

# vim: shiftwidth=4

import sys
import re

CODELINE = (r'^(?P<spaces>\s*)'
            r'(((?P<logickw>while|if|elif)(?P<logicexpr>.*):)'
            r'|(?P<elsekw>else:)'
            r'|((?P<assignvar>\w+)(?P<index>\[[^][]*\])?'
            r'(?P<assign>\s*=\s*)(?P<assignexpr>.*))'
            r'|(?P<comment>(#.*)?)'
            r'|((?P<defkw>def\s*)(?P<funcname>\w+)(?P<params>\(.*\):))'
            r'|((?P<returnkw>return)(?P<returnexpr>.*))'
            r'|((?P<calledfunc>\w+)(?P<calledfuncparams>\(.*\)))'
            r')$')

def preproc_logic(groups, line, fout):
    print(line, file = fout)
    traced_line = \
            '{spaces}    print(\'{num:3} {logickw}{logicexpr}\')'.format(**groups)
    print(traced_line, file = fout)

def preproc_else(groups, line, fout):
    print(line, file = fout)
    print('{spaces}    print(\'{num:3} else:\')'.format(**groups), file = fout)

def preproc_assign(groups, line, fout):
    print(line, file = fout)
    # TODO: индекс
    traced_line = ('{spaces}'
                   'print(\'{num:3} {assignvar}{assign}{assignexpr}\')'
                   .format(**groups))
    print(traced_line, file = fout)
    traced_line = ('{spaces}'
                   'print(\'    {assignvar}{assign}\', {assignexpr})'
                   .format(**groups))
    print(traced_line, file = fout)

def preproc_comment(groups, line, fout):
    print(line, file = fout)

def preproc_defkw(groups, line, fout):
    traced_line = ('{spaces}    '
                   'print(\'{num:3} in function {funcname}{params}\')'
                   .format(**groups))
    print(line, file = fout)
    print(traced_line, file = fout)

def preproc_return(groups, line, fout):
    traced_line= ('{spaces}'
                  'print(\'{num:3} return\', {returnexpr})'
                  .format(**groups))
    print(traced_line, file = fout)
    print(line, file = fout)

def preproc_callfunc(groups, line, fout):
    traced_line = ('{spaces}'
                   'print(\'{num:3} call {calledfunc}{calledfuncparams}\')'
                   .format(**groups))
    print(traced_line, file = fout)
    print(line, file = fout)

def preproc_file(input_name, output_name, format_name):
    with open(input_name) as fin, \
         open(output_name, 'w') as fout, \
         open(format_name, 'w') as ffmt:
        num = 1
        FORMATTERS = [
            ('logickw', preproc_logic, 'Logic operator:'),
            ('elsekw', preproc_else, 'Else keyword:'),
            ('assign', preproc_assign, 'Assign:'),
            ('comment', preproc_comment, 'Comment:'),
            ('defkw', preproc_defkw, 'Function def:'),
            ('returnkw', preproc_return, 'Return:'),
            ('calledfunc', preproc_callfunc, 'Call func:'),
        ]
        re_line = re.compile(CODELINE)
        for line in fin:
            line = line.rstrip()
            print("{0:3} {1}".format(num, line), file=ffmt)

            parsed = re_line.match(line)
            for group, preproc, message in FORMATTERS:
                if parsed.group(group):
                    groupdict = parsed.groupdict()
                    groupdict['num'] = num
                    print('{num:3} {message:17} |{line}'
                          .format(num = num, message = message, line = line))
                    preproc(groupdict, line, fout)
                    break;
            else:
                if line == '' or parsed.group('spaces'):
                    print('{num:3} Empty line:'.format(num = num))
                    print(line, file = fout)
                else:
                    print('{num:3} Bad line:         |{line}'
                          .format(num = num, line = line))
                    return False
            num += 1
    return True

if __name__ == "__main__":
    if len (sys.argv) > 1:
        preproc_file(sys.argv[1],
                     '~' + sys.argv[1] + '.out.py',
                     '~' + sys.argv[1] + '.lst')
    else:
        print('Bad command line')
