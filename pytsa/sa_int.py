from pytsa import sa_bool, sa_number
from pytsa._base_rule import new_rule


@sa_number('rule_val')
def _int_gte(arg_name, rule_val):
    def _check(val):
        if val < rule_val:
            raise ValueError('int argument \'{}\' with value {} was not greater than or equal to {}'.format(arg_name,
                                                                                                            val,
                                                                                                            rule_val))

    return _check


@sa_number('rule_val')
def _int_lte(arg_name, rule_val):
    def _check(val):
        if val > rule_val:
            raise ValueError('int argument \'{}\' with value {} was not lesser than or equal to {}'.format(arg_name,
                                                                                                           val,
                                                                                                           rule_val))

    return _check


@sa_number('rule_val')
def _int_gt(arg_name, rule_val):
    def _check(val):
        if val <= rule_val:
            raise ValueError('int argument \'{}\' with value {} was not greater than {}'.format(arg_name, val,
                                                                                                rule_val))

    return _check


@sa_number('rule_val')
def _int_lt(arg_name, rule_val):
    def _check(val):
        if val >= rule_val:
            raise ValueError('int argument \'{}\' with value {} was not larger than {}'.format(arg_name, val,
                                                                                               rule_val))

    return _check


@sa_bool('rule_val')
def _int_nonzero(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        if val == 0:
            raise ValueError('int argument \'{}\' with value {} was 0'.format(arg_name, val))

    return _check


@sa_number('rule_val')
def _int_modulo(arg_name, rule_val):
    def _check(val):
        if val % rule_val != 0:
            raise ValueError('int argument \'{}\' with value {} was not a multiple of {}'.format(arg_name, val,
                                                                                                 rule_val))

    return _check


sa_int = new_rule(
    rule_name='sa_int',
    rule_types_name='int',
    rule_rules={
        'gte': _int_gte,
        'lte': _int_lte,
        'gt': _int_gt,
        'lt': _int_lt,
        'non_zero': _int_nonzero,
        'mod': _int_modulo
    },
    type_checker=lambda val: isinstance(val, int) and not isinstance(val, bool)
)
