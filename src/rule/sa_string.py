import inspect

from src.strictargs import sa_bool


def sa_string(arg_name, **rules):
    """
    Ensures the given parameter is of type string and not None, and abides by all given rules
    """

    def _sa_string(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'string argument name \'{arg_name}\' not found in argument specification'

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, f'string argument \'{arg_name}\' was None'
            assert isinstance(val, str), f'string argument \'{arg_name}\' with value \'{val}\' was of type {type(val)}, not of type \'str\''

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in STRING_RULES, f'rule \'{rule}\' is unknown for sa_string'
            _checker = STRING_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_string

@sa_bool('rule_val')
def _string_not_empty(arg_name, rule_val, func):
    """ensure there is one or more character in the string"""
    def _check(val):
        assert not rule_val or len(val) > 0,\
            f'string argument \'{arg_name}\' with value \'{val}\' did not contain at least one non-whitespace character'
        func(val)
    return _check

@sa_bool('rule_val')
def _string_not_blank(arg_name, rule_val, func):
    """ensure there is one or more non-whitespace characters in the string"""
    def _check(val):
        print(val.isspace(), val)
        assert not rule_val or (len(val) > 0 and not val.isspace()),\
            f'string argument \'{arg_name}\' with value \'{val}\' did not contain at least one character'
        func(val)
    return _check


STRING_RULES = {
    'not_empty': _string_not_empty,
    'not_blank': _string_not_blank
}