def test_int_parameter(self, deco, rule):
    """Make sure the rule for this decorator only accepts an integer"""

    # accepts int
    @deco('a', **{rule: 2})
    def _test(a):
        return a

    # accepts 0
    @deco('a', **{rule: 0})
    def _test(a):
        return a

    # accepts negative
    @deco('a', **{rule: -2})
    def _test(a):
        return a

    # should not accept None
    with self.assertRaises(Exception):
        @deco('a', **{rule: None})
        def _test(a):
            return a

    # should not accept float
    with self.assertRaises(Exception):
        @deco('a', **{rule: 4.3})
        def _test(a):
            return a

    # should not accept string
    with self.assertRaises(Exception):
        @deco('a', **{rule: 'abc'})
        def _test(a):
            return a

def test_boolean_parameter(self, deco, rule):
    """Make sure the rule for this decorator only accepts a boolean"""

    # accepts int
    @deco('a', **{rule: True})
    def _test(a):
        return a

    # accepts 0
    @deco('a', **{rule: False})
    def _test(a):
        return a

    # should not accept None
    with self.assertRaises(Exception):
        @deco('a', **{rule: None})
        def _test(a):
            return a

    # should not accept float
    with self.assertRaises(Exception):
        @deco('a', **{rule: 4.3})
        def _test(a):
            return a

    # should not accept string
    with self.assertRaises(Exception):
        @deco('a', **{rule: 'abc'})
        def _test(a):
            return a