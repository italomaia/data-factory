# -*- coding:utf-8 -*-

import re
import sys
import string
import random
import mimetypes

from functools import reduce
from decimal import Decimal
from datetime import datetime, timedelta


try:  # for py2 and py3
    __g = globals()
    unichr = __g['__builtins__'].get('unichr', chr)
    unicode = __g['__builtins__'].get('unicode', str)
    basestring = __g['__builtins__'].get('basestring', str)
except AttributeError:  # for pypy
    unichr = getattr(__g['__builtins__'], 'unichr', None)
    unicode = getattr(__g['__builtins__'], 'unicode', None)
    basestring = getattr(__g['__builtins__'], 'basestring', None)


MIN_TINY_INT, MAX_TINY_INT = -128, 127  # 8bits integer
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767  # 16bits integer
MIN_INT, MAX_INT = -2147483648, 2147483647  # 32bits integer
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808, 9223372036854775807  # 64bits integer

REAL_DIGITS = 23
DOUBLE_DIGITS = 53

# complete character ascii table
ASCII_TABLE = ''.join([chr(j) for j in range(255)])
SLUG_TABLE = string.ascii_letters + string.digits + '-_'
BINARY_TABLE = '01'


error_msgs = dict()
error_msgs["max_length"] = "Informed max_length %d is too small."
error_msgs["max_length_ext"] = "max_length is too small for given extensions"


def __make_decimal_str(max_digits, decimal_length=None, precision_length=None):
    """
    Makes a decimal number with up to `max_digits` digits.

    Arguments:
    max_digits - max number of digits for the number
    decimal_length - number of decimal places for the decimal part of the float
    precision_length - number of decimal places for the precision part of the float
    """

    if decimal_length is None and precision_length is None:
        decimal_length = random.randint(1, max_digits)
        precision_length = random.randint(0, max_digits - decimal_length)
    elif decimal_length is None and precision_length is not None:
        assert precision_length >= 0
        assert precision_length < max_digits
        decimal_length = random.randint(1, max_digits - precision_length)
    elif precision_length is None and decimal_length is not None:
        assert decimal_length <= max_digits
        assert decimal_length > 0
        precision_length = random.randint(0, max_digits - decimal_length)
    else:  # neither is none
        assert (decimal_length + precision_length) < max_digits
        assert decimal_length > 0
        assert precision_length >= 0
        assert precision_length < max_digits

    return "%s.%s" % (
        make_char_sequence(string.digits, decimal_length),
        make_char_sequence(string.digits, precision_length)
    )


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


def make_decimal(max_digits=None, decimal=None, precision=None):
    """
    Decimal with up to `digits` digits and `precision` decimal places.

    """

    return Decimal(__make_decimal_str(max_digits, decimal, precision)) * random.choice((1, -1))


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
    if length < 1:
        raise ValueError('length too short for binary')

    return make_char_sequence(BINARY_TABLE, length)


def make_ascii_string(max_length, empty=False):
    """
    Keyword arguments:
        max_length  -- max length for string
        empty       -- allow empty string?

    """
    return make_char_sequence(
        ASCII_TABLE,
        random.randint(int(not empty), max_length))


def make_string(max_length, empty=False):
    """
    Creates a random length non-empty string. If `empty` is set to True,
    an empty string can be generated.

    Keyword arguments:
        max_length  -- max length for string
        empty       -- allow empty string?

    """
    return make_char_sequence(
        string.printable,
        random.randint(int(not empty), max_length))


def make_unicode(max_length, empty=False):
    """
    Gets you a unicode string. Character range depends in the UCS your python
    was configured with (UCS2/UCS4).

    See http://pyref.infogami.com/unichr

    Keyword arguments:
        max_length  --
        empty       --
    @return: randomly generated unicode string
    """
    return ''.join(
        [
            unichr(random.randint(0, sys.maxunicode))
            for i in range(random.randint(int(not empty), max_length))
        ])


def make_slug(max_length, empty=False):
    """
    @see: https://docs.djangoproject.com/en/1.3/ref/models/fields/#slugfield

    @param max_length: max length for randomly generated slug.
    @param empty: allow empty slugs?
    @return:
    """
    return make_char_sequence(SLUG_TABLE, random.randint(int(not empty), max_length))


# TODO implement
#def get_xml():
#    pass


def make_boolean():
    """
    Returns True or False

    """
    return choose((True, False))


def make_datetime(from_date=None, to_date=None):
    """
    Creates a datetime in the past or in the future.

    @param from_date: limit date in the past random datetime will be generated.
    @param to_date: limit date in the future  random datetime will be
    generated. If not informed, generated datetime will be in the past.
    @return: datetime between from_date and to_date
    """
    now = datetime.now()

    from_date = from_date or now
    to_date = to_date or now

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


def make_hostname_label(length):
    """
    A hostname is formed by a series of labels joined with dots. This
    method should be used for that purpose.

    @see http://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_host_names
    @param length: length of the generated hostname
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


def make_hostname(max_length, domains=(".com", ".org", ".net")):
    """
    Creates an hostname with length up to max_length using one of the
    informed extensions.

    Keyword Arguments:
        max_length  -- max length for randomly generated hostname.
        domains     -- iterable with possible extensions for hostname
    """

    # verifies if max_length is in length range
    assert 0 < max_length < 256  # up to 255

    # complains if any len(ext) is less than max_length
    assert reduce(max, map(len, domains)) < max_length, \
        error_msgs["max_length_ext"]

    extension = random.choice(domains)

    max_length -= len(extension)
    label = make_hostname_label(random.randint(1, min(63, max_length)))

    return label + extension


def make_email_local_part(length):
    """
    Creates an email local part.

    See http://en.wikipedia.org/wiki/Email_address#Syntax

    """
    assert length > 0
    assert length < 65

    char_table = string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~"
    char_table_with_dot = char_table + "."
    local_str = ""

    for i in range(length):
        if (i == 0) or (local_str[-1] == ".") or (i == length - 1):
            local_str += random.choice(char_table)
        else:
            local_str += random.choice(char_table_with_dot)

    return local_str


def make_email(local_length, domain_length):
    """
    Creates an valid email address.
    domain as ip address and local part between double quotes are ignored

    See http://en.wikipedia.org/wiki/Email_address#Syntax
    """

    assert 0 < local_length <= 64
    assert 0 < (local_length + domain_length) <= 255

    local_part = make_email_local_part(local_length)
    domain_part = make_hostname(domain_length)
    return local_part + '@' + domain_part


def make_url(max_length, safe=False, port_number=None, domains=('.com',)):
    """
    Positional Arguments:
        max_length  -- max length of new url

    Keyword Arguments:
        safe        -- force https?
        port_number -- use port number?
        domains     -- list of acceptable domains
    """
    protocol = 'https://' if safe else 'http://'
    port_str = '' if port_number is None else ":" + str(port_number)
    extension_max_length = reduce(max, map(len, domains))

    min_length = len(protocol + port_str) + 1 + extension_max_length

    assert max_length >= min_length, error_msgs["max_length"] % min_length

    hostname_max_length = max_length - len(protocol) - len(port_str)
    return protocol + make_hostname(hostname_max_length, domains=domains) + port_str


def make_ip_address_str(*args, **kw):
    """
    Helper function that returns the ip_address in string format.
    Accepts same parameters as make_ip_address.

    Keyword Arguments:
        valid -- forces ip address to be valid
        v -- ip address version 4|6
    """
    ip_address = make_ip_address(*args, **kw)

    if kw['v'] == 4:
        return '.'.join(map(str, ip_address))
    elif kw['v'] == 6:
        return ':'.join(map(lambda v: v[2:], ip_address))


def make_ip_address(include_private=True, v=4):
    """
    Returns a IP address

    Private ip addresses for IPV4:
     - [0] 10.x.x.x
     - [1] 192.168.x.x
     - [2] 172.16.0.0 to 172.31.255.255

    Keyword Arguments:
        include_private -- include private ip addresses in result?
        v               -- ip address version 4|6

    """

    if v == 4:
        while True:
            ad = [random.randint(0, 255) for i in range(4)]

            if not include_private:
                if ad[0] == 10:
                    continue
                if (ad[0], ad[1]) == (192, 168):
                    continue
                if [172, 16, 0, 0] <= ad <= [172, 31, 255, 255]:
                    continue
            return ad

    elif v == 6:
        return [hex(random.randint(0, 65535)) for i in range(8)]


def make_mime_type():
    """
    Returns a valid mime type

    """
    types_tuple = tuple(mimetypes.types_map.values())
    return random.choice(types_tuple)


def make_filename(max_length, extensions=(".txt", ".odt", ".pdf")):
    """
    Returns a valid filename with one of the given extensions

    Positional Arguments:
        max_length  -- max length for the new filename

    Keyword Arguments:
        extensions  -- list of possible filename extensions

    """
    assert reduce(max, map(len, extensions)) < max_length, \
        error_msgs["max_length_ext"]

    char_table = re.sub(r'[/\?%*:|"<>]', '', string.printable)
    extension = random.choice(extensions)
    name = make_char_sequence(char_table, max_length - len(extension))

    return name + extension