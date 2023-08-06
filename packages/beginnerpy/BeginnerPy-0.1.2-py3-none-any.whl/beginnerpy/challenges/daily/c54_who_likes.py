import unittest
from typing import List


def likes(users: List[str]) -> str:
    if not users:
        return "no one likes this"

    if len(users) == 1:
        return f"{users[0]} likes this"

    primary = [users[0]]
    secondary = users[1]

    if len(users) > 2:
        primary.append(secondary)
        secondary = users[2]

    if len(users) > 3:
        secondary = f"{len(users) - 2} others"

    return f"{', '.join(primary)} and {secondary} like this"


class TestLikes(unittest.TestCase):
    def test_1(self):
        self.assertEqual('no one likes this', likes([]))

    def test_2(self):
        self.assertEqual('Peter likes this', likes(['Peter']))

    def test_3(self):
        self.assertEqual('Jacob and Alex like this', likes(['Jacob', 'Alex']))

    def test_4(self):
        self.assertEqual('Max, John and Mark like this', likes(['Max', 'John', 'Mark']))

    def test_5(self):
        self.assertEqual('Alex, Jacob and 2 others like this', likes(['Alex', 'Jacob', 'Mark', 'Max']))

    def test_6(self):
        self.assertEqual('Zech.Codes, Jacob and 2 others like this', likes(['Zech.Codes', 'Jacob', 'Mark', 'Max']))


if __name__ == "__main__":
    unittest.main()
