import inspect
import os

from decorator import decorator


def sa_bool(arg_name, **rules):
    """
    Ensures the given parameter is of type bool and not None, and abides by all given rules
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in BOOL_RULES, 'rule \'{}\' is unknown for sa_bool'.format(rule)
        rule_funcs.append(BOOL_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_bool(func, *args, **kw):

        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, 'bool argument name \'{}\' not found in argument specification'.format(arg_name)

        arg_index = args_spec.index(arg_name)
        val = args[arg_index]

        assert allow_none or val is not None, 'bool argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or isinstance(val, bool), \
            'bool argument \'{}\' with value {} was of type {}, not of type \'bool\''.format(arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_bool


BOOL_RULES = {
}
