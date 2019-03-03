from unittest import TestCase, mock

import decorator

from pytsa import sa_type


class TestSaTypeRules(TestCase):
    # Test that the rules for sa_type works as specified

    def test_rule_allow_none_true(self):
        @sa_type('a', allow_none=True)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test(int)
        _test(type(int))
        _test(bool)

        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.5)

    def test_rule_allow_none_false(self):
        @sa_type('a', allow_none=False)
        def _test(a):
            return a

        # Correct usage
        _test(int)
        _test(type(int))
        _test(bool)

        # Incorrect usage, got None
        with self.assertRaises(Exception):
            _test(None)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
            _test(2.5)


class TestSaTypeBase(TestCase):
    # Test that the sa_type works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_type('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_type('b')
            def _test(a):
                return a

            _test(int)

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_type('a', unknown_rule=True)
            def _test(a):
                return a

    def test_global_disable(self):
        # if the environment variable 'PYTSA_DISABLED' is set to True, the decorator should be ignored
        def _test(a):
            return a

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'True'}):
            _test_true = sa_type('a')(_test)
            assert _test_true == _test

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'False'}):
            _test_false = sa_type('a')(_test)
            assert _test_false != _test

        with mock.patch.dict('os.environ', {}):
            _test_false = sa_type('a')(_test)
            assert _test_false != _test

    def test_should_keep_signature(self):
        # After the decorator is applied, the returned function should have the exact same signature as before
        def _test(a, *, b, c=3):
            return a

        _test_signature = sa_type('a')(_test)
        assert decorator.getfullargspec(_test) == decorator.getfullargspec(_test_signature)

    def test_call_with_kwargs(self):
        @sa_type('b')
        def _test(a, *, b, c=0):
            return a

        _test(1, **{'b': int})
        _test(1, **{'b': str, 'c': 1})

        with self.assertRaises(Exception):
            _test(1, **{'b': 3})
        with self.assertRaises(Exception):
            _test(1, **{'a': 1, 'c': 3})

    def test_use_default_if_none(self):
        # If a default value is specified, and the default is not None, the rules should check the default value

        # No exception should be thrown as the default value 1 is used as no value for a is passed
        @sa_type('a')
        def _test_bool(a=bool):
            return

        _test_bool()

        # When it is a required kwarg as well
        @sa_type('b')
        def _test_bool_kwarg(a, b=bool):
            return

        _test_bool_kwarg(1.1)

        # Exception should be thrown as the default value None is used and no value for a is passed
        @sa_type('a')
        def _test_none(a=None):
            return

        with self.assertRaises(Exception):
            _test_none()

        # When it is a required kwarg as well
        @sa_type('b')
        def _test_none_kwarg(a, b=None):
            return

        with self.assertRaises(Exception):
            _test_none_kwarg(1.1)

        # Not when allow_none is True
        @sa_type('b', allow_none=True)
        def _test_none_kwarg_allow_none(a, b=None):
            return

        _test_none_kwarg_allow_none(1.1)

    def test_type(self):
        @sa_type('a')
        def _test(a):
            return a

        # correct
        _test(int)
        _test(type)
        _test(str)

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
        # not list
        with self.assertRaises(Exception):
            _test([1, 'a'])
        # not bool
        with self.assertRaises(Exception):
            _test(True)
