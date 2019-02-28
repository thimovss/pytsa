import inspect
import re

from src.pytsa import sa_bool
from src.utils import none_checker

LOWER_CASE = re.compile('.*[a-z].*')
UPPER_CASE = re.compile('.*[A-Z].*')


def sa_string(arg_name, **rules):
    """
    Ensures the given parameter is of type string and not None, and abides by all given rules
    """

    def _sa_string(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'string argument name \'{arg_name}\' not found in argument specification'.format(
            arg_name)

        arg_index = args_spec.index(arg_name)

        allow_none = rules.get('allow_none', False)
        rules.pop('allow_none', None)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert allow_none or val is not None, 'string argument \'{}\' was None'.format(arg_name)
            assert (allow_none and val is None) or isinstance(val,
                                                              str), 'string argument \'{}\' with value \'{}\' was of type {}, not of type \'str\''.format(
                arg_name, val, type(val))

            return func(*args, **kwargs)

        for rule in rules:
            if rule == 'allow_none':
                continue
            assert rule in STRING_RULES, 'rule \'{}\' is unknown for sa_string'.format(rule)
            _checker = none_checker(allow_none, STRING_RULES[rule](arg_name, rules[rule], _checker))

        return _checker

    return _sa_string


@sa_bool('rule_val')
def _string_not_empty(arg_name, rule_val, func):
    """ensure there is one or more character in the string"""
    if not rule_val:
        return func

    def _check(val):
        assert len(val) > 0, \
            'string argument \'{}\' with value \'{}\' did not contain at least one non-whitespace character'.format(
                arg_name, val)
        func(val)

    return _check


@sa_bool('rule_val')
def _string_not_blank(arg_name, rule_val, func):
    """ensure there is one or more non-whitespace characters in the string"""
    if not rule_val:
        return func

    def _check(val):
        assert len(val) > 0 and not val.isspace(), \
            'string argument \'{}\' with value \'{}\' did not contain at least one character'.format(arg_name, val)
        func(val)

    return _check


@sa_string('rule_val')
def _string_ends_with(arg_name, rule_val, func):
    """ensure the string ends with the given string"""

    def _check(val):
        assert val.endswith(rule_val), \
            'string argument \'{}\' with value \'{}\' did not end with \'{}\''.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_string('rule_val')
def _string_starts_with(arg_name, rule_val, func):
    """ensure the string starts with the given string"""

    def _check(val):
        assert val.startswith(rule_val), \
            'string argument \'{}\' with value \'{}\' did not start with \'{}\''.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_string('rule_val')
def _string_contains(arg_name, rule_val, func):
    """ensure the string contains the given string at least once"""

    def _check(val):
        assert val.find(rule_val) != -1, \
            'string argument \'{}\' with value \'{}\' did not contain \'{}\''.format(arg_name, val, rule_val)
        func(val)

    return _check


@sa_bool('rule_val')
def _string_is_lower(arg_name, rule_val, func):
    """ensure all characters in the string are lowercase"""
    if not rule_val:
        return func

    def _check(val):
        assert not UPPER_CASE.match(
            val), 'not all characters in string argument \'{}\' with value \'{}\' are lowercase'.format(arg_name, val)
        func(val)

    return _check


@sa_bool('rule_val')
def _string_is_upper(arg_name, rule_val, func):
    """ensure all characters in the string are uppercase"""
    if not rule_val:
        return func

    def _check(val):
        assert not LOWER_CASE.match(
            val), 'not all characters in string argument \'{}\' with value \'{}\' are uppercase'.format(arg_name, val)
        func(val)

    return _check


@sa_string('rule_val')
def _string_regex(arg_name, rule_val, func):
    """ensure the string matches the provided regex"""
    try:
        compiled_regex = re.compile(rule_val)

        def _check(val):
            assert compiled_regex.search(val), \
                'string argument \'{}\' with value \'{}\' did not match regex \'{}\''.format(arg_name, val, rule_val)
            func(val)
    except re.error as err:
        raise AssertionError('regex could not compile, got exception: {}').format(err)

    return _check


STRING_RULES = {
    'not_empty': _string_not_empty,
    'not_blank': _string_not_blank,
    'ends_with': _string_ends_with,
    'starts_with': _string_starts_with,
    'contains': _string_contains,
    'is_lower': _string_is_lower,
    'is_upper': _string_is_upper,
    'regex': _string_regex
}
