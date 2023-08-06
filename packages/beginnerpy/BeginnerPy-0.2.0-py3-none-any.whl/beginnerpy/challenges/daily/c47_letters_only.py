import unittest


letters_only=lambda s:"".join(filter(str.isalpha, s))
letters_only=lambda n:__import__("re").compile("[^a-zA-Z]").sub("",n)


class TestLettersOnly(unittest.TestCase):
    def test_1(self):
        self.assertEqual('Aladdin', letters_only(',1|2)")A^1<[_)?^"]l[a`3+%!d@8-0_0d.*}i@&n?='))

    def test_2(self):
        self.assertEqual('Up', letters_only('^U)6$22>8p).'))

    def test_3(self):
        self.assertEqual('Inception', letters_only('I5n!449+c@e*}@@1]p{2@`,~t:i0o%n<3%8'))

    def test_4(self):
        self.assertEqual('Psycho', letters_only('!)"P[s9)"69}yc3+?1]+33>3ho'))

    def test_5(self):
        self.assertEqual('Goodfellas', letters_only(':~;G{o}o{+524<df~:>}e24{l8:_l]a:?@]%s7'))

    def test_6(self):
        self.assertEqual('Shrek', letters_only('&&S~]@8>1-0!h#r),80<_>!}|e>_k:'))

    def test_7(self):
        self.assertEqual('Gladiator', letters_only(')^/|,!!09]=/1<G2?`=[l{a}d9]^i7a0|t6_o2*r'))

    def test_8(self):
        self.assertEqual('Vertigo', letters_only(']8;]V9e{=0r!.5t>i<^_g"4o"5~'))

    def test_9(self):
        self.assertEqual('Batman', letters_only('%%)?"?B#>/_4a#,;t8|m8675a(n'))

    def test_10(self):
        self.assertEqual('Halloween', letters_only('97H^)~a8567ll*o?"6%)w63e37e<n?@='))


if __name__ == "__main__":
    unittest.main()
