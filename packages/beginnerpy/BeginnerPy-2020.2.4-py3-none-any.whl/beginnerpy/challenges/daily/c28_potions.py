import unittest
import re
from typing import List


def apply_potions(potions: str) -> str:
    return (lambda tokens: "".join(
        str(
            int(token) + {"A": 1, "B": -1}.get(
                tokens[i + 1], 0
            )
        ) for i, token in enumerate(tokens) if token.isdigit()
    ))(re.findall(r"\d+|[AB]", potions) + [""])


def apply_potions(potions: str) -> str:
    digits = ""
    effects = {
        "A": 1,
        "B": -1
    }
    output = []
    for c in potions:
        if c.isdigit():
            digits += c
        elif c in effects:
            output.append(int(digits) + effects[c])
            digits = ""
    if digits:
        output.append(int(digits))
    return "".join(map(str, output))


def apply_potions(potions: str) -> str:

    split = list(potions)
    nlist = []
    num = ''
    for i, v in enumerate(split):
        if v.isnumeric() and i==len(split)-1: num = num + v; nlist.append(num)
        elif v.isnumeric(): num = num + v
        elif v.lower()=='a': nlist.append(str(int(num)+1)); num=''
        elif v.lower()=='b': nlist.append(str(int(num)-1)); num=''
    return ''.join(nlist)


class TestPotions(unittest.TestCase):
    def test_1(self):
        self.assertEqual(apply_potions("567"), "567")

    def test_2(self):
        self.assertEqual(apply_potions("3A78B51"), "47751")

    def test_3(self):
        self.assertEqual(apply_potions("9999B"), "9998")

    def test_4(self):
        self.assertEqual(apply_potions("9A123"), "10123")

    def test_5(self):
        self.assertEqual(apply_potions("1A2A3A4A"), "2345")

    def test_6(self):
        self.assertEqual(apply_potions("9B8B7B6A"), "8767")

    def test_7(self):
        self.assertEqual(apply_potions("19A10B99A1000B"), "209100999")


if __name__ == "__main__":
    unittest.main()
