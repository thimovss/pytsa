import inspect
import re

from src.strictargs import sa_bool

LOWER_CASE = re.compile('.*[a-z].*')
UPPER_CASE = re.compile('.*[A-Z].*')


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
            assert isinstance(val,
                              str), f'string argument \'{arg_name}\' with value \'{val}\' was of type {type(val)}, not of type \'str\''

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
        assert not rule_val or len(val) > 0, \
            f'string argument \'{arg_name}\' with value \'{val}\' did not contain at least one non-whitespace character'
        func(val)

    return _check


@sa_bool('rule_val')
def _string_not_blank(arg_name, rule_val, func):
    """ensure there is one or more non-whitespace characters in the string"""

    def _check(val):
        assert not rule_val or (len(val) > 0 and not val.isspace()), \
            f'string argument \'{arg_name}\' with value \'{val}\' did not contain at least one character'
        func(val)

    return _check


@sa_string('rule_val')
def _string_ends_with(arg_name, rule_val, func):
    """ensure the string ends with the given string"""

    def _check(val):
        assert val.endswith(rule_val), \
            f'string argument \'{arg_name}\' with value \'{val}\' did not end with \'{rule_val}\''
        func(val)

    return _check


@sa_string('rule_val')
def _string_starts_with(arg_name, rule_val, func):
    """ensure the string starts with the given string"""

    def _check(val):
        assert val.startswith(rule_val), \
            f'string argument \'{arg_name}\' with value \'{val}\' did not start with \'{rule_val}\''
        func(val)

    return _check


@sa_string('rule_val')
def _string_contains(arg_name, rule_val, func):
    """ensure the string contains the given string at least once"""

    def _check(val):
        assert val.find(rule_val) != -1, \
            f'string argument \'{arg_name}\' with value \'{val}\' did not contain \'{rule_val}\''
        func(val)

    return _check


@sa_bool('rule_val')
def _string_is_lower(arg_name, rule_val, func):
    """ensure all characters in the string are lowercase"""

    def _check(val):
        assert not rule_val or not UPPER_CASE.match(
            val), f'not all characters in string argument \'{arg_name}\' with value \'{val}\' are lowercase'
        func(val)

    return _check


@sa_bool('rule_val')
def _string_is_upper(arg_name, rule_val, func):
    """ensure all characters in the string are uppercase"""

    def _check(val):
        assert not rule_val or not LOWER_CASE.match(
            val), f'not all characters in string argument \'{arg_name}\' with value \'{val}\' are uppercase'
        func(val)

    return _check


STRING_RULES = {
    'not_empty': _string_not_empty,
    'not_blank': _string_not_blank,
    'ends_with': _string_ends_with,
    'starts_with': _string_starts_with,
    'contains': _string_contains,
    'is_lower': _string_is_lower,
    'is_upper': _string_is_upper
}
