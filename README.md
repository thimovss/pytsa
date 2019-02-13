Simple, human readable decorators to ensure your method abides to it's contract for Python

## Rules
| Rule                      | sa_int            | sa_float          | sa_bool | sa_string          |
|:--------------------------|:------------------|:------------------|:--------|:-------------------|
| **not zero**              | `non_zero` (bool) | `non_zero` (bool) |         |                    |
| **greater than**          | `gt` (int)        | `gt` (float)      |         |                    |
| **greater than or equal** | `gte` (int)       | `gte` (float)     |         |                    |
| **lesser than**           | `lt` (int)        | `lt` (float)      |         |                    |
| **lesser than or equal**  | `lte` (int)       | `lte` (float)     |         |                    |
| **modulo**                | `mod` (int)       | `mod` (float)     |         |                    |
| **not empty**             |                   |                   |         | `not_empty` (bool) |
| **not blank**             |                   |                   |         | `not_blank` (bool) |

| Rule                      | Description                                                                                                                                                                                                                                                                                                                                                                    |
|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **not zero**              | ensure the argument does not equal 0.<br>with rule `non_zero=True` and `call(0)` => Exception<br>with rule `non_zero=True` and `call(1)` => Accepted                                                                                                                                                                                                                           |
| **greater than**          | ensure the argument is greater than the rule value.<br>with rule `gt=3` and `call(2)` => Exception<br>with rule `gt=3` and `call(3)` => Exception<br>with rule `gt=3` and `call(4)` => Accepted                                                                                                                                                                                |
| **greater than or equal** | ensure the argument is greater than, or equal to the rule value.<br>with rule `gte=3` and `call(2)` => Exception<br>with rule `gte=3` and `call(3)` => Accepted<br>with rule `gte=3` and `call(4)` => Accepted                                                                                                                                                                 |
| **lesser than**           | ensure the argument is lesser than the rule value.<br>with rule `lt=3` and `call(2)` => Accepted<br>with rule `lt=3` and `call(3)` => Exception<br>with rule `lt=3` and `call(4)` => Exception                                                                                                                                                                                 |
| **lesser than or equal**  | ensure the argument is lesser than, or equal to the rule value.<br>with rule `lte=3` and `call(2)` => Accepted<br>with rule `lte=3` and `call(3)` => Accepted<br>with rule `lte=3` and `call(4)` => Exception                                                                                                                                                                  |
| **modulo**                | ensure the argument is a multiple of the rule value.<br>with rule `mod=4` and `call(6)` => Exception<br>with rule `mod=4` and `call(4)` => Accepted<br>with rule `mod=4` and `call(-4)` => Accepted<br>with rule `mod=4` and `call(0)` => Accepted                                                                                                                             |
| **not empty**             | ensure the argument is not an empty string.<br>with rule `not_empty=True` and `call('')` => Exception<br>with rule `not_empty=True` and `call(' ')` => Accepted<br>with rule `not_empty=True` and `call('abc')` => Accepted                                                                                                                                                    |
| **not blank**             | ensure the argument is not an empty string, or contains only whitespace characters, according to `Python String.isspace()`.<br>with rule `not_empty=True` and `call('')` => Exception<br>with rule `not_empty=True` and `call(' ')` => Exception<br>with rule `not_empty=True` and `call('\t \n   ')` => Exception<br>with rule `not_empty=True` and `call('abc')` => Accepted |

## Demo
Want a demo of other rules? check out the test directory, it has an example for every rule there is!
```
@sa_int('val', gt=0, lte=10)
def assign_score(val)
    ""assign an integer score higher than 0, up to 10""
    print('set score to {val}')
    score = val

assign_score(5)

assign_score(0)
> int argument val with value 0 was not greater than 0

assign_score('abc')
> int argument val with value 'abc' was of type string, not of type 'int'

assign_score(None)
> int argument val was None

assign_score(3.5)
> int argument val with value 0 was not greater than 0
```