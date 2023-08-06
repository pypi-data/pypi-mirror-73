import unittest
from typing import AnyStr


def first_before_second(p: AnyStr, f: AnyStr, s: AnyStr) -> bool:
    # return (c:=p.lower()).find(s.lower())>c.rfind(f.lower())
    return (l:=p.lower()).rfind(f)<l.find(s)
    return f not in (c:=p.lower())[c.find(s):]


def first_before_second(phrase: AnyStr, first: AnyStr, second: AnyStr) -> bool:
    return phrase.lower().rfind(first) < phrase.lower().find(second)


"""
    Unittests to ensure your code runs correctly.
    
    To run the tests just run this file. All errors will be output for you to see.
"""


class TestsForFirstBeforeSecond(unittest.TestCase):
    def test_1(self):
        self.assertTrue(first_before_second("A rabbit jumps joyfully", "a", "j"))

    def test_2(self):
        self.assertTrue(first_before_second("Knaves knew about waterfalls", "k", "w"))

    def test_3(self):
        self.assertTrue(first_before_second("Maria makes money", "m", "o"))

    def test_4(self):
        self.assertTrue(first_before_second("The hostess made pecan pie", "h", "p"))

    def test_5(self):
        self.assertTrue(first_before_second("Barry the butterfly flew away", "b", "f"))

    def test_6(self):
        self.assertTrue(first_before_second("Moody muggles", "m", "g"))

    def test_7(self):
        self.assertFalse(first_before_second("Happy birthday", "a", "y"))

    def test_8(self):
        self.assertFalse(first_before_second("Precarious kangaroos", "k", "a"))

    def test_9(self):
        self.assertFalse(first_before_second("Maria makes money", "m", "i"))

    def test_10(self):
        self.assertFalse(first_before_second("Taken by the beautiful sunrise", "u", "s"))

    def test_11(self):
        self.assertFalse(first_before_second("Sharp cheddar biscuit", "t", "s"))

    def test_12(self):
        self.assertFalse(first_before_second("Moody Muggles", "m", "o"))


if __name__ == "__main__":
    unittest.main()
