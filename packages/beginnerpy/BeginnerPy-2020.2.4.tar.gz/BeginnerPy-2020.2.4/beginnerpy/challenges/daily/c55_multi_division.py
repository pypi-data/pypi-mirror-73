import unittest


def abcmath(a: int, b: int, c: int) -> int:
    return 0  # Put your code here!


class TestMultiDivision(unittest.TestCase):
    def test_1(self):
        self.assertFalse(abcmath(1, 2, 3))

    def test_2(self):
        self.assertFalse(abcmath(69, 15, 9))

    def test_3(self):
        self.assertFalse(abcmath(9, 2, 52))

    def test_4(self):
        self.assertFalse(abcmath(5, 2, 3))

    def test_5(self):
        self.assertTrue(abcmath(5, 2, 1))

    def test_6(self):
        self.assertTrue(abcmath(261, 2, 1))

    def test_7(self):
        self.assertTrue(abcmath(22, 2, 22))

    def test_8(self):
        self.assertTrue(abcmath(69, 12, 3))


if __name__ == "__main__":
    unittest.main()
