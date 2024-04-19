from typing import *

__NO_RETURN_TYPE = 0

__CHECK_FAILURE = False
__CHECK_SUCCESS = True
__CHECK_ERROR = -1

class EnforceError(Exception):
    pass

def __show_types(types_t):
    if(len(types_t.__args__) == 1):
        return f"[{types_t.__args__[0].__name__}]"
    else:
        return list(map(lambda x: x.__name__, types_t.__args__))

def __is_one_of(types_t, arg) -> bool:
    return any(__assert_type(type_t, arg)[0] for type_t in types_t)

def __assert_type(type_t, arg) -> (bool, str):
    match type_t.__name__:
        case "list":
            if type(arg).__name__ != "list":
                return (__CHECK_FAILURE, f"expected '{arg}' to be of type 'list' but actual is of type '{type(arg).__name__}'")
            return (all(__is_one_of(type_t.__args__, arg_elem) for arg_elem in arg), f"expected all elements in '{arg}' to be of type 'oneof{__show_types(type_t)}'")
        case "int" | "str" | "float" | "bool":
            return (isinstance(arg, type_t), f"expected '{arg}' to be of type '{type_t.__name__}' but is of type '{type(arg).__name__}'")
        case _ :
            return (__CHECK_ERROR, f"type '{type_t.__name__}' cannot be enfoced")

def __enforce(fn, args):
    names = fn.__code__.co_varnames
    types = get_type_hints(fn)
    type_keys = types.keys()

    for index, name in enumerate(names):
        result, msg = __assert_type(types[name], args[index])
        if(__CHECK_FAILURE):
            raise TypeError(f"'{name}' has wrong type: {msg}")
        elif(__CHECK_ERROR):
                raise EnforceError(msg)

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
def my_func(a: tuple[int, float], b: int) -> int:
    return a[0]

my_func([1, "b"], 1)
