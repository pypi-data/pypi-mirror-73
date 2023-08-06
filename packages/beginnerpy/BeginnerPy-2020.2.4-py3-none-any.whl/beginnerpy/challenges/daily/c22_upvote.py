import unittest
from typing import AnyStr, List


def transform_upvotes(u):
    return [float(n.strip("k"))*1000**n.count("k") for n in u.split()]



class TestsForFirstBeforeSecond(unittest.TestCase):
    def test_1(self):
        self.assertEqual(transform_upvotes('20.3k 3.8k 7.7k 992'), [20300, 3800, 7700, 992])

    def test_2(self):
        self.assertEqual(transform_upvotes('5.5k 8.9k 32'), [5500, 8900, 32])

    def test_3(self):
        self.assertEqual(transform_upvotes('6.8k 13.5k'), [6800, 13500])

    def test_4(self):
        print(transform_upvotes('1k')[0] == 1000)


if __name__ == "__main__":
    unittest.main()
