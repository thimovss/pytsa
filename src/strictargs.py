import inspect

def _int_gte(arg_name, rule_val, val):
    assert val >= rule_val, f'int argument \'{arg_name}\' with value {val} was not greater than or equal to {rule_val}'

INT_RULES = {
    'gte': _int_gte
}

def sa_int(arg_name, **rules):
    """
    Ensures the given parameter is of type int and not None
    """
    def _sa_int(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'int argument name \'{arg_name}\' not found in argument specification'
        #TODO: bake all rule checking into one method
        #TODO: check if the rule values passed are correct, not None or type other than int
        for rule in rules:
            assert rule in INT_RULES, f'rule \'{rule}\' is unknown for sa_int'

        arg_index = args_spec.index(arg_name)
        def wrapper(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, f'int argument \'{arg_name}\' with value {val} was None'
            assert isinstance(val, int), f'int argument \'{arg_name}\' with value {val} was of type {type(val)}, not of type \'int\''
            for rule in rules:
                INT_RULES[rule](arg_name, rules[rule], val)
            return func(*args, **kwargs)

        return wrapper
    return _sa_int


def _float_gte(arg_name, rule_val, val):
    assert val >= rule_val, f'float argument \'{arg_name}\' with value {val} was not greater than or equal to {rule_val}'

FLOAT_RULES = {
    'gte': _float_gte
}

def sa_float(arg_name, **rules):
    """
    Ensures the given parameter is of type float and not None
    """
    def _sa_float(func):
        args_spec = inspect.getfullargspec(func).args
        assert arg_name in args_spec, f'float argument name \'{arg_name}\' not found in argument specification'
        #TODO: bake all rule checking into one method
        #TODO: check if the rule values passed are correct, not None or type other than int
        for rule in rules:
            assert rule in FLOAT_RULES, f'rule \'{rule}\' is unknown for sa_float'

        arg_index = args_spec.index(arg_name)
        def wrapper(*args, **kwargs):
            val = args[arg_index]
            assert val is not None, f'float argument \'{arg_name}\' with value {val} was None'
            assert isinstance(val, float), f'float argument \'{arg_name}\' with value {val} was of type {type(val)}, not of type \'float\''
            for rule in rules:
                FLOAT_RULES[rule](arg_name, rules[rule], val)
            return func(*args, **kwargs)

        return wrapper
    return _sa_float

#TODO:
# sa_float
# sa_number
# sa_string
# sa_unicode
# sa_text
# split into modules
# more useful rules
