from pycheck import *

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

some_calc(1,2)
