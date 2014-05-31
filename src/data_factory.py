# -*- coding:utf-8 -*-

import re
import sys
import string
import random
import mimetypes

from functools import reduce
from decimal import Decimal
from datetime import datetime, timedelta


# fix for python3 >= version
if sys.version_info >= (3, 0):
    unichr = chr
    basestring = unicode = str


MIN_TINY_INT, MAX_TINY_INT = -128, 127  # 8bits integer
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767  # 16bits integer
MIN_INT, MAX_INT = -2147483648, 2147483647  # 32bits integer
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808, 9223372036854775807  # 64bits integer

REAL_DIGITS = 23
DOUBLE_DIGITS = 53

# complete character ascii table
ASCII_TABLE = ''.join([chr(i) for i in range(255)])
BINARY_TABLE = '01'


error_msgs = {}
error_msgs["max_length"] = "Informed max_length is too small."
error_msgs["max_length_ext"] = "max_length is too small for given extensions"


def __make_decimal_str(max_digits, digits=None, precision=None):
    digits = digits or random.randint(1, max_digits)
    precision = precision or random.randint(0, digits)

    assert precision < digits
    assert digits <= max_digits

    number = [random.choice(string.digits) for i in range(random.randint(1, digits))]
    fraction = [random.choice(string.digits) for i in range(random.randint(0, digits - len(number)))]
    return "%s.%s" % (number, fraction)


def choose(choices):
    """
    Alias for random.choice

    """
    return random.choice(choices)


def unsigned(number):
    """
    Generates the corresponding unsigned integer for ``number``

    Arguments:
    number -- some integer value

    """
    return number * 2 + 1


def or_null(fnc, frequency=0.5):
    """
    Decorates a function so that it may return ``null``

    Arguments:
    fnc -- factory function

    Keyword arguments:
    frequency -- how often you should get a null value

    """
    def _fnc(*args, **kw):
        if random.random() < frequency:
            return None
        else:
            return fnc(*args, **kw)
    return _fnc


def make_tiny_integer():
    """
    Returns a 8bits complement 2 signed integer.

    """
    return random.randint(MIN_TINY_INT, MAX_TINY_INT)


def make_small_integer():
    """
    Returns a 16bits complement 2 signed integer.

    """
    return random.randint(MIN_SMALL_INT, MAX_SMALL_INT)


def make_integer():
    """
    Returns a 32bits complement 2 signed integer.

    """
    return random.randint(MIN_INT, MAX_INT)


def make_big_integer():
    """
    Returns a 64bits complement 2 signed integer.

    """
    return random.randint(MIN_BIG_INT, MAX_BIG_INT)


def make_unsigned_tiny_integer():
    """
    Returns a 8bits complement 2 unsigned integer.

    """
    return random.randint(0, unsigned(MAX_TINY_INT))


def make_unsigned_small_integer():
    """
    Returns a 16bits complement 2 unsigned integer.

    """
    return random.randint(0, unsigned(MAX_SMALL_INT))


def make_unsigned_integer():
    """
    Returns a 32bits complement 2 unsigned integer.

    """
    return random.randint(0, unsigned(MAX_INT))


def make_unsigned_big_integer():
    """
    Returns a 64bits complement 2 unsigned integer.

    """
    return random.randint(0, unsigned(MAX_BIG_INT))


def make_real(digits=None, precision=None):
    """
    Returns a 4bytes floating point number.

    """
    return float(__make_decimal_str(REAL_DIGITS, digits, precision)) * random.choice((1, -1))


def make_double(digits=None, precision=None):
    """
    Returns a 8bytes floating point number.

    """
    return float(__make_decimal_str(DOUBLE_DIGITS, digits, precision)) * random.choice((1, -1))


def make_decimal(max_digits, decimal_places):
    """
    Decimal with up to ``max_digits`` digits and ``precision`` decimal places.

    """
    return Decimal(__make_decimal_str(max_digits, max_digits, decimal_places)) * random.choice((1, -1))


def make_char_sequence(table, length):
    """
    Helper method that generates a random string from a char table.

    @param table: possible characters for the generated string.
    @param length: length for the given string.
    @return: randomly generated str with given length.
    """
    return ''.join([random.choice(table) for i in range(length)])


def make_binary(length):
    """
    Returns a binary string with informed length.

    @param length:
    @return: string in the format '01000101...'
    """
    return make_char_sequence(BINARY_TABLE, length)


def get_ascii_string(max_length, empty=False):
    """
    Example:

    >>> sample_string = get_ascii_string(10)
    >>> assert isinstance(sample_string, basestring)

    @param max_length:
    @param empty:
    @return:
    """
    return make_char_sequence(ASCII_TABLE,
        random.randint(empty and 1 or 0, max_length))


def get_string(max_length, empty=False):
    """
    Creates a random length non-empty string. If `empty` is set to True,
    an empty string can be generated.

    Example:

    >>> string_sample = get_string(10)
    >>> assert isinstance(string_sample, basestring)
    >>>
    >>> string_sample = get_string(10, True)
    >>> assert isinstance(string_sample, basestring)

    @param max_length:
    @param empty:
    @return:
    """
    return make_char_sequence(string.printable,
        random.randint(empty and 1 or 0, max_length))


def get_unicode(max_length, empty=False):
    """
    Gets you a unicode string. Character range depends in the UCS your python
    was configured with (UCS2/UCS4).

    Example:

    >>> unicode_string = get_unicode(20)
    >>> assert isinstance(unicode_string, basestring)
    >>> assert isinstance(unicode_string, unicode)
    >>> assert 1 <= len(unicode_string)
    >>> assert len(unicode_string) <= 20
    >>>
    >>> unicode_string = get_unicode(20, True)
    >>> assert isinstance(unicode_string, basestring)
    >>> assert isinstance(unicode_string, unicode)
    >>> assert 0 <= len(unicode_string)
    >>> assert len(unicode_string) <= 20

    @see: http://pyref.infogami.com/unichr
    @param max_length:
    @param empty:
    @return: randomly generated unicode string
    """
    return ''.join(
        [unichr(random.randint(0, sys.maxunicode))
        for i in range(random.randint(empty and 1 or 0, max_length))])


def get_slug(max_length, empty=False):
    """
    @see: https://docs.djangoproject.com/en/1.3/ref/models/fields/#slugfield

    @param max_length: max length for randomly generated slug.
    @param empty: allow empty slugs?
    @return:
    """
    return make_char_sequence(string.letters + string.digits + '-_',
        random.randint(empty and 1 or 0, max_length))


# TODO implement
#def get_xml():
#    pass


def make_boolean():
    """
    Returns True or False

    """
    return choose((True, False))


def get_datetime(from_date=None, to_date=None):
    """
    Creates a datetime in the past or in the future.

    Example:

    >>> # test for date in the present
    >>> date_in_present = get_datetime()
    >>> assert isinstance(date_in_present, datetime)
    >>>
    >>> # test for date in past
    >>> target_date = datetime(year=2005, month=4, day=13)
    >>> date_in_past = get_datetime(target_date)
    >>> assert isinstance(date_in_past, datetime)
    >>> assert target_date <= date_in_past
    >>> assert date_in_past <= datetime.now()
    >>>
    >>> # test for date in the future
    >>> target_date = datetime.now() + timedelta(days=100)
    >>> date_in_future = get_datetime(to_date=target_date)
    >>> assert isinstance(date_in_future, datetime)
    >>> assert target_date >= date_in_future
    >>> assert date_in_future >= datetime.now()
    >>>
    >>> # test for date in past or future
    >>> pdate = datetime.now() - timedelta(days=100)
    >>> fdate = datetime.now() + timedelta(days=100)
    >>> rdate = get_datetime(pdate, fdate)
    >>> assert isinstance(rdate, datetime)
    >>> assert pdate <= rdate
    >>> assert fdate >= rdate

    @param from_date: limit date in the past random datetime will be generated.
    @param to_date: limit date in the future  random datetime will be
    generated. If not informed, generated datetime will be in the past.
    @return: datetime between from_date and to_date
    """
    now = datetime.now()

    to_date = to_date or now
    from_date = from_date or now

    past_delta = now - from_date  # timedelta
    future_delta = to_date - now  # timedelta

    # seconds to the past
    past_delta_in_seconds = past_delta.total_seconds()

    # seconds to the future
    future_delta_in_seconds = future_delta.total_seconds()

    rp_delta_in_seconds = random.randint(0, int(past_delta_in_seconds))
    rf_delta_in_seconds = random.randint(0, int(future_delta_in_seconds))

    # result can be negative or positive
    delta_in_seconds = rf_delta_in_seconds - rp_delta_in_seconds  # in seconds

    return now + timedelta(seconds=delta_in_seconds)


def get_hostname_label(length):
    """
    A hostname is formed by a series of labels joined with dots. This
    method should be used for that purpose.

    Example:

    >>> hostname_label = get_hostname_label(20)
    >>> assert isinstance(hostname_label, basestring)
    >>> assert len(hostname_label) == 20
    >>>
    >>> hostname_label = get_hostname_label(30)
    >>> assert isinstance(hostname_label, basestring)
    >>> assert len(hostname_label) == 30

    @param length: length of the generated hostname.
    @return:
    """
    assert 0 < length < 64

    char_table = string.ascii_letters + string.digits
    char_table_with_hyphen = string.ascii_letters + string.digits + "-"
    local_str = ""

    for i in range(length):
        if i == 0 or i == length - 1:
            local_str += random.choice(char_table)
        else:
            local_str += random.choice(char_table_with_hyphen)

    return local_str


def get_hostname(max_length, extensions=[".com", ".org", ".net"]):
    """
    Creates an hostname with length up to max_length using one of the
    informed extensions.

    @param max_length: max length for randomly generated hostname.
    @param extensions: iterable with possible extensions for hostname.
    @return: proper normalized hostname string.
    """
    assert 0 < max_length < 256  # up to 255
    assert reduce(max, map(len, extensions)) < max_length, \
        error_msgs["max_length_ext"]

    extension = random.choice(extensions)

    max_length -= len(extension)
    label = get_hostname_label(random.randint(1, min(63, max_length)))

    return label + extension


def get_email_local_part(length):
    """
    Creates an email local part.

    Example:

    >>> email_local_part = get_email_local_part(20)
    >>> assert isinstance(email_local_part, basestring)
    >>> assert len(email_local_part) == 20

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
    Creates an valid email address.
    domain as ip address and local part between double quotes are ignored

    @see http://en.wikipedia.org/wiki/Email_address#Syntax
    """

    assert 0 < local_length <= 64
    assert 0 < (local_length + domain_length) <= 255

    local_part = get_email_local_part(local_length)
    domain_part = get_hostname(domain_length)
    return local_part + '@' + domain_part


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


def make_ip_address_str(*args, **kw):
    """
    Helper function that returns the ip_address in string format.
    Accept same parameters as get_ip_address.

    @return: string ip address
    """
    ip_address = make_ip_address(*args, **kw)

    if kw['v'] == 4:
        return '.'.join(map(str, ip_address))
    elif kw['v'] == 6:
        return ':'.join(map(lambda n: hex(n)[2:], ip_address))


def make_ip_address(valid=True, v=4):
    """
    Returns a IPV4/6 address

    Invalid addresses for IPV4:
     - [0] 10.x.x.x
     - [1] 192.168.x.x
     - [2] 172.16.0.0 to 172.31.255.255

    Keyword Arguments:
    valid -- forces created ip address to be valid
    v -- ip address version

    """

    if v == 4:
        while True:
            ad = [random.randint(0, 255) for i in range(4)]

            if valid:
                if ad[0] == 10:
                    continue
                if (ad[0], ad[1]) == (192, 168):
                    continue
                if [172, 16, 0, 0] <= ad <= [172, 31, 255, 255]:
                    continue
            return ad

    elif v == 6:
        return [random.randint(0, 65535) for i in range(8)]


def make_mime_type():
    """
    Returns a valid mime type

    """
    types_tuple = tuple(mimetypes.types_map.values())
    return random.choice(types_tuple)


def make_filename(max_length, extensions=[".txt", ".odt", ".pdf"]):
    """

    Example:

    >>> import tempfile
    >>> import os
    >>> from os import path
    >>>
    >>> new_filename = make_filename(50)
    >>> assert isinstance(new_filename, basestring)
    >>> name, ext = path.splitext(new_filename)
    >>> assert ext in (".txt", ".odt", ".pdf")
    >>>
    >>> tempfolder = tempfile.mkdtemp()
    >>> abs_filename = path.join(tempfolder, new_filename)
    >>> file = open(abs_filename, 'w')
    >>> file.close()
    >>> assert path.exists(abs_filename)
    >>>


    @param max_length: max length for the randomly generated filename.
    @param extensions:
    @return: filename string using one of the informed extensions.
    """
    assert reduce(max, map(len, extensions)) < max_length, \
        error_msgs["max_length_ext"]

    char_table = re.sub(r'[/\?%*:|"<>]', '', string.printable)
    extension = random.choice(extensions)
    name = make_char_sequence(char_table, max_length - len(extension))

    return name + extension
