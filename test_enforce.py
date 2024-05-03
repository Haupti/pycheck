from enforce import enforce, enforced, union, function, EnforceError, literal
import numpy as np

#
# to run the 'tests', run the file using the python interpreter
#
@enforce
def test1(i: int, j: list[float, int], k: bool, l: str) -> int:
    return i

@enforce
def test2(i: list[tuple[int, float], str]) -> int:
    return 1

@enforce
def test3(i: tuple[int, float]) -> int:
    return 1

@enforce
def test4(thing: any) -> int:
    return 1

@enforce
def test5(thing: union[str, float]) -> union[str, int]:
    return thing

@enforce
def test6(thing: list[str, int, float]) -> list[str, int, float]:
    return thing

@enforce
def test7(thing: list[str, int]) -> any:
    return thing

@enforce
def test8(thing: function, arg: int) -> int:
    return thing(arg)

@enforce
def test9(msg: str) -> None:
    "hi"

class ClassOne:
    var = "hi"
    @enforce
    def getVar(self: any) -> str:
        return self.var

class ClassTwo:
    hey = "whoop"
    def setHey(self, s):
        self.hey = var

@enforce
def test10(clazz: ClassOne) -> str:
    return clazz.getVar()

@enforce
def test11(thing: list) -> list:
    return thing

# special support for numpy arrays
@enforce
def test12(arr: np.ndarray) -> any:
    return arr[0]

@enforce
def test13(d: dict[{"num": int, "name": str}]) -> any:
    return d

@enforce
def test14(d: dict[{1: int, 2: list[int], "oh hi": dict[{"greet": str}]}]) -> any:
    some = "saaa"
    return d

@enforce
def test15(d: set[str, int]) -> any:
    return d

@enforce
def test16(d: list[int], y:int ,something: int = 1, something_else: str = "hi") -> str:
    listings = d
    for i, e in enumerate(listings):
        listings[i] = e
    return something_else


@enforce
def test17(d: literal["int", 2.5, True, 1]) -> any:
    return d

@enforce
def test18(d: union[int, float]) -> any:
    return d

@enforce
def test19(d: list[int, None]) -> any:
    return d

@enforce
def test20(d: union[int, None]=None) -> any:
    return d

test1(1, [22], True, "hi")
test2([(1,2.2), "hi", "hallo", (1, 5.5), "steve"])
test3((1,2.2))
test4("hi")
test4(123)
test5("hi")
test6([1])
test6([1.5, "hi", 2, 3])
test7(["s"])
test8(lambda x: 1+x, 2)
test9("hi")
test10(ClassOne())
test11([1, 2.5, True, "hi", np.array([1, 2, 3])])
test12(np.array([1]))
test13({"num": 1, "name": "steve"})
test14({1: 2, 2: [1,2,3], "oh hi": {"greet": "mark"}})
test15({1,True,2,"hi"}) # funny: this does not fail because True == 1 and the set already contains 1....
test16([1], 1, something_else="LOL")
test17("int")
test18(1)
test19([1, None])
test20(d=1)
enforced(1, int)
enforced([1], list[int])

