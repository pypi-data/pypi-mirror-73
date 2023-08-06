from math import prod
from functools import reduce
from operator import mul


def my_sum_dig_prod(*numbers):
    return (
        func := lambda value: v
        if (v := reduce(mul, map(int, str(value)))) < 10
        else func(v)
    )(sum(numbers))


def sum_dig_prod(*args):
    return (
        sum_dig_prod(sum(args))
        if len(args) > 1
        else sum_dig_prod(prod([int(x) for x in str(args[0])]))
        if len(str(args[0])) != 1
        else args[0]
    )


def sum_dig_prod(*args):
    total = sum(args)
    while len(str(total)) > 1:
        new_total = 1
        for i in str(total):
            new_total *= int(i)
        total = new_total
    return total


assert sum_dig_prod(8, 16, 89, 3) == 6
assert sum_dig_prod(16, 28) == 6
assert sum_dig_prod(9) == 9
assert sum_dig_prod(26, 497, 62, 841) == 6
assert sum_dig_prod(0) == 0
assert sum_dig_prod(17737, 98723, 2) == 6
assert sum_dig_prod(123, -99) == 8
assert sum_dig_prod(9, 8) == 7
assert sum_dig_prod(167, 167, 167, 167, 167, 3) == 8
assert sum_dig_prod(111111111) == 1
assert sum_dig_prod(98526, 54, 863, 156489, 45, 6156) == 2
assert sum_dig_prod(999, 999) == 8
assert sum_dig_prod(1, 2, 3, 4, 5, 6) == 2
assert sum_dig_prod(999, 2222) == 2
assert sum_dig_prod(8618, -2) == 6


for num in range(100000):
    if sum_dig_prod(num) != my_sum_dig_prod(num):
        print(num)
        print(testing := sum_dig_prod(num), value := my_sum_dig_prod(num))
        assert testing == value

print("Success")
