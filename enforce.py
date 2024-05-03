import typing as Typing
import types as Types

# global flag to enable/disable typechecking by enforce
_TYPECHECKING_ENABLED = True


# zero overhead'enum'
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
_TYPE_SET = 14
_TYPE_LITERAL = 15

class EnforceError(Exception):
    pass

class EnforceType:
    type_marker = _TYPE_UNKNOWN # EnforceTypeEnum
    inner_type = None # EnforceType, list of EnforceType, str (in case of class type), None, list of EnforceDictEntryType
    display_name = "" # str
    def __init__(self, marker, inner, name):
        self.type_marker = marker
        self.inner_type = inner
        self.display_name = name

class EnforceLiteralType:
    type_marker = _TYPE_LITERAL # EnforceTypeEnum
    allowed_values = None # list of values. must be int, str, float, bool
    display_name = "" # str
    def __init__(self, allowed_values, name):
        self.allowed_values = allowed_values
        self.display_name = name

class EnforceDictEntryType:
    enforce_type = None # EnforceType
    key_name ="" # str
    def __init__(self, type_e, key_name):
        self.enforce_type = type_e
        self.key_name = key_name

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
_NOSTR = ''

_TYPECHECK_SUCCESS = (True, '')

def __is_of_primitive_type(val: any) -> bool:
    return (isinstance(val, int) | isinstance(val, bool) | isinstance(val, float) | isinstance(val, str))

def __show_key_name(key_name):
    if isinstance(key_name, int):
        return str(key_name)
    if isinstance(key_name, float):
        return str(key_name)
    if isinstance(key_name, bool):
        return str(key_name)
    if isinstance(key_name, str):
        return f'"{key_name}"'

def __show_actual_type(value: any) -> str:
    if(value is None):
        return "None"
    type_name = type(value).__name__
    if(type_name == 'list'):
        type_set = set()
        [type_set.add(__show_actual_type(elem)) for elem in value]
        types_representation = ", ".join(map(str, type_set))
        return f"list[{types_representation}]"
    if(type_name == 'set'):
        type_set = set()
        [type_set.add(__show_actual_type(elem)) for elem in value]
        types_representation = ", ".join(map(str, type_set))
        return f"set[{types_representation}]"
    if(type_name == 'ndarray'):
        return f"numpy.ndarray[numpy.{value.dtype}]"
    if(type_name == 'tuple'):
        types_representation = ", ".join(map(str,[__show_actual_type(elem) for elem in value]))
        return f"tuple({types_representation})"
    if(type_name == 'dict'):
        types_representation = ", ".join(map(str,[f"{__show_key_name(elem[0])}: {__show_actual_type(elem[1])}" for elem in value.items()]))
        return "dict{" + types_representation + "}"
    if(type_name == "NoneType"):
        return "None"

    return type_name

def __create_error_type_hint(e):
    expected_type = None
    if isinstance(e, EnforceValue):
        expected_type = e.expected_type
    elif isinstance(e, EnforceType):
        expected_type = e
    elif e is None:
        return "None"
    else:
        expected_type = e
    match expected_type.display_name:
        case "int" | "str" | "float" | "bool" | "function" | "None" | "any":
            return expected_type.display_name
        case "list":
            inner_type_hints = ", ".join(map(str,[__create_error_type_hint(t) for t in expected_type.inner_type]))
            if len(inner_type_hints) == 0:
                return "list"
            return f"list[{inner_type_hints}]"
        case "set":
            inner_type_hints = ", ".join(map(str,[__create_error_type_hint(t) for t in expected_type.inner_type]))
            if len(inner_type_hints) == 0:
                return "set"
            return f"set[{inner_type_hints}]"
        case "ndarray":
            inner_type_hints = ", ".join(map(str,[__create_error_type_hint(t) for t in expected_type.inner_type]))
            if len(inner_type_hints) == 0:
                return "ndarray"
            return f"ndarray[{inner_type_hints}]"
        case "tuple":
            inner_type_hints = ", ".join(map(str,[__create_error_type_hint(t) for t in expected_type.inner_type]))
            return f"tuple[{inner_type_hints}]"
        case "dict":
            inner_type_hints = ", ".join(map(str,[f"{__show_key_name(t.key_name)}: {__create_error_type_hint(t.enforce_type)}" for t in expected_type.inner_type]))
            return f"dict[{inner_type_hints}]"
        case "literal":
            inner_type_hints = ", ".join(map(__show_key_name, expected_type.allowed_values))
            return f"literal[{inner_type_hints}]"
        case _ :
            return f"{expected_type.display_name}"


def __default_failure(enforce_value: EnforceValue) -> (bool, str):
    type_hint = __create_error_type_hint(enforce_value)
    return (False, f"expected '{enforce_value.name}' to be of type '{type_hint}'")

def __type_unknown_error(type_t):
    return EnforceError(f"_TYPE_UNKNOWN: type '{type_t}' is not supported by enforce")

def __type_invalid_error(type_t):
    return EnforceError(f"_TYPE_INVALID: type '{type_t}' is not a valid type to be handled by enforce")

def __get_verified_dict_innertype(type_t):
    list_type_args = list(type_t.__args__)
    if len(list_type_args) != 1:
        raise __type_invalid_error(type_t)
    type_arg = list_type_args[0]
    if type(type_arg).__name__ != 'dict':
        raise __type_invalid_error(type_t)
    return type_arg

def __verify_valid_type_innertypes(list_type_args, typename):
    if any([(list_type_arg or type(None)).__name__ == 'any' for list_type_arg in list_type_args]):
        raise __type_invalid_error(f"{typename}[any]")
    if len(list_type_args) == 0:
        raise __type_invalid_error(list_type_args)

def __verify_valid_list_innertypes(list_type_args):
    __verify_valid_type_innertypes(list_type_args, "list")

def __verify_valid_set_innertypes(list_type_args):
    __verify_valid_type_innertypes(list_type_args, "set")

def __verify_valid_ndarray_innertypes(list_type_args):
    __verify_valid_type_innertypes(list_type_args, "ndarray")

#
# type parsing functions
#
def __parse_types(args: list[any], kwargs: dict, defaults: any, types: dict) -> list[EnforceValue]:
    defaults_len = 0
    if not defaults is None:
        defaults_len = len(defaults)

    if (len(args) + defaults_len != len(types)):
        raise TypeError("all function arguments are required to have type annotations.")

    enforce_values = []
    for i, (name, type_t) in enumerate(types.items()):
        if i < len(args):
            ev = EnforceValue(args[i], name,__parse_type(type_t))
            enforce_values.append(ev)
        else:
            if name in kwargs.keys():
                ev = EnforceValue(kwargs[name], name, __parse_type(type_t))
                enforce_values.append(ev)
            else:
                ev = EnforceValue(defaults[i-(len(types.items()) - len(defaults))],name , __parse_type(type_t))
                enforce_values.append(ev)

    return enforce_values

def __parse_type(type_t: any) -> EnforceType:
    typename = None
    if(type_t is None):
        return EnforceType(_TYPE_NONE, None, "None")
    elif not hasattr(type_t, '__name__'):
        raise __type_unknown_error(type_t)
    else:
        typename = type_t.__name__
    match typename:
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
                return EnforceType(_TYPE_LIST, [] , "list")
            list_type_args = list(type_t.__args__)

            __verify_valid_list_innertypes(list_type_args)

            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            return EnforceType(_TYPE_LIST, inner_types, "list")
        case 'ndarray':
            if not hasattr(type_t, '__args__'): # inner type not specified
                return EnforceType(_TYPE_NDARRAY, [] , "ndarray")
            list_type_args = list(type_t.__args__)
            if len(list_type_args) > 1:
                raise EnforceError(f"_TYPE_INVALID: ndarray can only contain values of a single type")

            __verify_valid_ndarray_innertypes(list_type_args)

            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            return EnforceType(_TYPE_NDARRAY, inner_types, "ndarray")
        case 'tuple':
            list_type_args = list(type_t.__args__)
            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            return EnforceType(_TYPE_TUPLE, inner_types, "tuple")
        case 'Optional':
            list_type_args = list(type_t.__args__)
            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            inner_types.append(EnforceType(_TYPE_NONE, None, "None"))
            return EnforceType(_TYPE_UNION, inner_types, "union")
        case 'Union':
            list_type_args = list(type_t.__args__)
            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            return EnforceType(_TYPE_UNION, inner_types, "union")
        case 'dict':
            if not hasattr(type_t, '__args__'):
                return EnforceType(_TYPE_DICT, None, "dict")
            type_arg = __get_verified_dict_innertype(type_t)
            dict_entries = []
            for key, value in type_arg.items():
                dict_entries.append(EnforceDictEntryType(__parse_type(value), key))
            return EnforceType(_TYPE_DICT, dict_entries, "dict")
        case 'set':
            if not hasattr(type_t, '__args__'):
                return EnforceType(_TYPE_SET, None, "set")
            list_type_args = list(type_t.__args__)

            __verify_valid_set_innertypes(list_type_args)

            inner_types = [__parse_type(list_type_arg) for list_type_arg in list_type_args]
            return EnforceType(_TYPE_SET, inner_types, "set")
        case 'Literal':
            if not hasattr(type_t, "__args__"):
                raise EnforceError("'literal' type must have arguments")
            list_type_args = type_t.__args__
            if not all([__is_of_primitive_type(it) for it in list_type_args]):
                raise EnforceError("'literal' type arguments must be values of type 'int', 'float', 'str' or 'bool'. no type arguments of type 'type' are allowed.")
            return EnforceLiteralType(list_type_args,"literal")
        case _:
            return EnforceType(_TYPE_CLASS, typename, typename)

#
# type verification functions
#
def __enforce_types(enforce_values: list[EnforceValue]) -> None:
    for enforce_value in enforce_values:
        is_success, msg = __enforce_type(enforce_value)
        if not is_success:
            actual_type = __show_actual_type(enforce_value.value)
            raise TypeError(msg + " but actual was '" + actual_type + "'")

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
        if not str(enforce_value.value.dtype) == enforce_value.expected_type.inner_type[0].display_name:
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
    elif(marker == _TYPE_DICT):
        if not isinstance(enforce_value.value, dict):
            return __default_failure(enforce_value)
        for dict_entry_e in enforce_value.expected_type.inner_type:
            if enforce_value.value.get(dict_entry_e.key_name) is None:
                return __default_failure(enforce_value)
            if not __enforce_type(EnforceValue(enforce_value.value[dict_entry_e.key_name], _NOSTR, dict_entry_e.enforce_type))[0]:
                return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_SET):
        if not isinstance(enforce_value.value, set):
            return __default_failure(enforce_value)
        if len(enforce_value.expected_type.inner_type) == 0:
            return _TYPECHECK_SUCCESS
        for elem in enforce_value.value:
            if not any([__enforce_type(EnforceValue(elem, _NOSTR, type_e))[0] for type_e in enforce_value.expected_type.inner_type]):
                return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    elif(marker == _TYPE_LITERAL):
        if not any([enforce_value.value == literal_value for literal_value in enforce_value.expected_type.allowed_values]):
            return __default_failure(enforce_value)
        return _TYPECHECK_SUCCESS
    raise EnforceError("there might be a bug in here, please report.")

#general strategy is to fail as fast as possible
#-> return type check is done first, because if this fails, then nothing else has to be done.
def __force(fn, args, kwargs):
    names = fn.__code__.co_varnames
    types = Typing.get_type_hints(fn)

    # check if return type is not specified
    if(not 'return' in types.keys()):
        raise TypeError("enforce expects a return type to be specified")
    return_type = types['return'] # required at the end

    # checking argument types
    types.pop("return") # cannot be in the dict for the next step
    enforce_values = __parse_types(args, kwargs, fn.__defaults__, types)
    __enforce_types(enforce_values)

    # checking return type
    return_value = fn(*args, **kwargs)
    enforce_return_value = EnforceValue(return_value, 'return', __parse_type(return_type))
    __enforce_types([enforce_return_value])

    # return function result
    return return_value


#
# exposed
#

union = Typing.Union
function = Types.FunctionType
literal = Typing.Literal

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
    def wrapper(*args, **kwargs):
        global _TYPECHECKING_ENABLED
        if(_TYPECHECKING_ENABLED):
            return __force(fn, args, kwargs)
        else:
            return fn(*args)
    return wrapper
