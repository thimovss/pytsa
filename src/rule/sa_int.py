import inspect


def sa_int(arg_name, **rules):
    """
    Ensures the given parameter is of type int and not None, and abides by all given rules
    """

    def _sa_int(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'int argument name \'{arg_name}\' not found in argument specification'

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, f'int argument \'{arg_name}\' was None'
            assert isinstance(val, int) and not isinstance(val, bool), f'int argument \'{arg_name}\' with value {val} was of type {type(val)}, not of type \'int\''

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in INT_RULES, f'rule \'{rule}\' is unknown for sa_int'
            _checker = INT_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_int


@sa_int('rule_val')
def _int_gte(arg_name, rule_val, func):
    def _check(val):
        assert val >= rule_val, f'int argument \'{arg_name}\' with value {val} was not greater than or equal to {rule_val}'
        func(val)
    return _check


@sa_int('rule_val')
def _int_lte(arg_name, rule_val, func):
    def _check(val):
        assert val <= rule_val, f'int argument \'{arg_name}\' with value {val} was not lesser than or equal to {rule_val}'
        func(val)
    return _check


@sa_int('rule_val')
def _int_gt(arg_name, rule_val, func):
    def _check(val):
        assert val > rule_val, f'int argument \'{arg_name}\' with value {val} was not greater than {rule_val}'
        func(val)
    return _check


@sa_int('rule_val')
def _int_lt(arg_name, rule_val, func):
    def _check(val):
        assert val < rule_val, f'int argument \'{arg_name}\' with value {val} was not larger than {rule_val}'
        func(val)
    return _check

#TODO: sa_bool('rule_var')
def _int_nonzero(arg_name, rule_val, func):
    def _check(val):
        assert rule_val == False or val != 0, f'int argument \'{arg_name}\' with value {val} was 0'
        func(val)
    return _check

@sa_int('rule_val')
def _int_modulo(arg_name, rule_val, func):
    def _check(val):
        assert val % rule_val == 0, f'int argument \'{arg_name}\' with value {val} was not a multiple of {rule_val}'
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
