import unittest


def rearranged_difference(number: int) -> int:
    return int("".join(reversed(sorted(str(number))))) - int("".join(sorted(str(number))))


def rearranged_difference(number: int) -> int:

    max = sorted((str(number)), reverse=True)
    czer = (str(number)).count('0')
    if czer > 0: rzer = (str(number)).replace('0','')
    else: rzer = number
    min = sorted(str(rzer))
    if czer > 0: min.insert(1,'0'*czer)
    jmin = ''.join(min)
    jmax = ''.join(max)
    return int(jmax)-int(jmin)


class TestRearrangedDifference(unittest.TestCase):
    def test_1(self):
        self.assertEqual(rearranged_difference(9092564), 9719721)

    def test_2(self):
        self.assertEqual(rearranged_difference(1308821), 8719722)

    def test_3(self):
        self.assertEqual(rearranged_difference(8386568), 5319765)

    def test_4(self):
        self.assertEqual(rearranged_difference(7794084), 9429651)

    def test_5(self):
        self.assertEqual(rearranged_difference(6366093), 9329661)

    def test_6(self):
        self.assertEqual(rearranged_difference(7863060), 8729622)

    def test_7(self):
        self.assertEqual(rearranged_difference(3368327), 6429654)

    def test_8(self):
        self.assertEqual(rearranged_difference(7218787), 7599933)

    def test_9(self):
        self.assertEqual(rearranged_difference(7723188), 7639533)

    def test_10(self):
        self.assertEqual(rearranged_difference(8816317), 7739523)

    def test_11(self):
        self.assertEqual(rearranged_difference(8824349), 7539543)

    def test_12(self):
        self.assertEqual(rearranged_difference(3320707), 7709823)

    def test_13(self):
        self.assertEqual(rearranged_difference(1695488), 8429652)

    def test_14(self):
        self.assertEqual(rearranged_difference(2120034), 4309866)

    def test_15(self):
        self.assertEqual(rearranged_difference(5300586), 8619732)

    def test_16(self):
        self.assertEqual(rearranged_difference(3538814), 7519743)

    def test_17(self):
        self.assertEqual(rearranged_difference(1336939), 8629632)

    def test_18(self):
        self.assertEqual(rearranged_difference(6290200), 9619731)

    def test_19(self):
        self.assertEqual(rearranged_difference(5268866), 6299964)

    def test_20(self):
        self.assertEqual(rearranged_difference(5155458), 7099983)


if __name__ == "__main__":
    unittest.main()
