# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from decimal import Decimal
import re

import string
import random

MIN_TINY_INT, MAX_TINY_INT = -128, 127  # 8bits integer
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767  # 16bits integer
MIN_INT, MAX_INT = -2147483648, 2147483647
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808l, 9223372036854775807l

error_msgs = {}
error_msgs["max_length"] = "Informed max_length is too small."
error_msgs["max_length_ext"] = "max_length is too small for given extensions"


def _positive(number):
    """
    Generates the corresponding unsigned integer for a max integer value.

    @param number:
    @return:
    """
    return number * 2 + 1


def or_null(fnc, frequency=0.5):
    """
    Used to allow the return of null value for a fabric method.

    Example:

    >>> int_or_null = or_null(get_tiny_integer, 0.2)()  # returns a tiny integer or None
    >>> assert int_or_null is None or isinstance(int_or_null, int)
    >>>
    >>> # test with arguments
    >>> str_or_null = or_null(get_string)(30)  # returns a non empty string or None
    >>> assert str_or_null is None or isinstance(str_or_null, basestring)

    @param fnc:
    @param frequency:
    @return:
    """

    def _fnc(fnc, *args, **kw):
        if random.random() < frequency:
            return None
        else:
            return fnc
    return _fnc


def get_tiny_integer():
    """
    Returns a 8bits integer.

    Example:

    >>> tiny_integer = get_tiny_integer()
    >>> assert MIN_TINY_INTEGER <= tiny_integer <= MAX_TINY_INTEGER
    >>> assert isinstance(tiny_integer, int)

    @return: int complainant with 8bits integer
    """
    return random.randint(MIN_TINY_INTEGER, MAX_TINY_INTEGER)


def get_small_integer():
    """
    Returns a 16bits integer.

    Example:

    >>> small_integer = get_small_integer()
    >>> assert MIN_SMALL_INT <= small_integer <= MAX_SMALL_INT
    >>> assert isinstance(small_integer, int)

    @return: int complainant with 16bits integer
    """
    return random.randint(MIN_SMALL_INT, MAX_SMALL_INT)


def get_integer():
    """
    Returns a 32bits integer.

    @return: int complainant with 32bits integer
    """
    return random.randint(MIN_INT, MAX_INT)


def get_big_integer():
    """

    Example:

    >>> big_integer = get_big_integer()
    >>> assert MIN_BIG_INT <= big_integer <= MAX_BIG_INT
    >>> assert isinstance(big_integer, int) or isinstance(big_integer, long)

    @return: int complainant with 64bits integer
    """
    return random.randint(MIN_BIG_INT, MAX_BIG_INT)


def get_positive_tiny_integer():
    """
    Returns a integer that corresponds to a unsigned 8bits integer.

    Example:

    >>> positive_tiny_integer = get_positive_tiny_integer()
    >>> assert 0 <= positive_tiny_integer <= _positive(MAX_TINY_INT)

    @return: int complainant with unsigned 8bits integer
    """
    return random.randint(0, _positive(MAX_TINY_INT))


def get_positive_small_integer():
    """

    Example:

    >>> positive_small_integer = get_positive_small_integer()
    >>> assert 0 <= positive_small_integer <= _positive(MAX_SMALL_INT)

    @return: int complainant with unsigned 16bits integer
    """
    return random.randint(0, _positive(MAX_SMALL_INT))


def get_positive_integer():
    """

    Example:

    >>> positive_integer = get_positive_integer()
    >>> assert 0 <= positive_integer <= _positive(MAX_INT)

    @return: int complainant with unsigned 32bits integer
    """
    return random.randint(0, _positive(MAX_INT))


def get_positive_big_integer():
    """

    Example:

    >>> positive_big_integer = get_positive_big_integer()
    >>> assert 0 <= positive_big_integer <= _positive(MAX_BIG_INT)

    @return: int complainant with unsigned 64bits integer
    """
    return random.randint(0, _positive(MAX_BIG_INT))


def get_float():
    """

    Example:
    >>> float_number = get_float()
    >>> assert isinstance(float_number, float)

    @return:
    """
    return random.random() * get_integer()


def get_positive_float():
    """

    Example:

    >>> positive_float = get_postive_float()
    >>> assert 0 <= positive_float
    >>> assert isinstance(positive_float, float)

    @return:
    """
    return random.random() * get_positive_integer()


def get_positive_decimal(max_digits, decimal_places):
    """
    Decimal with `max_digits` digits and `decimal_places` decimal places.

    Example:

    >>> get_decimal(5, 2)  # produces a decimal number in the format 999.99
    >>> get_decimal(4, 1)  # produces a decimal number in the format 9999.9
    >>> get_decimal(8, 1)  # produces a decimal number in the format 99999999.9
    >>>
    >>> decimal_number = get_decimal(5, 2)
    >>> assert isinstance(decimal_number, Decimal)
    >>> assert 0 <= decimal_number <= Decimal('999.99')

    @param max_digits:
    @param decimal_places:
    @return: positive decimal number with given constrains.
    """
    numerator = random.randint(0, int('9' * (max_digits - decimal_places)))
    denominator = get_char_sequence(string.digits, decimal_places)
    return Decimal("%d.%s" % (numerator, denominator))


def get_decimal(max_digits, decimal_places):
    """
    Decimal with `max_digits` digits and `decimal_places` decimal places.

    Example:

    >>> get_decimal(5, 2)  # produces a decimal number in the format 999.99
    >>> get_decimal(4, 1)  # produces a decimal number in the format 9999.9
    >>> get_decimal(8, 1)  # produces a decimal number in the format 99999999.9
    >>>
    >>> decimal_number = get_decimal(5, 2)
    >>> assert isinstance(decimal_number, Decimal)
    >>> assert Decimal('-999.99') <= decimal_number <= Decimal('999.99')

    @param max_digits:
    @param decimal_places:
    @return: decimal number that might be positive or negative.
    """
    decimal_number = get_positive_decimal(max_digits, decimal_places)
    sign = random.choice([True, False]) and 1 or -1
    return decimal_number * sign


def get_char_sequence(table, length):
    """
    Helper method that generates a random string from a char table.

    @param table: possible characters for the generated string.
    @param length: length for the given string.
    @return: randomly generated str with given length.
    """
    return u''.join([random.choice(table) for i in range(length)])


def get_binary(length):
    """
    Returns a binary string with informed length.

    @param length:
    @return: string in the format '01000101...'
    """
    return get_char_sequence('01', length)


def get_ascii_string(max_length, empty=False):
    return get_char_sequence(string.ascii_letters,
        random.randint(empty and 1 or 0, max_length))


def get_string(max_length, empty=False):
    return get_char_sequence(string.printable,
        random.randint(empty and 1 or 0, max_length))


def get_text(max_length, empty=False):
    """
    Returns a string with variable size that might contain the newline character.

    @param max_length: max length for randomly generated text strings.
    @param empty: allow empty text strings?
    @return:
    """
    return get_char_sequence(string.printable + '\n',
        random.randint(empty and 1 or 0, max_length))


def get_slug(max_length, empty=False):
    """
    @see: https://docs.djangoproject.com/en/1.3/ref/models/fields/#slugfield

    @param max_length: max length for randomly generated slug.
    @param empty: allow empty slugs?
    @return:
    """
    return get_char_sequence(string.letters + string.digits + '-_',
        random.randint(empty and 1 or 0, max_length))


# TODO implement
def get_xml():
    pass


def get_from_choices(choices):
    """
    Generates value from the given choices. Choices can not be a empty list.
    This is actually a thin wrapper around random.choice.
    @param choices:
    @return:
    """
    return random.choice(choices)


def get_boolean():
    return get_from_choices((True, False))


def get_datetime(from_date, to_date=None):
    """
    Creates a datetime in the past or in the future.

    @param from_date: limit date in the past random datetime will be generated.
    @param to_date: limit date in the future  random datetime will be generated.
    If not informed, generated datetime will be in the past.
    @return: datetime between from_date and to_date
    """
    now = datetime.now()
    to_date = to_date or now
    to_past, to_future = now - from_date, to_date - now

    if now == to_date or random.choice([True, False]):  # past
        target = to_past
        operator = lambda x, y: x - y
    else :  # future
        target = to_future
        operator = lambda x, y: x + y

    days = random.randint(0, target.days)
    seconds = random.randint(0, target.seconds)
    microseconds = random.randint(0, target.microseconds)
    return operator(now, timedelta(days, seconds, microseconds))


def get_hostname_label(length):
    """
    A hostname is formed by a series of labels joined with dots. This method should
    be used for that purpose.

    @param length: length of the generated hostname.
    @return:
    """
    assert 0 < length < 64

    char_table =  string.ascii_letters + string.digits
    char_table_with_hyphen =  string.ascii_letters + string.digits + "-"
    local_str = ""

    for i in range(length):
        if i == 0 or i == length-1:
            local_str += random.choice(char_table)
        else:
            local_str += random.choice_with_hyphen(char_table)

    return local_str


def get_hostname(max_length, extensions=[".com", ".org", ".net"]):
    """
    Creates an hostname with length up to max_length using one of the informed extensions.

    @param max_length: max length for randomly generated hostname.
    @param extensions: iterable with possible extensions for hostname.
    @return: proper normalized hostname string.
    """
    assert 0 < length < 256  # up to 255
    assert reduce(lambda x, y: max(len(x), len(y)), extensions) < max_length, \
        error_msgs["max_length_ext"]

    extension = random.choice(extensions)

    max_length -= len(extension)
    label = get_hostname_label(random.randint(1, min(63, max_length)))

    return label + extension


def get_email_local_part(length):
    """
    Creates an email local part.

    @see http://en.wikipedia.org/wiki/Email_address#Syntax
    """

    char_table = string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~"
    char_table_with_dot = char_table + "."
    local_str = ""

    for i in range(length):
        if (i == 0) or (local_str[-1] == ".") or (i == length - 1):
            local_str += random.choice(char_table)
        else:
            local_str += random.choice(char_table_with_dot)

    return local_str


def get_email(local_length, domain_length):
    """
    domain as ipaddress and local part between double quotes are ignored

    @see http://en.wikipedia.org/wiki/Email_address#Syntax
    """

    assert 0 < local_length <= 64
    assert 0 < (local_length + domain_length) <= 255

    local_part = get_email_local_part(local_length)
    domain_part = get_hostname(domain_length)
    return local_part + '@' + domain_part

# TODO implement
def get_url(max_length, safe=False, port_number=""):
    """

    @param max_length:
    @param safe:
    @param port_number:
    @return:
    """
    assert max_length > 10, error_msgs["max_length"]

    if port_number:
        port_number = ":" + str(port_number)

    scheme_name = safe and "https" or "http"
    protocol = scheme_name + "://"
    hostname_max_length = max_length - len(protocol) - len(port_number)
    return protocol + get_hostname(hostname_max_length) + port_number


# TODO implement
def get_filename(max_length, extensions=[".txt", ".odt", ".pdf"]):
    """


    @param max_length: max length for the randomly generated filename.
    @param extensions:
    @return: filename string using one of the informed extensions.
    """
    assert reduce(lambda x, y: max(len(x), len(y)), extensions) < max_length, \
        error_msgs["max_length_ext"]

    char_table = re.sub(r'[/\?%*:|"<>]', '', string.printable)
    extension = random.choice(extensions)
    name = get_char_sequence(char_table, max_length - len(extension))

    return name + extension
