import unittest
from typing import Any, List


def delete_occurrences(values, N):
    official_list = []
    for stuff in values:
        if official_list.count(stuff) < N:
            official_list.append(stuff)
    return official_list


class TestRemoveExtras(unittest.TestCase):
    def test_1(self):
        self.assertEqual(delete_occurrences([1, 1, 1, 1], 2), [1, 1])

    def test_2(self):
        self.assertEqual(delete_occurrences([True, True, True], 3), [True, True, True])

    def test_3(self):
        self.assertEqual(delete_occurrences([13, True, 13, None], 1), [13, True, None])

    def test_4(self):
        self.assertEqual(delete_occurrences([], 100), [])

    def test_5(self):
        self.assertEqual(delete_occurrences(["John", "John", "Marry", "Marry"], 1), ["John", "Marry"])

    def test_6(self):
        self.assertEqual(delete_occurrences(["Marry", "John", None, "John", False, "John", 0, "John", "Marry", "Marry", "John"], 3), ["Marry", "John", None, "John", False, "John", 0, "Marry", "Marry"])

    def test_7(self):
        self.assertEqual(delete_occurrences([20, 37, 20, 21], 1), [20, 37, 21])

    def test_8(self):
        self.assertEqual(delete_occurrences([1, 1, 3, 3, 7, 2, 2, 2, 2], 3), [1, 1, 3, 3, 7, 2, 2, 2])

    def test_9(self):
        self.assertEqual(delete_occurrences([1, 2, 3, 1, 1, 2, 1, 2, 3, 3, 2, 4, 5, 3, 1],3), [1, 2, 3, 1, 1, 2, 2, 3, 3, 4, 5])
