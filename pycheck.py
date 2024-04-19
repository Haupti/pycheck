__TYPECHECK_SUCCESS = (True, 801)
def __TYPECHECK_FAILURE(hint):
    return (False, hint)

__RETURN_TYPE_MARKER = 1

def return_t(type_t):
    return (__RETURN_TYPE_MARKER, type_t)

def int_t(arg):
   return (type(arg) == int, f"{int}")

def float_t(arg):
   return (type(arg) == float, f"{float}")

def str_t(arg):
   return (type(arg) == str, f"{str}")

def bool_t(arg):
   return (type(arg) == bool, f"{bool}")

def list_t(arg):
   return (type(arg) == list, f"{list}")

def range_t(arg):
   return (type(arg) == range, f"{range}")

def tuple_t(arg):
   return (type(arg) == tuple, f"{tuple}")

def function_t(arg):
   return (hasattr(arg, "__call__") , f"<class 'function'>")

def dict_t(arg):
   return (type(arg) == dict, f"{dict}")

def any_t(arg):
    return __TYPECHECK_SUCCESS

def class_t(clazz):
    def check(arg):
        props = dir(arg)
        for cd in dir(clazz):
            if(not cd in props):
                return __TYPECHECK_FAILURE(f": structure not matching. property {cd} of expected type {clazz} is not in {arg}")
        return __TYPECHECK_SUCCESS
    return check

def list_of_t(fn_t):
    def for_each(lst):

        # checks if the argument is a list
        result_out, hint_out = list_t(lst)
        if(not result_out):
            return (result_out, hint_out)

        # checks if each element in the list is of the expected type given
        for l in lst:
            result, hint = fn_t(l)
            if(not result):
                return __TYPECHECK_FAILURE(f"{list} of {hint}")

        # if the previous type checks did not fail, and thus return, we will land here, and everything is ok
        return __TYPECHECK_SUCCESS
    return for_each

def tuple_of_t(*types_t):
    def for_each(arg):
        # check if the argument is a tuple
        result_tuple, hint_tuple = tuple_t(arg)
        if(not result_tuple):
            return (result_tuple, hint_tuple)

        num_types = len(types_t)
        num_args = len(arg)
        if(num_types != num_args):
            return __TYPECHECK_FAILURE(f": type signature cannot match: expected {num_types} elements in {tuple}, but it has {num_args} elements.")

        # check if each element of the tuple is of the expected type given
        for i, (a, fn_t) in enumerate(zip(arg, types_t)):
            result, hint = fn_t(a)
            if(not result):
                return __TYPECHECK_FAILURE(f": element {i+1} was expected to have type {hint}")

        # if the previous type checks did not fail, and thus return, we will land here and everything is ok
        return __TYPECHECK_SUCCESS
    return for_each


def typedef_dict_t(typedef_dict):
    required_keys = typedef_dict.keys()
    def dict_type_check(arg):

        # checks if the given argument is a dict
        result_dict, hint_dict = dict_t(arg)
        if(not result_dict):
            return (result_dict, hint_dict)

        # checks if all requird keys are inside of the given dict and if they are of correct type (there can be more, they are not checked)
        for required_key in required_keys:
            try:
                value = arg[required_key]
            except:
                return __TYPECHECK_FAILURE(f": expected a key '{required_key}', but it is not there.")
            result, hint = typedef_dict[required_key](value)
            if(not result):
                return __TYPECHECK_FAILURE(f": expected value of '{required_key}' to be of type {hint}")

        return __TYPECHECK_SUCCESS
    return dict_type_check

def typedef_t(*oneof):
    def is_one_of(arg):
        if not any(arg == o for o in oneof):
            return __TYPECHECK_FAILURE(f": expected one of {oneof}")
        else:
            return __TYPECHECK_SUCCESS
    return is_one_of

def typedef_range_t(from_v, to_v):
    def is_in_range(arg):
        if not (from_v <= arg <= to_v):
            return __TYPECHECK_FAILURE(f": value not in range {from_v}...{to_v}")
        else:
            return __TYPECHECK_SUCCESS
    return is_in_range

def __check_type(type_t, arg):
    result, hint = type_t(arg)
    if(not result):
        raise TypeError(f"'{arg}' of type {type(arg)} is not of expected type {hint}")

def __check_types(types, args):
    num_types = len(types)
    num_args = len(args)
    if(num_types != num_args):
        raise TypeError(f"type signature cannot match: expected {num_types} arguments, but got {num_args} arugments")
    for (typecheck, arg) in zip(types, args):
        __check_type(typecheck, arg)


def assert_t(type_t, arg):
    __check_type(type_t, arg)

def assume_t(type_t, arg):
    __check_type(type_t, arg)
    return arg


# thats wyld, bro... conditional function definition...
def check(*types):
    match types[-1]:
        case (__RETURN_TYPE_MARKER, return_type_t):
            def decorator(fn):
                def wrapper(*args):
                    __check_types(types[:-1], args)
                    return assume_t(return_type_t, fn(*args))
                return wrapper
        case _:
            def decorator(fn):
                def wrapper(*args):
                    __check_types(types, args)
                    return fn(*args)
                return wrapper
    return decorator


