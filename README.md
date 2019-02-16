[![Build Status](https://travis-ci.org/thimovss/pytsa.svg?branch=master)](https://travis-ci.org/thimovss/pytsa)[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)[![Python 3.5](https://img.shields.io/badge/python-3.5-green.svg)](https://www.python.org/downloads/release/python-350/)[![Python 3.4](https://img.shields.io/badge/python-3.4-green.svg)](https://www.python.org/downloads/release/python-340/)
# PYThon StrictArguments
Simple, human readable decorators to ensure your method abides to it's contract for Python
## Install
```$ pip install pytsa```   
https://pypi.org/project/pytsa
## How to use
Pytsa provides decorators for most python types.  
These decorators allow you to verify that the arguments passed to your method are of a certain type and/or follow the rules you specify.  
The decorator name specifies the type you expect, for example sa_int if you expect an integer.  
The first argument of the decorator is the name of the parameter this decorator applies to.  
The arguments after the first one specify the rules this parameter has to follow, if any.  
`@sa_TYPE(PARAM_NAME, RULE1=RULE1_VAL, RULE2=RULE2_VAL)`  
For example,
```
@sa_string('a', starts_with='a', ends_with='c', is_lower=True, contains='1')
```
```
@sa_path('b', is_dir=True, is_abs=True)
```
```
@sa_list('c', len=8, type=float)
```
```
@sa_int('d', gt=-4, lte=4, non_zero=True, mod=2)
```
## Demo
Want a demo of other rules? check out the test directory, it has an example for every rule there is!
```
from src.pytsa import sa_int

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
```
## Rules
For a more a more detailed description on the behaviour of a rule, make sure to check out its test cases!
Not sure how @sa_list's len handles None type? see ['test/test_sa_list.py' test_rule_len()](https://github.com/thimovss/pytsa/blob/master/test/test_sa_list.py)

### String **`@sa_string`**

Rule | Description
--- | ---
**not_empty**(bool)|ensure the argument is not an empty string.
**not_blank**(bool)|ensure the argument is not an empty string, or contains only whitespace characters. According to `string.isspace()`
**ends_with**(string)|ensure the argument ends with the rule value. According to `string.endswith()`
**starts_with**(string)|ensure the argument starts with the rule value. According to `string.startswith()`
**contains**(string)|ensure the argument contains the rule value. According to `string.find()`
**is_lower**(bool)|ensure all non-whitespace characters in the argument are lowercase.
**is_upper**(bool)|ensure all non-whitespace characters in the argument are uppercase.
**regex**(string)|ensure the argument matches the regex. According to `re.search()`

### Integer **`@sa_int`**:

Rule | Description
--- | ---
**non_zero**(bool)|ensure the argument does not equal 0.
**gt**(int)|ensure the argument is greater than the rule value.
**gte**(int)|ensure the argument is greater than, or equal to the rule value.
**lt**(int)|ensure the argument is lesser than the rule value.
**lte**(int)|ensure the argument is lesser than, or equal to the rule value.
**mod**(int)|ensure the argument is a multiple of the rule value.

### Float **`@sa_float`**:

Rule | Description
--- | ---
**non_zero**(bool)|ensure the argument does not equal 0.0.
**gt**(float)|ensure the argument is greater than the rule value.
**gte**(float)|ensure the argument is greater than, or equal to the rule value.
**lt**(float)|ensure the argument is lesser than the rule value.
**lte**(float)|ensure the argument is lesser than, or equal to the rule value.
**mod**(float)|ensure the argument is a multiple of the rule value.

### Boolean **`@sa_bool`**:

there are no rules for bool available.

### List **`@sa_list`**:
**! Warning: some tests such as type will brute-force the whole list every time the method is called, this could cause performance issues.**  

Rule | Description
--- | ---
**type**(type)|ensure all the values in the list are of the given type. (*Tip: make sure not to call as `type=type(int)`, as this will check if everything is of type type, instead of type int*)
**len**(int)|ensure the argument has the given length. None is counted in the length.
**not_empty**(bool)|ensure the argument is not an empty list


### Path **`@sa_path`**:

Rule | Description
--- | ---
**exists**(bool)|ensure that the argument is an existing path. According to `os.path.exists()`
**is_dir**(bool)|ensure the argument is an existing path to a directory. According to `os.path.isdir()`
**is_file**(bool)|ensure the argument is an existing path to a file. According to `os.path.isfile()`
**is_abs**(bool)|ensure the argument is an absolute path. According to `os.path.isabs()`

# License
licensed under the [MIT License](https://github.com/thimovss/pytsa/blob/master/LICENSE)
