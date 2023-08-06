import unittest
from typing import Optional


def left_digit(string: str) -> Optional[int]:
    for c in string:
        if c.isdigit():
            return int(c)
    return None


def left_digit(string: str) -> str:
    i = 0
    while i != len(string) and not string[i].isdigit():
        i += 1
    if string[i].isdigit():
        return int(string[i])
    else:
        return None


class TestLeftDigit(unittest.TestCase):
    def test_1(self):
        self.assertEqual(left_digit("TSU2Astneuoah"), 2)

    def test_2(self):

        self.assertEqual(left_digit("TS3NHriu4et"), 3)
    def test_3(self):
        self.assertEqual(left_digit("nsTPh/@uat$n1"), 1)

    def test_4(self):
        self.assertEqual(left_digit("5utarhRHUEHrchU"), 5)

    def test_5(self):
        self.assertEqual(left_digit("LRCHPYu0ruh'u0aehna"), 0)

    def test_6(self):
        self.assertEqual(left_digit("TSUthea876543ousth"), 8)

    def test_7(self):
        self.assertIs(left_digit("ThealdruCuanTat"), None)


if __name__ == "__main__":
    unittest.main()
