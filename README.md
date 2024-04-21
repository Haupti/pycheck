# enforce

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

if you want to double check within your functions, you can use the `enforced` function:
```python
def my_other_function(a):
    return enforced(a, int)

# type checking will occur here:
my_other_function(1)
```

## general

the decorator requires all function arguments to be typed.\
the decorator requires a return type.\
there is no typechecking of a function without the decorator.\
*note:*
*typechecking takes time. especially if you are typechecking large lists. to verify that the list is of the correct type,*
*enforce has to iterate over the list.*


## api

| export prop | type | description |
| ----------- | ---- | ----------- |
| enforce | decorator | runs typechecking on the input parameters and return value of the function it is decorating |
| enforced | function | runs typechecking on the input parameter and then returns the value, raises TypeError if the type is not matched |
| enable_enforce | function() -> None | enables typechecking globaly (default) |
| disable_enforce | function() -> None | disable typechecking globaly |
| union | type | alias for typing.Union (exported by the typing module) |
| function | type | alias for types.FunctionType (exported by the types module) |



## which types are supported
at the moment, the following types are supported:
| type | examples | the parameter annotated with this type... |
| --- | --- | --- |
| int | 1, 2, 3 | ... must be of type int (bool is **not** treated as an int) |
| float | 1.1, 2.2, 3.0 | ... must be of type float |
| str | "wow" | ... must be of type str |
| bool | True | ... must be of type bool (bool is **not** treated as an int) |
| function | |  ... must be of type function (lambda or function, but **not** a class method) |
| any | |  ...is not checked |
| None | | ... must not be there or explicity None (works for return/no returns) |
| union | union[int, float] | ... must be of either of type int or float |
| list[\<types\>] | list[int, float] | ... must be a list and all elements must be either of type int or of type float |
|  | list[str] | ... must be a list and all elements in this list must be of type str |
| tuple[\<types\>] | tuple[str, int] | ... must be a tuple and all elements in the given tuple must be of the types hinted (in order) |
| \<class\> |  | ... must be an object the class in the annotation |

for the class case here is another example:
```python
class Person:
    name = "steve"

    @enfoce
    def getMyName(self: any) -> str:
        return self.name

@enforce
def getName(p: Person) -> str:
    return p.getMyName()


#  type checking will occur here:
getName(Person())
```

