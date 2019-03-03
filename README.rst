
.. image:: https://img.shields.io/pypi/pyversions/pytsa.svg
   :target: https://github.com/thimovss/pytsa/
.. image:: http://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/thimovss/pytsa/blob/master/LICENSE
.. image:: http://img.shields.io/travis/thimovss/pytsa.svg
   :target: https://travis-ci.org/thimovss/pytsa
.. image:: https://coveralls.io/repos/github/thimovss/pytsa/badge.svg
   :target: https://coveralls.io/github/thimovss/pytsa

PYThon StrictArguments
======================

Simple, human-readable, fully tested, signature-preserving Python decorators to ensure your method abides to its contract.
Get rid of testing all those edge cases for passed arguments, by making the method's contract more strict!

Install
-------

| ``$ pip install pytsa``
| `https://pypi.org/project/pytsa <https://pypi.org/project/pytsa>`__

How to use
----------

| Pytsa provides decorators for most python types.
| These decorators allow you to verify that the arguments passed to your
  method are of a certain type and/or follow the rules you specify.
| The decorator name specifies the type you expect, for example sa_int
  if you expect an integer.
| The first argument of the decorator is the name of the parameter this
  decorator applies to.
| The arguments after the first one specify the rules this parameter has
  to follow, if any.
| ``@sa_TYPE(PARAM_NAME, RULE1=RULE1_VAL, RULE2=RULE2_VAL)``
| For example,

::

   @sa_string('a', starts_with='a', ends_with='c', is_lower=True, contains='1')
   def foo(a):
       ...

::

   @sa_path('b', is_dir=True, is_abs=True)
   def bar(b):
       ...

::

   @sa_list('c', len=8, type=float)
   def foo(a, b, c):
       ...

::

   @sa_int('d', gt=-4, lte=4, non_zero=True, mod=2)
   def bar(d):
       ...

Demo
----

Want a demo of other rules? check out the test directory, it has an
example for every rule there is!

::

   from pytsa import sa_int

   @sa_int('val', gt=0, lte=10)
   def assign_score(val)
       ""assign an integer score higher than 0, up to 10""
       print('set score to {val}')
       score = val

   assign_score(5)
   > set score to 5

   assign_score(0)
   > Error: int argument val with value 0 was not greater than 0

   assign_score('abc')
   > Error: int argument val with value 'abc' was of type string, not of type 'int'

   assign_score(None)
   > Error: int argument val was None

   assign_score(35)
   > Error: int argument val with value 35 was not less than, or equal to 10

Rules
-----

For a more a more detailed description on the behaviour of a rule, make
sure to check out its test cases! Not sure how @sa_list's len handles
None type? see `'test/test_sa_list.py'
test_rule_len() <https://github.com/thimovss/pytsa/blob/master/test/test_sa_list.py>`__

All rules
~~~~~~~~~

====================== =======================================================================================================================================================================================================================================
Rule                   Description
====================== =======================================================================================================================================================================================================================================
**allow_none**\ (bool) By default, no rule allows a value of None. This can be circumvented with the rule **``allow_none``**\ (bool), which is available for every rule. **important!**: If the value provided is None, all other checks will not be executed!
====================== =======================================================================================================================================================================================================================================

String ``@sa_string``
~~~~~~~~~~~~~~~~~~~~~~~~~

========================= =====================================================================================================================
Rule                      Description
========================= =====================================================================================================================
**not_empty**\ (bool)     ensure the argument is not an empty string.
**not_blank**\ (bool)     ensure the argument is not an empty string, or contains only whitespace characters. According to ``string.isspace()``
**ends_with**\ (string)   ensure the argument ends with the rule value. According to ``string.endswith()``
**starts_with**\ (string) ensure the argument starts with the rule value. According to ``string.startswith()``
**contains**\ (string)    ensure the argument contains the rule value. According to ``string.find()``
**is_lower**\ (bool)      ensure all non-whitespace characters in the argument are lowercase.
**is_upper**\ (bool)      ensure all non-whitespace characters in the argument are uppercase.
**regex**\ (string)       ensure the argument matches the regex. According to ``re.search()``
========================= =====================================================================================================================

Number (Float, Integer) ``@sa_number`` ``@sa_float`` ``@sa_int``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| The rule @sa_number accepts both integer and float values.
| The rules @sa_number, @sa_int, and @sa_float share the same rule set.
| The rules @sa_int and @sa_float only accept arguments of their
  respective types, but accept both floats and integers as values to
  their rules.

==================== ================================================================
Rule                 Description
==================== ================================================================
**non_zero**\ (bool) ensure the argument does not equal 0 or 0.0.
**gt**\ (number)     ensure the argument is greater than the rule value.
**gte**\ (number)    ensure the argument is greater than, or equal to the rule value.
**lt**\ (number)     ensure the argument is lesser than the rule value.
**lte**\ (number)    ensure the argument is lesser than, or equal to the rule value.
**mod**\ (number)    ensure the argument is a multiple of the rule value.
==================== ================================================================

Boolean ``@sa_bool``:
~~~~~~~~~~~~~~~~~~~~~~~~~

there are no rules for bool available.

List ``@sa_list``:
~~~~~~~~~~~~~~~~~~~~~~

**! Warning: some tests such as type will brute-force the whole list
every time the method is called, this could cause performance issues.**

===================== ====================================================================================================================================================================================
Rule                  Description
===================== ====================================================================================================================================================================================
**type**\ (type)      ensure all the values in the list are of the given type. (*Tip: make sure not to call as ``type=type(int)``, as this will check if everything is of type type, instead of type int*)
**len**\ (int)        ensure the argument has the given length. None is counted in the length.
**not_empty**\ (bool) ensure the argument is not an empty list
===================== ====================================================================================================================================================================================

Path ``@sa_path``:
~~~~~~~~~~~~~~~~~~~~~~

============================== ========================================================================================
Rule                           Description
============================== ========================================================================================
**exists**\ (bool)             ensure that the argument is an existing path. According to ``os.path.exists()``
**is_dir**\ (bool)             ensure the argument is an existing path to a directory. According to ``os.path.isdir()``
**is_file**\ (bool)            ensure the argument is an existing path to a file. According to ``os.path.isfile()``
**is_abs**\ (bool)             ensure the argument is an absolute path. According to ``os.path.isabs()``
**can_owner_read**\ (bool)     ensure the owner has read permission.
**can_group_read**\ (bool)     ensure the group has read permission.
**can_others_read**\ (bool)    ensure the others has read permission.
**can_owner_write**\ (bool)    ensure the owner has write permission.
**can_group_write**\ (bool)    ensure the group has write permission.
**can_others_write**\ (bool)   ensure the others has write permission.
**can_owner_execute**\ (bool)  ensure the owner has execute permission.
**can_group_execute**\ (bool)  ensure the group has execute permission.
**can_others_execute**\ (bool) ensure the others has execute permission.
============================== ========================================================================================

Production
==========

| You might want to disable the processing of Pytsa decorators for your
  production deployments cause of performance reasons.
| Pytsa can be disabled by setting the environment variable
  'PYTSA_DISABLED' to 'True'

License
=======

licensed under the `MIT
License <https://github.com/thimovss/pytsa/blob/master/LICENSE>`__
