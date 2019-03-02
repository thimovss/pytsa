import inspect
import os

from decorator import decorator

from src.pytsa import sa_bool, sa_number


def sa_float(arg_name, **rules):
    """
    Ensures the given parameter is of type float and not None, and abides by all given rules
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in FLOAT_RULES, 'rule \'{}\' is unknown for sa_float'.format(rule)
        rule_funcs.append(FLOAT_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_float(func, *args, **kw):

        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'float argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)
        val = args[arg_index]

        assert allow_none or val is not None, 'float argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or isinstance(val,
                                                          float), 'float argument \'{}\' with value {} was of type {}, not of type \'float\''.format(
            arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_float


@sa_number('rule_val')
def _float_gte(arg_name, rule_val):
    def _check(val):
        assert val >= rule_val, 'float argument \'{}\' with value {} was not greater than or equal to {}'.format(
            arg_name, val, rule_val)

    return _check


@sa_number('rule_val')
def _float_lte(arg_name, rule_val):
    def _check(val):
        assert val <= rule_val, 'float argument \'{}\' with value {} was not lesser than or equal to {}'.format(
            arg_name, val, rule_val)

    return _check


@sa_number('rule_val')
def _float_gt(arg_name, rule_val):
    def _check(val):
        assert val > rule_val, 'float argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                    rule_val)

    return _check


@sa_number('rule_val')
def _float_lt(arg_name, rule_val):
    def _check(val):
        assert val < rule_val, 'float argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                   rule_val)

    return _check


@sa_bool('rule_val')
def _float_nonzero(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert val != 0, 'float argument \'{}\' with value {} was 0'.format(arg_name, val)

    return _check


@sa_number('rule_val')
def _float_modulo(arg_name, rule_val):
    def _check(val):
        assert val % rule_val == 0, 'float argument \'{}\' with value {} was not a multiple of {}'.format(arg_name, val,
                                                                                                          rule_val)

    return _check


FLOAT_RULES = {
    'gte': _float_gte,
    'lte': _float_lte,
    'gt': _float_gt,
    'lt': _float_lt,
    'non_zero': _float_nonzero,
    'mod': _float_modulo
}
