class StateMachine:
    def __init__(self):
        self.value = None
        self.start = State("<start>")
        self.current_state = self.start

    def transition(self, state):
        self.value = self.current_state.transition(state)
        self.current_state = state


class State:
    def __init__(self, name, default_rule=None):
        self.name = name
        self.transitions = {}
        self.default_rule = default_rule

    def add_rule(self, edge, *states):
        for state in states:
            self.transitions[state] = edge

    def transition(self, state):
        return self.transitions.get(state, self.default_rule)


def find_cadence(chords: list) -> str:
    states = {
        "I": State("I", "no cadence"),
        "IV": State("IV", "no cadence"),
        "V": State("V", "interrupted"),
        "any": State("any", "no cadence")
    }

    machine = StateMachine()

    machine.start.default_rule = "no cadence"
    states["any"].add_rule("imperfect", states["V"])
    states["V"].add_rule("perfect", states["I"])
    states["IV"].add_rule("plagal", states["I"])
    states["I"].add_rule("imperfect", states["V"])
    states["IV"].add_rule("imperfect", states["V"])

    for chord in chords:
        machine.transition(states.get(chord.upper(), states["any"]))

    return machine.value


assert find_cadence(["I", "IV", "V"]) == "imperfect"
assert find_cadence(["ii", "V", "I"]) == "perfect"
assert find_cadence(["I", "IV", "I", "V", "vi"]) == "interrupted"
assert find_cadence(["I", "IV", "I", "V", "IV"]) == "interrupted"
assert find_cadence(["I", "III", "IV", "V"]) == "imperfect"
assert find_cadence(["I", "IV", "I"]) == "plagal"
assert find_cadence(["V", "IV", "I"]) == "plagal"
assert find_cadence(["V", "IV", "V", "I"]) == "perfect"
assert find_cadence(["V", "IV", "V", "I", "vi"]) == "no cadence"
assert find_cadence(["V", "IV", "V", "III", "vi"]) == "no cadence"
assert find_cadence(["II", "V"]) == "imperfect"
print("Success")