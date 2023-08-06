from typing import List


def antipodes_average_runner(l):
    a = antipodes_average(l)
    print(a)
    return a


antipodes_average = lambda l : ([x/2 for x in [l[0:int(len(l)/2)][x] + list(reversed(l[int(len(l)/2)::]))[x] for x in range(int(len(l)/2))]]) if len(l)%2 == 0 else [x/2 for x in [l[0:int(len(l)/2)][x] + list(reversed(l[int(len(l)/2)+1::]))[x] for x in range(len(l[0:int(len(l)/2)]))]]


assert antipodes_average_runner([1, 2, 3, 4]) == [2.5, 2.5]
assert antipodes_average_runner([1, 2, 3, 4, 5]) == [3, 3]
assert antipodes_average_runner([1, -2, 3, 4, 5, 6, 7, 8, 9, 10, -12, 14, 545, 6346]) == [
    3173.5,
    271.5,
    8.5,
    -4.0,
    7.5,
    7.5,
    7.5,
]
assert antipodes_average_runner([-1, -2]) == [-1.5]
assert antipodes_average_runner([1, 2, 5, 10]) == [5.5, 3.5]
assert antipodes_average_runner([1, 2, 3, 5, 7, 9]) == [5, 4.5, 4]
assert antipodes_average_runner([-1, -4, -12, -2, -11, -6]) == [-3.5, -7.5, -7]
assert antipodes_average_runner([5, -80, 66, -8, -6]) == [-0.5, -44]
assert antipodes_average_runner([-1, 0, 1]) == [0]
print("You've successfully computed the Antipodes Average for all tests!")
