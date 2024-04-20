import typing as Typing
"""docs

# Rules

* enforce expects every argument to be annotated, it will fail if there is no annotation.
  if the type is to hard to figure out or something, you can set the type to 'any'

* return values are always checked and expected, enforce will fail if there is no return type. you can set it to 'any' though
"""

# global flag to enable/disable typechecking by enforce
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
    type_marker = _TYPE_UNKNOWN # EnforceTypeEnum
    inner_type = None # EnforceType, list of EnforceType, None
    display_name = "" # str
    def __init__(self, marker, inner, name):
        self.type_marker = marker
        self.inner_type = inner
        self.display_name = name

class EnforceValue:
    value = None # any
    name = None # string
    expected_type = None # EnfoceType
    def __init__(self, v, n, e):
        self.value = v
        self.name = n
        self.expected_type = e

def __parse_types(names: list[str], args: list[any], types: dict) -> list[EnforceValue]:
    if len(args) != len(types):
        raise TypeError("all function arguments are required to have type annotations.")

    # build enforce values
    enforce_values = []
    for (name, arg) in zip(names, args):
        type_t = types[name]
        enforce_type = __parse_type(type_t)
        enforce_values.append(EnforceValue(arg, name, enforce_type))

    return enforce_values

def __parse_type(type_t: any) -> EnforceType:
    match type_t.__name__:
        case 'int':
            return EnforceType(_TYPE_INT, None, "int")
        case 'float':
            return EnforceType(_TYPE_FLOAT, None, "float")
        case 'bool':
            return EnforceType(_TYPE_BOOL, None, "bool")
        case 'str':
            return EnforceType(_TYPE_STR, None, "str")
        case 'any':
            return EnforceType(_TYPE_ANY, None, "any")
        case _:
            return EnforceType(_TYPE_UNKNOWN, None, f"{type(type_t)}")

    return EnforceType(_TYPE_UNKNOWN, None, "???")

def __enforce_types(enforce_values: list[EnforceValue]) -> None:
    for enforce_value in enforce_values:
        __enforce_type(enforce_value)

def __raise_default_err(enforce_value: EnforceValue) -> None:
    raise TypeError(f"expected '{enforce_value.name}' to be of type '{enforce_value.expected_type.display_name}'")

def __enforce_type(enforce_value: EnforceValue) -> None:
    marker = enforce_value.expected_type.type_marker
    if(marker == _TYPE_INT):
        if not isinstance(enforce_value.value, int):
            __raise_default_err(enforce_value)
    elif(marker == _TYPE_FLOAT):
        if not isinstance(enforce_value.value, float):
            __raise_default_err(enforce_value)
    elif(marker == _TYPE_BOOL):
        if not isinstance(enforce_value.value, bool):
            __raise_default_err(enforce_value)
    elif(marker == _TYPE_STR):
        if not isinstance(enforce_value.value, str):
            __raise_default_err(enforce_value)
    elif(marker == _TYPE_ANY):
        pass
    else:
        raise TypeError(f"_TYPE_UNKNOWN: type '{enforce_value.expected_type.display_name}' of '{enforce_value.name}' is not supported by enforce")

#general strategy is to fail as fast as possible
#-> return type check is done first, because then nothing else has to be done, if this fails
def __force(fn, args):
    names = fn.__code__.co_varnames
    types = Typing.get_type_hints(fn)

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
    enforce_return_value = EnforceValue(return_value, 'return', __parse_type(return_type))
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

@force
def test1(i: int, j: list[float], k: bool, l: str) -> int:
    return i

test1(1, 1.1, True, "hi")
