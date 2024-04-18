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


add(1,2)
sum([1,2,3])
ran((1,"lol"))
function_test(sum, [1,2,3])


