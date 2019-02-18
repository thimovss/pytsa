import inspect

from src.pytsa import sa_bool


def sa_number(arg_name, **rules):
    """
    Ensures the given parameter is of type number, float, or long and not None, and abides by all given rules
    """

    def _sa_number(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'number argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'number argument \'{}\' was None'.format(arg_name)
            assert (isinstance(val, int) or isinstance(val, float)) and not isinstance(val, bool), \
                'number argument \'{}\' with value {} was of type {}, not one of number types \'int\' or \'float\'' \
                    .format(arg_name, val, type(val))

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in NUMBER_RULES, 'rule \'{}\' is unknown for sa_number'.format(rule)
            _checker = NUMBER_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_number


@sa_number('rule_val')
def _number_gte(arg_name, rule_val, func):
    def _check(val):
        assert val >= rule_val, 'number argument \'{}\' with value {} was not greater than or equal to {}'.format(
            arg_name,
            val,
            rule_val)
        func(val)

    return _check


@sa_number('rule_val')
def _number_lte(arg_name, rule_val, func):
    def _check(val):
        assert val <= rule_val, 'number argument \'{}\' with value {} was not lesser than or equal to {}'.format(
            arg_name,
            val,
            rule_val)
        func(val)

    return _check


@sa_number('rule_val')
def _number_gt(arg_name, rule_val, func):
    def _check(val):
        assert val > rule_val, 'number argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                     rule_val)
        func(val)

    return _check


@sa_number('rule_val')
def _number_lt(arg_name, rule_val, func):
    def _check(val):
        assert val < rule_val, 'number argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                    rule_val)
        func(val)

    return _check


@sa_bool('rule_val')
def _number_nonzero(arg_name, rule_val, func):
    if not rule_val:
        return func

    def _check(val):
        assert val != 0, 'number argument \'{}\' with value {} was 0'.format(arg_name, val)
        func(val)

    return _check


@sa_number('rule_val')
def _number_modulo(arg_name, rule_val, func):
    def _check(val):
        assert val % rule_val == 0.0, 'number argument \'{}\' with value {} was not a multiple of {}'.format(arg_name,
                                                                                                           val,
                                                                                                           rule_val)
        func(val)

    return _check


NUMBER_RULES = {
    'gte': _number_gte,
    'lte': _number_lte,
    'gt': _number_gt,
    'lt': _number_lt,
    'non_zero': _number_nonzero,
    'mod': _number_modulo
}
