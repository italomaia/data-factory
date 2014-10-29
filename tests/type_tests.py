# coding:utf-8

import sys
import string
import unittest

integer_types = (int,)

if sys.version_info < (3, 0):
    integer_types += (long,)
else:
    basestring = unicode = str


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


class IsStringMixin(HasMake):
    def test_makes_string(self):
        result = self.make()
        self.assertTrue(isinstance(result, basestring))


class HasDefaultStringInterfaceMixin(IsStringMixin):
    def test_makes_non_empty_string_by_default(self):
        result = self.make()
        self.assertTrue(len(result) > 0)

    def test_makes_empty_returns_empty_or_non_empty_string(self):
        flag = 0
        for i in range(10):
            result = self.make(1, True)  # allow empty result

            if len(result) == 0:
                flag |= 1
            elif len(result) > 0:
                flag |= 2
            elif flag == 3:
                break
        self.assertEqual(flag, 3)  # may assert false positive


class HasHostnameLabelMixin(IsStringMixin):
    def is_hostname_label(self, label):
        charset = string.ascii_letters + string.digits + '-'

        self.assertGreaterEqual(len(label), 1)
        self.assertLessEqual(len(label), 63)

        for c in label:
            self.assertIn(c, charset)

        return True


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


class TestPy2Py3Hacks(unittest.TestCase):
    def test_unichr_exists(self):
        import data_factory
        assert hasattr(data_factory, 'unichr'), 'unichr not available'

    def test_basestring_exists(self):
        import data_factory as df
        assert hasattr(df, 'basestring'), 'basestring not available'

    def test_unicode_exists(self):
        import data_factory as df
        assert hasattr(df, 'unicode'), 'unicode not available'


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
    def make(self):
        from data_factory import make_small_integer
        return make_small_integer()

    def get_lower_bound(self):
        from data_factory import MIN_SMALL_INT
        return MIN_SMALL_INT

    def get_upper_bound(self):
        from data_factory import MAX_SMALL_INT
        return MAX_SMALL_INT


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


class TestMakeBinary(unittest.TestCase, HasMake):
    def make(self, length=8):
        from data_factory import make_binary

        return make_binary(length=length)

    def test_makes_binary(self):
        result = self.make()

        for c in result:
            self.assertIn(c, '01')

    def test_obeys_length(self):
        from random import randint
        length = randint(1, 32)
        result = self.make(length)

        self.assertEqual(len(result), length)

    def test_binary_does_not_accepts_length_zero(self):
        self.assertRaises(ValueError, self.make, 0)


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


class TestMakeBoolean(unittest.TestCase, HasMake):
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


class TestMakeCharSequence(unittest.TestCase, IsStringMixin):
    def make(self, table='abc123', length=12):
        from data_factory import make_char_sequence
        self.table = table
        return make_char_sequence(table, length)

    def test_makes_char_sequence_from_given_table(self):
        result = self.make()

        for c in result:
            self.assertTrue(c in self.table)


class TestMakeASCII(unittest.TestCase, HasDefaultStringInterfaceMixin):
    def make(self, max_length=12, empty=False):
        from data_factory import make_ascii_string
        return make_ascii_string(max_length, empty)

    def test_makes_ascii_string(self):
        from data_factory import ASCII_TABLE

        result = self.make()
        for c in result:
            self.assertTrue(c in ASCII_TABLE)


class TestMakeUnicode(unittest.TestCase, HasDefaultStringInterfaceMixin):
    def make(self, max_length=12, empty=False):
        from data_factory import make_unicode
        return make_unicode(max_length, empty)

    def test_makes_unicode_string(self):
        import sys

        result = self.make()
        for c in result:
            self.assertTrue(0 <= ord(c) <= sys.maxunicode)


class TestMakeSlug(unittest.TestCase, HasDefaultStringInterfaceMixin):
    def make(self, max_length=12, empty=False):
        from data_factory import make_slug
        return make_slug(max_length, empty)

    def test_makes_slug_string(self):
        from data_factory import SLUG_TABLE
        result = self.make()

        for c in result:
            self.assertTrue(c in SLUG_TABLE)


class TestMakeDatetime(unittest.TestCase):
    def make(self, from_date=None, to_date=None):
        from data_factory import make_datetime
        return make_datetime(from_date, to_date)

    def test_makes_datetime(self):
        from datetime import datetime
        result = self.make()
        self.assertTrue(isinstance(result, datetime))

    def test_default_datetime_is_now(self):
        from datetime import datetime

        result = self.make()  # now
        now = datetime.now()
        self.assertEqual(result.year, now.year)
        self.assertEqual(result.month, now.month)
        self.assertEqual(result.day, now.day)

        self.assertEqual(result.hour, now.hour)
        self.assertEqual(result.minute, now.minute)

        try:
            # there may be a false positive here in some cases. Unlikely though.
            self.assertEqual(result.second, now.second)
        except Exception:
            import sys
            import logging
            logging.getLogger('TestMakeDatetime.test_default_datetime_is_now').info('Maybe a false positive... Run it again!')
            raise sys.exc_info()[1]

    def test_past_datetime_works(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        last_week = now - timedelta(weeks=1)

        result = self.make(from_date=last_week)
        self.assertGreaterEqual(now, result)

    def test_future_datetime_works(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        next_week = now + timedelta(weeks=1)

        result = self.make(to_date=next_week)
        self.assertLessEqual(now, result)


class TestMakeHostnameLabel(unittest.TestCase, IsStringMixin):
    def make(self, length=12):
        from data_factory import make_hostname_label
        return make_hostname_label(length)

    def test_makes_label_with_requested_length(self):
        from random import randint
        length = randint(1, 63)
        result = self.make(length)
        self.assertEqual(len(result), length)

    def test_label_length_restriction(self):
        # between 1 and 63 characters
        self.assertRaises(AssertionError, lambda: self.make(0))
        self.assertRaises(AssertionError, lambda: self.make(64))

    def test_label_has_proper_charset(self):
        result = self.make()
        charset = string.ascii_letters + string.digits + '-'

        for c in result:
            self.assertIn(c, charset)


class TestMakeHostname(unittest.TestCase, HasHostnameLabelMixin):
    def make(self, **kwargs):
        from data_factory import make_hostname

        kwargs['max_length'] = kwargs.get('max_length', 12)
        return make_hostname(**kwargs)

    def test_is_formed_of_valid_labels(self):
        result = self.make()

        for label in result.split('.'):
            self.assertTrue(self.is_hostname_label(label))

    def test_hostname_labels_length_are_valid(self):
        result = self.make()

        for label in result.split('.'):
            self.assertGreater(len(label), 0)

    def test_hostname_has_enough_labels(self):
        result = self.make()
        self.assertGreater(len(result.split('.')), 1)

    def test_default_domain_composition(self):
        from os import path
        result = self.make()
        name, ext = path.splitext(result)
        self.assertIn(ext, (".com", ".org", ".net"))

    def test_provided_domain_is_used(self):
        from random import choice

        domains = ['.com.br', '.cc', '.io']
        domain = choice(domains)
        result = self.make(domains=[domain])
        self.assertTrue(result.endswith(domain))

    def test_hostname_complains_if_length_is_too_small(self):
        self.assertRaises(AssertionError, lambda: self.make(max_length=2, domains=['.com.br']))


class TestMakeEmailLocalPart(unittest.TestCase, IsStringMixin):
    def make(self, length=None):
        from random import randint
        from data_factory import make_email_local_part

        length = randint(1, 64) if length is None else length
        return make_email_local_part(length)

    def test_makes_local_part_with_requested_length(self):
        from random import randint
        length = randint(1, 64)
        result = self.make(length)
        self.assertEqual(len(result), length)

    def test_local_part_length_restriction(self):
        # between 1 and 63 characters
        self.assertRaises(AssertionError, lambda: self.make(0))
        self.assertRaises(AssertionError, lambda: self.make(65))

    def test_label_has_proper_charset(self):
        result = self.make()
        charset = string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~."

        for c in result:
            self.assertIn(c, charset)

    def test_no_consecutive_dots(self):
        result = self.make()
        flag = False

        for c in result:
            if c != '.':
                flag = False
            else:
                self.assertFalse(flag)
                flag = True


class TestMakeEmail(unittest.TestCase, IsStringMixin):
    def is_local_part(self, text):
        charset = string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~."

        self.assertTrue(0 < len(text) < 65)

        for c in text:
            self.assertTrue(c in charset)

        return True

    def is_hostname_label(self, label):
        charset = string.ascii_letters + string.digits + '-'

        self.assertGreaterEqual(len(label), 1)
        self.assertLessEqual(len(label), 63)

        for c in label:
            self.assertIn(c, charset)

        return True

    def make(self, local_length=6, domain_length=8):
        from data_factory import make_email
        return make_email(local_length, domain_length)

    def test_if_looks_like_an_email(self):
        result = self.make()
        self.assertIn('@', result)
        self.assertEqual(len(result.split('@')), 2)

    def test_if_local_part_is_valid(self):
        result = self.make()
        local_part = result.split('@')[0]
        self.assertTrue(self.is_local_part(local_part))

    def test_if_domain_part_is_valid(self):
        result = self.make()
        domain_part = result.split('@')[1]
        split = domain_part.split('.')

        self.assertGreater(len(split), 0)
        for label in split:
            self.assertTrue(self.is_hostname_label(label))


class TestMakeUrl(unittest.TestCase, HasHostnameLabelMixin):
    def make(self, **kwargs):
        from data_factory import make_url
        kwargs['max_length'] = kwargs.get('max_length', 20)
        return make_url(**kwargs)

    def test_safe_param_produces_https_url(self):
        result = self.make(safe=True)
        self.assertTrue(result.startswith('https:'))

    def test_default_safe_param_produces_http_url(self):
        result = self.make(safe=False)
        self.assertTrue(result.startswith('http:'))

    def test_min_max_length_is_possible(self):
        result = self.make(max_length=10, domains=['.c'])
        self.assertEqual(len(result), 10)

    def test_provided_domain_is_used(self):
        from random import choice
        char = choice(string.ascii_lowercase)
        result = self.make(max_length=10, domains=['.%s' % char])
        self.assertTrue(result.endswith('.%s' % char))

    def test_hostname_part_is_actually_a_hostname(self):
        result = self.make()
        protocol, hostname = result.split('://')
        labels = hostname.split('.')

        for label in labels:
            self.assertTrue(self.is_hostname_label(label))


class TestMakeIP(unittest.TestCase):
    def make(self, include_private=True, v=4):
        from data_factory import make_ip_address
        return make_ip_address(include_private=include_private, v=v)

    def test_makes_ipv4(self):
        result = self.make()
        self.assertEqual(len(result), 4)

        for bit in result:
            self.assertTrue(0 <= bit <= 255)

    def test_makes_non_private_ipv4(self):
        result = self.make(include_private=False)

        # [0] 10.x.x.x
        self.assertNotEqual(result[0], 10)

        # [1] 192.168.x.x
        self.assertFalse(result[0] == 192 and result[1] == 168)

        # [2] 172.16.0.0 to 172.31.255.255
        self.assertTrue(result < [172, 16, 0, 0] or result > [172, 31, 255, 255])

    def test_makes_ipv6(self):
        result = self.make(v=6)

        for bit in result:
            try:
                int(bit, 16)
            except ValueError:
                assert False, 'Non hex in ipv6'

        self.assertEqual(len(result), 8)


class TestMakeIPStr(unittest.TestCase):
    def make(self, v=4):
        from data_factory import make_ip_address_str
        return make_ip_address_str(v=v)

    def test_makes_valid_ipv4_formatted_string(self):
        import re
        result = self.make()
        c = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        self.assertIsNotNone(c.match(result))

    def test_makes_valid_ipv6_formatted_string(self):
        import re
        result = self.make(v=6)
        c = re.compile(r'[\da-f]{0,4}(:[\da-f]{0,4}){7}')
        self.assertIsNotNone(c.match(result))


class TestMakeMimeType(unittest.TestCase, IsStringMixin):
    def make(self):
        from data_factory import make_mime_type
        return make_mime_type()

    def test_if_is_valid_mimetype(self):
        import mimetypes
        result = self.make()
        self.assertIn(result, mimetypes.types_map.values())


class TestMakeFilename(unittest.TestCase, IsStringMixin):
    def make(self, **kwargs):
        from data_factory import make_filename
        kwargs['max_length'] = kwargs.get('max_length', 12)
        return make_filename(**kwargs)

    def test_charset(self):
        charset = string.printable
        result = self.make()

        for c in result:
            self.assertIn(c, charset)

    def test_uses_default_extensions(self):
        from os.path import splitext
        result = self.make()
        name, ext = splitext(result)
        self.assertIn(ext, (".txt", ".odt", ".pdf"))

    def test_uses_provided_extensions(self):
        result = self.make(extensions=['.odt'])
        self.assertTrue(result.endswith('.odt'))