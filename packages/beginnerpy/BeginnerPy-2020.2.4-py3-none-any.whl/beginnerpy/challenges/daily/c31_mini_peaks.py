import unittest
from typing import List


def mini_peaks(l):
    return [y for x,y,z in zip(l[:-2],l[1:-1],l[2:]) if z<y>x]



class TestMiniPeaks(unittest.TestCase):
    def test_custom(self):
        self.assertEqual(mini_peaks([9, 10, 9, 10]), [10])

    def test_1(self):
        self.assertEqual(mini_peaks([4, 5, 2, 1, 4, 9, 7, 2]), [5, 9])

    def test_2(self):
        self.assertEqual(mini_peaks([1, 2, 1, 1, 3, 2, 5, 4, 4]), [2, 3, 5])

    def test_3(self):
        self.assertEqual(mini_peaks([1, 2, 3, 4, 5, 6]), [])

    def test_4(self):
        self.assertEqual(mini_peaks([6, 4, 3]), [])

    def test_5(self):
        self.assertEqual(mini_peaks([1, 1, 1, 1, 2, 1, 1, 1]), [2])

    def test_6(self):
        self.assertEqual(mini_peaks([1, 9, 1, 8, 2, 7, 6]), [9, 8, 7])

    def test_7(self):
        self.assertEqual(mini_peaks([7, 8, 7, 8, 7, 8, 5, 1, 2, 0]), [8, 8, 8, 2])


if __name__ == "__main__":
    unittest.main()
