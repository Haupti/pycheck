# enforce / pycheck

the new version is called enforce.\
its a very basic type checking lib. just copy the 'enforce.py' file in your project, import the 'enforce' decorator and there you go.\
it uses the python type hints to verify the correct types at runtime.\
\
here is a very simple example:
```python

from enforce import enforce

@enforce
def my_function(a: int, b: str, c: list[int, float]) -> int:
    ...
    return a

# type checking will occur here:
my_function(1, "wow", [1, 2.5, 3.8, 9])
```

## general

the decorator requires all function arguments to be typed.\
the decorator requires a return type.

## api

| export prop | type | description |
| ----------- | ---- | ----------- |
| enforce | decorator | runs typechecking on the input parameters and return value of the function it is decorating |
| enable_enforce | function() -> None | enables typechecking globaly (default) |
| disable_enforce | function() -> None | disable typechecking globaly |
| union | type | alias for typing.Union (exported by the typing module) |

