from unittest import TestCase, mock

import decorator

from pytsa import sa_list
from test.test_utils import test_int_parameter, test_type_parameter, test_boolean_parameter


class TestSaListParameters(TestCase):
    # Test that the decorator only accepts the correct parameters

    def test_rule_len_takes_int(self):
        test_int_parameter(self, sa_list, 'len')

    def test_rule_type_takes_type(self):
        test_type_parameter(self, sa_list, 'type')

    def test_rule_type_takes_type(self):
        test_boolean_parameter(self, sa_list, 'not_empty')


class TestSaListRules(TestCase):
    # Test that the rules for sa_list works as specified

    def test_rule_len(self):
        @sa_list('a', len=3)
        def _test(a):
            return a

        # Correct usage
        _test([1, 2, 3])
        _test([6.5, 'a', 3])
        _test([None, None, None])

        # Incorrect usage, length is 2
        with self.assertRaises(Exception):
            _test([1, 2])
        # Incorrect usage, length is 4
        with self.assertRaises(Exception):
            _test([1, 2, 3, 4])
        # Incorrect usage, None should be counted
        with self.assertRaises(Exception):
            _test([None, 1, 2, 3])

    def test_should_keep_signature(self):
        # After the decorator is applied, the returned function should have the exact same signature as before
        def _test(a, *, b, c=3):
            return a

        _test_signature = sa_list('a')(_test)
        assert decorator.getfullargspec(_test) == decorator.getfullargspec(_test_signature)

    def test_call_with_kwargs(self):
        @sa_list('b')
        def _test(a, *, b, c=0):
            return a

        _test(1, **{'b': []})
        _test(1, **{'b': [1, 2], 'c': 1})

        with self.assertRaises(Exception):
            _test(1, **{'b': {}})
        with self.assertRaises(Exception):
            _test(1, **{'a': 1, 'c': 3})

    def test_use_default_if_none(self):
        # If a default value is specified, and the default is not None, the rules should check the default value

        # No exception should be thrown as the default value 1 is used as no value for a is passed
        @sa_list('a')
        def _test_l1(a=[1]):
            return

        _test_l1()

        # When it is a required kwarg as well
        @sa_list('b')
        def _test_l1_kwarg(a, b=[1]):
            return

        _test_l1_kwarg(1.1)

        # Exception should be thrown as the default value None is used and no value for a is passed
        @sa_list('a')
        def _test_none(a=None):
            return

        with self.assertRaises(Exception):
            _test_none()

        # When it is a required kwarg as well
        @sa_list('b')
        def _test_none_kwarg(a, b=None):
            return

        with self.assertRaises(Exception):
            _test_none_kwarg(1.1)

        # Not when allow_none is True
        @sa_list('b', allow_none=True)
        def _test_none_kwarg_allow_none(a, b=None):
            return

        _test_none_kwarg_allow_none(1.1)

    def test_rule_type(self):
        @sa_list('a', type=int)
        def _test(a):
            return a

        # Correct usage
        _test([1, 2, 3])
        _test([])
        _test([-19])

        # Incorrect usage, should not accept None
        with self.assertRaises(Exception):
            _test([1, None, 3])
        # Incorrect usage, got floats
        with self.assertRaises(Exception):
            _test([1.0, 2.0, 3.0])

    def test_rule_not_empty_true(self):
        @sa_list('a', not_empty=True)
        def _test(a):
            return a

        # Correct usage
        _test([1, 2, 3])
        _test(['a', 1.2, 3])
        _test([None])

        # Incorrect usage, empty list
        with self.assertRaises(Exception):
            _test([])
        # Incorrect usage, empty list
        with self.assertRaises(Exception):
            _test(list())

    def test_rule_not_empty_false(self):
        @sa_list('a', not_empty=False)
        def _test(a):
            return a

        # Correct usage
        _test([1, 2, 3])
        _test(['a', 1.2, 3])
        _test([None])
        _test([])
        _test(list())

    def test_rule_allow_none_true(self):
        @sa_list('a', allow_none=True)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test([1, 2, 3])
        _test(['a', 1.2, 3])
        _test([None])
        _test([])
        _test(list())

        # Incorrect usage, got int
        with self.assertRaises(Exception):
            _test(2)

    def test_rule_allow_none_false(self):
        @sa_list('a', allow_none=False)
        def _test(a):
            return a

        # Correct usage
        _test([1, 2, 3])
        _test(['a', 1.2, 3])
        _test([None])
        _test([])
        _test(list())

        # Incorrect usage, got None
        with self.assertRaises(Exception):
            _test(None)
        # Incorrect usage, got int
        with self.assertRaises(Exception):
            _test(2)

    def test_rule_allow_none_other_rules(self):
        @sa_list('a', allow_none=True, not_empty=True)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test([1, 2, 3])
        _test(['a', 1.2, 3])
        _test([None])

        # Incorrect usage, empty list
        with self.assertRaises(Exception):
            _test([])
        # Incorrect usage, empty list
        with self.assertRaises(Exception):
            _test(list())


class TestSaListBase(TestCase):
    # Test that the sa_list works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_list('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_list('b')
            def _test(a):
                return a

            _test([])

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_list('a', unknown_rule=True)
            def _test(a):
                return a

    def test_global_disable(self):
        # if the environment variable 'PYTSA_DISABLED' is set to True, the decorator should be ignored
        def _test(a):
            return a

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'True'}):
            _test_true = sa_list('a')(_test)
            assert _test_true == _test

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'False'}):
            _test_false = sa_list('a')(_test)
            assert _test_false != _test

        with mock.patch.dict('os.environ', {}):
            _test_false = sa_list('a')(_test)
            assert _test_false != _test

    def test_type(self):
        @sa_list('a')
        def _test(a):
            return a

        # correct
        _test(['a'])
        _test([])
        _test([1])
        _test(['b', 1, True])

        # not zero
        with self.assertRaises(Exception):
            _test(0)
        # not None
        with self.assertRaises(Exception):
            _test(None)
        # not int
        with self.assertRaises(Exception):
            _test(1)
        # not float
        with self.assertRaises(Exception):
            _test(3.0)
        # not string
        with self.assertRaises(Exception):
            _test('abc')
            _test(3.0)
        # not bool
        with self.assertRaises(Exception):
            _test(True)
        # not type
        with self.assertRaises(Exception):
            _test(list)
