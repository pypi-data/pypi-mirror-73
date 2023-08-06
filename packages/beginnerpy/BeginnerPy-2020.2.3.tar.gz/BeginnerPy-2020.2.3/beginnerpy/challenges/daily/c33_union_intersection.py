import unittest
from typing import List, Tuple


def intersection_union(list_a: List[int], list_b: List[int]) -> Tuple[List[int], List[int]]:
    intersection = list({item for item in list_a if item in list_b})
    intersection.sort()
    union = list(set(list_a) | set(list_b))
    union.sort()
    return intersection, union


def intersection_union(a,b):
    return sorted(set(a)&set(b)),sorted(set(a+b))


def intersection_union(list1: list, list2: list) -> list:
    intersection = sorted(list(set([element for element in list1
                                    if element in list2])))
    union = sorted(list(set(list1 + list2)))
    return intersection, union


def intersection_union(list1, list2):
    intersection = list(set([item for item in list1 if item in list2]))
    union = list(set(list1+list2))
    return (sorted(intersection), sorted(union))


class TestIntersectionUnion(unittest.TestCase):
    def test_1(self):
        self.assertEqual(intersection_union([1, 2, 3, 4, 4], [4, 5, 9]), ([4], [1, 2, 3, 4, 5, 9]))

    def test_2(self):
        self.assertEqual(intersection_union([1, 2, 3], [4, 5, 6]), ([], [1, 2, 3, 4, 5, 6]))

    def test_3(self):
        self.assertEqual(intersection_union([1, 1], [1, 1, 1, 1]), ([1], [1]))

    def test_4(self):
        self.assertEqual(intersection_union([5, 5], [5, 6]), ([5], [5, 6]))

    def test_5(self):
        self.assertEqual(intersection_union([7, 8, 9, 6], [9, 7, 6, 8]), ([6, 7, 8, 9], [6, 7, 8, 9]))

    def test_6(self):
        self.assertEqual(intersection_union([4, 1, 1, 2], [1, 4, 4, 4, 4, 4, 4]), ([1, 4], [1, 2, 4]))


if __name__ == "__main__":
    unittest.main()
