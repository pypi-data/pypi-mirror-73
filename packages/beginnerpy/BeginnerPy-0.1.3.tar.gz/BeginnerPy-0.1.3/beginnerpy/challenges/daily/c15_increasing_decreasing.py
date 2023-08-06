from typing import Sequence, AnyStr


def check(numbers):
    direction = "neither"
    previous_direction = "start"
    index = 1
    while index < len(numbers) and ((direction != "neither" and direction == previous_direction) or previous_direction == "start"):
        previous_direction = direction
        difference = numbers[index] - numbers[index - 1]
        print(numbers[index], numbers[index - 1])
        if difference < 0:
            direction = "decreasing"
        elif difference > 0:
            direction = "increasing"
        else:
            direction = "neither"
        index += 1
    print(direction)
    return direction


assert check([1, 2, 3]) == "increasing"
assert check([3, 2, 1]) == "decreasing"
assert check([1, 2, 1]) == "neither"
assert check([1, 1, 2]) == "neither"
assert check([1, 3, 5, 7, 9, 10]) == "increasing"
assert check([5, 6, 5, 7, 9, 10]) == "neither"
assert check([5, 7]) == "increasing"
assert check([9, 7, 1]) == "decreasing"
print("Challenge #15 passed")
