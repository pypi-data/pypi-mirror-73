import unittest
from typing import List


def can_find(bigrams: List[str], words: List[str]) -> bool:

    b_res = []
    for bigram in bigrams:
        w_res = []
        for word in words:
            w_res.append(word.find(bigram))
        b_res.append(w_res.count(-1) != len(words))
    return False not in b_res


class TestBigrams(unittest.TestCase):
    def test_0(self):
        self.assertEqual(can_find(["ow"], ["hello", "world"]), False)

    def test_1(self):
        self.assertEqual(can_find(["at", "be", "th", "au"], ["beautiful", "the", "hat"]), True)

    def test_2(self):
        self.assertEqual(can_find(["bo", "ta", "el", "st", "ca"], ["books", "table", "cap", "hostel"]), True)

    def test_3(self):
        self.assertEqual(can_find(["la", "te"], ["latte"]), True)

    def test_4(self):
        self.assertEqual(can_find(["th", "fo", "ma", "or"], ["the", "many", "for", "forest"]), True)

    def test_5(self):
        self.assertEqual(can_find(["ay", "be", "ta", "cu"], ["maybe", "beta", "abet", "course"]), False)

    def test_6(self):
        self.assertEqual(can_find(["oo", "mi", "ki", "la"], ["milk", "chocolate", "cooks"]), False)

    def test_7(self):
        self.assertEqual(can_find(["la"], []), False)

    def test_8(self):
        self.assertEqual(can_find(["la", "at", "te", "ea"], ["latte"]), False)


if __name__ == "__main__":
    unittest.main()
