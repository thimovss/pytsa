from unittest import TestCase

from src.pytsa import sa_bool

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
