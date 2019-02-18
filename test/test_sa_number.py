from unittest import TestCase

from src.pytsa import sa_number
from test.utils import test_number_parameter, test_boolean_parameter


class TestSaNumberParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_lte_takes_number(self):
        test_number_parameter(self, sa_number, 'lte')

    def test_rule_gte_takes_number(self):
        test_number_parameter(self, sa_number, 'gte')

    def test_rule_gt_takes_number(self):
        test_number_parameter(self, sa_number, 'gt')

    def test_rule_lt_takes_number(self):
        test_number_parameter(self, sa_number, 'lt')

    def test_rule_mod_takes_number(self):
        test_number_parameter(self, sa_number, 'mod')

    def test_rule_non_zero_takes_boolean(self):
        test_boolean_parameter(self, sa_number, 'non_zero')


class TestSaNumberRules(TestCase):
    # Test that the rules for sa_number works as specified

    def test_rule_gte_int(self):
        @sa_number('a', gte=2)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(2)
        _test(3.0)
        _test(2.0)

        # Incorrect usage, number lower than value
        with self.assertRaises(Exception):
            _test(1)
        with self.assertRaises(Exception):
            _test(1.1)

    def test_rule_gte_float(self):
        @sa_number('a', gte=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(2)
        _test(3.0)
        _test(2.0)

        # Incorrect usage, number lower than value
        with self.assertRaises(Exception):
            _test(1)
        with self.assertRaises(Exception):
            _test(1.1)

    def test_rule_lte_int(self):
        @sa_number('a', lte=2)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(2)
        _test(1.0)
        _test(2.0)

        # Incorrect usage, number lower than value
        with self.assertRaises(Exception):
            _test(3)
            _test(3.3)

    def test_rule_lte_int(self):
        @sa_number('a', lte=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(2)
        _test(1.0)
        _test(2.0)

        # Incorrect usage, number lower than value
        with self.assertRaises(Exception):
            _test(3)
            _test(3.3)

    def test_rule_gt_int(self):
        @sa_number('a', gt=2)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(4)
        _test(3.0)
        _test(4.0)

        # Incorrect usage, number lower than value
        with self.assertRaises(Exception):
            _test(1)
        with self.assertRaises(Exception):
            _test(1.0)
        # Incorrect usage, number equal to value
        with self.assertRaises(Exception):
            _test(2)
        with self.assertRaises(Exception):
            _test(2.0)

    def test_rule_gt_float(self):
        @sa_number('a', gt=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(4)
        _test(3.0)
        _test(4.0)

        # Incorrect usage, number lower than value
        with self.assertRaises(Exception):
            _test(1)
        with self.assertRaises(Exception):
            _test(1.0)
        # Incorrect usage, number equal to value
        with self.assertRaises(Exception):
            _test(2)
        with self.assertRaises(Exception):
            _test(2.0)

    def test_rule_lt_int(self):
        @sa_number('a', lt=2)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(1)
        _test(0.0)
        _test(1.0)

        # Incorrect usage, number higher than value
        with self.assertRaises(Exception):
            _test(3)
        with self.assertRaises(Exception):
            _test(3.0)
        # Incorrect usage, number equal to value
        with self.assertRaises(Exception):
            _test(2)
        with self.assertRaises(Exception):
            _test(2.0)

    def test_rule_lt_float(self):
        @sa_number('a', lt=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(1)
        _test(0.0)
        _test(1.0)

        # Incorrect usage, number higher than value
        with self.assertRaises(Exception):
            _test(3)
        with self.assertRaises(Exception):
            _test(3.0)
        # Incorrect usage, number equal to value
        with self.assertRaises(Exception):
            _test(2)
        with self.assertRaises(Exception):
            _test(2.0)

    def test_rule_non_zero_true(self):
        @sa_number('a', non_zero=True)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(-1)

        # Incorrect usage, is 0
        with self.assertRaises(Exception):
            _test(0)

        # Incorrect usage, float given instead of number
        with self.assertRaises(Exception):
            _test(0.0)

    def test_rule_non_zero_false(self):
        @sa_number('a', non_zero=False)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(0)
        _test(-1)

    def test_rule_mod_int(self):
        @sa_number('a', mod=2)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(2)
        _test(4)
        _test(-2)
        _test(0.0)
        _test(0.5)
        _test(2.0)
        _test(4.0)
        _test(-2.0)

        # Incorrect usage, 3 % 2 results in 1
        with self.assertRaises(Exception):
            _test(3)
        with self.assertRaises(Exception):
            _test(3.0)

    def test_rule_mod_float(self):
        @sa_number('a', mod=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(2)
        _test(4)
        _test(-2)
        _test(0.0)
        _test(0.5)
        _test(2.0)
        _test(4.0)
        _test(-2.0)

        # Incorrect usage, 3 % 2 results in 1
        with self.assertRaises(Exception):
            _test(3)
        with self.assertRaises(Exception):
            _test(3.0)


class TestSaNumberBase(TestCase):
    # Test that the sa_number works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_number('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_number('b')
            def _test(a):
                return a

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_number('a', unknown_rule=True)
            def _test(a):
                return a

    def test_type(self):
        @sa_number('a')
        def _test(a):
            return a

        # correct
        _test(1)
        _test(0)
        _test(-1)
        _test(1.1)
        _test(0.0)
        _test(-1.1)

        # not None
        with self.assertRaises(Exception):
            _test(None)
        # not bool
        with self.assertRaises(Exception):
            _test(True)
        # not string
        with self.assertRaises(Exception):
            _test('abc')
        # not list
        with self.assertRaises(Exception):
            _test([1, 'a'])
        # not type
        with self.assertRaises(Exception):
            _test(int)


class TestSaNumberMultipleRules(TestCase):

    def test_multiple_rules_case1(self):
        @sa_number('a', gt=-4, lte=4, non_zero=True, mod=2)
        def _test(a):
            return a

        correct_numbers = [-2, 2, 4]
        incorrect_numbers = [-4, -3, -1, 0, 1, 3]

        # correct numbers should not throw exception
        for correct_number in correct_numbers:
            _test(correct_number)

        # incorrect numbers should all throw exception
        for incorrect_number in incorrect_numbers:
            with self.assertRaises(Exception):
                _test(incorrect_number)

    def test_multiple_rules_case2(self):
        @sa_number('a', gte=-6, lt=7, non_zero=False, mod=3)
        def _test(a):
            return a

        correct_numbers = [-6, -3, 0, 3, 6]
        incorrect_numbers = [-5, -4, -2, -1, 1, 2, 4, 5]

        # correct numbers should not throw exception
        for correct_number in correct_numbers:
            _test(correct_number)

        # incorrect numbers should all throw exception
        for incorrect_number in incorrect_numbers:
            with self.assertRaises(Exception):
                _test(incorrect_number)