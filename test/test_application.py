import itertools
from unittest import TestCase

from pytsa import sa_int, sa_number, sa_string, sa_type


class TestMultipleRules(TestCase):

    def test_multiple_rules_case(self):

        @sa_int('a', gt=-4, lte=4.0)
        @sa_string('b', starts_with='ab', is_lower=True)
        @sa_type('c')
        @sa_number('d', gte=-5, lte=6.5, allow_none=True)
        def _test(a, b, *, c=int, d):
            return

        correct_a = [4, 0, -3]
        incorrect_a = [-4, 5, 2.2, None]
        correct_b = ['abcd', 'ab', 'ab\t3']
        incorrect_b = ['bcd', 'AB', '', None]
        correct_c = [int, str, type(int)]
        incorrect_c = ['int', 'bool', None]
        correct_d = [-5.0, 6.5, None, 0]
        incorrect_d = ['3', -7.2, 11]

        # Test all possible combinations

        # - All correct
        for a, b, c, d in itertools.product(correct_a, correct_b, correct_c, correct_d):
            _test(a, b, **{'c': c, 'd': d})

        # - A Incorrect
        for a, b, c, d in itertools.product(incorrect_a, correct_b, correct_c, correct_d):
            with self.assertRaises(Exception):
                _test(a, b, **{'c': c, 'd': d})

        # - B Incorrect
        for a, b, c, d in itertools.product(correct_a, incorrect_b, correct_c, correct_d):
            with self.assertRaises(Exception):
                _test(a, b, **{'c': c, 'd': d})

        # - C Incorrect
        for a, b, c, d in itertools.product(correct_a, correct_b, incorrect_c, correct_d):
            with self.assertRaises(Exception):
                _test(a, b, **{'c': c, 'd': d})

        # - D Incorrect
        for a, b, c, d in itertools.product(correct_a, correct_b, correct_c, incorrect_d):
            with self.assertRaises(Exception):
                _test(a, b, **{'c': c, 'd': d})

        # - All Incorrect
        for a, b, c, d in itertools.product(incorrect_a, incorrect_b, incorrect_c, incorrect_d):
            with self.assertRaises(Exception):
                _test(a, b, **{'c': c, 'd': d})
