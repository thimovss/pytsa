import inspect


def sa_bool(arg_name, **rules):
    """
    Ensures the given parameter is of type bool and not None, and abides by all given rules
    """

    def _sa_bool(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'bool argument name \'{arg_name}\' not found in argument specification'

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, f'bool argument \'{arg_name}\' was None'
            assert isinstance(val, bool), f'bool argument \'{arg_name}\' with value {val} was of type {type(val)}, not of type \'bool\''
            return func(*args, **kwargs)

        for rule in rules:
            assert rule in BOOL_RULES, f'rule \'{rule}\' is unknown for sa_bool'
            _checker = BOOL_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_bool

BOOL_RULES = {
}