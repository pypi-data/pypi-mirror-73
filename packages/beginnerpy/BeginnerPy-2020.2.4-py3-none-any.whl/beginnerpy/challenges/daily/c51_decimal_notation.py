import unittest
from typing import List


def convert_to_decimal(percentages: List[str]) -> List[float]:
    return []  # Put your one liner here ;)


def convert_to_decimal(percentages: List[str]) -> List[int]:
    return [float(perc.replace('%',''))/100 for perc in percentages]


class TestConvertToDecimal(unittest.TestCase):
    def test_1(self):
        self.assertEqual(
            [0.33, 0.981, 0.5644, 1],
            convert_to_decimal(["33%", "98.1%", "56.44%", "100%"])
        )

    def test_2(self):
        self.assertEqual(
            [0.45, 0.32, 0.97, 0.33],
            convert_to_decimal(["45%", "32%", "97%", "33%"])
        )

    def test_3(self):
        self.assertEqual(
            [0.01, 0.02, 0.03],
            convert_to_decimal(["1%", "2%", "3%"])
        )


if __name__ == "__main__":
    unittest.main()
