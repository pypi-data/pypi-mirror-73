import unittest


def sock_pairs(sock_drawer: str) -> int:
    return sum(x // 2 for x in __import__("collections").Counter(sock_drawer).values())


sock_pairs = lambda string:\
    int(
        sum(
            [
                (
                    string.count(
                        sorted(
                            list(
                                dict.fromkeys(
                                    [
                                        char for char in string
                                    ]
                                )
                            )
                        )[i]
                    ) - (
                        string.count(
                            sorted(
                                list(
                                    dict.fromkeys(
                                        [
                                            char for char in string
                                        ]
                                    )))
                            [i]
                        ) % 2
                    )
                )/2
                for i in range(
                    len(
                        sorted(
                            list(
                                dict.fromkeys(
                                    [
                                        char for char in string
                                    ]
                                )
                            )
                        )
                    )
                )
            ]
        )
    )


class TestSockPairs(unittest.TestCase):
    def test_0(self):
        self.assertEqual(1, sock_pairs("AA"))

    def test_1(self):
        self.assertEqual(2, sock_pairs("ABABC"))

    def test_2(self):
        self.assertEqual(4, sock_pairs("CABBACCC"))

    def test_3(self):
        self.assertEqual(1, sock_pairs("AACDE"))

    def test_4(self):
        self.assertEqual(0, sock_pairs("ACDBE"))

    def test_5(self):
        self.assertEqual(0, sock_pairs(""))

    def test_6(self):
        self.assertEqual(2, sock_pairs("ABABAB"))

    def test_7(self):
        self.assertEqual(2, sock_pairs("AAAAA"))

    def test_8(self):
        self.assertEqual(3, sock_pairs("AAACCBB"))

    def test_9(self):
        sock_drawer = "".join(
            [
                "SCQTXMTAOJFEUPEHEAFRGBRVUMCHPDGOHBKQUGSOLWFKJVBWMBJITCVSKJBYFSSXNCOIRIRTHFKBJPLQZNAMDUOJRUORMHCFHYGW",
                "TMNSCKTACRNILQAVWISNGKHFAMUKGZCGJOSPCIBOCAYSGTJQXSOLYWKRHAOCCGWVWMGFWRUVDGKQXHTMOVBWQBJSWDSGOOGYMYGL",
                "TQLWPEZTXUHTVYCAAPKYIDKWQPQMDEQSKSSUXCWRBGZOCXWVDFSSPESVPZWQQSGCTMKMHOMIVUXSLHHUZQSZZMSSFKBMHPSOWXUI",
                "CHTEIQQKKJPQEPLZVEQPEJFUOMQDZFIILOVXTZAEWDJHQWZJVJMEWMOCSIRJYPAXCTJRGNUKKRHKVRHWRIRQGZODZMNYBEYDMMCL",
                "DNBOMBJYQBBBDBLAYFKMLFZBYIYHCBDYFYQYBOASCCLYMAMYZVKDZUDIMXVRWZLLANUWVQKVMSXNEOJVEQZSWXUHCQGWPPEXEAFX",
                "FNBBTUUXPRWFLIQFDUWQIBLSQCBDEUGOINRLKLTHHARZGOBOSXIDOEVCVYKGRVTRAQHUBCYTJXMJAYZSNPPQFGPBRWXMQERHASIA",
                "ERKARPBGRJRPVOSWZWACUJEMSJQLGUPAWKLXVOSGQALRAQGPHCFWLYCFIBEMQJSGZFFULQGDKABILLBGELKULBPIVDFMXFGJBVKF",
                "HJWWDDXLMDTPZDZEWAAKUFAAREQXBQVBYDBUSHLVDNANGSTSTIBKIHSTAEYSCJPRWKBKOFLPITYABATATCOQBPFFQVOXNCKWIWHP",
                "OLQEXHJKPKBQMAWPCALHBCNFXUJTDTMYDOLNWEYOBRATHUECTFATPROADPGYMKEJZTRAXZECQCMNKYSEFWYIQTXKMMAFZHXPUMQV",
                "GPPSBADXQJYYSLVBKENVGMXHNKFESHDJAEVGDEUFAWUYSEVUDWCBXGRZTNXPYUOZGMDTLOZERTLYRAQPKZZSNPVFLDWJVDEDDZML",
                "GSQWJMMKHGLAYUCGGXDOSTORHLFIWVGDVSNBFFCNIFAEKXPEUOAQFEZITMBVYPFWEJHUZPQZQNZJOUJEXIBSZCSYEOBZNCLYUJMA",
                "TQCHEMYICUBCTTGENMQETRROQVAHGMPHUURQXUSTOOEXJNFZRRYUZDOVSUDPAFBUENBQZJBMCVIYDPWCWBOHBYSMIPERVYNASPCS"
            ]
        )
        self.assertEqual(594, sock_pairs(sock_drawer))



if __name__ == "__main__":
    unittest.main()
