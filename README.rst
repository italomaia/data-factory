.. image:: https://travis-ci.org/italomaia/data-factory.svg?branch=master
  :target: https://travis-ci.org/italomaia/data-factory

.. image:: https://coveralls.io/repos/italomaia/flask-empty/badge.png
  :target: https://coveralls.io/r/italomaia/flask-empty

Data Factory
============
Data factory is a simple data generator easily coupled with your web project. It's main use is to
generate data for your **orm** during tests.

Random
======
All data generated with data-factory is **pseudo-random**. That means a factory
method does not **always** return the same value, but it always return the
same "kind of value" you expect. This is very important because
this way your tests became **fuzzy**.

If you have a field in your model that can receive a integer of any kind and
you always give it the same number for testing purpose, your field will *ONLY*
be tested for that particular number.

If you test your model field with data from a range of numbers (like the field domain),
like [1,2,3,4,5] even if only one of these numbers is randomly picked each time,
your field test is safe for the whole range of numbers (theoretically). That's
fuzzy testing!

What Data Factory is NOT!
=========================
DataFactory_ is not a object factory for ORM's, like ModelMommy_ or
DynamicFixture_. It only creates the right raw fuzzy data that you expect.
However, DataFactory_ could be easily used to power up a object factory as
it tries to give you just the right range for the most common types.


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
- Real
- Double
- Binary
- String
- ASCII String
- Unicode String
- Slug_


Usage
=====

>>> from data_factory import make_integer, make_small_integer
>>> random_integer = make_integer()  # gets you a 32bits random integer
>>> random_small_integer = make_small_integer()  # gets you a 16bits random integer

About some fields
=================
This section cover some useful information about generated data.

* Positive integer methods were made, mostly, to generate proper values for database unsigned types.
* Positive decimal data is mostly used for monetary values which, usually, can not be negative.

.. _ModelMommy: https://github.com/vandersonmota/model_mommy/
.. _DynamicFixture: http://code.google.com/p/django-dynamic-fixture/
.. _Slug: is a newspaper term. A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They're generally used in URLs. (ref:https://docs.djangoproject.com/en/1.3/ref/models/fields/#slugfield)
.. _DataFactory: https://github.com/italomaia/data-factory/

