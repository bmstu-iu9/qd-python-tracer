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

def preproc_file(input_name):
    with open(input_name) as fin:
        num = 1
        FORMATTERS = [
            ('logickw', preproc_logic),
            ('elsekw', preproc_else),
            ('assign', preproc_assign),
            ('comment', preproc_comment),
            ('defkw', preproc_defkw),
            ('returnkw', preproc_return),
            ('calledfunc', preproc_callfunc),
            ('from', preproc_from),
        ]
        lines_out = []
        logic_funcs = []

        for line in fin:
            line = line.rstrip()
            parsed = RE_CODELINE.match(line)
            if not parsed:
                print('{input_name}:{num}:Bad line: {line}'.format(**locals()))
                return []

            for group, preproc in FORMATTERS:
                if parsed and parsed.group(group):
                    groupdict = parsed.groupdict()
                    groupdict['num'] = num
                    preproc(groupdict, line, lines_out, logic_funcs)
                    break;
            else:
                if line == '' or parsed.group('spaces'):
                    lines_out.append(line)
                else:
                    print('{input_name}:{num}:Bad line: {line}'
                          .format(**locals()))
                    return False
            num += 1

        return '\n'.join(logic_funcs + lines_out)


def preproc_logic(groups, line, lines_out, logic_funcs):
    (fmt_expr, vars) = expr_format(groups['logicexpr'])
    groups['fmt_expr'] = fmt_expr
    groups['args'] = ', '.join(vars)
    logic_funcs.append('def trace_logic_func_{num}({args}):'.format(**groups))
    logic_funcs.append('    trace_res = {logicexpr}'.format(**groups))
    logic_funcs.append('    print(\'{num:3} {logickw}\' + {fmt_expr} + '
                       '\': --- \' + repr(trace_res))'.format(**groups))
    logic_funcs.append('    return trace_res'.format(**groups))
    logic_funcs.append('')
    lines_out.append('{spaces}{logickw} trace_logic_func_{num}({args}):'
                     .format(**groups))

def preproc_else(groups, line, lines_out, logic_funcs):
    lines_out.append(line)
    lines_out.append('{spaces}    print(\'{num:3} else:\')'.format(**groups))

def preproc_assign(groups, line, lines_out, logic_funcs):
    if groups['index']:
        groups['format'] = expr_format(groups['assignexpr'])[0]
        lines_out.append('{spaces}trace_index = {index}'.format(**groups))
        lines_out.append('{spaces}r_trace_index = repr(trace_index)'
                         .format(**groups))
        lines_out.append('{spaces}'
                         'print(\'{num:3} {assignvar}[\' + r_trace_index + \']'
                         '{assign}\' + {format})'
                         .format(**groups))
        lines_out.append('{spaces}trace_res = {assignexpr}'.format(**groups))
        lines_out.append('{spaces}'
                         'print(\'    {assignvar}[\' + r_trace_index +\']'
                         '{assign}\' + repr(trace_res))'
                         .format(**groups))
        lines_out.append('{spaces}{assignvar}[trace_index]{assign}trace_res'
                         .format(**groups))
    else:
        groups['format'] = expr_format(groups['assignexpr'])[0]
        lines_out.append('{spaces}'
                         'print(\'{num:3} {assignvar}{assign}\' + {format})'
                         .format(**groups))
        lines_out.append('{spaces}trace_res = {assignexpr}'.format(**groups))
        lines_out.append('{spaces}'
                         'print(\'    {assignvar}{assign}\' + repr(trace_res))'
                         .format(**groups))
        lines_out.append('{spaces}{assignvar}{assign}trace_res'.format(**groups))

def preproc_comment(groups, line, lines_out, logic_funcs):
    lines_out.append(line)

def preproc_defkw(groups, line, lines_out, logic_funcs):
    (format, vars) = expr_format(groups['params'])
    groups['formal_params'] = ', '.join(['{}={{}}'.format(arg) for arg in vars])
    groups['actual_params'] = ', '.join(vars)
    lines_out.append(line)
    lines_out.append('{spaces}    '
                     'print(\'{num:3} def {funcname}({formal_params})\''
                     '.format({actual_params}))'
                     .format(**groups))

def preproc_return(groups, line, lines_out, logic_funcs):
    lines_out.append('{spaces}trace_res = {returnexpr}'.format(**groups))
    lines_out.append('{spaces}print(\'{num:3} return\', repr(trace_res))'
                     .format(**groups))
    lines_out.append('{spaces}return trace_res'.format(**groups))

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


VARIABLE=(r'((?P<variable>[A-Za-z]\w*\b(?![\x5B\x28]))'
          r'|(?P<indexvar>[A-Za-z]\w*\b(?=[\x5B\x28]))'
          r'|(?P<novariable>[^\'"]'
          r'|(?P<quote>[\'"])([^\'"\\]|\\.)*(?P=quote)))')
RE_VARIABLE=re.compile(VARIABLE)

KEYWORDS = set(('and', 'or', 'not'))

def expr_format(expr):
    format = ''
    vars = []
    ivars = []
    for token in RE_VARIABLE.finditer(expr):
        var = token.group('variable')
        ivar = token.group('indexvar')
        if var:
            if var not in KEYWORDS:
                format += '{{{}!r}}'.format(var)
                if var not in (vars + ivars):
                    vars += [var]
            else:
                format += var
        elif ivar:
            format += ivar
            if ivar not in (vars + ivars):
                ivars += [ivar]
        else:
            format += token.group('novariable')
    args = ', '.join([var + '=' + var for var in vars])
    format = '{!r}.format({})'.format(format, args)
    return (format, vars + ivars)

if __name__ == "__main__":
    if len (sys.argv) > 1:
        lines = preproc_file(sys.argv[1])
        with open('~' + sys.argv[1] + '.out.py', 'w') as fout:
            print(lines, file = fout)
    else:
        print('Bad command line')
