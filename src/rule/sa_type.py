import inspect
import os

from src.utils import none_checker


def sa_type(arg_name, **rules):
    """
    Ensures the given parameter is of type type and not None, and abides by all given rules
    """

    def _sa_type(func):
        if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
            return func

        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'type argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)

        allow_none = rules.get('allow_none', False)
        rules.pop('allow_none', None)

        def _checker(*args, **kwargs):
            val = args[arg_index]
            assert allow_none or val is not None, 'type argument \'{}\' was None'.format(arg_name)
            assert (allow_none and val is None) or isinstance(val,
                                                              type), 'type argument \'{}\' with value {} was of type {}, not of type \'type\''.format(
                arg_name, val, type(val))
            return func(*args, **kwargs)

        for rule in rules:
            assert rule in TYPE_RULES, 'rule \'{}\' is unknown for sa_type'.format(rule)
            _checker = none_checker(allow_none, TYPE_RULES[rule](arg_name, rules[rule], _checker))

        return _checker

    return _sa_type


TYPE_RULES = {
}
