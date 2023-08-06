import unittest
from typing import List


def sum_every_nth(numbers: List[int], nth: int) -> int:
    return sum(numbers[nth-1::nth])


def sum_every_nth(inList, n):
    outInt = 0
    print(inList, n)
    for i in range(0,len(inList),n):
        outInt += inList[i]
    print(outInt)
    return outInt




class TestSumEveryNth(unittest.TestCase):
    def test_1(self):
        self.assertEqual(sum_every_nth([2, 5, 3, 9, 5, 7, 10, 7, 3, 3, 3], 9), 3)

    def test_2(self):
        self.assertEqual(sum_every_nth([10, 9, 2, 5, 9, 6, 4, 6, 7, 10, 9, 9, 9, 9, 2, 1, 2], 7), 13)

    def test_3(self):
        self.assertEqual(sum_every_nth([4, 5, 8, 7, 8, 1, 7, 9, 7, 4, 6, 2, 8, 8, 9, 9, 1, 7, 4], 6), 10)

    def test_4(self):
        self.assertEqual(sum_every_nth([8, 3, 5, 2, 6, 1, 5, 4, 3, 6, 6, 8, 5, 10, 7, 3, 7, 3, 5], 11), 6)

    def test_5(self):
        self.assertEqual(sum_every_nth([8, 9, 4, 8, 7, 5, 2, 9, 1, 8, 3, 8, 4, 9, 9, 6], 11), 3)

    def test_6(self):
        self.assertEqual(sum_every_nth([8, 2, 2, 7, 10, 6, 3, 5, 4, 4], 12), 0)

    def test_7(self):
        self.assertEqual(sum_every_nth([7, 4, 4, 10, 2, 6, 1, 9, 5, 10, 6, 4, 6, 6, 5, 9, 4, 10, 9], 8), 18)

    def test_8(self):
        self.assertEqual(sum_every_nth([5, 10, 10, 9, 10, 3, 5, 6, 6, 2, 10, 2, 9, 6, 8, 9, 10, 9, 4], 16), 9)

    def test_9(self):
        self.assertEqual(sum_every_nth([10, 4, 8, 4, 3, 9, 1, 1, 10, 7, 1, 4, 5, 5, 6, 1, 9], 6), 13)

    def test_10(self):
        self.assertEqual(sum_every_nth([2, 6, 3, 10, 6, 5, 4, 7, 9, 4, 1, 8, 9, 10, 8, 7, 2, 3, 6], 8), 14)

    def test_11(self):
        self.assertEqual(sum_every_nth([10, 9, 7, 8, 5, 7, 9, 5, 3, 3, 1], 7), 9)

    def test_12(self):
        self.assertEqual(sum_every_nth([7, 2, 9, 6, 1, 8, 8, 10, 2, 5, 5, 7, 3, 10, 1], 2), 48)

    def test_13(self):
        self.assertEqual(sum_every_nth([3, 10, 3, 8, 10, 9, 1, 3, 7, 2], 2), 32)

    def test_14(self):
        self.assertEqual(sum_every_nth([6, 5, 7, 9, 4, 2, 2, 9, 8, 10, 5, 2, 8], 7), 2)

    def test_15(self):
        self.assertEqual(sum_every_nth([9, 3, 7, 10, 3, 10, 2, 8, 8, 7, 1], 11), 1)

    def test_16(self):
        self.assertEqual(sum_every_nth([4, 6, 10, 8, 4, 7, 10, 10, 4, 4, 9, 2, 1, 9, 9, 8, 6, 6, 10], 7), 19)

    def test_17(self):
        self.assertEqual(sum_every_nth([3, 3, 2, 6, 4, 4, 10, 2, 10, 5, 5, 8, 6], 1), 68)

    def test_18(self):
        self.assertEqual(sum_every_nth([10, 1, 10, 8, 3, 2, 10, 8, 2, 3, 8, 7, 6, 4, 8], 6), 9)

    def test_19(self):
        self.assertEqual(sum_every_nth([5, 1, 4, 7, 3, 9, 4, 5, 9, 6, 1, 6, 9, 6, 7, 6, 8, 1], 14), 6)

    def test_20(self):
        self.assertEqual(sum_every_nth([2, 1, 7, 4, 2, 6, 2, 4, 6, 1, 2, 2, 10, 10], 2), 28)


if __name__ == "__main__":
    unittest.main()
