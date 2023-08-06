from itertools import accumulate


def accumulating_list(numlist):
    a = 0
    sumlist = []
    for i in range(len(numlist)):
        a = a + numlist[i]
        sumlist.append(a)
    return sumlist


assert accumulating_list([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]
assert accumulating_list([1, 5, 7]) == [1, 6, 13]
assert accumulating_list([1, 0, 1, 0, 1]) == [1, 1, 2, 2, 3]
assert accumulating_list([1, 2, 3, 0, 0, 1]) == [1, 3, 6, 6, 6, 7]
assert accumulating_list([10]) == [10]
assert accumulating_list([]) == []
print("Success")