import typing as Typing
import types as Types
"""docs

# Rules

* enforce expects every argument to be annotated, it will fail if there is no annotation.
  if the type is to hard to figure out or something, you can set the type to 'any'

* return values are always checked and expected, enforce will fail if there is no return type. you can set it to 'any' though
"""

# global flag to enable/disable typechecking by enforce
_TYPECHECKING_ENABLED = True


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
_TYPE_FUNCTION = 11
_TYPE_NONE = 12
_TYPE_NDARRAY = 13

class EnforceError(Exception):
    pass

class EnforceType:
    type_marker = _TYPE_UNKNOWN # EnforceTypeEnum
    inner_type = None # EnforceType, list of EnforceType, str (in case of class type), None
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

#
# utilities
#
def __show_list(lst):
    return "[{0}]".format(', '.join(map(str, lst)))
def __show_tuple(lst):
    return "({0})".format(', '.join(map(str, lst)))

_NOSTR = ''

_TYPECHECK_SUCCESS = (True, '')

def __default_failure(enforce_value: EnforceValue) -> (bool, str):
    return (False, f"expected '{enforce_value.name}' to be of type '{enforce_value.expected_type.display_name}'")

def __get_type_hint_for_error(type_t):
    err_hint = type_t
    try:
        if isinstance(type_t, list):
            err_hint = __show_list([t.__name__ for t in type_t])
        elif isinstance(type_t, tuple):
            err_hint = __show_tuple([t.__name__ for t in type_t])
    except:
        pass
    return err_hint

def __type_unknown_error(type_t):
    err_hint = __get_type_hint_for_error(type_t)
    raise EnforceError(f"_TYPE_UNKNOWN: type '{err_hint}' is not supported by enforce")

def __type_invalid_error(type_t):
    err_hint = __get_type_hint_for_error(type_t)
    raise EnforceError(f"_TYPE_INVALID: type '{err_hint}' is not a valid type to be handled by enforce")

def __type_unknown_failure(typename: str, argname: str) -> (bool, str):
    return (False, f"_TYPE_UNKNOWN: type '{typename}' of '{argname}' is not supported by enforce")

def __invalid_type_failure(type_t):
    typename = ''
    try:
        if(isinstance(type_t, list) or isinstance(type_t, tuple)):
            typename = __show_list(type_t)
    except:
        typename = type_t
    return (False, f"_TYPE_UNKNOWN: type '{typename}' is not supported by enforce")


def __verify_valid_array_innertypes(list_type_args: list[EnforceType]) -> None:
    if len(list_type_args) == 0:
        return __type_invalid_error(type_t)
    if any([list_type_arg.__name__ == 'any' for list_type_arg in list_type_args]):
        return __type_invalid_error(type_t)

#
# type parsing functions
#
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
    typename = None
    if not hasattr(type_t, '__name__'):
        __type_unknown_error(type_t)
    else:
        typename = type_t.__name__
    match typename:
        # union
        # class
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
        case 'function':
            return EnforceType(_TYPE_FUNCTION, None, "function")
        case 'NoneType':
            return EnforceType(_TYPE_NONE, None, "None")
        case 'list':
            if not hasattr(type_t, '__args__'): # inner type not specified
                return EnforceType(_TYPE_LIST, [] , f"list[any]")
            list_type_args = list(type_t.__args__)

            __verify_valid_array_innertypes(list_type_args)

            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            type_hint = __show_list([inner_type.display_name for inner_type in inner_types])
            return EnforceType(_TYPE_LIST, inner_types, f"list{type_hint}")
        case 'ndarray':
            if not hasattr(type_t, '__args__'): # inner type not specified
                return EnforceType(_TYPE_LIST, [] , f"ndarray[any]")
            list_type_args = list(type_t.__args__)

            __verify_valid_array_innertypes(list_type_args)

            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            type_hint = __show_list([inner_type.display_name for inner_type in inner_types])
            return EnforceType(_TYPE_NDARRAY, inner_types, f"ndarray{type_hint}")
        case 'tuple':
            list_type_args = list(type_t.__args__)
            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            type_hint = __show_list(tuple([inner_type.display_name for inner_type in inner_types]))
            return EnforceType(_TYPE_TUPLE, inner_types, f"tuple{type_hint}")
        case 'Union':
            list_type_args = list(type_t.__args__)
            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            type_hint = __show_list([inner_type.display_name for inner_type in inner_types])
            return EnforceType(_TYPE_UNION, inner_types, f"union{type_hint}")
        case _:
            return EnforceType(_TYPE_CLASS, typename, typename)

#
# type verification functions
#
def __enforce_types(enforce_values: list[EnforceValue]) -> None:
    for enforce_value in enforce_values:
        is_success, msg = __enforce_type(enforce_value)
        if not is_success:
            raise TypeError(msg)

def __enforce_type(enforce_value: EnforceValue) -> (bool, str):
    marker = enforce_value.expected_type.type_marker
    if(marker == _TYPE_INT):
        # boolean is a subtype of int, hence isinstance(True, int) is True...
        if isinstance(enforce_value.value, bool):
            return __default_failure(enforce_value)
        if not isinstance(enforce_value.value, int):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_FLOAT):
        if not isinstance(enforce_value.value, float):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_BOOL):
        if not isinstance(enforce_value.value, bool):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_STR):
        if not isinstance(enforce_value.value, str):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_LIST):
        if not isinstance(enforce_value.value, list):
            return __default_failure(enforce_value)
        if len(enforce_value.expected_type.inner_type) == 0:
            return _TYPECHECK_SUCCESS
        for elem in enforce_value.value:
            if not any([__enforce_type(EnforceValue(elem, _NOSTR, type_e))[0] for type_e in enforce_value.expected_type.inner_type]):
                return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_NDARRAY):
        if not (type(enforce_value.value).__name__ == 'ndarray'):
            return __default_failure(enforce_value)
        if len(enforce_value.expected_type.inner_type) == 0:
            return _TYPECHECK_SUCCESS
        for elem in enforce_value.value:
            if not any([__enforce_type(EnforceValue(elem, _NOSTR, type_e))[0] for type_e in enforce_value.expected_type.inner_type]):
                return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_TUPLE):
        if not isinstance(enforce_value.value, tuple):
            return __default_failure(enforce_value)
        for (elem, type_e) in zip(enforce_value.value, enforce_value.expected_type.inner_type):
            if not __enforce_type(EnforceValue(elem, _NOSTR, type_e))[0]:
                return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_UNION):
        if not any([__enforce_type(EnforceValue(enforce_value.value, _NOSTR, type_e))[0] for type_e in enforce_value.expected_type.inner_type]):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_FUNCTION):
        if not isinstance(enforce_value.value, function):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_CLASS):
        if not enforce_value.value.__class__.__name__ == enforce_value.expected_type.inner_type:
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_NONE):
        if not enforce_value.value is None:
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_ANY):
        return _TYPECHECK_SUCCESS
    else:
        return __type_unknown_failure(enforce_value.expected_type.display_name, enforce_value.name)

#general strategy is to fail as fast as possible
#-> return type check is done first, because then nothing else has to be done, if this fails
def __force(fn, args):
    names = fn.__code__.co_varnames
    types = Typing.get_type_hints(fn)

    # check if return type is not specified
    if(not 'return' in types.keys()):
        raise TypeError("enforce expects a return type to be specified")
    return_type = types['return'] # required at the end

    # checking argument types
    types.pop("return") # cannot be in the dict for the next step
    enforce_values = __parse_types(names, args, types)
    __enforce_types(enforce_values)

    # checking return type
    return_value = fn(*args)
    enforce_return_value = EnforceValue(return_value, 'return', __parse_type(return_type))
    __enforce_types([enforce_return_value])

    # return function result
    return return_value

#
# exposed
#

union = Typing.Union
function = Types.FunctionType

def enforced(arg, type_t):
    @enforce
    def wrapper(value: type_t) -> any:
        return value
    return wrapper(arg)

def enable_enforce():
    global _TYPECHECKING_ENABLED
    _TYPECHECKING_ENABLED = True

def disable_enforce():
    global _TYPECHECKING_ENABLED
    _TYPECHECKING_ENABLED = False

def enforce(fn):
    def wrapper(*args):
        global _TYPECHECKING_ENABLED
        if(_TYPECHECKING_ENABLED):
            return __force(fn, args)
        else:
            return fn(*args)
    return wrapper
