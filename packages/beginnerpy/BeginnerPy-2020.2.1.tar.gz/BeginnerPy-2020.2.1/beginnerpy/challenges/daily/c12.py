class Shiritori:
    def __init__(self):
        self.words = list()
        self.game_over = False

    def play(self, wrd):

        if not self.words:
            self.words.append(wrd)
            return self.words

        if wrd not in self.words and wrd[0] is self.words[-1][-1]:
            self.words.append(wrd)
            return self.words

        self.game_over = True
        return "game over"

    def restart(self):
        del self.words[::]
        self.game_over = False
        return "game restarted"


my_shiritori = Shiritori()

assert my_shiritori.game_over == False
assert my_shiritori.play("apple") == ["apple"]
assert my_shiritori.words == ["apple"]
assert my_shiritori.play("ear") == ["apple", "ear"]
assert my_shiritori.play("rhino") == ["apple", "ear", "rhino"]
assert my_shiritori.play("ocelot") == ["apple", "ear", "rhino", "ocelot"]
assert my_shiritori.game_over is False
assert my_shiritori.play("oops") == "game over"
assert my_shiritori.game_over is True
assert my_shiritori.words == ["apple", "ear", "rhino", "ocelot"]

assert my_shiritori.restart() == "game restarted"
assert my_shiritori.words == []
assert my_shiritori.game_over is False
assert my_shiritori.play("hostess") == ["hostess"]
assert my_shiritori.game_over is False
assert my_shiritori.play("stash") == ["hostess", "stash"]
assert my_shiritori.play("hostess") == "game over"
assert my_shiritori.words == ["hostess", "stash"]
print("Challenge #12 - Shiritori - Success")