import re

from pytsa import sa_bool
from pytsa._base_rule import new_rule

LOWER_CASE = re.compile('.*[a-z].*')
UPPER_CASE = re.compile('.*[A-Z].*')


def _check_type_string(val):
    if val is None:
        raise ValueError('rule value was None, expected a string')
    if not isinstance(val, str):
        raise TypeError('rule value was of type {} with value {}, expected type string'.format(type(val), val))


@sa_bool('rule_val')
def _string_not_empty(arg_name, rule_val):
    """ensure there is one or more character in the string"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        if len(val) == 0:
            raise ValueError(
                'string argument \'{}\' with value \'{}\' did not contain at least one non-whitespace character'.format(
                    arg_name, val))

    return _check


@sa_bool('rule_val')
def _string_not_blank(arg_name, rule_val):
    """ensure there is one or more non-whitespace characters in the string"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        if len(val) == 0 or val.isspace():
            raise ValueError(
                'string argument \'{}\' with value \'{}\' did not contain at least one character'.format(arg_name, val))

    return _check


def _string_ends_with(arg_name, rule_val):
    """ensure the string ends with the given string"""
    _check_type_string(rule_val)

    def _check(val):
        if not val.endswith(rule_val):
            raise ValueError(
                'string argument \'{}\' with value \'{}\' did not end with \'{}\''.format(arg_name, val, rule_val))

    return _check


def _string_starts_with(arg_name, rule_val):
    """ensure the string starts with the given string"""
    _check_type_string(rule_val)

    def _check(val):
        if not val.startswith(rule_val):
            raise ValueError(
                'string argument \'{}\' with value \'{}\' did not start with \'{}\''.format(arg_name, val, rule_val))

    return _check


def _string_contains(arg_name, rule_val):
    """ensure the string contains the given string at least once"""
    _check_type_string(rule_val)

    def _check(val):
        if val.find(rule_val) == -1:
            raise ValueError(
                'string argument \'{}\' with value \'{}\' did not contain \'{}\''.format(arg_name, val, rule_val))

    return _check


@sa_bool('rule_val')
def _string_is_lower(arg_name, rule_val):
    """ensure all characters in the string are lowercase"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        if UPPER_CASE.match(
                val):
            raise ValueError(
                'not all characters in string argument \'{}\' with value \'{}\' are lowercase'.format(arg_name, val))

    return _check


@sa_bool('rule_val')
def _string_is_upper(arg_name, rule_val):
    """ensure all characters in the string are uppercase"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        if LOWER_CASE.match(
                val):
            raise ValueError(
                'not all characters in string argument \'{}\' with value \'{}\' are uppercase'.format(arg_name, val))

    return _check


def _string_regex(arg_name, rule_val):
    """ensure the string matches the provided regex"""
    _check_type_string(rule_val)
    try:
        compiled_regex = re.compile(rule_val)

        def _check(val):
            if not compiled_regex.search(val):
                raise ValueError(
                    'string argument \'{}\' with value \'{}\' did not match regex \'{}\''.format(arg_name, val,
                                                                                                 rule_val))
    except re.error as err:
        raise ValueError('regex could not compile, got exception: {}'.format(err))

    return _check


sa_string = new_rule(
    rule_name='sa_string',
    rule_types_name='string',
    rule_rules={
        'not_empty': _string_not_empty,
        'not_blank': _string_not_blank,
        'ends_with': _string_ends_with,
        'starts_with': _string_starts_with,
        'contains': _string_contains,
        'is_lower': _string_is_lower,
        'is_upper': _string_is_upper,
        'regex': _string_regex
    },
    type_checker=lambda val: isinstance(val, str)
)
