import inspect
import os

from decorator import decorator


def sa_type(arg_name, **rules):
    """
    Ensures the given parameter is of type type and not None, and abides by all given rules
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in TYPE_RULES, 'rule \'{}\' is unknown for sa_type'.format(rule)
        rule_funcs.append(TYPE_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_type(func, *args, **kw):

        func_spec = inspect.getfullargspec(func)
        args_spec = func_spec.args
        kwargs_spec = func_spec.kwonlyargs
        val = None
        if arg_name in args_spec:
            arg_index = args_spec.index(arg_name)
            val = args[arg_index]
        elif arg_name in kwargs_spec:
            val = kw[arg_name]
        else:
            raise AssertionError('int argument name \'{}\' not found in argument specification'.format(arg_name))

        assert allow_none or val is not None, 'type argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or isinstance(val, type), \
            'type argument \'{}\' with value {} was of type {}, not of type \'type\''.format(arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_type


TYPE_RULES = {
}
