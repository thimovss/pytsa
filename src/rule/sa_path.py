import inspect
from os import path

from src.pytsa import sa_bool


def sa_path(arg_name, **rules):
    """
    Ensures the given parameter is of type string and not None, and abides by all given rules
    On its own this rule does nothing, except validate that the argument is a string
    """

    def _sa_path(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'path argument name \'{arg_name}\' not found in argument specification'.format(
            arg_name)

        arg_index = args_spec.index(arg_name)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, 'path argument \'{}\' was None'.format(arg_name)
            assert isinstance(val,
                              str), 'path argument \'{}\' with value \'{}\' was of type {}, not of type \'str\''.format(
                arg_name, val, type(val))

            return func(*args, **kwargs)

        for rule in rules:
            assert rule in PATH_RULES, 'rule \'{}\' is unknown for sa_path'.format(rule)
            _checker = PATH_RULES[rule](arg_name, rules[rule], _checker)

        return _checker

    return _sa_path


@sa_bool('rule_val')
def _path_exists(arg_name, rule_val, func):
    """ensure the path exists, using os.path.exists"""
    if not rule_val:
        return func

    def _check(val):
        assert path.exists(val), 'file did not exist for path argument \'{}\' with value \'{}\''.format(arg_name, val)
        func(val)

    return _check


PATH_RULES = {
    'exists': _path_exists,
}
