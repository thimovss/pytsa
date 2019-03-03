import tempfile
from os import path, chmod
from unittest import TestCase, mock

import decorator

from pytsa import sa_path
from test.test_utils import test_boolean_parameter


class TestSaPathParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_exists_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'exists')

    def test_rule_is_dir_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'is_dir')

    def test_rule_is_file_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'is_file')

    def test_rule_is_file_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'is_abs')

    def test_rule_can_owner_write_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_owner_write')

    def test_rule_can_group_write_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_group_write')

    def test_rule_can_others_write_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_others_write')

    def test_rule_can_owner_read_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_owner_read')

    def test_rule_can_group_read_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_group_read')

    def test_rule_can_others_read_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_others_read')

    def test_rule_can_owner_execute_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_owner_execute')

    def test_rule_can_group_execute_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_group_execute')

    def test_rule_can_others_execute_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'can_others_execute')


class TestSaPathRules(TestCase):
    # Test that the rules for sa_path works as specified

    def _create_test_file_structure(self):
        """
        Create a simple file structure for testing where group, user and other all have full permissions.
        /temp_dir [777]
            /test.txt [777]
        """
        self.test_dir = tempfile.mkdtemp()
        self.test_file = path.join(self.test_dir, 'test.txt')
        with open(self.test_file, 'w') as f:
            f.write('Temp test.txt file')
            f.close()
        chmod(self.test_dir, 0o0777)
        chmod(self.test_file, 0o0777)

    def test_rule_exists_true(self):
        self._create_test_file_structure()

        @sa_path('a', exists=True)
        def _test(a):
            return a

        # Correct usage
        _test(self.test_dir)
        _test(path.join(self.test_dir, 'test.txt'))

        # Incorrect usage, non existent file
        with self.assertRaises(Exception):
            _test(path.join(self.test_dir, 'non-existent.txt'))

        # Incorrect usage, non existent dir
        with self.assertRaises(Exception):
            _test('/non-existent')

    def test_rule_exists_false(self):
        @sa_path('a', exists=False)
        def _test(a):
            return a

        # Correct usage
        _test('./files')
        _test('./files/')
        _test('./files/test.txt')
        _test('./files/non-existent.txt')

    def test_rule_is_dir_true(self):
        self._create_test_file_structure()

        @sa_path('a', is_dir=True)
        def _test(a):
            return a

        # Correct usage
        _test(self.test_dir)

        # Incorrect usage, is file
        with self.assertRaises(Exception):
            _test(self.test_file)

        # Incorrect usage, non existent dir
        with self.assertRaises(Exception):
            _test('/non-existent')

    def test_rule_is_dir_false(self):
        @sa_path('a', is_dir=False)
        def _test(a):
            return a

        # Correct usage
        _test('.')
        _test('./')
        _test('./files')
        _test('./files/')
        _test('./files/test.txt')
        _test('./non-existent')

    def test_rule_is_file_true(self):
        self._create_test_file_structure()

        @sa_path('a', is_file=True)
        def _test(a):
            return a

        # Correct usage
        _test(self.test_file)

        # Incorrect usage, is dir
        with self.assertRaises(Exception):
            _test(self.test_dir)

        # Incorrect usage, non existent dir
        with self.assertRaises(Exception):
            _test('/non-existent.txt')

    def test_rule_is_file_false(self):
        @sa_path('a', is_file=False)
        def _test(a):
            return a

        # Correct usage
        _test('./files/test.txt')
        _test('./files')
        _test('./non-existent.txt')

    def test_rule_is_abs_true(self):
        @sa_path('a', is_abs=True)
        def _test(a):
            return a

        # Correct usage
        _test('/files/test.txt')
        _test('/non-existent.txt')
        _test('/non-existent/test.txt')

        # Incorrect usage, is not absolute
        with self.assertRaises(Exception):
            _test('./files/test.txt')
        # Incorrect usage, does not exist
        with self.assertRaises(Exception):
            _test('./non-existent.txt')

    def test_rule_is_abs_false(self):
        @sa_path('a', is_abs=False)
        def _test(a):
            return a

        # Correct usage
        _test('/files/test.txt')
        _test('/non-existent.txt')
        _test('/non-existent/test.txt')
        _test('./files/test.txt')
        _test('./non-existent.txt')

    def test_rule_can_owner_write_true(self):
        self._create_test_file_structure()

        @sa_path('a', can_owner_write=True)
        def _test(a):
            return a

        # Correct usage
        _test(self.test_dir)
        _test(self.test_file)

        # Now remove the permissions
        chmod(self.test_dir, 0o0577)
        chmod(self.test_file, 0o0577)

        # Incorrect usage, permission was removed
        with self.assertRaises(Exception):
            _test(self.test_dir)

        # Incorrect usage, permission was removed
        with self.assertRaises(Exception):
            _test(self.test_file)

        # Incorrect usage, non existent file
        with self.assertRaises(Exception):
            _test(path.join(self.test_dir, 'non-existent.txt'))

        # Incorrect usage, non existent dir
        with self.assertRaises(Exception):
            _test('/non-existent')

    def _test_permissions(self, rule, permission_removed_mode):
        self._create_test_file_structure()

        @sa_path('a', **{rule: True})
        def _test(a):
            return a

        # Correct usage
        _test(self.test_dir)
        _test(self.test_file)

        # Now remove the permissions
        chmod(self.test_file, permission_removed_mode)
        chmod(self.test_dir, permission_removed_mode)

        # Incorrect usage, permission was removed
        with self.assertRaises(Exception):
            _test(self.test_dir)

        # Incorrect usage, permission was removed
        with self.assertRaises(Exception):
            _test(self.test_file)

        # Incorrect usage, non existent file
        with self.assertRaises(Exception):
            _test(path.join(self.test_dir, 'non-existent.txt'))

        # Incorrect usage, non existent dir
        with self.assertRaises(Exception):
            _test('/non-existent')

    def test_rule_can_owner_write_true(self):
        self._test_permissions('can_owner_write', 0o0577)

    def test_rule_can_group_write_true(self):
        self._test_permissions('can_group_write', 0o0757)

    def test_rule_can_others_write_true(self):
        self._test_permissions('can_others_write', 0o0775)

    def test_rule_can_owner_read_true(self):
        self._test_permissions('can_owner_read', 0o0377)

    def test_rule_can_group_read_true(self):
        self._test_permissions('can_group_read', 0o0737)

    def test_rule_can_others_read_true(self):
        self._test_permissions('can_others_read', 0o0773)

    def test_rule_can_owner_execute_true(self):
        self._test_permissions('can_owner_execute', 0o0677)

    def test_rule_can_group_execute_true(self):
        self._test_permissions('can_group_execute', 0o0767)

    def test_rule_can_others_execute_true(self):
        self._test_permissions('can_others_execute', 0o0776)

    def test_rule_allow_none_true(self):
        self._create_test_file_structure()

        @sa_path('a', allow_none=True)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test(self.test_dir)
        _test(self.test_file)

    def test_rule_allow_none_false(self):
        self._create_test_file_structure()

        @sa_path('a', allow_none=False)
        def _test(a):
            return a

        # Correct usage
        _test(self.test_dir)
        _test(self.test_file)

        # Incorrect usage, got None
        with self.assertRaises(Exception):
            _test(None)

    def test_rule_allow_none_other_rules(self):
        @sa_path('a', allow_none=True, is_abs=True)
        def _test(a):
            return a

        # Correct
        _test(None)
        _test('/files/test.txt')
        _test('/non-existent.txt')
        _test('/non-existent/test.txt')

        # Incorrect usage, is not absolute
        with self.assertRaises(Exception):
            _test('./files/test.txt')
        # Incorrect usage, does not exist
        with self.assertRaises(Exception):
            _test('./non-existent.txt')


class TestSaPathBase(TestCase):
    # Test that the sa_path works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_path('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_path('b')
            def _test(a):
                return a

            _test('./')

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_path('a', unknown_rule=True)
            def _test(a):
                return a

    def test_global_disable(self):
        # if the environment variable 'PYTSA_DISABLED' is set to True, the decorator should be ignored
        def _test(a):
            return a

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'True'}):
            _test_true = sa_path('a')(_test)
            assert _test_true == _test

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'False'}):
            _test_false = sa_path('a')(_test)
            assert _test_false != _test

        with mock.patch.dict('os.environ', {}):
            _test_false = sa_path('a')(_test)
            assert _test_false != _test

    def test_should_keep_signature(self):
        # After the decorator is applied, the returned function should have the exact same signature as before
        def _test(a, *, b, c=3):
            return a

        _test_signature = sa_path('a')(_test)
        assert decorator.getfullargspec(_test) == decorator.getfullargspec(_test_signature)

    def test_call_with_kwargs(self):
        @sa_path('b')
        def _test(a, *, b, c=0):
            return a

        _test(1, **{'b': './'})
        _test(1, **{'b': './', 'c': 1})

        with self.assertRaises(Exception):
            _test(1, **{'b': 3})
        with self.assertRaises(Exception):
            _test(1, **{'a': 1, 'c': 3})

    def test_use_default_if_none(self):
        # If a default value is specified, and the default is not None, the rules should check the default value

        # No exception should be thrown as the default value 1 is used as no value for a is passed
        @sa_path('a')
        def _test_cwd(a='./'):
            return

        _test_cwd()

        # When it is a required kwarg as well
        @sa_path('b')
        def _test_cwd_kwarg(a, b='./'):
            return

        _test_cwd_kwarg(1.1)

        # Exception should be thrown as the default value None is used and no value for a is passed
        @sa_path('a')
        def _test_none(a=None):
            return

        with self.assertRaises(Exception):
            _test_none()

        # When it is a required kwarg as well
        @sa_path('b')
        def _test_none_kwarg(a, b=None):
            return

        with self.assertRaises(Exception):
            _test_none_kwarg(1.1)

        # Not when allow_none is True
        @sa_path('b', allow_none=True)
        def _test_none_kwarg_allow_none(a, b=None):
            return

        _test_none_kwarg_allow_none(1.1)

    def test_type(self):
        @sa_path('a')
        def _test(a):
            return a

        # correct
        _test('')
        _test('   ')
        _test('completely incorrect path, because on it\'s own it does nothing')

        # not None
        with self.assertRaises(Exception):
            _test(None)
        # not bool
        with self.assertRaises(Exception):
            _test(True)
        # not float
        with self.assertRaises(Exception):
            _test(3.0)
        # not int
        with self.assertRaises(Exception):
            _test(2)
        # not list
        with self.assertRaises(Exception):
            _test([1, 'a'])
        # not type
        with self.assertRaises(Exception):
            _test(str)
