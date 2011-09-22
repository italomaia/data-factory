# -*- coding:utf-8 -*-

import re
import string
import random
import mimetypes

from decimal import Decimal
from datetime import datetime, timedelta

MIN_TINY_INT, MAX_TINY_INT = -128, 127  # 8bits integer
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767  # 16bits integer
MIN_INT, MAX_INT = -2147483648, 2147483647
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808l, 9223372036854775807l

ASCII_TABLE = ''.join([chr(i) for i in range(128)])
BINARY_TABLE = '01'


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

    >>> # returns a tiny integer or None
    >>> int_or_null = or_null(lambda: 10, 0.2)()
    >>> assert (int_or_null is None or isinstance(int_or_null, int))
    >>>
    >>> # test with arguments
    >>> # returns a non empty string or None
    >>> str_or_null = or_null(lambda length: length * 'c')(30)
    >>> assert (str_or_null is None or isinstance(str_or_null, basestring))

    @param fnc:
    @param frequency:
    @return:
    """
    def _fnc(*args, **kw):
        if random.random() < frequency:
            return None
        else:
            return fnc(*args, **kw)
    return _fnc


def get_tiny_integer():
    """
    Returns a 8bits integer.

    Example:

    >>> tiny_integer = get_tiny_integer()
    >>> assert MIN_TINY_INT <= tiny_integer
    >>> assert tiny_integer <= MAX_TINY_INT
    >>> assert isinstance(tiny_integer, int)

    @return: int complainant with 8bits integer
    """
    return random.randint(MIN_TINY_INT, MAX_TINY_INT)


def get_small_integer():
    """
    Returns a 16bits integer.

    Example:

    >>> small_integer = get_small_integer()
    >>> assert MIN_SMALL_INT <= small_integer
    >>> assert small_integer <= MAX_SMALL_INT
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

    >>> positive_float = get_positive_float()
    >>> assert 0 <= positive_float
    >>> assert isinstance(positive_float, float)

    @return:
    """
    return random.random() * get_positive_integer()


def get_positive_decimal(max_digits, decimal_places):
    """
    Decimal with `max_digits` digits and `decimal_places` decimal places.

    Example:

    >>> decimal_number = get_positive_decimal(5, 2)
    >>> assert isinstance(decimal_number, Decimal)
    >>> assert 0 <= decimal_number
    >>> assert decimal_number <= Decimal('999.99')

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

    >>> decimal_number = get_decimal(5, 2)
    >>> assert isinstance(decimal_number, Decimal)
    >>> assert Decimal('-999.99') <= decimal_number
    >>> assert decimal_number <= Decimal('999.99')

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
    return get_char_sequence(BINARY_TABLE, length)


def get_ascii_string(max_length, empty=False):
    """
    Example:

    >>> sample_string = get_ascii_string(10)
    >>> assert isinstance(sample_string, basestring)

    @param max_length:
    @param empty:
    @return:
    """
    return get_char_sequence(ASCII_TABLE,
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
    return get_char_sequence(string.printable,
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
#def get_xml():
#    pass


def get_from_choices(choices):
    """
    Generates value from the given choices. Choices can not be a empty list.
    This is actually a thin wrapper around random.choice.

    Example:

    >>> possible_vacation_spots = ("bahamas", "brazil", "england")
    >>> vacation_spot = get_from_choices(possible_vacation_spots)
    >>> assert vacation_spot in possible_vacation_spots

    @param choices: iterable with possible results
    @return:
    """
    return random.choice(choices)


def get_boolean():
    """
    Example:

    >>> lucky_guess = get_boolean()
    >>> assert isinstance(lucky_guess, bool)
    >>> assert lucky_guess in (True, False)


    @return: True or False
    """
    return get_from_choices((True, False))


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
    assert 0 < length < 256  # up to 255
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


def get_ip_address_str(*args, **kw):
    """
    Helper function that returns the ip_address in string format.
    Accept same parameters as get_ip_address.

    @return: string ip address
    """
    ip_address = get_ip_address(*args, **kw)

    if kw['v'] == 4:
        return '.'.join(map(str, ip_address))
    elif kw['v'] == 6:
        return ':'.join(map(lambda n: hex(n)[2:], ip_address))


def get_ip_address(valid=True, v=4):
    '''
    Generates a valid IPV4/6 address

    Invalid addresses for IPV4:
     - [0] 10.x.x.x
     - [1] 192.168.x.x
     - [2] 172.16.0.0 to 172.31.255.255

    Example:

    >>> ip_address = get_ip_address()
    >>> assert isinstance(ip_address, list)
    >>> assert len(ip_address) == 4
    >>>
    >>> ip_address = get_ip_address(False)
    >>> assert isinstance(ip_address, list)
    >>> assert [0, 0, 0, 0] <= ip_address
    >>> assert ip_address <= [255, 255, 255, 255]
    >>>
    >>> ip_address = get_ip_address(v=6)
    >>> assert isinstance(ip_address, list)
    >>> assert len(ip_address) == 8

    @param valid: generated ip_address must be valid (only works with ipv4)
    @param v: ip version compliance (4 or 6)
    @return: list with ip address values
    '''

    if v == 4:
        while True:
            ad = [random.randint(0, 255) for i in range(4)]

            if valid:
                if ad[0] == 10:
                    continue
                if (ad[0], ad[1]) == (192, 168):
                    continue
                if (172, 16, 0, 0) <= ad <= (172, 31, 255, 255):
                    continue
            return ad

    elif v == 6:
        return [random.randint(0, 65535) for i in range(8)]


def get_mime_type():
    """

    Example:

    >>> mime_type = get_mime_type()
    >>> assert isinstance(mime_type, basestring)
    >>> assert mime_type in mimetypes.types_map.values()

    @return:
    """
    return random.choice(mimetypes.types_map.values())


def get_filename(max_length, extensions=[".txt", ".odt", ".pdf"]):
    """

    Example:

    >>> import tempfile
    >>> import os
    >>> from os import path
    >>>
    >>> new_filename = get_filename(50)
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
    name = get_char_sequence(char_table, max_length - len(extension))

    return name + extension


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Data Factory '
                                                 'argument parser.')
    parser.add_argument('-t', '--test', action='store_true', help="Run tests")
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    verbose = False

    if args.verbose:
        verbose = True

    if args.test:
        import doctest
        doctest.testmod(verbose=verbose)
