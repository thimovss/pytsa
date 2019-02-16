import inspect


def sa_bool(arg_name, **rules):
    """
    Ensures the given parameter is of type bool and not None, and abides by all given rules
    """

    def _sa_bool(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'bool argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'bool argument \'{}\' was None'.format(arg_name)
            assert isinstance(val,
                              bool), 'bool argument \'{}\' with value {} was of type {)}, not of type \'bool\''.format(arg_name, val, type(val))
            return func(*args, **kwargs)

        for rule in rules:
            assert rule in BOOL_RULES, 'rule \'{}\' is unknown for sa_bool'.format(rule)
            _checker = BOOL_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_bool


BOOL_RULES = {
}
