[![Build Status](https://travis-ci.org/thimovss/pytsa.svg?branch=master)](https://travis-ci.org/thimovss/pytsa)[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)[![Python 3.5](https://img.shields.io/badge/python-3.5-green.svg)](https://www.python.org/downloads/release/python-350/)[![Python 3.4](https://img.shields.io/badge/python-3.4-green.svg)](https://www.python.org/downloads/release/python-340/)
# PYThon StrictArguments
Simple, human readable decorators to ensure your method abides to it's contract for Python
## Install
```$ pip install pytsa```   
https://pypi.org/project/pytsa
## Rules
String **`@sa_string`**

Rule | Description
--- | ---
**not_empty**(bool)|ensure the argument is not an empty string.
**not_blank**(bool)|ensure the argument is not an empty string, or contains only whitespace characters, according to Python String.isspace().
**ends_with**(string)|ensure the argument ends with the rule value, according to Python String.endswith().
**starts_with**(string)|ensure the argument starts with the rule value, according to Python String.startswith().
**contains**(string)|ensure the argument contains the rule value, according to Python String.find().
**is_lower**(bool)|ensure all non-whitespace characters in the argument are lowercase.
**is_upper**(bool)|ensure all non-whitespace characters in the argument are uppercase.
**regex**(string)|ensure the argument matches the regex using Python re.search().

Integer **`@sa_int`**:

Rule | Description
--- | ---
**non_zero**(bool)|ensure the argument does not equal 0.
**gt**(int)|ensure the argument is greater than the rule value.
**gte**(int)|ensure the argument is greater than, or equal to the rule value.
**lt**(int)|ensure the argument is lesser than the rule value.
**lte**(int)|ensure the argument is lesser than, or equal to the rule value.
**mod**(int)|ensure the argument is a multiple of the rule value.

Float **`@sa_float`**:

Rule | Description
--- | ---
**non_zero**(bool)|ensure the argument does not equal 0.0.
**gt**(float)|ensure the argument is greater than the rule value.
**gte**(float)|ensure the argument is greater than, or equal to the rule value.
**lt**(float)|ensure the argument is lesser than the rule value.
**lte**(float)|ensure the argument is lesser than, or equal to the rule value.
**mod**(float)|ensure the argument is a multiple of the rule value.

Boolean **`@sa_bool`**:

there are no rules for bool available.

## Rule examples

### String `sa_string`
**not_empty(bool)**: ensure the argument is not an empty string.
```
@sa_string('x', not_empty=True)
call(x):
    return x

call('') => Exception
call(' ') => Accepted
call('abc') => Accepted
```
**not_blank(bool)**: ensure the argument is not an empty string, or contains only whitespace characters, according to Python String.isspace().
```
@sa_string('x', not_blank=True)
call(x):
    return x

call('') => Exception
call(' ') => Exception
call('\t \n ') => Exception
call('abc') => Accepted
```
**ends_with(string)**: ensure the argument ends with the rule value, according to Python String.endswith().
```
@sa_string('x', ends_with='ab')
call(x):
    return x

call('ab1') => Exception
call('') => Exception
call('cab') => Accepted
call('123ab') => Accepted
```
**starts_with(string)**: ensure the argument starts with the rule value, according to Python String.startswith().
```
@sa_string('x', starts_with='ab')
call(x):
    return x

call('1ab') => Exception
call('') => Exception
call('abc') => Accepted
call('ab123') => Accepted
```
**contains(string)**: ensure the argument contains the rule value, according to Python String.find().
```
@sa_string('x', contains='ab')
call(x):
    return x

call('a b') => Exception
call('a1b') => Exception
call('abcd') => Accepted
call('12ab34') => Accepted
```
**is_lower(bool)**: ensure all non-whitespace characters in the argument are lowercase.
```
@sa_string('x', is_lower=True)
call(x):
    return x

call('ABC') => Exception
call('aBc') => Exception
call('abc') => Accepted
call(' ! ') => Accepted 
call('') => Accepted
```
**is_upper(bool)**: ensure all non-whitespace characters in the argument are uppercase.
```
@sa_string('x', is_upper=True)
call(x):
    return x

call('abc') => Exception
call('AbC') => Exception
call('12AB34') => Accepted
call(' ! ') => Accepted
call('') => Accepted
```
**regex(string)**: ensure the argument matches the regex using Python re.search().
```
@sa_string('x', regex='test[12]')
call(x):
    return x

call('test3') => Exception
call('test2') => Accepted
call('test1') => Accepted
```

### Boolean `sa_bool`
there are no rules for bool available.

### Integer `sa_int`
**non_zero(bool)**: ensure the argument does not equal 0.
```
@sa_int('x', non_zero=True)
call(x):
    return x

call(0) => Exception
call(1) => Accepted
```
**gt(int)**: ensure the argument is greater than the rule value.
```
@sa_int('x', gt=3)
call(x):
    return x

call(2) => Exception
call(3) => Exception
call(4) => Accepted
```
**gte(int)**: ensure the argument is greater than, or equal to the rule value.
```
@sa_int('x', gte=3)
call(x):
    return x

call(2) => Exception
call(3) => Accepted
call(4) => Accepted
```
**lt(int)**: ensure the argument is lesser than the rule value.
```
@sa_int('x', lt=3)
call(x):
    return x

call(2) => Accepted
call(3) => Exception
call(4) => Exception
```
**lte(int)**: ensure the argument is lesser than, or equal to the rule value.
```
@sa_int('x', lte=3)
call(x):
    return x
    
call(2) => Accepted
call(3) => Accepted
call(4) => Exception
```
**mod(int)**: ensure the argument is a multiple of the rule value.
```
@sa_int('x', mod=4)
call(x):
    return x
    
call(6) => Exception
call(4) => Accepted
call(-4) => Accepted
call(0) => Accepted
```

### Float `sa_float`
**non_zero(bool)**: ensure the argument does not equal 0.0.
```
@sa_float('x', non_zero=True)
call(x):
    return x

call(0.0) => Exception
call(1.0) => Accepted
```
**gt(float)**: ensure the argument is greater than the rule value.
```
@sa_float('x', gt=3.0)
call(x):
    return x

call(2.0) => Exception
call(3.0) => Exception
call(4.0) => Accepted
```
**gte(float)**: ensure the argument is greater than, or equal to the rule value.
```
@sa_float('x', gte=3.0)
call(x):
    return x

call(2.0) => Exception
call(3.0) => Accepted
call(4.0) => Accepted
```
**lt(float)**: ensure the argument is lesser than the rule value.
```
@sa_float('x', lt=3.0)
call(x):
    return x

call(2.0) => Accepted
call(3.0) => Exception
call(4.0) => Exception
```
**lte(float)**: ensure the argument is lesser than, or equal to the rule value.
```
@sa_float('x', lte=3.0)
call(x):
    return x
    
call(2.0) => Accepted
call(3.0) => Accepted
call(4.0) => Exception
```
**mod(float)**: ensure the argument is a multiple of the rule value.
```
@sa_float('x', mod=4.0)
call(x):
    return x
    
call(6.0) => Exception
call(4.0) => Accepted
call(-4.0) => Accepted
call(0.0) => Accepted
```

### List `sa_list`
**len(int)**: ensure the argument has the given length. None is counted in the length.
```
@sa_list('x', len=3)
call(x):
    return x

call([1, 2, 3]) => Accepted
call([1, 2]) => Exception
call([1, 2, 3, None]) => Exception
```
**type(type)**: ensure all the values in the list are of the given type.

**! Warning: this will iterate the whole list everytime the method is called, this could cause performance issues.**  
*Tip: make sure not to call as type=type(int), as this will check if everything is of type type, instead of int*
```
@sa_list('x', type=3)
call(x):
    return x

call([1.0, 2.0]) => Exception
call([1, None, 3]) => Exception
call([1, 2, 3]) => Accepted
call([]) => Accepted
```
**not_empty(bool)**: ensure the argument is not an empty list
```
@sa_list('x', not_empty=True)
call(x):
    return x

call([]) => Exception
call([1, 2, 3]) => Accepted
call([None]) => Accepted
call(['a', 1.2, 3]) => Accepted
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

assign_score(0)
> Error: int argument val with value 0 was not greater than 0

assign_score('abc')
> Error: int argument val with value 'abc' was of type string, not of type 'int'

assign_score(None)
> Error: int argument val was None

assign_score(3.5)
> Error: int argument val with value 0 was not greater than 0
```
