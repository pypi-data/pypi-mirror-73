import unittest


def remove_vowels(phrase: str) -> str:
    return ""  # Put your one liner here ;)


def remove_vowels(p: str) -> str:
    return p.translate({ord(v):""for v in"aeiouAEIOU"})
    return "".join(c for c in p if c not in"aeiouAEIOU")
    return "".join(c for c in p if c.lower()not in"aeiou")


def remove_vowels(phrase: str) -> str:
    return "".join(filter(lambda x: x.lower() not in 'aeiou', phrase))


class TestRemoveVowels(unittest.TestCase):
    def test_1(self):
        self.assertEqual(
            "f bm rsgns frm ffc NW, thrby dng  grt srvc t th cntry -  wll gv hm fr lftm glf t ny n f my crss!",
            remove_vowels(
                "If Obama resigns from office NOW, thereby doing a great service to the country - I will give him free "
                "lifetime golf at any one of my courses!"
            )
        )

    def test_2(self):
        self.assertEqual(
            "Ths lctn s  ttl shm nd  trvsty. W r nt  dmcrcy!",
            remove_vowels("This election is a total sham and a travesty. We are not a democracy!")
        )

    def test_3(self):
        self.assertEqual(
            " hv nvr sn  thn prsn drnkng Dt Ck.",
            remove_vowels("I have never seen a thin person drinking Diet Coke.")
        )

    def test_4(self):
        self.assertEqual(
            "vrybdy wnts m t tlk bt Rbrt Pttnsn nd nt Brn Wllms -  gss ppl jst dn't cr bt Brn!",
            remove_vowels(
                "Everybody wants me to talk about Robert Pattinson and not Brian Williams - I guess people just don't "
                "care about Brian!"
            )
        )

    def test_5(self):
        self.assertEqual(
            "Kty, wht th hll wr y thnkng whn y mrrd lsr Rssll Brnd. Thr s  gy wh hs gt nthng gng,  wst!",
            remove_vowels(
                "Katy, what the hell were you thinking when you married loser Russell Brand. There is a guy who has "
                "got nothing going, a waste!"
            )
        )

    def test_6(self):
        self.assertEqual(
            "Wndmlls r th grtst thrt n th S t bth bld nd gldn gls. Md clms fctnl 'glbl wrmng' s wrs.",
            remove_vowels(
                "Windmills are the greatest threat in the US to both bald and golden eagles. Media claims fictional "
                "'global warming' is worse."
            )
        )

    def test_7(self):
        self.assertEqual(
            "Srry lsrs nd htrs, bt my .Q. s n f th hghst - nd y ll knw t! Pls dn't fl s stpd r nscr, t's nt yr flt",
            remove_vowels(
                "Sorry losers and haters, but my I.Q. is one of the highest - and you all know it! Please don't feel "
                "so stupid or insecure, it's not your fault"
            )
        )

    def test_8(self):
        self.assertEqual(
            "Hppy Thnksgvng t ll -- vn th htrs nd lsrs!",
            remove_vowels("Happy Thanksgiving to all -- even the haters and losers!")
        )

    def test_9(self):
        self.assertEqual(
            "Wtch Ksch sqrm --- f h s nt trthfl n hs ngtv ds  wll s hm jst fr fn!",
            remove_vowels(
                "Watch Kasich squirm --- if he is not truthful in his negative ads I will sue him just for fun!"
            )
        )

    def test_10(self):
        self.assertEqual(
            "bm s, wtht qstn, th WRST VR prsdnt.  prdct h wll nw d smthng rlly bd nd ttlly stpd t shw mnhd!",
            remove_vowels(
                "Obama is, without question, the WORST EVER president. I predict he will now do something really bad "
                "and totally stupid to show manhood!"
            )
        )


if __name__ == "__main__":
    unittest.main()
