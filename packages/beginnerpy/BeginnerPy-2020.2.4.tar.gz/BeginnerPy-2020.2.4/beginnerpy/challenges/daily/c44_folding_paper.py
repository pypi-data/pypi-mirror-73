import unittest


num_layers=lambda n:f"{2**n/2000}m"


num_layers=lambda n:f"{2**n/2E3}m"


class TestFoldThickness(unittest.TestCase):
    def test_1(self):
        self.assertEqual("0.0005m", num_layers(0))

    def test_2(self):
        self.assertEqual("0.001m", num_layers(1))

    def test_3(self):
        self.assertEqual("0.002m", num_layers(2))

    def test_4(self):
        self.assertEqual("0.004m", num_layers(3))

    def test_5(self):
        self.assertEqual("0.008m", num_layers(4))

    def test_6(self):
        self.assertEqual("0.016m", num_layers(5))

    def test_7(self):
        self.assertEqual("0.032m", num_layers(6))

    def test_8(self):
        self.assertEqual("0.064m", num_layers(7))

    def test_9(self):
        self.assertEqual("0.128m", num_layers(8))

    def test_10(self):
        self.assertEqual("0.256m", num_layers(9))

    def test_11(self):
        self.assertEqual("0.512m", num_layers(10))

    def test_12(self):
        self.assertEqual("1.024m", num_layers(11))

    def test_13(self):
        self.assertEqual("2097.152m", num_layers(22))

    def test_14(self):
        self.assertEqual("1073741.824m", num_layers(31))

    def test_15(self):
        self.assertEqual("2199023255.552m", num_layers(42))

    def test_16(self):
        self.assertEqual("4503599627370.496m", num_layers(53))

    def test_17(self):
        self.assertEqual("9223372036854776.0m", num_layers(64))

    def test_18(self):
        self.assertEqual("1.1805916207174113e+18m", num_layers(71))

    def test_19(self):
        self.assertEqual("3.022314549036573e+20m", num_layers(79))

    def test_20(self):
        self.assertEqual("1.9342813113834067e+22m", num_layers(85))

    def test_21(self):
        self.assertEqual("6.189700196426902e+23m", num_layers(90))

    def test_22(self):
        self.assertEqual("6.338253001141147e+26m", num_layers(100))


if __name__ == "__name__":
    unittest.main()
