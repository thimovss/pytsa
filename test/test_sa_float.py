from unittest import TestCase

from src.pytsa import sa_float
from test.utils import test_float_parameter, test_boolean_parameter


class TestSaFloatParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_lte_takes_float(self):
        test_float_parameter(self, sa_float, 'lte')

    def test_rule_gte_takes_float(self):
        test_float_parameter(self, sa_float, 'gte')

    def test_rule_gt_takes_float(self):
        test_float_parameter(self, sa_float, 'gt')

    def test_rule_lt_takes_float(self):
        test_float_parameter(self, sa_float, 'lt')

    def test_rule_mod_takes_float(self):
        test_float_parameter(self, sa_float, 'mod')

    def test_rule_non_zero_takes_boolean(self):
        test_boolean_parameter(self, sa_float, 'non_zero')


class TestSaFloatRules(TestCase):
    # Test that the rules for sa_float works as specified

    def test_rule_gte(self):
        @sa_float('a', gte=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(3.0)
        _test(2.0)

        # Incorrect usage, float lower than value
        with self.assertRaises(Exception):
            _test(1.0)
        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(3)

    def test_rule_lte(self):
        @sa_float('a', lte=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(1.0)
        _test(2.0)

        # Incorrect usage, float lower than value
        with self.assertRaises(Exception):
            _test(3.0)
        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(1)

    def test_rule_gt(self):
        @sa_float('a', gt=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(3.0)
        _test(4.0)

        # Incorrect usage, float lower than value
        with self.assertRaises(Exception):
            _test(1.0)
        # Incorrect usage, float equal to value
        with self.assertRaises(Exception):
            _test(2.0)
        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(3)

    def test_rule_lt(self):
        @sa_float('a', lt=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(0.0)
        _test(1.0)

        # Incorrect usage, float higher than value
        with self.assertRaises(Exception):
            _test(3.0)
        # Incorrect usage, float equal to value
        with self.assertRaises(Exception):
            _test(2.0)
        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(1)

    def test_rule_non_zero_true(self):
        @sa_float('a', non_zero=True)
        def _test(a):
            return a

        # Correct usage
        _test(1.0)
        _test(-1.0)

        # Incorrect usage, is 0.0
        with self.assertRaises(Exception):
            _test(0.0)

        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(0)

    def test_rule_non_zero_false(self):
        @sa_float('a', non_zero=False)
        def _test(a):
            return a

        # Correct usage
        _test(1.0)
        _test(0.0)
        _test(-1.0)

    def test_rule_mod(self):
        @sa_float('a', mod=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(0.0)
        _test(2.0)
        _test(4.0)
        _test(-2.0)

        # Incorrect usage, 3.0 % 2.0 results in 1.0
        with self.assertRaises(Exception):
            _test(3.0)
        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(2)

class TestSaIntBase(TestCase):
    # Test that the sa_float works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_float('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_float('b')
            def _test(a):
                return a

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_float('a', unknown_rule=True)
            def _test(a):
                return a

    def test_type(self):
        @sa_float('a')
        def _test(a):
            return a

        # correct
        _test(1.2)
        _test(0.0)
        _test(-1.0)

        # not None
        with self.assertRaises(Exception):
            _test(None)
        # not bool
        with self.assertRaises(Exception):
            _test(True)
        # not int
        with self.assertRaises(Exception):
            _test(3)
        # not string
        with self.assertRaises(Exception):
            _test('abc')
