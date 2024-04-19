from pycheck import *
import time

@check(int_t, int_t)
def add(x,y):
    return x + y

@check(list_of_t(int_t))
def sum(lst):
    thesum = 0
    for l in lst:
        thesum += l
    return thesum

@check(tuple_t)
def ran(r):
    return "is a tuple"

@check(function_t, any_t)
def function_test(fn, arg):
    return fn(arg)

class Lmao:
    steve = 1
    def steve_extra(self):
        return self.steve+1

class Wrong:
    @check(any_t, str_t)
    def greet(self, name):
        return f"hi {name}"

@check(class_t(Lmao))
def takes_lmao(lmao):
    return lmao.steve_extra()

@check(int_t, int_t)
def do_stuff(a, b):
    result = a / 2
    assert_t(float_t, result)
    return result

@check(tuple_of_t(int_t, str_t, list_of_t(int_t)))
def takes_typed_tuple(t):
    return t

class MyClass:
    prop = 0
    def somefun(self):
        return self.prop + 1

@check(class_t(MyClass), tuple_of_t(int_t, int_t, str_t))
def complex_stuff(a, b):
    b1, b2, str_in_b = b
    return str_in_b, a.somefun() + b1 + b2

@check(int_t, int_t, return_t(int_t))
def some_calc(a,b):
    return a+b


@check(dict_t)
def takes_dict(d):
    return d


some_dict = {
     1: "hi",
     "hi": 2,
     }

some_complex_dict = {
        "key0": 1,
        "key1": some_dict
        }

my_type_t = typedef_dict_t({
    1: str_t,
    "hi": int_t,
    })

my_other_type_t = typedef_dict_t({
    "key0": int_t,
    "key1": my_type_t
    })


add(1,2)
sum([1,2,3])
ran((1,"lol"))
function_test(sum, [1,2,3])
takes_lmao(Lmao())
do_stuff(2,2)
takes_typed_tuple((1,"hi", [1,2,3]))
complex_stuff(MyClass(), (1,1, "hi"))
Wrong().greet('marwin')
some_number = assume_t(list_of_t(int_t), [1,2,3]) # runs a check
if(some_number != [1,2,3]):
    raise Error("!!!")
some_calc(1,2)
takes_dict({1: "lol"})
assert_t(my_other_type_t, some_complex_dict)

# some super small basic profiling resulted in the following approximations:
# if you remove all the check decorators and run the lines above 100 times then it is ~7-9 times faster
# -> this takes some time!

# note that the above functions are really small and thus the time difference of execution with and without checking is huge
# if the function does more then the checking will not in take more time, its time requirement is constant
# maybe dont check functions that are THAT simple...
