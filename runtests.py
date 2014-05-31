# coding:utf-8

import sys
import unittest

integer_types = (int,)

if sys.version < '3':
    integer_types += (long,)



class HasMake(object):
    def make(self):
        raise NotImplemented()


class TestIntegerMixin(HasMake):
    def make(self):
        raise NotImplemented()

    def get_lower_bound(self):
        raise NotImplemented()

    def get_upper_bound(self):
        raise NotImplemented()

    def test_lower_bound(self):
        result = self.make()
        self.assertGreaterEqual(result, self.get_lower_bound())

    def test_upper_bound(self):
        result = self.make()
        self.assertLessEqual(result, self.get_upper_bound())

    def test_makes_integer(self):
        result = self.make()
        self.assertIn(type(result), integer_types)


class TestUnsignedIntegerMixin(TestIntegerMixin):
    def get_lower_bound(self):
        return 0

    def get_upper_bound(self):
        return super(TestUnsignedIntegerMixin, self).get_upper_bound() * 2 + 1


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


class TestMakeTinyInteger(unittest.TestCase, TestIntegerMixin):
    def get_lower_bound(self):
        from data_factory import MIN_TINY_INT
        return MIN_TINY_INT

    def get_upper_bound(self):
        from data_factory import MAX_TINY_INT
        return MAX_TINY_INT

    def make(self):
        from data_factory import make_tiny_integer
        return make_tiny_integer()


class TestMakeSmallInteger(unittest.TestCase, TestIntegerMixin):
    def get_lower_bound(self):
        from data_factory import MIN_SMALL_INT
        return MIN_SMALL_INT

    def get_upper_bound(self):
        from data_factory import MAX_SMALL_INT
        return MAX_SMALL_INT

    def make(self):
        from data_factory import make_small_integer
        return make_small_integer()


class TestMakeInteger(unittest.TestCase, TestIntegerMixin):
    def make(self):
        from data_factory import make_integer
        return make_integer()

    def get_lower_bound(self):
        from data_factory import MIN_INT
        return MIN_INT

    def get_upper_bound(self):
        from data_factory import MAX_INT
        return MAX_INT


class TestMakeBigInteger(unittest.TestCase, TestIntegerMixin):
    def make(self):
        from data_factory import make_big_integer
        return make_big_integer()

    def get_lower_bound(self):
        from data_factory import MIN_BIG_INT
        return MIN_BIG_INT

    def get_upper_bound(self):
        from data_factory import MAX_BIG_INT
        return MAX_BIG_INT


class TestMakeUnsignedTinyInteger(TestUnsignedIntegerMixin, TestMakeTinyInteger):
    def make(self):
        from data_factory import make_unsigned_tiny_integer
        return make_unsigned_tiny_integer()


class TestMakeUnsignedSmallInteger(TestUnsignedIntegerMixin, TestMakeSmallInteger):
    def make(self):
        from data_factory import make_unsigned_small_integer
        return make_unsigned_small_integer()


class TestMakeUnsignedInteger(TestUnsignedIntegerMixin, TestMakeInteger):
    def make(self):
        from data_factory import make_unsigned_integer
        return make_unsigned_integer()


class TestMakeUnsignedBigInteger(TestUnsignedIntegerMixin, TestMakeBigInteger):
    def make(self):
        from data_factory import make_unsigned_big_integer
        return make_unsigned_big_integer()


class TestMakeMimeType(unittest.TestCase, HasMake):
    def make(self):
        from data_factory import make_mime_type
        return make_mime_type()

    def test_returns_string(self):
        return self.assertEqual(type(self.make()), str)


class TestRealMixin(HasMake):
    def test_makes_float(self):
        result = self.make()
        self.assertEqual(type(result), float)


class TestMakeReal(unittest.TestCase, TestRealMixin):
    def make(self):
        from data_factory import make_real
        return make_real()

    def test_makes_real(self):
        from data_factory import REAL_DIGITS
        result = self.make()
        result_len = len(str(result)) - 1  # dot not considered as a position
        self.assertLessEqual(result_len, REAL_DIGITS)


class TestMakeDouble(unittest.TestCase, TestRealMixin):
    def make(self):
        from data_factory import make_double
        return make_double()

    def test_makes_real(self):
        from data_factory import DOUBLE_DIGITS
        result = self.make()
        result_len = len(str(result)) - 1  # dot not considered as a position
        self.assertLessEqual(result_len, DOUBLE_DIGITS)


class TestMakeDecimal(unittest.TestCase, HasMake):
    def make(self, max_digits=None, decimal_places=None):
        from data_factory import make_decimal
        return make_decimal(max_digits, decimal_places)


if __name__ == '__main__':
    import sys

    sys.path.insert(0, 'src/')
    unittest.main()