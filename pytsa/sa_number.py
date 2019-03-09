from decimal import Decimal

# @sa_number('rule_val')
from pytsa._base_rule import new_rule


def is_type_number(val):
    return (isinstance(val, int) or isinstance(val, float)) and not isinstance(val, bool)

def is_type_bool(val):
    return isinstance(val, bool)

def _number_gte(arg_name, rule_val):
    assert is_type_number(rule_val)
    def _check(val):
        assert val >= rule_val, 'number argument \'{}\' with value {} was not greater than or equal to {}'.format(
            arg_name,
            val,
            rule_val)

    return _check


def _number_lte(arg_name, rule_val):
    assert is_type_number(rule_val)
    assert is_type_number(rule_val)
    def _check(val):
        assert val <= rule_val, 'number argument \'{}\' with value {} was not lesser than or equal to {}'.format(
            arg_name,
            val,
            rule_val)

    return _check


def _number_gt(arg_name, rule_val):
    assert is_type_number(rule_val)
    def _check(val):
        assert val > rule_val, 'number argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                     rule_val)

    return _check


def _number_lt(arg_name, rule_val):
    assert is_type_number(rule_val)
    def _check(val):
        assert val < rule_val, 'number argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                    rule_val)

    return _check


def _number_nonzero(arg_name, rule_val):
    assert is_type_bool(rule_val)
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert val != 0, 'number argument \'{}\' with value {} was 0'.format(arg_name, val)

    return _check


def _number_modulo(arg_name, rule_val):
    assert is_type_number(rule_val)
    def _check(val):
        assert Decimal(val) % Decimal(rule_val) == Decimal(
            '0.0'), 'number argument \'{}\' with value {} was not a multiple of {}'.format(arg_name,
                                                                                           val,
                                                                                           rule_val)

    return _check


sa_number = new_rule(
    rule_name='sa_number',
    rule_types_name='number',
    rule_rules={
        'gte': _number_gte,
        'lte': _number_lte,
        'gt': _number_gt,
        'lt': _number_lt,
        'non_zero': _number_nonzero,
        'mod': _number_modulo
    },
    type_checker=lambda val: (isinstance(val, int) or isinstance(val, float)) and not isinstance(val, bool)
)
