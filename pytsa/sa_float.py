from pytsa import sa_bool, sa_number
from pytsa._base_rule import new_rule


@sa_number('rule_val')
def _float_gte(arg_name, rule_val):
    def _check(val):
        assert val >= rule_val, 'float argument \'{}\' with value {} was not greater than or equal to {}'.format(
            arg_name, val, rule_val)

    return _check


@sa_number('rule_val')
def _float_lte(arg_name, rule_val):
    def _check(val):
        assert val <= rule_val, 'float argument \'{}\' with value {} was not lesser than or equal to {}'.format(
            arg_name, val, rule_val)

    return _check


@sa_number('rule_val')
def _float_gt(arg_name, rule_val):
    def _check(val):
        assert val > rule_val, 'float argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                    rule_val)

    return _check


@sa_number('rule_val')
def _float_lt(arg_name, rule_val):
    def _check(val):
        assert val < rule_val, 'float argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                                   rule_val)

    return _check


@sa_bool('rule_val')
def _float_nonzero(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert val != 0, 'float argument \'{}\' with value {} was 0'.format(arg_name, val)

    return _check


@sa_number('rule_val')
def _float_modulo(arg_name, rule_val):
    def _check(val):
        assert val % rule_val == 0, 'float argument \'{}\' with value {} was not a multiple of {}'.format(arg_name, val,
                                                                                                          rule_val)

    return _check


sa_float = new_rule(
    rule_name='sa_float',
    rule_types_name='float',
    rule_rules={
        'gte': _float_gte,
        'lte': _float_lte,
        'gt': _float_gt,
        'lt': _float_lt,
        'non_zero': _float_nonzero,
        'mod': _float_modulo
    },
    type_checker=lambda val: isinstance(val, float)
)
