# coding:utf-8

import unittest


class TestOrNull(unittest.TestCase):
    def setUp(self):
        from data_factory import or_null

        self.or_null = or_null
        self.fnc = lambda: 10
        self.fnc_or_null = self.or_null(self.fnc)

    def test_makes_null(self):
        result = []
        for i in range(10):
            result.append(self.fnc_or_null())

        # may give false negative, but very unlikely
        self.assertIn(None, result)

    def test_makes_non_null(self):
        result = []
        for i in range(10):
            result.append(self.fnc_or_null())

        # may give false negative, but very unlikely
        self.assertIn(self.fnc(), result)


class TestInteger(object):
    lower_bound = None
    upper_bound = None

    def make(self):
        raise NotImplemented()

    def test_lower_bound(self):
        result = self.make()
        self.assertGreaterEqual(result, self.lower_bound)

    def test_upper_bound(self):
        result = self.make()
        self.assertLessEqual(result, self.upper_bound)


class TestUnsignedInteger(TestInteger):
    def test_lower_bound(self):
        result = self.make()
        self.assertGreaterEqual(result, 0)

    def test_upper_bound(self):
        result = self.make()
        self.assertLessEqual(result, self.upper_bound * 2 + 1)


class TestMakeTinyInteger(unittest.TestCase, TestInteger):
    def setUp(self):
        from data_factory import make_tiny_integer
        from data_factory import MIN_TINY_INT, MAX_TINY_INT

        self.make = make_tiny_integer
        self.lower_bound = MIN_TINY_INT
        self.upper_bound = MAX_TINY_INT


class TestMakeSmallInteger(unittest.TestCase, TestInteger):
    def setUp(self):
        from data_factory import make_small_integer
        from data_factory import MIN_SMALL_INT, MAX_SMALL_INT

        self.make = make_small_integer
        self.lower_bound = MIN_SMALL_INT
        self.upper_bound = MAX_SMALL_INT


class TestMakeInteger(unittest.TestCase, TestInteger):
    def setUp(self):
        from data_factory import make_integer
        from data_factory import MIN_INT, MAX_INT

        self.make = make_integer
        self.lower_bound = MIN_INT
        self.upper_bound = MAX_INT


class TestMakeBigInteger(unittest.TestCase, TestInteger):
    def setUp(self):
        from data_factory import make_big_integer
        from data_factory import MIN_BIG_INT, MAX_BIG_INT

        self.make = make_big_integer
        self.lower_bound = MIN_BIG_INT
        self.upper_bound = MAX_BIG_INT


class TestMakeUnsignedTinyInteger(unittest.TestCase, TestUnsignedInteger):
    def setUp(self):
        from data_factory import make_unsigned_tiny_integer
        from data_factory import MAX_TINY_INT

        self.make = make_unsigned_tiny_integer
        self.upper_bound = MAX_TINY_INT


class TestMakeUnsignedSmallInteger(unittest.TestCase, TestUnsignedInteger):
    def setUp(self):
        from data_factory import make_unsigned_small_integer
        from data_factory import MAX_SMALL_INT

        self.make = make_unsigned_small_integer
        self.upper_bound = MAX_SMALL_INT


class TestMakeUnsignedInteger(unittest.TestCase, TestUnsignedInteger):
    def setUp(self):
        from data_factory import make_unsigned_integer
        from data_factory import MAX_INT

        self.make = make_unsigned_integer
        self.upper_bound = MAX_INT


class TestMakeUnsignedBigInteger(unittest.TestCase, TestUnsignedInteger):
    def setUp(self):
        from data_factory import make_unsigned_big_integer
        from data_factory import MAX_BIG_INT

        self.make = make_unsigned_big_integer
        self.upper_bound = MAX_BIG_INT


class TestMakeFloat(unittest.TestCase):
    pass


if __name__ == '__main__':
    import sys

    sys.path.insert(0, 'src/')
    unittest.main()