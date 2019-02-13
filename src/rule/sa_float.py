import inspect
from src.strictargs import sa_bool

def sa_float(arg_name, **rules):
    """
    Ensures the given parameter is of type float and not None, and abides by all given rules
    """

    def _sa_float(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'float argument name \'{arg_name}\' not found in argument specification'

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, f'float argument \'{arg_name}\' was None'
            assert isinstance(val,
                              float), f'float argument \'{arg_name}\' with value {val} was of type {type(val)}, not of type \'float\''

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in INT_RULES, f'rule \'{rule}\' is unknown for sa_float'
            _checker = INT_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_float


@sa_float('rule_val')
def _float_gte(arg_name, rule_val, func):
    def _check(val):
        assert val >= rule_val, f'float argument \'{arg_name}\' with value {val} was not greater than or equal to {rule_val}'
        func(val)
    return _check


@sa_float('rule_val')
def _float_lte(arg_name, rule_val, func):
    def _check(val):
        assert val <= rule_val, f'float argument \'{arg_name}\' with value {val} was not lesser than or equal to {rule_val}'
        func(val)
    return _check


@sa_float('rule_val')
def _float_gt(arg_name, rule_val, func):
    def _check(val):
        assert val > rule_val, f'float argument \'{arg_name}\' with value {val} was not greater than {rule_val}'
        func(val)
    return _check


@sa_float('rule_val')
def _float_lt(arg_name, rule_val, func):
    def _check(val):
        assert val < rule_val, f'float argument \'{arg_name}\' with value {val} was not larger than {rule_val}'
        func(val)
    return _check


@sa_bool('rule_val')
def _float_nonzero(arg_name, rule_val, func):
    def _check(val):
        assert rule_val == False or val != 0, f'float argument \'{arg_name}\' with value {val} was 0'
        func(val)
    return _check

@sa_float('rule_val')
def _float_modulo(arg_name, rule_val, func):
    def _check(val):
        assert val % rule_val == 0, f'float argument \'{arg_name}\' with value {val} was not a multiple of {rule_val}'
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
