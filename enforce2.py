"""docs

# Rules

* enforce expects every argument to be annotated, it will fail if there is no annotation.
  if the type is to hard to figure out or something, you can set the type to 'any'

* return values are always checked and expected, enforce will fail if there is no return type. you can set it to 'any' though
"""

# zero overhead 'enum'
# EnforceTypeEnum
__TYPE_UNKNOWN= 0
__TYPE_ANY = 1
__TYPE_STR = 2
__TYPE_INT = 3
__TYPE_FLOAT = 4
__TYPE_BOOL = 5
__TYPE_LIST = 6
__TYPE_TUPLE = 7
__TYPE_UNION = 8
__TYPE_DICT = 9
__TYPE_CLASS = 10
__TYPE_NONE = 11

class EnforceType:
    type_t = __UNKNOWN_TYPE # EnforceTypeEnum
    inner_type = None # EnforceType, list of EnforceType

class EnforceValue:
    value = None # any
    name = None # string
    expected_type = None # EnfoceType

def __parse_types(names: list[str], args: list[any], types: dict) -> list[EnforceValue]:
    pass # TODO
def __parse_type(name: str, arg: any, type_t: any) -> EnforceValue:
    pass # TODO
def __enforce_types(enforce_values: list[EnforceValue]) -> None:
    pass # TODO
def __enforce_type(enforce_value: EnforceValue) -> None:
    pass # TODO



def __force(fn, args):
    names = fn.__code__.co_varnames
    types = get_type_hints(fn)
    enforce_values = __parse_types(names, args, types)
    __enforce_types(enforce_values)
    types_keys = types.keys()
    if(not 'return' in type_keys):
        raise TypeError("enforce expects a return type to be specified")
    return_value = fn(*args)
    enforce_return_value = __parse_type('retrun', return_value, types['return'])
    __enforce_type(enforce_return_value)
    return return_value

def force(fn: union[]):
    def wrapper(*args):
        return __force(fn, args)
    return wrapper
