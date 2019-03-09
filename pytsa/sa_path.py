import os
import stat

from pytsa import sa_bool
from pytsa._base_rule import new_rule


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


sa_path = new_rule(
    rule_name='sa_path',
    rule_types_name='path',
    rule_rules={
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
    },
    type_checker=lambda val: isinstance(val, str)
)
