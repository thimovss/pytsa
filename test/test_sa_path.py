from os import path
from unittest import TestCase

from src.pytsa import sa_path
from test.utils import test_boolean_parameter

import tempfile

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


class TestSaPathRules(TestCase):
    # Test that the rules for sa_path works as specified

    def _create_test_file_structure(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = path.join(self.test_dir, 'test.txt')
        with open(self.test_file, 'w') as f:
            f.write('Temp test.txt file')
            f.close()


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

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_path('a', unknown_rule=True)
            def _test(a):
                return a

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
