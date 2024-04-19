from typing import *

__NO_RETURN_TYPE = 0

def __is_one_of(types_t, arg) -> bool:
    return any(__assert_type(type_t, arg)[0] for type_t in types_t)

def __assert_type(type_t, arg) -> (bool, str):
    match type_t.__name__:
        case "list":
            if type(arg).__name__ != "list":
                return (False, f"expected '{arg}' to be of type 'list' but actual is of type '{type(arg).__name__}'")
            return (all(__is_one_of(type_t.__args__, arg_elem) for arg_elem in arg), f"expected all elements in '{arg}' to be of type 'oneof{type_t.__args__}'")
        case "int" | "str" | "float" | "bool":
            return (isinstance(arg, type_t), f"expected '{arg}' to be of type '{type_t.__name__}' but is of type '{type(arg).__name__}'")
        case _ :
            return (False, "type not checked")

def __enforce(fn, args):
    names = fn.__code__.co_varnames
    types = get_type_hints(fn)
    type_keys = types.keys()

    for index, name in enumerate(names):
        is_success, msg = __assert_type(types[name], args[index])
        if not is_success:
            raise TypeError(msg)
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
def my_func(a: list[int, list[float]], b: int) -> int:
    return a[0]

my_func([1, [1.5]], 1)
