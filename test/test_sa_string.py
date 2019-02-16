from unittest import TestCase

from src.pytsa import sa_string
from test.utils import test_boolean_parameter, test_string_parameter


class TestSaStringParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_non_empty_takes_boolean(self):
        test_boolean_parameter(self, sa_string, 'not_empty')

    def test_rule_non_blank_takes_boolean(self):
        test_boolean_parameter(self, sa_string, 'not_blank')

    def test_rule_ends_with_takes_string(self):
        test_string_parameter(self, sa_string, 'ends_with')

    def test_rule_starts_with_takes_string(self):
        test_string_parameter(self, sa_string, 'starts_with')

    def test_rule_contains_takes_string(self):
        test_string_parameter(self, sa_string, 'contains')

    def test_rule_is_lower_takes_boolean(self):
        test_boolean_parameter(self, sa_string, 'is_lower')

    def test_rule_is_upper_takes_boolean(self):
        test_boolean_parameter(self, sa_string, 'is_upper')


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

    def test_rule_starts_with(self):
        @sa_string('a', starts_with='ab')
        def _test(a):
            return a

        # Correct usage
        _test('abc')
        _test('ab123')
        _test('ab')
        _test('ab \n ')

        # Incorrect usage, doesn't start with 'bc'
        with self.assertRaises(Exception):
            _test('1ab')
        with self.assertRaises(Exception):
            _test('')

    def test_rule_contains(self):
        @sa_string('a', contains='ab')
        def _test(a):
            return a

        # Correct usage
        _test('abcd')
        _test('12ab34')
        _test('ab')
        _test('\n \t ab \n ')

        # Incorrect usage, doesn't contain 'bc'
        with self.assertRaises(Exception):
            _test('a1b')
        with self.assertRaises(Exception):
            _test('a b')
        with self.assertRaises(Exception):
            _test('')

    def test_rule_is_lower_true(self):
        @sa_string('a', is_lower=True)
        def _test(a):
            return a

        # Correct usage
        _test('abcd')
        _test('12ab34')
        _test('ab')
        _test('\n \t ab \n ')
        _test(' ')
        _test('')
        _test(' ! ')

        # Incorrect usage, doesn't end with 'bc'
        with self.assertRaises(Exception):
            _test('ABC')
        with self.assertRaises(Exception):
            _test('A')
        with self.assertRaises(Exception):
            _test('aBc')

    def test_rule_is_lower_false(self):
        @sa_string('a', is_lower=False)
        def _test(a):
            return a

        # Correct usage
        _test('abcd')
        _test('12ab34')
        _test('ab')
        _test('\n \t ab \n ')
        _test('')
        _test(' ')
        _test('ABC')
        _test('A')
        _test('aBc')
        _test(' ! ')

    def test_rule_is_upper_true(self):
        @sa_string('a', is_upper=True)
        def _test(a):
            return a

        # Correct usage
        _test('ABCD')
        _test('12AB34')
        _test('AB')
        _test('\n \t AB \n ')
        _test('')
        _test(' ')
        _test(' ! ')

        # Incorrect usage, doesn't end with 'bc'
        with self.assertRaises(Exception):
            _test('abc')
        with self.assertRaises(Exception):
            _test('a')
        with self.assertRaises(Exception):
            _test('AbC')

    def test_rule_is_upper_false(self):
        @sa_string('a', is_upper=False)
        def _test(a):
            return a

        # Correct usage
        _test('ABCD')
        _test('12AB34')
        _test('AB')
        _test('\n \t AB \n ')
        _test('')
        _test(' ')
        _test('abc')
        _test('a')
        _test('AbC')
        _test(' ! ')

    def test_rule_regex(self):
        @sa_string('a', regex='test[12]')
        def _test(a):
            return a

        # Correct usage
        _test('test1')
        _test('test2')

        # Incorrect usage, doesn't match regex
        with self.assertRaises(Exception):
            _test('test3')

    def test_rule_regex_incorrect(self):
        # incorrect regex should raise exception
        with self.assertRaises(Exception):
            @sa_string('a', regex='[')
            def _test(a):
                return a


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

class TestSaStringMultipleRules(TestCase):

    def test_multiple_rules_case1(self):
        @sa_string('a', starts_with='a', ends_with='c', is_lower=True, contains='1')
        def _test(a):
            return a

        correct_strings = ['a1c', 'abc123defc', 'a  1  c']
        incorrect_strings = ['a1Vc', ' ', 'c1a', 'A1C', ' a1c', 'a1c ']

        # correct strings should not throw exception
        for correct_string in correct_strings:
            _test(correct_string)

        # incorrect strings should all throw exception
        for incorrect_string in incorrect_strings:
            with self.assertRaises(Exception):
                _test(incorrect_string)

    def test_multiple_rules_case2(self):
        @sa_string('a', is_upper=True, is_lower=False, not_blank=True)
        def _test(a):
            return a

        correct_strings = ['A', ' BC', '\tD\n!B']
        incorrect_strings = [' ', 'AbC', '', '\t\n']

        # correct strings should not throw exception
        for correct_string in correct_strings:
            _test(correct_string)

        # incorrect strings should all throw exception
        for incorrect_string in incorrect_strings:
            with self.assertRaises(Exception):
                _test(incorrect_string)

    def test_multiple_rules_case3(self):
        @sa_string('a', is_upper=True, ends_with='\t', not_blank=True)
        def _test(a):
            return a

        correct_strings = [' !\t', 'A\t']
        incorrect_strings = ['', '  ', 'AbC', '\t', '\t\n']

        # correct strings should not throw exception
        for correct_string in correct_strings:
            _test(correct_string)

        # incorrect strings should all throw exception
        for incorrect_string in incorrect_strings:
            with self.assertRaises(Exception):
                _test(incorrect_string)
