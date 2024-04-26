def expect(actual, expected):
    if actual == expected:
        print("\x1b[2;36msuccess\x1b[2;0m")
    else:
        print(f"\x1b[2;31mFAILURE: expected '{actual}' to be '{expected}'\x1b[2;0m")
