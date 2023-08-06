from typing import List


def combo_runner(lst: List[int], n: int) -> List[List[int]]:
    ret = combo(lst, n)
    print(n, ret)
    return ret


combo=lambda l,n:list(map(list,__import__("itertools").combinations(l,n)))


assert combo_runner([1, 2, 3, 4], 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
assert combo_runner([1, 2, 3, 4], 3) == [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
assert combo_runner([1, 2, 3, 4], 1) == [[1], [2], [3], [4]]
assert combo_runner([1, 2, 3, 4], 5) == []
assert combo_runner([1, 2, 3, 4], 0) == [[]]
assert combo_runner(['a', 'b', 'c'], 0) == [[]]
assert combo_runner(['a', 'b', 'c'], 4) == []
assert combo_runner(['a', 'b', 'c'], 1) == [['a'], ['b'], ['c']]
assert combo_runner(['a', 'b', 'c'], 2) == [['a', 'b'], ['a', 'c'], ['b', 'c']]
assert combo_runner(['a', 'b', 'c'], 3) == [['a', 'b', 'c']]
print("You successfully passed all Challenge 19 tests!!!")
