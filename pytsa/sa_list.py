from pytsa import sa_int, sa_bool, sa_type
from pytsa._base_rule import new_rule


def _format_list(val):
    if len(val) <= 3:
        return str(val)
    return '[{}, {}, {}, ...]'.format(val[0], val[1], val[2])


@sa_int('rule_val')
def _list_len(arg_name, rule_val):
    def _check(val):
        assert len(val) == rule_val, 'list argument \'{}\' with value {} and length of {} was not equal to {}'.format(
            arg_name, _format_list(val), len(val), rule_val)

    return _check


@sa_type('rule_val')
def _list_type(arg_name, rule_val):
    def _check(val):
        for i, v in enumerate(val):
            assert isinstance(v,
                              rule_val), 'list argument \'{}\' with type {} had value with type {} on index {}'.format(
                arg_name, rule_val, type(v), i)

    return _check


@sa_bool('rule_val')
def _list_not_empty(arg_name, rule_val):
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert len(val) != 0, 'list argument \'{}\' was an empty array'.format(arg_name)

    return _check


sa_list = new_rule(
    rule_name='sa_list',
    rule_types_name='list',
    rule_rules={
        'len': _list_len,
        'type': _list_type,
        'not_empty': _list_not_empty,
    },
    type_checker=lambda val: isinstance(val, list)
)
