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

def any_t(arg):
    return (True, "*")

def class_t(clazz):
    def check(arg):
        props = dir(arg)
        for cd in dir(clazz):
            if(not cd in props):
                return (False, f": structure not matching. property {cd} of expected type {clazz} is not in {arg}")
        return (True, "")
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
                return (False, f"{list} of {hint}")

        # if the previous type checks did not fail, and thus return, we will land here, and everything is ok
        return (True, f"{list} of {hint}")
    return for_each


def assert_t(type_t, arg):
    check_types([type_t], [arg])

def check_types(types, args):
    num_types = len(types)
    num_args = len(args)
    if(num_types != num_args):
        raise TypeError(f"type signature cannot match: expected {num_types} arguments, but got {num_args} arugments")
    for i, (typecheck, arg) in enumerate(zip(types, args)):
        result, hint = typecheck(arg)
        if(not result):
            raise TypeError(f"'{arg}' of type {type(arg)} is not of expected type {hint}")

def check(*types):
    def decorator(fn):
        def wrapper(*args):
            check_types(types, args)
            return fn(*args)
        return wrapper
    return decorator


