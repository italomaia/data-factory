Data Factory
============
Data factory is a simple data generator easily coupled with your web project. It's main use is to
generate test data for your orm during tests.

All data generated with data-factory is *random*. That means a factory method does not "always" return a same value.
This is very important because if used in tests, a method that returns only one value covers the TestCase for that
value alone.

By that, I mean that if you have a field that can receive a integer and you always give it the same number, during
tests, like 5, your field will only be tested for that particular number ONLY! If you test your field with a range
of numbers, like [1,2,3,4,5] even if only one of these numbers is randomly picked, your field test is safe for
that range of numbers (theoretically). The one thing you got to know is that your tests are better with random data,
even if from a finite set of options. Always. If your set of data covers all the possible input data, even better!

What Data Factory is NOT!
=========================
Data Factory is not a object factory for ORM's like ModelMommy_

Supported data
==============
- Tiny integer (and positive tiny integer)
- Small integer (and positive small integer)
- Integer (and positive integer)
- Big integer (and positive big integer)
- Decimal (and positive decimal)
- Float (and positive float)
- Binary
- String
- Text (string with newline character)
- Slug_


About some fields
=================
This section cover some useful information about generated data.
- Positive integer methods were made, mostly, to generate proper values for database unsigned types.
- .. _Slug: is a newspaper term. A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They're generally used in URLs. (ref:https://docs.djangoproject.com/en/1.3/ref/models/fields/#slugfield)
- Positive decimal data is mostly used for monetary values which, usually, can not be negative.
-

.. _ModelMommy: https://github.com/vandersonmota/model_mommy/
