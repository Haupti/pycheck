from enforce import __show_actual_type
import numpy as np


def expect(actual, expected):
    if actual == expected:
        print("\x1b[2;36msuccess\x1b[2;0m")
    else:
        print(f"\x1b[2;31mFAILURE: expected '{actual}' to be '{expected}'\x1b[2;0m")

class MyClass:
    def what(self):
        pass

def somefunc():
    pass

expect(__show_actual_type(1), "int")
expect(__show_actual_type("hi mark"), "str")
expect(__show_actual_type(6.2), "float")
expect(__show_actual_type(True), "bool")
expect(__show_actual_type(MyClass()), "MyClass")
expect(__show_actual_type([1,2,3]), "list[int]")
expect(__show_actual_type(np.array([1,2,3])), "numpy.ndarray[numpy.int64]")
expect(__show_actual_type((1,2, "hi", 2.5, MyClass())), "tuple(int, int, str, float, MyClass)")
expect(__show_actual_type({"hi": "mark", 1: True, 2.5: "yes", "steve": "is cool"}), 'dict{"hi": str, 1: bool, 2.5: str, "steve": str}')
expect(__show_actual_type(None), "None")
expect(__show_actual_type(lambda x: x), "function")
expect(__show_actual_type(somefunc), "function")
expect(__show_actual_type(MyClass().what), "method")

