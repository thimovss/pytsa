from unittest import TestCase, mock

import decorator

from pytsa import sa_int
from test.test_utils import test_boolean_parameter, test_number_parameter


class TestSaIntParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_lte_takes_number(self):
        test_number_parameter(self, sa_int, 'lte')

    def test_rule_gte_takes_number(self):
        test_number_parameter(self, sa_int, 'gte')

    def test_rule_gt_takes_number(self):
        test_number_parameter(self, sa_int, 'gt')

    def test_rule_lt_takes_number(self):
        test_number_parameter(self, sa_int, 'lt')

    def test_rule_mod_takes_number(self):
        test_number_parameter(self, sa_int, 'mod')

    def test_rule_non_zero_takes_boolean(self):
        test_boolean_parameter(self, sa_int, 'non_zero')


class TestSaIntRules(TestCase):
    # Test that the rules for sa_int works as specified

    def test_rule_gte_int(self):
        @sa_int('a', gte=2)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(2)

        # Incorrect usage, int lower than value
        with self.assertRaises(Exception):
            _test(1)
        # Incorrect usage, float given instead of int
        with self.assertRaises(Exception):
            _test(2.1)

    def test_rule_gte_float(self):
        @sa_int('a', gte=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(2)

        # Incorrect usage, int lower than value
        with self.assertRaises(Exception):
            _test(1)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.1)

    def test_rule_lte_int(self):
        @sa_int('a', lte=2)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(2)

        # Incorrect usage, int lower than value
        with self.assertRaises(Exception):
            _test(3)
        # Incorrect usage, float given instead of int
        with self.assertRaises(Exception):
            _test(1.9)

    def test_rule_lte_float(self):
        @sa_int('a', lte=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(2)

        # Incorrect usage, int lower than value
        with self.assertRaises(Exception):
            _test(3)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(1.9)

    def test_rule_gt_int(self):
        @sa_int('a', gt=2)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(4)

        # Incorrect usage, int lower than value
        with self.assertRaises(Exception):
            _test(1)
        # Incorrect usage, int equal to value
        with self.assertRaises(Exception):
            _test(2)
        # Incorrect usage, float given instead of int
        with self.assertRaises(Exception):
            _test(2.1)

    def test_rule_gt_float(self):
        @sa_int('a', gt=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(3)
        _test(4)

        # Incorrect usage, int lower than value
        with self.assertRaises(Exception):
            _test(1)
        # Incorrect usage, int equal to value
        with self.assertRaises(Exception):
            _test(2)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.1)

    def test_rule_lt_int(self):
        @sa_int('a', lt=2)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(1)

        # Incorrect usage, int higher than value
        with self.assertRaises(Exception):
            _test(3)
        # Incorrect usage, int equal to value
        with self.assertRaises(Exception):
            _test(2)
        # Incorrect usage, float given instead of int
        with self.assertRaises(Exception):
            _test(1.9)

    def test_rule_lt_float(self):
        @sa_int('a', lt=2.0)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(1)

        # Incorrect usage, int higher than value
        with self.assertRaises(Exception):
            _test(3)
        # Incorrect usage, int equal to value
        with self.assertRaises(Exception):
            _test(2)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(1.9)

    def test_rule_non_zero_true(self):
        @sa_int('a', non_zero=True)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(-1)

        # Incorrect usage, is 0
        with self.assertRaises(Exception):
            _test(0)

        # Incorrect usage, float given instead of int
        with self.assertRaises(Exception):
            _test(0.0)

    def test_rule_non_zero_false(self):
        @sa_int('a', non_zero=False)
        def _test(a):
            return a

        # Correct usage
        _test(1)
        _test(0)
        _test(-1)

    def test_rule_mod_int(self):
        @sa_int('a', mod=2)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(2)
        _test(4)
        _test(-2)

        # Incorrect usage, 3 % 2 results in 1
        with self.assertRaises(Exception):
            _test(3)
        # Incorrect usage, float given instead of int
        with self.assertRaises(Exception):
            _test(2.0)

    def test_rule_mod_float(self):
        @sa_int('a', mod=2.5)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(5)

        # Incorrect usage, 3 % 2.5 results in .5
        with self.assertRaises(Exception):
            _test(3)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.5)

    def test_rule_allow_none_true(self):
        @sa_int('a', allow_none=True)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test(0)
        _test(5)

        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.5)

    def test_rule_allow_none_false(self):
        @sa_int('a', allow_none=False)
        def _test(a):
            return a

        # Correct usage
        _test(0)
        _test(5)

        # Incorrect usage, got None
        with self.assertRaises(Exception):
            _test(None)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.5)

    def test_rule_allow_none_other_rules(self):
        @sa_int('a', allow_none=True, gte=2)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test(5)
        _test(4)

        # Incorrect usage, not greather than or equal to 2
        with self.assertRaises(Exception):
            _test(1)


class TestSaIntBase(TestCase):
    # Test that the sa_int works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_int('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_int('b')
            def _test(a):
                return a

            _test(1)

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_int('a', unknown_rule=True)
            def _test(a):
                return a

    def test_global_disable(self):
        # if the environment variable 'PYTSA_DISABLED' is set to True, the decorator should be ignored
        def _test(a):
            return a

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'True'}):
            _test_true = sa_int('a')(_test)
            assert _test_true == _test

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'False'}):
            _test_false = sa_int('a')(_test)
            assert _test_false != _test

        with mock.patch.dict('os.environ', {}):
            _test_false = sa_int('a')(_test)
            assert _test_false != _test

    def test_should_keep_signature(self):
        # After the decorator is applied, the returned function should have the exact same signature as before
        def _test(a, *, b, c=3):
            return a

        _test_signature = sa_int('a')(_test)
        assert decorator.getfullargspec(_test) == decorator.getfullargspec(_test_signature)

    def test_call_with_kwargs(self):
        @sa_int('b')
        def _test(a, *, b, c=0):
            return a

        _test(1, **{'b': 3})
        _test(1, **{'b': 3, 'c': 1})

        with self.assertRaises(Exception):
            _test(1, **{'b': 3.3})
        with self.assertRaises(Exception):
            _test(1, **{'a': 1, 'c': 3})

    def test_use_default_if_none(self):
        # If a default value is specified, and the default is not None, the rules should check the default value

        # No exception should be thrown as the default value 1 is used as no value for a is passed
        @sa_int('a')
        def _test_1(a=1):
            return

        _test_1()

        # When it is a required kwarg as well
        @sa_int('b')
        def _test_1_kwarg(a, b=1):
            return

        _test_1_kwarg(1.1)

        # Exception should be thrown as the default value None is used and no value for a is passed
        @sa_int('a')
        def _test_none(a=None):
            return

        with self.assertRaises(Exception):
            _test_none()

        # When it is a required kwarg as well
        @sa_int('b')
        def _test_none_kwarg(a, b=None):
            return

        with self.assertRaises(Exception):
            _test_none_kwarg(1.1)

        # Not when allow_none is True
        @sa_int('b', allow_none=True)
        def _test_none_kwarg_allow_none(a, b=None):
            return

        _test_none_kwarg_allow_none(1.1)

    def test_type(self):
        @sa_int('a')
        def _test(a):
            return a

        # correct
        _test(1)
        _test(0)
        _test(-1)

        # not None
        with self.assertRaises(Exception):
            _test(None)
        # not bool
        with self.assertRaises(Exception):
            _test(True)
        # not float
        with self.assertRaises(Exception):
            _test(3.0)
        # not string
        with self.assertRaises(Exception):
            _test('abc')
        # not list
        with self.assertRaises(Exception):
            _test([1, 'a'])
        # not type
        with self.assertRaises(Exception):
            _test(int)


class TestSaIntMultipleRules(TestCase):

    def test_multiple_rules_case1(self):
        @sa_int('a', gt=-4, lte=4.0, non_zero=True, mod=2.0)
        def _test(a):
            return a

        correct_ints = [-2, 2, 4]
        incorrect_ints = [-4, -3, -1, 0, 1, 3]

        # correct ints should not throw exception
        for correct_int in correct_ints:
            _test(correct_int)

        # incorrect ints should all throw exception
        for incorrect_int in incorrect_ints:
            with self.assertRaises(Exception):
                _test(incorrect_int)

    def test_multiple_rules_case2(self):
        @sa_int('a', gte=-6.0, lt=7, non_zero=False, mod=3)
        def _test(a):
            return a

        correct_ints = [-6, -3, 0, 3, 6]
        incorrect_ints = [-5, -4, -2, -1, 1, 2, 4, 5]

        # correct ints should not throw exception
        for correct_int in correct_ints:
            _test(correct_int)

        # incorrect ints should all throw exception
        for incorrect_int in incorrect_ints:
            with self.assertRaises(Exception):
                _test(incorrect_int)
