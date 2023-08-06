import unittest


def is_symmetrical(n: int) -> bool:
    return (m:=str(n))==m[::-1]
    return str(n)==str(n)[::-1]


def is_symetrical(number: int) -> bool:
    if str(number) == str(number)[::-1]:
        return True
    return False


class TestIsSymmetrical(unittest.TestCase):
    def test_1(self):
        self.assertFalse(is_symmetrical(9562))

    def test_2(self):
        self.assertFalse(is_symmetrical(10019))

    def test_3(self):
        self.assertTrue(is_symmetrical(1))

    def test_4(self):
        self.assertTrue(is_symmetrical(3223))

    def test_5(self):
        self.assertTrue(is_symmetrical(95559))

    def test_6(self):
        self.assertTrue(is_symmetrical(66566))


if __name__ == "__main__":
    unittest.main()
