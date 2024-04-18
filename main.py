from enum import Enum

class Type(Enum):
    Int = ["int", lambda arg: type(arg) == int]
    Float = ["float", lambda arg: type(arg) == float]
    List = ["list", lambda arg: type(arg) == list]
    Bool = ["bool", lambda arg: type(arg) == bool]
    Str = ["str", lambda arg: type(arg) == str]

def check_types(types, args):
    for i, (typ, arg) in enumerate(zip(types, args)):
        if(not typ.value[1](arg)):
            raise TypeError(f"argument #{i+1} '{arg}' of type {type(arg)} is not of expected type '{typ.value[0]}'")

def check(*types):
    def decorator(fn):
        def wrapper(*args):
            check_types(types, args)
            return fn(*args)
        return wrapper
    return decorator


@check(Type.Int, Type.Int)
def add(x,y):
    return x + y

print(add(1.1,2))

