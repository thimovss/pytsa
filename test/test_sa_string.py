from unittest import TestCase

from src.strictargs import sa_string
from test.utils import test_boolean_parameter, test_string_parameter


class TestSaStringParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_non_empty_takes_boolean(self):
        test_boolean_parameter(self, sa_string, 'not_empty')

    def test_rule_non_blank_takes_boolean(self):
        test_boolean_parameter(self, sa_string, 'not_blank')

    def test_rule_ends_with_takes_string(self):
        test_string_parameter(self, sa_string, 'ends_with')


class TestSaStringRules(TestCase):
    # Test that the rules for sa_string works as specified

    def test_rule_not_empty_true(self):
        @sa_string('a', not_empty=True)
        def _test(a):
            return a

        # Correct usage
        _test('a')
        _test('123')
        _test(' ')

        # Incorrect usage, no characters in string
        with self.assertRaises(Exception):
            _test('')


    def test_rule_not_empty_false(self):
        @sa_string('a', not_empty=False)
        def _test(a):
            return a
        _test('a')
        _test('123')
        _test(' ')
        _test('')

    def test_rule_not_blank_true(self):
        @sa_string('a', not_blank=True)
        def _test(a):
            return a

        # Correct usage
        _test('a')
        _test('123')

        # Incorrect usage, no characters in string
        with self.assertRaises(Exception):
            _test('')

        # Incorrect usage, whitespace characters in string
        with self.assertRaises(Exception):
            _test(' ')
        with self.assertRaises(Exception):
            _test('\t')
        with self.assertRaises(Exception):
            _test('\t \n  ')


    def test_rule_not_blank_false(self):
        @sa_string('a', not_blank=False)
        def _test(a):
            return a
        _test('a')
        _test('123')
        _test('')
        _test(' ')
        _test('\t')
        _test('\t \n  ')

    def test_rule_ends_with(self):
        @sa_string('a', ends_with='bc')
        def _test(a):
            return a

        # Correct usage
        _test('abc')
        _test('123bc')
        _test('bc')
        _test(' \n bc')

        # Incorrect usage, doesn't end with 'bc'
        with self.assertRaises(Exception):
            _test('abcd')
        with self.assertRaises(Exception):
            _test('')


class TestSaStringBase(TestCase):
    # Test that the sa_string works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_string('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_string('b')
            def _test(a):
                return a

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_string('a', unknown_rule=True)
            def _test(a):
                return a

    def test_type(self):
        @sa_string('a')
        def _test(a):
            return a

        # correct
        _test('abc')
        _test('')
        _test('   ')
        _test('\n')

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
