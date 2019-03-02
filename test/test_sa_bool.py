from unittest import TestCase, mock

import decorator

from src.pytsa import sa_bool


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
        with self.assertRaises(Exception):
            _test(2.5)

    def test_rule_allow_none_false(self):
        @sa_bool('a', allow_none=False)
        def _test(a):
            return a

        # Correct usage
        _test(True)
        _test(False)

        # Incorrect usage, got None
        with self.assertRaises(Exception):
            _test(None)
        # Incorrect usage, got float
        with self.assertRaises(Exception):
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
        with self.assertRaises(Exception):
            @sa_bool('b')
            def _test(a):
                return a

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
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
        def _test(a, b, c):
            return a

        _test_signature = sa_bool('a')(_test)
        assert decorator.getfullargspec(_test) == decorator.getfullargspec(_test_signature)

    def test_type(self):
        @sa_bool('a')
        def _test(a):
            return a

        # correct
        _test(True)
        _test(False)

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
        # not type
        with self.assertRaises(Exception):
            _test(bool)
