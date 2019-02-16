import inspect

from src.pytsa import sa_bool


def sa_int(arg_name, **rules):
    """
    Ensures the given parameter is of type int and not None, and abides by all given rules
    """

    def _sa_int(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'int argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'int argument \'{}\' was None'.format(arg_name)
            assert isinstance(val, int) and not isinstance(val,
                                                           bool), 'int argument \'{}\' with value {} was of type {}, not of type \'int\''.format(arg_name, val, type(val))

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in INT_RULES, 'rule \'{}\' is unknown for sa_int'.format(rule)
            _checker = INT_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_int


@sa_int('rule_val')
def _int_gte(arg_name, rule_val, func):
    def _check(val):
        assert val >= rule_val, 'int argument \'{}\' with value {} was not greater than or equal to {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_int('rule_val')
def _int_lte(arg_name, rule_val, func):
    def _check(val):
        assert val <= rule_val, 'int argument \'{}\' with value {} was not lesser than or equal to {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_int('rule_val')
def _int_gt(arg_name, rule_val, func):
    def _check(val):
        assert val > rule_val, 'int argument \'{}\' with value {} was not greater than {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_int('rule_val')
def _int_lt(arg_name, rule_val, func):
    def _check(val):
        assert val < rule_val, 'int argument \'{}\' with value {} was not larger than {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_bool('rule_val')
def _int_nonzero(arg_name, rule_val, func):
    def _check(val):
        assert rule_val == False or val != 0, 'int argument \'{}\' with value {} was 0'.format(arg_name, val)
        func(val)

    return _check


@sa_int('rule_val')
def _int_modulo(arg_name, rule_val, func):
    def _check(val):
        assert val % rule_val == 0, 'int argument \'{}\' with value {} was not a multiple of {}'.format(arg_name, val, rule_val)
        func(val)

    return _check


INT_RULES = {
    'gte': _int_gte,
    'lte': _int_lte,
    'gt': _int_gt,
    'lt': _int_lt,
    'non_zero': _int_nonzero,
    'mod': _int_modulo
}
