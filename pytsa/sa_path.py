import inspect
import os
import stat

from decorator import decorator

from pytsa import sa_bool


def sa_path(arg_name, **rules):
    """
    Ensures the given parameter is of type string and not None, and abides by all given rules
    On its own this rule does nothing, except validate that the argument is a string
    """
    allow_none = rules.get('allow_none', False)
    rules.pop('allow_none', None)

    rule_funcs = []
    for rule in rules:
        assert rule in PATH_RULES, 'rule \'{}\' is unknown for sa_path'.format(rule)
        rule_funcs.append(PATH_RULES[rule](arg_name, rules[rule]))

    # If environment variable PYTSA_DISABLED is set, return the original function
    if os.environ.get('PYTSA_DISABLED', 'False') == 'True':
        # Don't use @decorator as it creates a copy of the method with the same signature
        def _a(func):
            return func

        return _a

    @decorator
    def _sa_path(func, *args, **kw):

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

        assert allow_none or val is not None, 'path argument \'{}\' was None'.format(arg_name)
        assert (allow_none and val is None) or isinstance(val,
                                                          str), 'path argument \'{}\' with value \'{}\' was of type {}, not of type \'str\''.format(
            arg_name, val, type(val))

        if val is not None:
            for rule_func in rule_funcs:
                rule_func(val)

        return func(*args, **kw)

    return _sa_path


@sa_bool('rule_val')
def _path_exists(arg_name, rule_val):
    """ensure the path exists, using os.path.exists"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert os.path.exists(val), 'path argument \'{}\' with value \'{}\' did not exist'.format(arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_is_dir(arg_name, rule_val):
    """ensure the path is a directory, using os.path.isdir"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert os.path.isdir(val), 'path argument \'{}\' with value \'{}\' was not a directory'.format(arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_is_file(arg_name, rule_val):
    """ensure the path is a file, using os.path.isfile"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert os.path.isfile(val), 'path argument \'{}\' with value \'{}\' was not a file'.format(arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_is_abs(arg_name, rule_val):
    """ensure the path is an absolute pathname, using os.path.isabs"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert os.path.isabs(val), 'path argument \'{}\' with value \'{}\' was not absolute'.format(arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_owner_write(arg_name, rule_val):
    """ensure the path has permission for owner to write using stat.S_IWUSR"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IWUSR), 'path argument \'{}\' with value \'{}\' was not writeable for owner'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_group_write(arg_name, rule_val):
    """ensure the path has permission for group to write using stat.S_IWGRP"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IWGRP), 'path argument \'{}\' with value \'{}\' was not writeable for group'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_others_write(arg_name, rule_val):
    """ensure the path has permission for others to write using stat.S_IWOTH"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IWOTH), 'path argument \'{}\' with value \'{}\' was not writeable for others'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_owner_read(arg_name, rule_val):
    """ensure the path has permission for owner to read using stat.S_IRUSR"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IRUSR), 'path argument \'{}\' with value \'{}\' was not readable for owner'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_group_read(arg_name, rule_val):
    """ensure the path has permission for group to read using stat.S_IRGRP"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IRGRP), 'path argument \'{}\' with value \'{}\' was not readable for group'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_others_read(arg_name, rule_val):
    """ensure the path has permission for others to read using stat.S_IROTH"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IROTH), 'path argument \'{}\' with value \'{}\' was not readable for others'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_owner_execute(arg_name, rule_val):
    """ensure the path has permission for owner to execute using stat.S_IXUSR"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IXUSR), 'path argument \'{}\' with value \'{}\' was not executeable for owner'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_group_execute(arg_name, rule_val):
    """ensure the path has permission for group to execute using stat.S_IXGRP"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IXGRP), 'path argument \'{}\' with value \'{}\' was not executeable for group'.format(
            arg_name, val)

    return _check


@sa_bool('rule_val')
def _path_can_others_execute(arg_name, rule_val):
    """ensure the path has permission for others to execute using stat.S_IXOTH"""
    if not rule_val:
        def _check(val):
            return

        return _check

    def _check(val):
        assert bool(os.stat(
            val).st_mode & stat.S_IXOTH), 'path argument \'{}\' with value \'{}\' was not executeable for others'.format(
            arg_name, val)

    return _check


PATH_RULES = {
    'exists': _path_exists,
    'is_dir': _path_is_dir,
    'is_file': _path_is_file,
    'is_abs': _path_is_abs,
    'can_owner_write': _path_can_owner_write,
    'can_group_write': _path_can_group_write,
    'can_others_write': _path_can_others_write,
    'can_owner_read': _path_can_owner_read,
    'can_group_read': _path_can_group_read,
    'can_others_read': _path_can_others_read,
    'can_owner_execute': _path_can_owner_execute,
    'can_group_execute': _path_can_group_execute,
    'can_others_execute': _path_can_others_execute,
}
