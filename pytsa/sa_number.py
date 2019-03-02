import inspect
import os
from decimal import Decimal

from decorator import decorator

from pytsa import sa_bool


def sa_number(arg_name, **rules):
    """
    Ensures the given parameter is of type number, float, or long and not None, and abides by all given rules
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in NUMBER_RULES, 'rule \'{}\' is unknown for sa_number'.format(rule)
        rule_funcs.append(NUMBER_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_number(func, *args, **kw):

        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'number argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)
        val = args[arg_index]

        assert allow_none or val is not None, 'number argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or (isinstance(val, int) or isinstance(val, float)) and not isinstance(
            val, bool), \
            'number argument \'{}\' with value {} was of type {}, not one of number types \'int\' or \'float\'' \
                .format(arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_number


@sa_number('rule_val')
def _number_gte(arg_name, rule_val):
    def _check(val):
        assert val >= rule_val, 'number argument \'{}\' with value {} was not greater than or equal to {}'.format(
            arg_name,
            val,
            rule_val)

    return _check


@sa_number('rule_val')
def _number_lte(arg_name, rule_val):
    def _check(val):
        assert val <= rule_val, 'number argument \'{}\' with value {} was not lesser than or equal to {}'.format(
            arg_name,
            val,
            rule_val)

    return _check


@sa_number('rule_val')
def _number_gt(arg_name, rule_val):
    def _check(val):
        assert val > rule_val, 'number argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                     rule_val)

    return _check


@sa_number('rule_val')
def _number_lt(arg_name, rule_val):
    def _check(val):
        assert val < rule_val, 'number argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                    rule_val)

    return _check


@sa_bool('rule_val')
def _number_nonzero(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert val != 0, 'number argument \'{}\' with value {} was 0'.format(arg_name, val)

    return _check


@sa_number('rule_val')
def _number_modulo(arg_name, rule_val):
    def _check(val):
        assert Decimal(val) % Decimal(rule_val) == Decimal(
            '0.0'), 'number argument \'{}\' with value {} was not a multiple of {}'.format(arg_name,
                                                                                           val,
                                                                                           rule_val)

    return _check


NUMBER_RULES = {
    'gte': _number_gte,
    'lte': _number_lte,
    'gt': _number_gt,
    'lt': _number_lt,
    'non_zero': _number_nonzero,
    'mod': _number_modulo
}
