import inspect

from src.pytsa import sa_bool


def sa_float(arg_name, **rules):
    """
    Ensures the given parameter is of type float and not None, and abides by all given rules
    """

    def _sa_float(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'float argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'float argument \'{}\' was None'.format(arg_name)
            assert isinstance(val,
                              float), 'float argument \'{}\' with value {} was of type {}, not of type \'float\''.format(arg_name, val, type(val))

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in INT_RULES, 'rule \'{}\' is unknown for sa_float'.format(rule)
            _checker = INT_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_float


@sa_float('rule_val')
def _float_gte(arg_name, rule_val, func):
    def _check(val):
        assert val >= rule_val, 'float argument \'{}\' with value {} was not greater than or equal to {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_float('rule_val')
def _float_lte(arg_name, rule_val, func):
    def _check(val):
        assert val <= rule_val, 'float argument \'{}\' with value {} was not lesser than or equal to {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_float('rule_val')
def _float_gt(arg_name, rule_val, func):
    def _check(val):
        assert val > rule_val, 'float argument \'{}\' with value {} was not greater than {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_float('rule_val')
def _float_lt(arg_name, rule_val, func):
    def _check(val):
        assert val < rule_val, 'float argument \'{}\' with value {} was not larger than {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_bool('rule_val')
def _float_nonzero(arg_name, rule_val, func):
    def _check(val):
        assert rule_val == False or val != 0, 'float argument \'{}\' with value {} was 0'.format(arg_name, val)
        func(val)

    return _check


@sa_float('rule_val')
def _float_modulo(arg_name, rule_val, func):
    def _check(val):
        assert val % rule_val == 0, 'float argument \'{}\' with value {} was not a multiple of {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


INT_RULES = {
    'gte': _float_gte,
    'lte': _float_lte,
    'gt': _float_gt,
    'lt': _float_lt,
    'non_zero': _float_nonzero,
    'mod': _float_modulo
}
