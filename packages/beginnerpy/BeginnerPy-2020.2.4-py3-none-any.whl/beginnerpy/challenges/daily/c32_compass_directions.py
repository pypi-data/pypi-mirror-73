import unittest
from typing import List


def final_direction(f: str, t: List[str]) -> str:
    return (c:="NESW")[(c.index(f)-(o:=t.count)("L")+o("R"))%4]


def final_direction(facing: str, turns: List[str]) -> str:

    dir = {'N':0, 'E':1, 'S':2, 'W':3, 0:'N', 1:'E', 2:'S', 3:'W'}
    return dir[(turns.count('R')-turns.count('L')+dir[facing])%4]


class TestFinalDirection(unittest.TestCase):
    def test_1(self):
        self.assertEqual(final_direction('N', ['L', 'L', 'L']), 'E')

    def test_2(self):
        self.assertEqual(final_direction('N', ['R', 'R', 'R', 'R', 'R', 'R', 'R']), 'W')

    def test_3(self):
        self.assertEqual(final_direction('N', ['R', 'R', 'R', 'L']), 'S')

    def test_4(self):
        self.assertEqual(final_direction('N', ['R', 'R', 'R', 'R']), 'N')

    def test_5(self):
        self.assertEqual(final_direction('N', ['R', 'L']), 'N')

    def test_6(self):
        self.assertEqual(final_direction('S', ['R', 'L', 'R', 'L', 'R']), 'W')

    def test_7(self):
        self.assertEqual(final_direction('S', ['R', 'L', 'R', 'L', 'R', 'L']), 'S')

    def test_8(self):
        self.assertEqual(final_direction('S', ['R', 'L', 'R', 'L', 'L', 'L']), 'N')

    def test_9(self):
        self.assertEqual(final_direction('S', ['R', 'R']), 'N')

    def test_10(self):
        self.assertEqual(final_direction('S', ['R']), 'W')

    def test_11(self):
        self.assertEqual(final_direction('S', ['L']), 'E')

    def test_12(self):
        self.assertEqual(final_direction('W', ['L', 'R', 'R']), 'N')

    def test_13(self):
        self.assertEqual(final_direction('W', ['R', 'L', 'L']), 'S')

    def test_14(self):
        self.assertEqual(final_direction('E', ['L', 'R', 'R']), 'S')

    def test_15(self):
        self.assertEqual(final_direction('E', ['R', 'L', 'L']), 'N')


if __name__ == "__main__":
    unittest.main()
