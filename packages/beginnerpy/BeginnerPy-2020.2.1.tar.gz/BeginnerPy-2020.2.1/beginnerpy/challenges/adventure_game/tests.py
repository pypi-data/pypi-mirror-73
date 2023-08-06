from beginnerpy.challenges.adventure_game.game_builder import generate_game
from beginnerpy.challenges.testing.test_case import TestCases


class Tests(TestCases):
    def test_1(self, solution):
        player, grail = generate_game(1)
        assert grail == solution(player)

    def test_2(self, solution):
        player, grail = generate_game(2)
        assert grail == solution(player)

    def test_3(self, solution):
        player, grail = generate_game(3)
        assert grail == solution(player)

    def test_4(self, solution):
        player, grail = generate_game(4)
        assert grail == solution(player)

    def test_5(self, solution):
        player, grail = generate_game(5)
        assert grail == solution(player)

    def test_6(self, solution):
        player, grail = generate_game(6)
        assert grail == solution(player)

    def test_7(self, solution):
        player, grail = generate_game(7)
        assert grail == solution(player)

    def test_8(self, solution):
        player, grail = generate_game(8)
        assert grail == solution(player)

    def test_9(self, solution):
        player, grail = generate_game(9)
        assert grail == solution(player)

    def test_10(self, solution):
        player, grail = generate_game(10)
        assert grail == solution(player)
