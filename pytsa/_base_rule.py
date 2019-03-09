import inspect
import os

from decorator import decorator


def new_rule(rule_name, rule_types_name, rule_rules, type_checker):
    def sa_rule(arg_name, **rules):
        """
        Ensures the given parameter is of type int and not None, and abides by all given rules
        """
        allow_none = rules.get('allow_none', False)
        rules.pop('allow_none', None)

        rule_funcs = []
        for rule in rules:
            assert rule in rule_rules, 'rule \'{}\' is unknown for {}'.format(rule, rule_name)
            rule_funcs.append(rule_rules[rule](arg_name, rules[rule]))

        # If environment variable PYTSA_DISABLED is set, return the original function
        if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
            # Don't use @decorator as it creates a copy of the method with the same signature
            def _a(func):
                return func

            return _a

        @decorator
        def _sa_rule(func, *args, **kw):
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
                raise AssertionError(
                    '{} argument name \'{}\' not found in argument specification'.format(rule_types_name, arg_name))

            if not allow_none:
                assert val is not None, '{} argument \'{}\' was None'.format(rule_types_name, arg_name)

            if val is not None:
                assert type_checker(val), '{} argument \'{}\' with value {} was of type {}, not of type \'{}\'' \
                    .format(rule_types_name, arg_name, val, type(val), rule_types_name)
                for rule_func in rule_funcs:
                    rule_func(val)

            return func(*args, **kw)

        return _sa_rule

    return sa_rule
