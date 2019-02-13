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

    # should not accept Boolean
    with self.assertRaises(Exception):
        @deco('a', **{rule: True})
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

def test_float_parameter(self, deco, rule):
    """Make sure the rule for this decorator only accepts a float"""

    # accepts float
    @deco('a', **{rule: 2.0})
    def _test(a):
        return a

    # accepts 0.0
    @deco('a', **{rule: 0.0})
    def _test(a):
        return a

    # accepts negative
    @deco('a', **{rule: -2.0})
    def _test(a):
        return a

    # should not accept None
    with self.assertRaises(Exception):
        @deco('a', **{rule: None})
        def _test(a):
            return a

    # should not accept boolean
    with self.assertRaises(Exception):
        @deco('a', **{rule: True})
        def _test(a):
            return a

    # should not accept int
    with self.assertRaises(Exception):
        @deco('a', **{rule: 4})
        def _test(a):
            return a

    # should not accept string
    with self.assertRaises(Exception):
        @deco('a', **{rule: 'abc'})
        def _test(a):
            return a

def test_boolean_parameter(self, deco, rule):
    """Make sure the rule for this decorator only accepts a boolean"""

    # accepts boolean True
    @deco('a', **{rule: True})
    def _test(a):
        return a

    # accepts boolean False
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

    # should not accept int
    with self.assertRaises(Exception):
        @deco('a', **{rule: 4})
        def _test(a):
            return a

    # should not accept string
    with self.assertRaises(Exception):
        @deco('a', **{rule: 'abc'})
        def _test(a):
            return a

def test_string_parameter(self, deco, rule):
    """Make sure the rule for this decorator only accepts a string"""

    # accepts string
    @deco('a', **{rule: 'abc'})
    def _test(a):
        return a

    # accepts string empty
    @deco('a', **{rule: ''})
    def _test(a):
        return a

    # accepts string whitespace
    @deco('a', **{rule: ' '})
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

    # should not accept int
    with self.assertRaises(Exception):
        @deco('a', **{rule: 4})
        def _test(a):
            return a

    # should not accept bool
    with self.assertRaises(Exception):
        @deco('a', **{rule: True})
        def _test(a):
            return a
