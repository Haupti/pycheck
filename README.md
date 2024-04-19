# pycheck

this is a super simple single-header (or whatever this would be in python) lib.\
just copy pycheck.py into your project and import it, then u can use it.

## how does it work

this lib privides:
* a decorator for runtime checking the types of the function arguments and return value
* `assert_t` function for checks inside functions
* `assume_t` function for checked assignments
* `typedef_dict_t` function which creates a type checking function for a given dictionary structure

the decorator takes the types as arguments, that your funciton is expecting.\
optionally you can add return value check as last argument (see examples).\
it then runs a check on all given arguments when you call the function to verify they are what you told the decorator they are.\

## how to use

there are examples in the test.py file.

however:

```python
@check(int_t, int_t)
def do_stuff(a, b):
    result = a / 2
    assert_t(float_t, result)
    return result
```

the `check` decorator will check that, when called, the arguments given are of type int and will raise an TypeError if they are not.\
also it will check, that there are, in fact, two arguments.\
the `assert_t` will check if the `result` variable is of type `float` and raise a TypeError if it is not.

```python
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

```python
@check(int_t, int_t, return_t(int_t))
def some_calc(a,b):
    return a+b
```

in this case the first two arguments of the `check` function check the input values of the function during runtime.\
the third one is used to verify the return type of the function after its execution.\
\
and another one:
```python
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

unlike the `assert_t` function the `assume_t` function returns the second argument it is given, but also performs the same check as `assert_t` does.\
this is simply anohter utility function.\


### the `typedef_dict_t` function

this one is kind of special, which is why i have a separate section for it.\
using this, you can define your own type checking function for dictionary types.\
here is an example:
```python
my_type_t = typedef_dict_t({
    "some_key" : int_t,
    123: str_t,
    "some_other_key": list_of_t(int_t),
    })

@check(my_type_t)
def does_stuff(d):
    fst = d["some_key"]
    snd = fst + d["some_other_key"][0]
    return snd
```

this way it is verified that the thing given contains all keys that are defined in `my_type_t`, and all of them are of the type specified.\
this does **not** check if the required keys form `my_type_t` are the only keys in the dictionary. so there can be more.

### the `typedef_t` function

with this you can create type check that check the arguments against one of the allowed values:\
```python
my_type_t = typedef_t("first option", "second option", 5, True)
assert_t(my_type_t, "oh no") # -> raises TypeError
```
