from unittest import TestCase

from src.pytsa import sa_list

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

    def test_incorrect_rule(self):
        # if an unknown rule is provided, throw an exception
        with self.assertRaises(Exception):
            @sa_list('a', unknown_rule=True)
            def _test(a):
                return a


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
