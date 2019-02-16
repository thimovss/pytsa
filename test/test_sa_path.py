from unittest import TestCase

from src.pytsa import sa_path
from test.utils import test_boolean_parameter


class TestSaPathParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_exists_takes_boolean(self):
        test_boolean_parameter(self, sa_path, 'exists')


class TestSaPathRules(TestCase):
    # Test that the rules for sa_path works as specified

    def test_rule_exists_true(self):
        @sa_path('a', exists=True)
        def _test(a):
            return a

        # Correct usage
        _test('./files')
        _test('./files/')
        _test('./files/test.txt')

        # Incorrect usage
        with self.assertRaises(Exception):
            _test('/files')
        with self.assertRaises(Exception):
            _test('/files/')
        with self.assertRaises(Exception):
            _test('/files/non-existent.txt')

    def test_rule_exists_false(self):
        @sa_path('a', exists=False)
        def _test(a):
            return a

        # Correct usage
        _test('./files')
        _test('./files/')
        _test('./files/test.txt')
        _test('/files')
        _test('/files/')
        _test('/files/non-existent.txt')


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
