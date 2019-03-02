import itertools
from unittest import TestCase

from src.pytsa import sa_int, sa_number, sa_string, sa_type


class TestSaMultipleRules(TestCase):

    def test_multiple_rules_case1(self):

        @sa_int('a', gt=-4, lte=4.0)
        @sa_string('b', starts_with='ab', lower_case=True)
        @sa_type('c')
        @sa_number('d', gte=-5, lte=6.5, allow_none=True)
        def _test(a, b, c, d):
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
        print(itertools.product(correct_a, correct_b))