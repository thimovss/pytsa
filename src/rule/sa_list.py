import inspect


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
                              list), 'list argument \'{}\' with value {} was of type {)}, not of type \'list\''.format(arg_name, val, type(val))
            return func(*args, **kwargs)

        for rule in rules:
            assert rule in LIST_RULES, 'rule \'{}\' is unknown for sa_list'.format(rule)
            _checker = LIST_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_list


LIST_RULES = {
}
