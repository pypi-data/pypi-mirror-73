import unittest


def round_number(m: int, n: int) -> int:
    return a if m-(a:=(m//n)*n)<(b:=a+n)-m else b


def round_number(num: int, n: int) -> int:
    if (abs((int(num / n) * n) - num) < ((int(num / n) + 1) * n) - num):
        return int(num / n) * n
    else:
        return (int(num / n) + 1) * n 


class TestRoundNumber(unittest.TestCase):
    def test_1(self):
        self.assertEqual(round_number(34, 25), 25)

    def test_2(self):
        self.assertEqual(round_number(54, 8), 56)

    def test_3(self):
        self.assertEqual(round_number(65, 10), 70)

    def test_4(self):
        self.assertEqual(round_number(6247, 163), 6194)

    def test_5(self):
        self.assertEqual(round_number(532, 12), 528)

    def test_6(self):
        self.assertEqual(round_number(642234, 1523), 642706)

    def test_7(self):
        self.assertEqual(round_number(5123, 10), 5120)

    def test_8(self):
        self.assertEqual(round_number(96623443, 7650), 96627150)

    def test_9(self):
        self.assertEqual(round_number(125123, 520), 125320)

    def test_10(self):
        self.assertEqual(round_number(12121212, 144), 12121200)



if __name__ == "__main__":
    unittest.main()
