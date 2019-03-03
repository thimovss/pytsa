import inspect
import os

from decorator import decorator

from pytsa import sa_int, sa_bool, sa_type


def _format_list(val):
    if len(val) <= 3:
        return str(val)
    return '[{}, {}, {}, ...]'.format(val[0], val[1], val[2])


def sa_list(arg_name, **rules):
    """
    Ensures the given parameter is of type list and not None, and abides by all given rules
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in LIST_RULES, 'rule \'{}\' is unknown for sa_list'.format(rule)
        rule_funcs.append(LIST_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_list(func, *args, **kw):

        func_spec = inspect.getfullargspec(func)
        args_spec = func_spec.args
        kwargs_spec = func_spec.kwonlyargs
        val = None
        if arg_name in args_spec:
            arg_index = args_spec.index(arg_name)
            val = args[arg_index]
        elif arg_name in kwargs_spec:
            val = kw[arg_name]
        else:
            raise AssertionError('int argument name \'{}\' not found in argument specification'.format(arg_name))

        assert allow_none or val is not None, 'list argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or isinstance(val, list), \
            'list argument \'{}\' with value {} was of type {}, not of type \'list\''.format(arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_list


@sa_int('rule_val')
def _list_len(arg_name, rule_val):
    def _check(val):
        assert len(val) == rule_val, 'list argument \'{}\' with value {} and length of {} was not equal to {}'.format(
            arg_name, _format_list(val), len(val), rule_val)

    return _check


@sa_type('rule_val')
def _list_type(arg_name, rule_val):
    def _check(val):
        for i, v in enumerate(val):
            assert isinstance(v,
                              rule_val), 'list argument \'{}\' with type {} had value with type {} on index {}'.format(
                arg_name, rule_val, type(v), i)

    return _check


@sa_bool('rule_val')
def _list_not_empty(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert len(val) != 0, 'list argument \'{}\' was an empty array'.format(arg_name)

    return _check


LIST_RULES = {
    'len': _list_len,
    'type': _list_type,
    'not_empty': _list_not_empty,
}
