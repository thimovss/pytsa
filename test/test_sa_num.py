from unittest import TestCase

from src.strictargs import sa_num


class TestSa_num(TestCase):

    def test(self):
        # no exceptions should be thrown with correct usage
        @sa_num('a')
        def _test(a):
            return a

    def test_args_name_missing(self):
        # the annotation should throw an exception if the name passed in the decorator is not present in the argument
        with self.assertRaises(Exception):
            @sa_num('b')
            def _test(a):
                return a

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an error
        with self.assertRaises(Exception):
            @sa_num('a', unknown_rule=True)
            def _test(a):
                return a
        return

    def test_not_num(self):
        return

    def test_rule_gte(self):
        @sa_num('a', gte=2)
        def _test(a):
            return a
        # Correct usage
        _test(3)
        _test(2)
        _test(3.0)
        _test(2.0)

        # Incorrect usage
        with self.assertRaises(Exception):
            _test(1)

