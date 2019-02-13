from unittest import TestCase

from src.strictargs import sa_float


class TestSa_float(TestCase):

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
        return

    def test_none(self):
        # if the passed argument is None, throw an exception
        @sa_float('a')
        def _test(a):
            return a

        with self.assertRaises(Exception):
            _test(None)

    def test_not_float(self):
        # if the passed argument is not of type float, throw an exception
        @sa_float('a')
        def _test(a):
            return a

        with self.assertRaises(Exception):
            _test('abc')

        with self.assertRaises(Exception):
            _test(3)

    def test_rule_gte(self):
        @sa_float('a', gte=2.0)
        def _test(a):
            return a
        # Correct usage
        _test(3.2)
        _test(2.0)

        # Incorrect usage, float lower than value
        with self.assertRaises(Exception):
            _test(1.0)
        # Incorrect usage, int given instead of float
        with self.assertRaises(Exception):
            _test(3)

