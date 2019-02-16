import inspect

from src.pytsa import sa_int, sa_bool, sa_type


def _format_list(val):
    if len(val) <= 3:
        return str(val)
    return '[{}, {}, {}, ...]'.format(val[0], val[1], val[2])


def sa_list(arg_name, **rules):
    """
    Ensures the given parameter is of type list and not None, and abides by all given rules
    """

    def _sa_list(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'list argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'list argument \'{}\' was None'.format(arg_name)
            assert isinstance(val,
                              list), 'list argument \'{}\' with value {} was of type {)}, not of type \'list\''.format(
                arg_name, val, type(val))
            return func(*args, **kwargs)

        for rule in rules:
            assert rule in LIST_RULES, 'rule \'{}\' is unknown for sa_list'.format(rule)
            _checker = LIST_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_list


@sa_int('rule_val')
def _list_len(arg_name, rule_val, func):
    def _check(val):
        assert len(val) == rule_val, 'list argument \'{}\' with value {} and length of {} was not equal to {}'.format(
            arg_name, _format_list(val), len(val), rule_val)
        func(val)

    return _check


@sa_type('rule_val')
def _list_type(arg_name, rule_val, func):
    def _check(val):
        for i, v in enumerate(val):
            assert isinstance(v,
                              rule_val), 'list argument \'{}\' with type {} had value with type {} on index {}'.format(
                arg_name, rule_val, type(v), i)
        func(val)

    return _check


@sa_bool('rule_val')
def _list_not_empty(arg_name, rule_val, func):
    if not rule_val:
        return func
    def _check(val):
        assert len(val) != 0, 'list argument \'{}\' was an empty array'.format(arg_name)
        func(val)

    return _check


LIST_RULES = {
    'len': _list_len,
    'type': _list_type,
    'not_empty': _list_not_empty,
}
