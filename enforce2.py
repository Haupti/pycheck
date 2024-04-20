"""docs

# Rules

* enforce expects every argument to be annotated, it will fail if there is no annotation.
  if the type is to hard to figure out or something, you can set the type to 'any'

* return values are always checked and expected, enforce will fail if there is no return type. you can set it to 'any' though
"""

# global flag to enable/disable typechecking by enfoce
TYPECHECKING_ENABLED = True

# zero overhead 'enum'
# EnforceTypeEnum
_TYPE_UNKNOWN = 0
_TYPE_ANY = 1
_TYPE_STR = 2
_TYPE_INT = 3
_TYPE_FLOAT = 4
_TYPE_BOOL = 5
_TYPE_LIST = 6
_TYPE_TUPLE = 7
_TYPE_UNION = 8
_TYPE_DICT = 9
_TYPE_CLASS = 10
_TYPE_NONE = 11

class EnforceType:
    type_t = _TYPE_UNKNOWN # EnforceTypeEnum
    inner_type = None # EnforceType, list of EnforceType

class EnforceValue:
    value = None # any
    name = None # string
    expected_type = None # EnfoceType

def __parse_types(names: list[str], args: list[any], types: dict) -> list[EnforceValue]:
    if len(args) != len(types):
        raise TypeError("all function arguments are required to have type annotations. there are {len(args)} arguments but {len(types)} type annotations.")
    enforce_values = []
    return []

def __parse_type(name: str, arg: any, type_t: any) -> EnforceValue:
    pass # TODO

def __enforce_types(enforce_values: list[EnforceValue]) -> None:
    pass # TODO
def __enforce_type(enforce_value: EnforceValue) -> None:
    pass # TODO

"""
general strategy is to fail as fast as possible
-> return type check is done first, because then nothing else has to be done, if this fails
"""
def __force(fn, args):
    names = fn.__code__.co_varnames
    types = get_type_hints(fn)

    # check if return type is not specified
    return_type = types['return'] # required at the end
    if(not 'return' in types.keys()):
        raise TypeError("enforce expects a return type to be specified")

    # checking argument types
    types.pop("return") # cannot be in the dict for the next step
    enforce_values = __parse_types(names, args, types)
    __enforce_types(enforce_values)

    # checking return type
    return_value = fn(*args)
    enforce_return_value = __parse_type('retrun', return_value, return_type)
    __enforce_type(enforce_return_value)

    # return function result
    return return_value

def force(fn):
    def wrapper(*args):
        if(TYPECHECKING_ENABLED):
            return __force(fn, args)
        else:
            return fn(*args)
    return wrapper

dic = { "hi": 1, "hallo": 2}
if "steve" in dic.keys(): dic.pop("steve")
