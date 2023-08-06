import unittest


def correct_inequality(expression: str) -> bool:
    tokens = expression.split(" ")
    for index in range(0, len(tokens) - 2, 2):
        a, op, b = tokens[index:index+3]
        if op not in {">", "<"} or not a.isdigit() or not b.isdigit():
            return False
        elif op == "<" and int(a) >= int(b):
            return False
        elif op == ">" and int(a) <= int(b):
            return False
    return len(tokens) >= 3 and (len(tokens) - 3) % 2 == 0


def correct_inequality(expression: str) -> bool:
    try:
        ret = eval(expression)
    except Exception:
        return False
    else:
        return isinstance(ret, bool) and ret


correct_inequality=lambda e:(lambda t:all(((a:=t[i]).isdigit()and(o:=t[i+1])in"<>"and(b:=t[i+2]).isdigit()and((o==">"and int(a)>int(b)) or (o=="<"and int(a)<int(b))) for i in range(0,len(t)-2,2)))if len(t)>=3 and(len(t)-3)%2==0 else False)(e.split())
correct_inequality=lambda e:False if len(l:=e.split())<3 or not all(t.isdigit()for t in[l[0],l[-1]]) or all(t.isdigit()for t in l)or not all(int(l[i-1])<int(l[i+1])if t=="<"else int(l[i-1])>int(l[i+1])for i,t in enumerate(l)if t in"<>")else True


def correct_inequality(expression: str) -> bool:
    splt = expression.split(' ')
    res = []
    if len(splt) < 3:
        return False
    for i in range(0, len(splt)-2, 2):
        res.append(splt[i].isdigit() and splt[i+2].isdigit())
        if splt[i+1] == '>':
            res.append(int(splt[i]) > int(splt[i+2]))
        elif splt [i+1] == '<':
            res.append(int(splt[i]) < int(splt[i+2]))
        else:
            return False
    return all(res)


class TestCorrectInequality(unittest.TestCase):
    def test_1(self):
        self.assertTrue(correct_inequality("3 < 7 < 11"))

    def test_2(self):
        self.assertFalse(correct_inequality("13 > 44 > 33 > 1"))

    def test_3(self):
        self.assertTrue(correct_inequality("1 < 2 < 6 < 9 > 3"))

    def test_4(self):
        self.assertTrue(correct_inequality("4 > 3 > 2 > 1"))

    def test_5(self):
        self.assertTrue(correct_inequality("5 < 7 > 1"))

    def test_6(self):
        self.assertFalse(correct_inequality("5 > 7 > 1"))

    def test_7(self):
        self.assertFalse(correct_inequality("9 < 9"))

    def test_8(self):
        self.assertFalse(correct_inequality("9 <"))

    def test_9(self):
        self.assertFalse(correct_inequality("9 8 7"))

    def test_10(self):
        self.assertFalse(correct_inequality(""))

    def test_11(self):
        self.assertFalse(correct_inequality("11"))


if __name__ == "__main__" and False:
    unittest.main()
