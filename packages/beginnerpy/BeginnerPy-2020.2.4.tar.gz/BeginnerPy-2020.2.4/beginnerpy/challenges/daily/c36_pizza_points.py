import unittest
from typing import Dict, List


def pizza_points(customers: Dict[str, List[int]], min_orders: int, min_order_price: int) -> List[str]:
    return []  # Put your code here!!!


def pizza_points(customers, order_num, min_price):
    qual_customers = []
    for customer in customers:
        if len([item for item in customers[customer] if item >= min_price]) >= order_num:
            qual_customers.append(customer)
    return sorted(qual_customers)


class TestPizzaPoints(unittest.TestCase):
    def setUp(self):
        self.dict1 = {
          'Batman': [22, 30, 11, 17, 15, 52, 27, 12],
          'Spider-Man': [5, 17, 30, 33, 40, 22, 26, 10, 11, 45]
        }

        self.dict2 = {
          'Captain America': [10, 10, 54, 14, 51, 33, 42, 73, 66, 33, 55, 42, 47],
          'Iron Man': [30, 56, 38, 14, 17],
          'Hulk': [53, 25, 13, 7, 61, 16, 17, 29, 64, 8],
          'Superman': [27, 28]
        }

        self.dict3 = {
          'Zorro': [13, 53, 10, 51],
          'Wolverine': [16],
          'Elon Musk': [26, 61, 23, 61, 39, 50, 53, 54, 45, 46, 42, 49, 18, 75, 11, 73, 42, 61, 15, 60, 70, 67, 8, 9, 63, 55, 55, 35, 24, 59, 13, 49, 46, 26, 7, 8, 8, 34, 73, 60, 27, 28, 28, 48, 10]
        }

    def test_1(self):
        self.assertEqual(pizza_points(self.dict1, 5, 20), ["Spider-Man"])

    def test_2(self):
        self.assertEqual(pizza_points(self.dict2, 1, 5), ["Captain America", "Hulk", "Iron Man", "Superman"])

    def test_3(self):
        self.assertEqual(pizza_points(self.dict3, 7, 15), ["Elon Musk"])

    def test_4(self):
        self.assertEqual(pizza_points(self.dict1, 10, 5), ["Spider-Man"])

    def test_5(self):
        self.assertEqual(pizza_points(self.dict2, 2, 35), ["Captain America", "Hulk", "Iron Man"])

    def test_6(self):
        self.assertEqual(pizza_points(self.dict3, 3, 25), ["Elon Musk"])

    def test_7(self):
        self.assertEqual(pizza_points(self.dict3, 4, 12), ["Elon Musk"])

    def test_8(self):
        self.assertEqual(pizza_points(self.dict2, 1, 75), [])

    def test_9(self):
        self.assertEqual(pizza_points(self.dict1, 100, 1), [])

    def test_10(self):
        self.assertEqual(pizza_points(self.dict3, 2, 67), ["Elon Musk"])


if __name__ == "__main__":
    unittest.main()
