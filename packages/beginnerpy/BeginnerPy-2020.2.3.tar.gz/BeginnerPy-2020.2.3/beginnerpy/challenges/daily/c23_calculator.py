import unittest
from typing import AnyStr, Any, Callable, Union
from abc import ABC, abstractmethod
from functools import wraps


class StackMachine(ABC):
    def __init__(self):
        self.operators = {}
        self.stack = []
        self._load_operators()

    def _load_operators(self):
        for name, attr in self.__class__.__dict__.items():
            if hasattr(attr, "operator_name"):
                self.operators[attr.operator_name] = self._operator_caller(
                    attr,
                    attr.operator_operands,
                    attr.operator_push
                )

    def _operator_caller(self, operator: Callable, num_operands: int, push: bool) -> Callable:
        @wraps(operator)
        def caller():
            ret = operator(self, *[self.stack.pop() for i in range(num_operands)])
            if push:
                self.stack.append(ret)
            return ret

        return caller

    def run(self, instructions: AnyStr) -> Any:
        for token in instructions.split():
            if token in self.operators:
                self.operators[token]()
            elif self.is_literal(token):
                self.stack.append(self.parse_literal(token))
            else:
                return f"Invalid instruction: {token}"
        return self.stack[-1]

    @abstractmethod
    def is_literal(self, token: AnyStr) -> bool:
        return False

    @abstractmethod
    def parse_literal(self, raw_literal: AnyStr) -> Any:
        return None

    @classmethod
    def operation(cls, name: AnyStr, num_operands: int, push: bool = True) -> Callable:
        def get_handler(func: Callable) -> Callable:
            func.operator_name = name
            func.operator_operands = num_operands
            func.operator_push = push
            return func
        return get_handler


class StackCalculator(StackMachine):
    def __init__(self):
        super().__init__()
        self.stack.append(0)

    @StackMachine.operation("+", 2)
    def add(self, a: int, b: int) -> int:
        return a + b

    @StackMachine.operation("-", 2)
    def subtract(self, a: int, b: int) -> int:
        return a - b

    @StackMachine.operation("*", 2)
    def multiply(self, a: int, b: int) -> int:
        return a * b

    @StackMachine.operation("/", 2)
    def divide(self, a: int, b: int) -> int:
        return a // b

    @StackMachine.operation("DUP", 1, False)
    def duplicate(self, top: int):
        self.stack.extend([top] * 2)

    @StackMachine.operation("POP", 1, False)
    def pop(self, *_):
        return

    def is_literal(self, token: AnyStr) -> bool:
        return token.isdigit()

    def parse_literal(self, raw_literal: AnyStr) -> Any:
        return int(raw_literal)


def compute(instructions: AnyStr) -> Union[int, str]:
    return StackCalculator().run(instructions)


class TestCalculator(unittest.TestCase):
    def test_1(self):
        self.assertEqual(compute('12'), 12)

    def test_2(self):
        self.assertEqual(compute('5 6 +'), 11)

    def test_3(self):
        self.assertEqual(compute('3 6 -'), 3)

    def test_4(self):
        self.assertEqual(compute('3 DUP +'), 6)

    def test_5(self):
        self.assertEqual(compute('2 5 - 5 + DUP +'), 16)

    def test_6(self):
        self.assertEqual(compute('9 14 DUP + - 3 POP'), 19)

    def test_7(self):
        self.assertEqual(compute('1 2 3 4 5 POP POP POP'), 2)

    def test_8(self):
        self.assertEqual(compute('13 DUP 4 POP 5 DUP + DUP + -'), 7)

    def test_9(self):
        self.assertEqual(compute('6 5 5 7 * - /'), 5)

    def test_10(self):
        self.assertEqual(compute('4 2 4 * 3 + 5 + / 5 -'), 1)

    def test_11(self):
        self.assertEqual(compute('5 8 + 4 5 1 + POP 13 +'), 17)

    def test_12(self):
        self.assertEqual(compute('x'), 'Invalid instruction: x')

    def test_13(self):
        self.assertEqual(compute('4 6 + x'), 'Invalid instruction: x')

    def test_14(self):
        self.assertEqual(compute('y x *'), 'Invalid instruction: y')

    def test_15(self):
        self.assertEqual(compute(''), 0)

    def test_16(self):
        self.assertEqual(compute('4 POP'), 0)


unittest.main()
