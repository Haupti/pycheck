from typing import *

__NO_RETURN_TYPE = 0

__CHECK_FAILURE = False
__CHECK_SUCCESS = True
__CHECK_ERROR = -1

class EnforceError(Exception):
    pass

def __typerr_msg(actual_value, actual_type, expected_type):
    return f"expected '{actual_value}' to be of type '{expected_type}' but actual is of type '{actual_type}'"
def __typerr_lst_msg(actual_value, expected_type):
    return f"expected all elements in '{actual_value}' to be of type '{expected_type}'"
def __len_mismatch_msg(actual_value, expected_len, type_signature):
    return  f"expected '{actual_value}' to have {expected_len} elements with type signature '{type_signature}'"

def __show_types(types_t):
    if(len(types_t.__args__) == 1):
        return f"[{types_t.__args__[0].__name__}]"
    else:
        return list(map(lambda x: x.__name__, types_t.__args__))

def __is_one_of(types_t, arg) -> bool:
    # checks if the argument matches any type in the given collection (type-union)
    return any(__assert_type(type_t, arg)[0] for type_t in types_t)

def __check_tuple(type_t, arg):
    # check if it is a tuple
    if type(arg).__name__ != "tuple":
        return (__CHECK_FAILURE, __typerr_msg(arg, type(arg).__name__,'tuple'))

    # check if lenght matches
    if(len(type_t.__args__) != len(arg)):
        return (__CHECK_FAILURE, __len_mismatch_msg(arg, len(type_t.__args__), type(arg).__args__))

    # check if all entries are of the correct type
    for index, (t, v) in enumerate(zip(type_t.__args__, arg)):
        result, msg = __assert_type(t, v)
        if(result != __CHECK_SUCCESS):
            return (result, f"in tuple position {index}: {msg}")

    # no return so far -> everything ok
    return (__CHECK_SUCCESS, "")

def __check_list(type_t, arg):
    # check if it is a list
    if type(arg).__name__ != "list":
        return (__CHECK_FAILURE, __typerr_msg(arg,type(arg).__name__, "list"))

    # check if all values in the list are of the expected type(s)
    return (all(__is_one_of(type_t.__args__, arg_elem) for arg_elem in arg), __typerr_lst_msg(arg, f'union{__show_types(type_t)}'))

def __check_primitive(type_t, arg):
    return (isinstance(arg, type_t), __typerr_msg(arg, type(arg).__name__, type_t.__name__))

def __check_union(type_t, arg):
        return (__is_one_of(type_t.__args__, arg), __typerr_msg(arg, f'union{__show_types(type_t)}', type(arg)))

def __assert_type(type_t, arg) -> (bool, str):
    typetype= type(type_t).__name__
    if not ((typetype == "type") | (typetype == "GenericAlias") | (typetype == "_UnionGenericAlias")):
        return (__CHECK_ERROR, f"the given type argument '{type_t}' is not a type")

    match type_t.__name__:
        case "tuple":
            return __check_tuple(type_t, arg)
        case "list":
            return __check_list(type_t, arg)
        case "int" | "str" | "float" | "bool":
            return __check_primitive(type_t, arg)
        case "Union":
            return __check_union(type_t, arg)
        case _:
            return (__CHECK_ERROR, f"type '{type_t.__name__}' cannot be enfoced")

#TODO a utility function that can be called in code if needed


def __enforce(fn, args):
    names = fn.__code__.co_varnames
    types = get_type_hints(fn)
    type_keys = types.keys()

    present_names = [name for name in names if name in type_keys]
    print(present_names)
    # TODO indexes do not match anymore....
    # check all the types of function arguments, if they have annotation
    for index, name in enumerate(present_names):
        result, msg = __assert_type(types[name], args[index])
        if(result == __CHECK_FAILURE):
            raise TypeError(f"'{name}' has wrong type: {msg}")
        elif(result == __CHECK_ERROR):
                raise EnforceError(msg)

    # return the expected type of the return-value or 'nothing', if it should not be checked
    try:
        return types['return']
    except KeyError:
        return __NO_RETURN_TYPE


def __return(type_t, val):
    result, msg = __assert_type(type_t, val)
    if(result == __CHECK_SUCCESS):
        return val
    else:
        raise TypeError(f"in return value: {msg}")

def enforce(fn):
    def wrapper(*args):
        return_type = __enforce(fn, args)
        if(return_type == __NO_RETURN_TYPE):
            return fn(*args)
        else:
            __return(return_type, fn(*args))
    return wrapper

@enforce
def my_func_1(a: tuple[int, float], b: str) -> int:
    return 1

@enforce
def my_func_2(a: list[list[int], float], b: int) -> list[int, float]:
    return [a[0][0], 1.5]

@enforce
def my_func_3(a: int) -> Union[int, float]:
    return a 

class MyClass:
    name = "steve"
    @enforce
    def my_func_class(self, a: int) -> str:
        return f"{self.name} + {a}"
