from unittest import TestCase, mock

import decorator

from pytsa import sa_bool


class TestSaBoolRules(TestCase):
    # Test that the rules for sa_bool works as specified

    def test_rule_allow_none_true(self):
        @sa_bool('a', allow_none=True)
        def _test(a):
            return a

        # Correct usage
        _test(None)
        _test(True)
        _test(False)

        # Incorrect usage, got float
        with self.assertRaises(TypeError):
            _test(2.5)

    def test_rule_allow_none_false(self):
        @sa_bool('a', allow_none=False)
        def _test(a):
            return a

        # Correct usage
        _test(True)
        _test(False)

        # Incorrect usage, got None
        with self.assertRaises(ValueError):
            _test(None)
        # Incorrect usage, got float
        with self.assertRaises(TypeError):
            _test(2.5)


class TestSaBoolBase(TestCase):
    # Test that the sa_bool works as specified

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_bool('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(ValueError):
            @sa_bool('b')
            def _test(a):
                return a

            _test(True)

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(ValueError):
            @sa_bool('a', unknown_rule=True)
            def _test(a):
                return a

    def test_global_disable(self):
        # if the environment variable 'PYTSA_DISABLED' is set to True, the decorator should be ignored
        def _test(a):
            return a

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'True'}):
            _test_true = sa_bool('a')(_test)
            assert _test_true == _test

        with mock.patch.dict('os.environ', {'PYTSA_DISABLED': 'False'}):
            _test_false = sa_bool('a')(_test)
            assert _test_false != _test

        with mock.patch.dict('os.environ', {}):
            _test_false = sa_bool('a')(_test)
            assert _test_false != _test

    def test_should_keep_signature(self):
        # After the decorator is applied, the returned function should have the exact same signature as before
        def _test(a, *, b, c=3):
            return a

        _test_signature = sa_bool('a')(_test)
        assert decorator.getfullargspec(_test) == decorator.getfullargspec(_test_signature)

    def test_call_with_kwargs(self):
        @sa_bool('b')
        def _test(a, *, b, c=0):
            return a

        _test(1, **{'b': True})
        _test(1, **{'b': False, 'c': 1})

        with self.assertRaises(TypeError):
            _test(1, **{'b': 3.3})
        with self.assertRaises(ValueError):
            _test(1, **{'b': None, 'c': 3})

    def test_use_default_if_none(self):
        # If a default value is specified, and the default is not None, the rules should check the default value

        # No exception should be thrown as the default value 1 is used as no value for a is passed
        @sa_bool('a')
        def _test_1(a=True):
            return

        _test_1()

        # When it is a required kwarg as well
        @sa_bool('b')
        def _test_1_kwarg(a, b=True):
            return

        _test_1_kwarg(1.1)

        # Exception should be thrown as the default value None is used and no value for a is passed
        @sa_bool('a')
        def _test_none(a=None):
            return

        with self.assertRaises(ValueError):
            _test_none()

        # When it is a required kwarg as well
        @sa_bool('b')
        def _test_none_kwarg(a, b=None):
            return

        with self.assertRaises(ValueError):
            _test_none_kwarg(1.1)

        # Not when allow_none is True
        @sa_bool('b', allow_none=True)
        def _test_none_kwarg_allow_none(a, b=None):
            return

        _test_none_kwarg_allow_none(1.1)

    def test_type(self):
        @sa_bool('a')
        def _test(a):
            return a

        # correct
        _test(True)
        _test(False)

        # not None
        with self.assertRaises(ValueError):
            _test(None)
        # not zero
        with self.assertRaises(TypeError):
            _test(0)
        # not int
        with self.assertRaises(TypeError):
            _test(1)
        # not float
        with self.assertRaises(TypeError):
            _test(3.0)
        # not string
        with self.assertRaises(TypeError):
            _test('abc')
        # not list
        with self.assertRaises(TypeError):
            _test([1, 'a'])
        # not type
        with self.assertRaises(TypeError):
            _test(bool)
