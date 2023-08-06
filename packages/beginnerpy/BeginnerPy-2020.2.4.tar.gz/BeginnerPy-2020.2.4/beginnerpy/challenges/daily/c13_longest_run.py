from typing import Sequence, Generator, Tuple
from itertools import chain


# def count(numbers: Sequence[int], direction: int) -> Generator[int]:
#     counter = 1
#     for index in range(len(numbers) - 1):
#         if numbers[index + 1] - numbers[index] == direction:
#             counter += 1
#         else:
#             yield counter
#             counter = 1
#     yield counter


def rec(numbers: Sequence[int], direction: int, counter: int) -> int:
    return


def longest_run(nums):
    return max(
        (
            count := lambda numbers, direction, counter: (
                new_counter
                if (
                    new_counter := count(
                        numbers[1:],
                        direction,
                        counter + 1 if numbers[1] - numbers[0] == direction else 1,
                    )
                )
                > counter
                else counter
            )
            if len(numbers) > 1
            else counter
        )(nums, 1, 1),
        count(nums, -1, 1),
    )


assert longest_run([1, 2, 3, 5, 6, 7, 8, 9]) == 5
assert longest_run([1, 2, 3, 10, 11, 15]) == 3
assert longest_run([-7, -6, -5, -4, -3, -2, -1]) == 7
assert longest_run([3, 5, 6, 10, 15]) == 2
assert longest_run([3, 5, 7, 10, 15]) == 1

directional_aware = longest_run([4, 3, 2, 1]) == 4
if directional_aware:
    print("Directionally Aware")
    assert longest_run([5, 3, 2]) == 2
    assert longest_run([9, 8, 7, 4, 3, 2, 1, 2, 1]) == 4
    assert longest_run([9, 8, 7, 8, 7, 6, 5]) == 4

print("Challenge 13 Successful")
