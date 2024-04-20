from enforce import enforce, union, function

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
