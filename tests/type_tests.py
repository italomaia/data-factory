# coding:utf-8

import sys
import unittest

integer_types = (int,)

if sys.version < '3':
    integer_types += (long,)


class HasMake(object):
    def make(self):
        raise NotImplemented()


class IsIntegerMixin(HasMake):
    def test_makes_integer(self):
        result = self.make()
        self.assertIn(type(result), integer_types)


class IsFloatMixin(HasMake):
    def test_makes_float(self):
        result = self.make()
        self.assertEqual(type(result), float)


class IntegerIsInBoundsMixin(IsIntegerMixin):
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


class UnsignedIntegerMixin(IntegerIsInBoundsMixin):
    def get_lower_bound(self):
        return 0

    def get_upper_bound(self):
        return super(UnsignedIntegerMixin, self).get_upper_bound() * 2 + 1


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


class TestMakeTinyInteger(unittest.TestCase, IntegerIsInBoundsMixin):
    def get_lower_bound(self):
        from data_factory import MIN_TINY_INT
        return MIN_TINY_INT

    def get_upper_bound(self):
        from data_factory import MAX_TINY_INT
        return MAX_TINY_INT

    def make(self):
        from data_factory import make_tiny_integer
        return make_tiny_integer()


class TestMakeSmallInteger(unittest.TestCase, IntegerIsInBoundsMixin):
    def get_lower_bound(self):
        from data_factory import MIN_SMALL_INT
        return MIN_SMALL_INT

    def get_upper_bound(self):
        from data_factory import MAX_SMALL_INT
        return MAX_SMALL_INT

    def make(self):
        from data_factory import make_small_integer
        return make_small_integer()


class TestMakeInteger(unittest.TestCase, IntegerIsInBoundsMixin):
    def make(self):
        from data_factory import make_integer
        return make_integer()

    def get_lower_bound(self):
        from data_factory import MIN_INT
        return MIN_INT

    def get_upper_bound(self):
        from data_factory import MAX_INT
        return MAX_INT


class TestMakeBigInteger(unittest.TestCase, IntegerIsInBoundsMixin):
    def make(self):
        from data_factory import make_big_integer
        return make_big_integer()

    def get_lower_bound(self):
        from data_factory import MIN_BIG_INT
        return MIN_BIG_INT

    def get_upper_bound(self):
        from data_factory import MAX_BIG_INT
        return MAX_BIG_INT


class TestMakeUnsignedTinyInteger(UnsignedIntegerMixin, TestMakeTinyInteger):
    def make(self):
        from data_factory import make_unsigned_tiny_integer
        return make_unsigned_tiny_integer()


class TestMakeUnsignedSmallInteger(UnsignedIntegerMixin, TestMakeSmallInteger):
    def make(self):
        from data_factory import make_unsigned_small_integer
        return make_unsigned_small_integer()


class TestMakeUnsignedInteger(UnsignedIntegerMixin, TestMakeInteger):
    def make(self):
        from data_factory import make_unsigned_integer
        return make_unsigned_integer()


class TestMakeUnsignedBigInteger(UnsignedIntegerMixin, TestMakeBigInteger):
    def make(self):
        from data_factory import make_unsigned_big_integer
        return make_unsigned_big_integer()


class TestMakeMimeType(unittest.TestCase, HasMake):
    def make(self):
        from data_factory import make_mime_type
        return make_mime_type()

    def test_returns_string(self):
        return self.assertEqual(type(self.make()), str)


class TestMakeReal(unittest.TestCase, IsFloatMixin):
    def make(self):
        from data_factory import make_real
        return make_real()

    def test_makes_real(self):
        from data_factory import REAL_DIGITS
        result = self.make()
        result_len = len(str(result)) - 1  # dot not considered as a position
        self.assertLessEqual(result_len, REAL_DIGITS)


class TestMakeDouble(unittest.TestCase, IsFloatMixin):
    def make(self):
        from data_factory import make_double
        return make_double()

    def test_makes_real(self):
        from data_factory import DOUBLE_DIGITS
        result = self.make()
        result_len = len(str(result)) - 1  # dot not considered as a position
        self.assertLessEqual(result_len, DOUBLE_DIGITS)


class TestMakeDecimal(unittest.TestCase, HasMake):
    def make(self, max_digits=None, decimal=None, precision=None):
        from data_factory import make_decimal
        return make_decimal(max_digits, decimal, precision)

    def test_makes_decimal(self):
        from decimal import Decimal

        result = self.make(12)
        self.assertTrue(isinstance(result, Decimal))

    def test_makes_decimal_with_expected_max_digits(self):
        max_digits = 10

        result = abs(self.make(max_digits))  # negative can count as a character. We don't want that here
        self.assertLessEqual(len(str(result)), max_digits + 1)  # accounting the dot

    def test_decimal_has_two_digits_if_decimal_and_precision_length_informed(self):
        result = abs(self.make(10, 1, 1))
        result_str = str(result)
        self.assertEqual(len(result_str), 2 + 1)  # accounting the dot

    def test_if_decimal_length_parameter_works(self):
        max_digits = 10
        decimal_length = 2

        result = abs(self.make(max_digits, decimal_length))
        split = str(result).split('.')

        # ex: '10.0' => Decimal('10.0')
        # ex: '01.005' => Decimal('1.005')
        self.assertLessEqual(len(split[0]), decimal_length)

    def test_if_fraction_length_parameter_works(self):
        max_digits = 10
        precision = 3

        result = abs(self.make(max_digits, None, precision))
        split = str(result).split('.')

        # ex: '5.0020' => Decimal('5.020')
        self.assertEqual(len(split[1]), precision)

class TesteMakeBoolean(unittest.TestCase, HasMake):
    def make(self):
        from data_factory import make_boolean

        return make_boolean()

    def test_makes_boolean(self):
        result = self.make()
        self.assertTrue(isinstance(result, bool))

    def test_makes_true_or_false(self):
        values = [True, False]

        for i in range(10):
            result = self.make()
            if result in values:
                values.remove(result)

                if len(values) == 0:
                    break
        # may give false positive in rare occasions
        self.assertEqual(len(values), 0)
