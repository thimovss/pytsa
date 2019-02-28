from unittest import TestCase, mock

from src.pytsa import sa_list
from src.utils import test_int_parameter, test_type_parameter, test_boolean_parameter


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
