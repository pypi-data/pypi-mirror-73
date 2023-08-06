import unittest
from typing import Optional, Tuple


class Game:
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.current_player = 1

    def turn(self, *dice):
        score = self.player_1_score if self.current_player == 1 else self.player_2_score
        score += sum(dice)
        if score > 21:
            score = 0
        if self.current_player == 1:
            self.player_1_score = score
            self.current_player = 2
        else:
            self.player_2_score = score
            self.current_player = 1

    def is_game_over(self):
        return 21 in {self.player_1_score, self.player_2_score}

    def get_scores(self):
        return self.player_1_score, self.player_2_score

    def winner(self):
        if self.is_game_over():
            return 1 if self.player_1_score == 21 else 2
        return None


class Game:
    def __init__(self):
        ...

    def turn(self, *dice: int):
        ...

    def is_game_over(self) -> bool:
        return False

    def get_scores(self) -> Tuple[int, int]:
        return 0, 0

    def winner(self) -> Optional[int]:
        return None


class Game:
    def __init__(self):
        self.first_player = 0
        self.second_player = 0
        self.turn_num = 0

    def get_scores(self):
        return self.first_player, self.second_player

    def is_game_over(self):
        if self.first_player == 21 or self.second_player == 21:
            return True
        else:
            return False

    def turn(self, *dice):
        if self.turn_num % 2 == 0:
            self.first_player += sum(dice)
            if self.first_player > 21:
                self.first_player = 0
        else:
            self.second_player += sum(dice)
            if self.second_player > 21:
                self.second_player = 0
        self.turn_num += 1

    def winner(self):
        if self.first_player == 21:
            return 1
        elif self.second_player == 21:
            return 2
        else:
            return



class TestGame(unittest.TestCase):
    def game_1(self):
        game = Game()
        game.turn(1, 2, 3)  # Player 1 - 6
        game.turn(2, 3, 4)  # Player 2 - 9
        game.turn(1, 2, 3)  # Player 1 - 12
        game.turn(2, 3, 4)  # Player 2 - 18
        game.turn(1, 2, 3)  # Player 1 - 18
        game.turn(1, 1, 1)  # Player 2 - 21 - Game Over
        return game

    def test_1(self):
        game = self.game_1()
        self.assertTrue(game.is_game_over())

    def test_2(self):
        game = self.game_1()
        self.assertEqual(2, game.winner())

    def test_3(self):
        game = self.game_1()
        self.assertEqual((18, 21), game.get_scores())

    def game_2(self):
        game = Game()
        game.turn(1, 2, 3)  # Player 1 - 6
        game.turn(2, 3, 4)  # Player 2 - 9
        game.turn(1, 2, 3)  # Player 1 - 12
        game.turn(2, 3, 4)  # Player 2 - 18
        game.turn(1, 2, 3)  # Player 1 - 18
        game.turn(2, 3, 4)  # Player 2 - 0
        return game

    def test_4(self):
        game = self.game_2()
        self.assertFalse(game.is_game_over())

    def test_5(self):
        game = self.game_2()
        self.assertIsNone(game.winner())

    def test_6(self):
        game = self.game_2()
        self.assertEqual((18, 0), game.get_scores())

    def game_3(self):
        game = Game()
        game.turn(1, 2, 3, 4, 5)  # Player 1 - 15
        game.turn(2, 3, 4, 1, 1)  # Player 2 - 11
        game.turn(1, 2, 3, 4, 5)  # Player 1 - 0
        game.turn(2, 3, 4, 1, 1)  # Player 2 - 0
        game.turn(1, 2, 3, 1, 2)  # Player 1 - 9
        game.turn(2, 3, 4, 5, 6)  # Player 2 - 20
        game.turn(1, 2, 1, 1, 2)  # Player 1 - 16
        game.turn(2, 3, 4, 5, 6)  # Player 2 - 0
        game.turn(1, 1, 1, 1, 1)  # Player 1 - 21
        return game

    def test_7(self):
        game = self.game_3()
        self.assertTrue(game.is_game_over())

    def test_8(self):
        game = self.game_3()
        self.assertEqual(1, game.winner())

    def test_9(self):
        game = self.game_3()
        self.assertEqual((21, 0), game.get_scores())


if __name__ == "__main__":
    unittest.main()
