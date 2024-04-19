# pycheck

this is a super simple single-header (or whatever this would be in python) lib.\
just copy pycheck.py into your project and import it, then u can use it.

## how does it work

this lib privides:
* a decorator for runtime checking the types of the function arguments and return value
* `assert_t` function for checks inside functions
* `assume_t` function for checked assignments

the decorator takes the types as arguments, that your funciton is expecting.\
optionally you can add return value check as last argument (see examples).\
it then runs a check on all given arguments when you call the function to verify they are what you told the decorator they are.\

## how to use

there are examples in the test.py file.

however:

```
@check(int_t, int_t)
def do_stuff(a, b):
    result = a / 2
    assert_t(float_t, result)
    return result
```

the `check` decorator will check that, when called, the arguments given are of type int and will raise an TypeError if they are not.\
also it will check, that there are, in fact, two arguments.\
the `assert_t` will check if the `result` variable is of type `float` and raise a TypeError if it is not.

```
class MyClass:
    prop = 0
    def somefun(self):
        return self.prop + 1

@check(class_t(MyClass), tuple_of_t(int_t, int_t, str_t))
def do_stuff(a, b):
    b1, b2, str_in_b = b
    print(str_in_b, a.somefun() + b1 + b2)
```

the `class_t` takes a class type as argument and checks if all members of the class type (expected) are present in the object `a`.\
this does not neccessarily mean, that `a` must be of type `MyClass` but, that all members of the expected type `MyClass` are in fact in `a`.\
i.e. `a` could have more members, thats ok.\
**IMPORTANT**: this does **NOT** check the type of the members!\
\
the `tuple_of_t(int_t,int_t, str_t)` part checks that the second argument is of type `tuple` and that it has three entries which are **in order** of types: `int`, `int`, `str`.\
\
another one:

```
@check(int_t, int_t, return_t(int_t))
def some_calc(a,b):
    return a+b
```

in this case the first two arguments of the `check` function check the input values of the function during runtime.\
the third one is used to verify the return type of the function after its execution.\
\
and the last one:
```
def my_calc_long(b):
    ...
    assert_t(list_of_t(int_t), b)
    some_numbers = b
    ...


def my_calc(b):
    ...
    some_numbers = assume_t(list_of_t(int_t), b)
    ...
```

unlike the `assert_t` function the `assume_t` function returns the second argument it is given, but also performs the same check as `assert_t` does.
this is simply anohter utility function.




