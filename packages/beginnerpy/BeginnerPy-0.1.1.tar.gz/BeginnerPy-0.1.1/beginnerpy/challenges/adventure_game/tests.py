from beginnerpy.challenges.adventure_game.solution import find_the_holy_grail
from beginnerpy.challenges.adventure_game.game_builder import generate_game
import unittest


def run_tests():
    unittest.main(module=__name__)


class TestFindTheHolyGrail(unittest.TestCase):
    def test_1(self):
        player, grail = generate_game(1)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_2(self):
        player, grail = generate_game(2)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_3(self):
        player, grail = generate_game(3)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_4(self):
        player, grail = generate_game(4)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_5(self):
        player, grail = generate_game(5)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_6(self):
        player, grail = generate_game(6)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_7(self):
        player, grail = generate_game(7)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_8(self):
        player, grail = generate_game(8)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_9(self):
        player, grail = generate_game(9)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )

    def test_10(self):
        player, grail = generate_game(10)
        self.assertIs(
            grail,
            find_the_holy_grail(player)
        )
