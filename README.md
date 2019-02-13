Simple, human readable decorators to ensure your method abides to it's contract

## Rules
| Rule                      | sa_int               | sa_float             | sa_string | sa_boolean |
|:--------------------------|:---------------------|:---------------------|:----------|:-----------|
| **not zero**              | `non_zero` (boolean) | `non_zero` (boolean) |           |            |
| **greater than**          | `gt` (int)           | `gt` (int)           |           |            |
| **greater than or equal** | `gte` (int)          | `gte` (int)          |           |            |
| **lesser than**           | `lt` (int)           | `lt` (int)           |           |            |
| **lesser than or equal**  | `lte` (int)          | `lte` (int)          |           |            |

## Demo
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