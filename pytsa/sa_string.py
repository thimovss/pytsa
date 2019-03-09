import re

from pytsa import sa_bool
from pytsa._base_rule import new_rule

LOWER_CASE = re.compile('.*[a-z].*')
UPPER_CASE = re.compile('.*[A-Z].*')

def is_type_string(val):
    return isinstance(val, str)

@sa_bool('rule_val')
def _string_not_empty(arg_name, rule_val):
    """ensure there is one or more character in the string"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert len(val) > 0, \
            'string argument \'{}\' with value \'{}\' did not contain at least one non-whitespace character'.format(
                arg_name, val)

    return _check


@sa_bool('rule_val')
def _string_not_blank(arg_name, rule_val):
    """ensure there is one or more non-whitespace characters in the string"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert len(val) > 0 and not val.isspace(), \
            'string argument \'{}\' with value \'{}\' did not contain at least one character'.format(arg_name, val)

    return _check


def _string_ends_with(arg_name, rule_val):
    """ensure the string ends with the given string"""
    assert is_type_string(rule_val)

    def _check(val):
        assert val.endswith(rule_val), \
            'string argument \'{}\' with value \'{}\' did not end with \'{}\''.format(arg_name, val, rule_val)

    return _check


def _string_starts_with(arg_name, rule_val):
    assert is_type_string(rule_val)
    """ensure the string starts with the given string"""

    def _check(val):
        assert val.startswith(rule_val), \
            'string argument \'{}\' with value \'{}\' did not start with \'{}\''.format(arg_name, val, rule_val)

    return _check


def _string_contains(arg_name, rule_val):
    """ensure the string contains the given string at least once"""
    assert is_type_string(rule_val)

    def _check(val):
        assert val.find(rule_val) != -1, \
            'string argument \'{}\' with value \'{}\' did not contain \'{}\''.format(arg_name, val, rule_val)

    return _check


@sa_bool('rule_val')
def _string_is_lower(arg_name, rule_val):
    """ensure all characters in the string are lowercase"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert not UPPER_CASE.match(
            val), 'not all characters in string argument \'{}\' with value \'{}\' are lowercase'.format(arg_name, val)

    return _check


@sa_bool('rule_val')
def _string_is_upper(arg_name, rule_val):
    """ensure all characters in the string are uppercase"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert not LOWER_CASE.match(
            val), 'not all characters in string argument \'{}\' with value \'{}\' are uppercase'.format(arg_name, val)

    return _check


def _string_regex(arg_name, rule_val):
    """ensure the string matches the provided regex"""
    assert is_type_string(rule_val)
    try:
        compiled_regex = re.compile(rule_val)

        def _check(val):
            assert compiled_regex.search(val), \
                'string argument \'{}\' with value \'{}\' did not match regex \'{}\''.format(arg_name, val, rule_val)
    except re.error as err:
        raise AssertionError('regex could not compile, got exception: {}').format(err)

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
