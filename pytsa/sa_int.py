import inspect
import os

from decorator import decorator

from pytsa import sa_bool, sa_number


def sa_int(arg_name, **rules):
    """
    Ensures the given parameter is of type int and not None, and abides by all given rules
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in INT_RULES, 'rule \'{}\' is unknown for sa_int'.format(rule)
        rule_funcs.append(INT_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_int(func, *args, **kw):

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

        assert allow_none or val is not None, 'int argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or (isinstance(val, int) and not isinstance(val, bool)), \
            'int argument \'{}\' with value {} was of type {}, not of type \'int\''.format(arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_int


@sa_number('rule_val')
def _int_gte(arg_name, rule_val):
    def _check(val):
        assert val >= rule_val, 'int argument \'{}\' with value {} was not greater than or equal to {}'.format(arg_name,
                                                                                                               val,
                                                                                                               rule_val)

    return _check


@sa_number('rule_val')
def _int_lte(arg_name, rule_val):
    def _check(val):
        assert val <= rule_val, 'int argument \'{}\' with value {} was not lesser than or equal to {}'.format(arg_name,
                                                                                                              val,
                                                                                                              rule_val)

    return _check


@sa_number('rule_val')
def _int_gt(arg_name, rule_val):
    def _check(val):
        assert val > rule_val, 'int argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                  rule_val)

    return _check


@sa_number('rule_val')
def _int_lt(arg_name, rule_val):
    def _check(val):
        assert val < rule_val, 'int argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                 rule_val)

    return _check


@sa_bool('rule_val')
def _int_nonzero(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert val != 0, 'int argument \'{}\' with value {} was 0'.format(arg_name, val)

    return _check


@sa_number('rule_val')
def _int_modulo(arg_name, rule_val):
    def _check(val):
        assert val % rule_val == 0, 'int argument \'{}\' with value {} was not a multiple of {}'.format(arg_name, val,
                                                                                                        rule_val)

    return _check


INT_RULES = {
    'gte': _int_gte,
    'lte': _int_lte,
    'gt': _int_gt,
    'lt': _int_lt,
    'non_zero': _int_nonzero,
    'mod': _int_modulo
}