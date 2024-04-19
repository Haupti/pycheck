from typing import *

__NO_RETURN_TYPE = 0

def __enforce(fn, args):
    names = fn.__code__.co_varnames
    types = get_type_hints(fn)
    type_keys = types.keys()

    for index, name in enumerate(names):
        if(name in type_keys):
            if not type(args[index]) == types[name]:
                raise TypeError(f"expected type of '{name}' is {types[name]}, but actual was {type(args[index])}")
    try:
        return types['return']
    except KeyError:
        return __NO_RETURN_TYPE

def __return(type_t, val):
    if(type(val) == type_t):
        return val
    else:
        raise TypeError(f"expected return type {type_t} but was {type(val)}")

def enforce(fn):
    def wrapper(*args):
        return_type = __enforce(fn, args)
        if(return_type == __NO_RETURN_TYPE):
            return fn(*args)
        else:
            __return(return_type, fn(*args))
    return wrapper

@enforce
def my_func(a: int, b:int) -> int:
    return b

my_func(1,2)
