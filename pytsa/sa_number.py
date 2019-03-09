from decimal import Decimal

# @sa_number('rule_val')
from pytsa._base_rule import new_rule


def _check_type_number(val):
    if val is None:
        raise ValueError('rule value was None, expected a float or int')
    if isinstance(val, bool) or (not isinstance(val, int) and not isinstance(val, float)):
        raise TypeError(
            'rule value was of type {} with value {}, expected either type float or type int'.format(type(val), val))


def _check_type_bool(val):
    if val is None:
        raise ValueError('rule value was None, expected a bool')
    if not isinstance(val, bool):
        raise TypeError('rule value was of type {} with value {}, expected type bool'.format(type(val), val))


def _number_gte(arg_name, rule_val):
    _check_type_number(rule_val)

    def _check(val):
        if val < rule_val:
            raise ValueError('number argument \'{}\' with value {} was not greater than or equal to {}'.format(
                arg_name,
                val,
                rule_val))

    return _check


def _number_lte(arg_name, rule_val):
    _check_type_number(rule_val)

    def _check(val):
        if val > rule_val:
            raise ValueError('number argument \'{}\' with value {} was not lesser than or equal to {}'.format(
                arg_name,
                val,
                rule_val))

    return _check


def _number_gt(arg_name, rule_val):
    _check_type_number(rule_val)

    def _check(val):
        if val <= rule_val:
            raise ValueError('number argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                   rule_val))

    return _check


def _number_lt(arg_name, rule_val):
    _check_type_number(rule_val)

    def _check(val):
        if val >= rule_val:
            raise ValueError('number argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                  rule_val))

    return _check


def _number_nonzero(arg_name, rule_val):
    _check_type_bool(rule_val)
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        if val == 0:
            raise ValueError('number argument \'{}\' with value {} was 0'.format(arg_name, val))

    return _check


def _number_modulo(arg_name, rule_val):
    _check_type_number(rule_val)

    def _check(val):
        if Decimal(val) % Decimal(rule_val) != Decimal(
                '0.0'):
            raise ValueError('number argument \'{}\' with value {} was not a multiple of {}'.format(arg_name,
                                                                                                    val,
                                                                                                    rule_val))

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
