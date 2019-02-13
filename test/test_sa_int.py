from unittest import TestCase

from src.strictargs import sa_int


class TestSa_int(TestCase):

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

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_int('a', unknown_rule=True)
            def _test(a):
                return a
        return

    def test_none(self):
        # if the passed argument is None, throw an exception
        @sa_int('a')
        def _test(a):
            return a

        with self.assertRaises(Exception):
            _test(None)

    def test_not_int(self):
        # if the passed argument is not of type int, throw an exception
        @sa_int('a')
        def _test(a):
            return a

        with self.assertRaises(Exception):
            _test('abc')

        with self.assertRaises(Exception):
            _test(3.2)

    def test_rule_gte(self):
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
            _test(3.2)


    def test_rule_lte(self):
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
            _test(1.2)

    def test_rule_gt(self):
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
            _test(3.2)

    def test_rule_lt(self):
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
            _test(1.2)

