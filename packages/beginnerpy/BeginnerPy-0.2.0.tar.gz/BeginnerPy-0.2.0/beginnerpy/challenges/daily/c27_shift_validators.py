import unittest
from typing import List


def is_shifted(a,b):
    return len({j-i for i,j in zip(a,b)})<=1

def is_multiplied(a,b):
    return len({j/i for i,j in zip(a,b)})<=1


class TestValidators(unittest.TestCase):
    def test_1(self):
        self.assertEqual(is_shifted([1, 2, 3], [2, 3, 4]), True)

    def test_2(self):
        self.assertEqual(is_shifted([1, 2, 3], [-9, -8, -7]), True)

    def test_3(self):
        self.assertEqual(is_multiplied([1, 2, 3], [10, 20, 30]), True)

    def test_4(self):
        self.assertEqual(is_multiplied([1, 2, 3], [-0.5, -1, -1.5]), True )

    def test_5(self):
        self.assertEqual(is_multiplied([1, 2, 3], [0, 0, 0]), True )

    def test_6(self):
        self.assertEqual(is_shifted([1, 2, 3], [2, 3, 5]), False)

    def test_7(self):
        self.assertEqual(is_shifted([1, 2, 3], [-9, -1, -7]), False)

    def test_8(self):
        self.assertEqual(is_multiplied([1, 2, 3], [10, 20, 29]), False)

    def test_9(self):
        self.assertEqual(is_multiplied([1, 2, 3], [-0.5, -1, -2]), False)

    def test_10(self):
        self.assertEqual(is_multiplied([1, 2, 3], [0, 0, 1]), False)


if __name__ == "__main__":
    unittest.main()
