import inspect


def sa_type(arg_name, **rules):
    """
    Ensures the given parameter is of type type and not None, and abides by all given rules
    """

    def _sa_type(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'type argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'type argument \'{}\' was None'.format(arg_name)
            assert isinstance(val,
                              type), 'type argument \'{}\' with value {} was of type {}, not of type \'type\''.format(
                arg_name, val, type(val))
            return func(*args, **kwargs)

        for rule in rules:
            assert rule in TYPE_RULES, 'rule \'{}\' is unknown for sa_type'.format(rule)
            _checker = TYPE_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_type


TYPE_RULES = {
}
