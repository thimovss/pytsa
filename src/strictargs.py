import inspect

def _num_gte(arg_name, rule_val, val):
    assert val >= rule_val, f'argument \'{arg_name}\' with value {val} was not greater than or equal to {rule_val}'

NUM_RULES = {
    'gte': _num_gte
}

def sa_num(arg_name, **rules):
    """
    Ensures the given parameter is of type number and not None
    """
    def _sa_num(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'argument name \'{arg_name}\' not found in argument specification'
        #TODO: bake all rule checking into one method
        for rule in rules:
            assert rule in NUM_RULES, f'rule \'{rule}\' is unknown for sa_num'

        arg_index = args_spec.index(arg_name)
        def wrapper(*args, **kwargs):
            # print(func, inspect.getfullargspec(func), args, kwargs)
            for rule in rules:
                NUM_RULES[rule](arg_name, rules[rule], args[arg_index])
            return func(*args, **kwargs)

        return wrapper
    return _sa_num