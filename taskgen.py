#!/usr/bin/env python3

# vim: shiftwidth=4

import preproc_executor as pex

def gen_variant(tasklist, var, varset, ftasks, fanswers):
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
        args = ', '.join(repr(arg) for arg in real_args(args))
        print('{item_no}. {funcname}({args})'.format(**locals()), file = ftasks)

        print('{item_no}. {funcname}({args}) = {result!r}'.format(**locals()),
              file = fanswers)
        print('\n'.join(stdout), file = fanswers)
        print(file = fanswers)

    print('PAGEBREAK', file = ftasks)
    print('PAGEBREAK', file = fanswers)

def real_args(args):
    res = []
    for arg in args:
        if type(arg) == tuple:
            res += [arg[0](arg[1])]
        else:
            res += [arg]
    return res

def gen_task(source, funcname, genargsfunc, validfunc, num, varset):
    valid_task = False
    while not valid_task:
        args = genargsfunc()
        if (args, num) not in varset:
            (result, stdout) = \
                pex.exec_function_from(source, funcname, real_args(args))
            valid_task = validfunc(args, result, stdout)

    varset.add((args, num))

    return (args, result, stdout)
