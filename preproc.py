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
            r'|((?P<from>from)(?P<frommodule>.*)(?P<importstar>import\s*\*))'
            r')$')
RE_CODELINE = re.compile(CODELINE)

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
            ('from', preproc_from, 'From:'),
        ]
        lines_out = []
        logic_funcs = []

        for line in fin:
            line = line.rstrip()
            print("{0:3} {1}".format(num, line), file=ffmt)

            parsed = RE_CODELINE.match(line)
            for group, preproc, message in FORMATTERS:
                if parsed.group(group):
                    groupdict = parsed.groupdict()
                    groupdict['num'] = num
                    print('{num:3} {message:17} |{line}'
                          .format(num = num, message = message, line = line))
                    preproc(groupdict, line, lines_out, logic_funcs)
                    break;
            else:
                if line == '' or parsed.group('spaces'):
                    print('{num:3} Empty line:'.format(num = num))
                    lines_out.append(line)
                else:
                    print('{num:3} Bad line:         |{line}'
                          .format(num = num, line = line))
                    return False
            num += 1

        for line in logic_funcs + lines_out:
            print(line, file = fout)
    return True


def preproc_logic(groups, line, lines_out, logic_funcs):
    (fmt_expr, vars) = expr_format(groups['logicexpr'])
    groups['fmt_expr'] = fmt_expr
    groups['args'] = ', '.join(vars)
    logic_func = ('def trace_logic_func_{num}({args}):\n'
                  '    trace_res = {logicexpr}\n'
                  '    print(\'{num:3} {logickw}\' + {fmt_expr} + '
                  '\': --- {{!r}}\'.format(trace_res))\n'
                  '    return trace_res\n'
                  .format(**groups))
    logic_funcs.append(logic_func)
    lines_out.append('{spaces}{logickw} trace_logic_func_{num}({args}):'
                     .format(**groups))
    #lines_out.append(line)
    #lines_out.append('{spaces}    print(\'{num:3} {logickw}{logicexpr}\')'
    #                 .format(**groups))

def preproc_else(groups, line, lines_out, logic_funcs):
    lines_out.append(line)
    lines_out.append('{spaces}    print(\'{num:3} else:\')'.format(**groups))

def preproc_assign(groups, line, lines_out, logic_funcs):
    lines_out.append(line)
    # TODO: индекс
    lines_out.append('{spaces}'
                     'print(\'{num:3} {assignvar}{assign}{assignexpr}\')'
                     .format(**groups))
    groups['format'] = expr_format(groups['assignexpr'])[0]
    lines_out.append('{spaces}'
                     'print(\'    {assignvar}{assign}\' + {format})'
                     .format(**groups))
    lines_out.append('{spaces}'
                     'print(\'    {assignvar}{assign}\' + repr({assignexpr}))'
                     .format(**groups))

def preproc_comment(groups, line, lines_out, logic_funcs):
    lines_out.append(line)

def preproc_defkw(groups, line, lines_out, logic_funcs):
    lines_out.append(line)
    lines_out.append('{spaces}    '
                     'print(\'{num:3} in function {funcname}{params}\')'
                     .format(**groups))

def preproc_return(groups, line, lines_out, logic_funcs):
    lines_out.append('{spaces}'
                     'print(\'{num:3} return\', {returnexpr})'
                     .format(**groups))
    lines_out.append(line)

def preproc_callfunc(groups, line, lines_out, logic_funcs):
    lines_out.append('{spaces}'
                     'print(\'{num:3} call {calledfunc}{calledfuncparams}\')'
                     .format(**groups))
    lines_out.append(line)

def preproc_from(groups, line, lines_out, logic_funcs):
    lines_out.append('{spaces}'
                     'print(\'{num:3} importing {frommodule}\')'
                     .format(**groups))
    lines_out.append(line)


VARIABLE=r'((?P<variable>[A-Za-z]\w*\b(?![\x5B\x28]))|(?P<novariable>.))'
RE_VARIABLE=re.compile(VARIABLE)

def expr_format(expr):
    format = ''
    vars = []
    for token in RE_VARIABLE.finditer(expr):
        var = token.group('variable')
        if var:
            format += '{{{}}}'.format(var)
            if var not in vars:
                vars += [var]
        else:
            format += token.group('novariable')
    args = ', '.join([var + '=' + var for var in vars])
    format = '{!r}.format({})'.format(format, args)
    return (format, vars)

if __name__ == "__main__":
    if len (sys.argv) > 1:
        preproc_file(sys.argv[1],
                     '~' + sys.argv[1] + '.out.py',
                     '~' + sys.argv[1] + '.lst')
    else:
        print('Bad command line')
