from typing import Callable


class make_plus_function:
    def __init__(self, operand):
        self.operand = operand

    def __call__(self, number):
        return number + self.operand


def make_plus_function(inputnum):
    num = 0
    num += inputnum
    def add_num(addednum):
        nonlocal num
        num += addednum
        return num
    return add_num


plus_two = make_plus_function(2)
plus_five = make_plus_function(5)
plus_seven = make_plus_function(plus_two(plus_five(0)))
plus_ten = make_plus_function(10)

assert plus_two(0) == 2
assert plus_two(18) == 20
assert plus_two(-1) == 1
assert plus_five(0) == 5
assert plus_five(12) == 17
assert plus_five(-5) == 0
assert plus_seven(0) == 7
assert plus_seven(41) == 48
assert plus_seven(-117) == -110
assert plus_ten(0) == 10
assert plus_ten(1) == 11
assert plus_ten(-1) == 9

assert plus_two(plus_five(plus_seven(plus_ten(1)))) == 25

assert make_plus_function(8)(8) == 16
assert make_plus_function(-100)(0) == -100
assert make_plus_function(1)(100) == 101
assert make_plus_function(0)(0) == 0
print("Success")
