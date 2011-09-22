Data Factory
============
Data factory is a simple data generator easily coupled with your web project. It's main use is to
generate test data for your **orm** during tests.

Random
======
All data generated with data-factory is **random**. That means a factory method does not **always** return a same value.
This is very important because if used in tests, a method that returns only one value covers the TestCase for that
value alone.

If you have a field that can receive a integer and you always give it the same number for testing purpose,
your field will ONLY be tested for that particular number.

If you test your field with data from a range of numbers, like [1,2,3,4,5] even if only one of these numbers is
randomly picked, your field test is safe for that range of numbers (theoretically). The one thing you got to
know is that your tests are better with random data, even if from a finite set of options. Always. If your
set of data covers all the possible input data, even better!

What Data Factory is NOT!
=========================
DataFactory_ is not a object factory for ORMs like ModelMommy_ or DynamicFixture_ as it
only creates raw data, however, DataFactory_ could be easily used to power up a
object factory as it implements most raw generators needed for an object factory.


Supported data
==============
- None (with or_null)
- Boolean
- Choices (pick from list)
- DateTime
- Tiny integer (and positive tiny integer)
- Small integer (and positive small integer)
- Integer (and positive integer)
- Big integer (and positive big integer)
- Decimal (and positive decimal)
- Float (and positive float)
- Binary
- String
- ASCII String
- Unicode String
- Slug_


Usage
=====

>>> from data_factory import get_integer
>>>
>>> random_integer = get_integer()  # gets you a 32bits random integer

About some fields
=================
This section cover some useful information about generated data.

* Positive integer methods were made, mostly, to generate proper values for database unsigned types.
* Positive decimal data is mostly used for monetary values which, usually, can not be negative.

.. _ModelMommy: https://github.com/vandersonmota/model_mommy/
.. _DynamicFixture: http://code.google.com/p/django-dynamic-fixture/
.. _Slug: is a newspaper term. A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They're generally used in URLs. (ref:https://docs.djangoproject.com/en/1.3/ref/models/fields/#slugfield)
.. _DataFactory: https://github.com/italomaia/data-factory/

