import abc
import unittest
from typing import List


class MatrixMoverABC(abc.ABC):
    @abc.abstractmethod
    def __init__(self, matrix: List[List[int]]):
        ...

    @abc.abstractmethod
    def down(self) -> "MatrixMoverABC":
        ...

    @abc.abstractmethod
    def left(self) -> "MatrixMoverABC":
        ...

    @abc.abstractmethod
    def right(self) -> "MatrixMoverABC":
        ...

    @abc.abstractmethod
    def stop(self) -> "MatrixMoverABC":
        ...

    @abc.abstractmethod
    def up(self) -> "MatrixMoverABC":
        ...


class MatrixMover(MatrixMoverABC):
    def __init__(self, matrix: List[List[int]]):
        super().__init__(matrix)
        self.matrix = matrix

    def up(self) -> "MatrixMoverABC":
        self.matrix.append(self.matrix.pop(0))
        return self

    def down(self) -> "MatrixMoverABC":
        self.matrix.insert(0, self.matrix.pop())
        return self

    def right(self) -> "MatrixMoverABC":
        for row in self.matrix:
            row.insert(0, row.pop())
        return self

    def left(self) -> "MatrixMoverABC":
        for row in self.matrix:
            row.append(row.pop(0))
        return self

    def stop(self) -> List[List[int]]:
        return self.matrix


class MatrixMover():
    def __init__(self, matrix):
        self.matrix = matrix

    def up(self):
        line = None
        count = 0
        index = 0
        if len(self.matrix) == 1:
            return self
        for values in self.matrix:
            if 1 in values:
                line = values
                break
            count += 1
        for numbers in line:
            if 1 == numbers:
                break
            index += 1
        self.matrix[count][index] = 0
        if count == 0:
            self.matrix[len(self.matrix) - 1][index] = 1
        else:
            self.matrix[count - 1][index] = 1
        return self

    def down(self):
        line = None
        count = 0
        index = 0
        if len(self.matrix) == 1:
            return self
        for values in self.matrix:
            if 1 in values:
                line = values
                break
            count += 1
        for numbers in line:
            if 1 == numbers:
                break
            index += 1
        self.matrix[count][index] = 0
        if count == len(self.matrix) - 1:
            self.matrix[0][index] = 1
        else:
            self.matrix[count + 1][index] = 1
        return self

    def left(self):
        line = None
        count = 0
        index = 0
        if len(self.matrix) == 1:
            return self
        for values in self.matrix:
            if 1 in values:
                line = values
                break
            count += 1
        for numbers in line:
            if 1 == numbers:
                break
            index += 1
        self.matrix[count][index] = 0
        if index == 0:
            self.matrix[count][-1] = 1
        else:
            self.matrix[count][index - 1] = 1
        return self

    def right(self):
        line = None
        count = 0
        index = 0
        if len(self.matrix) == 1:
            return self
        for values in self.matrix:
            if 1 in values:
                line = values
                break
            count += 1
        for numbers in line:
            if 1 == numbers:
                break
            index += 1
        if self.matrix[count][index] == self.matrix[count][-1]:
            self.matrix[count][0] = 1
        else:
            self.matrix[count][index + 1] = 1
        self.matrix[count][index] = 0
        return self

    def stop(self):
        return self.matrix


class MatrixMover:
    def __init__(self, m):
        self.sx, self.sy = len(m[0]) - 1, len(m) - 1
        self.y = [i for i, x in enumerate(m) if 1 in x][0]
        self.x = [i for i, x in enumerate(m[self.y]) if x == 1][0]
    def c(self):
        self.y = self.sy if self.y < 0 else 0 if self.y > self.sy else self.y
        self.x = self.sx if self.x < 0 else 0 if self.x > self.sx else self.x
    def up(self):
        self.y -= 1
        self.c()
        return self
    def down(self):
        self.y += 1
        self.c()
        return self
    def left(self):
        self.x -= 1
        self.c()
        return self
    def right(self):
        self.x += 1
        self.c()
        return self
    def stop(self):
        return [[1 if cx == self.x and cy == self.y else 0 for cx in range(self.sx + 1)] for cy in range(self.sy + 1)]


class TestMove(unittest.TestCase):
    def setUp(self):
        self.one = [
            [1]
        ]
        self.two = [
            [1, 0],
            [0, 0]
        ]
        self.three = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        self.two_x_three = [
            [0, 0],
            [0, 1],
            [0, 0]
        ]

    def test_1(self):
        self.assertEqual(
            MatrixMover(self.one).up().stop(), [[1]]
        )

    def test_2(self):
        self.assertEqual(
            MatrixMover(self.one).down().stop(), [[1]]
        )

    def test_3(self):
        self.assertEqual(
            MatrixMover(self.one).left().stop(), [[1]]
        )

    def test_4(self):
        self.assertEqual(
            MatrixMover(self.one).right().stop(), [[1]]
        )

    def test_5(self):
        self.assertEqual(
            MatrixMover(self.one).right().up().stop(), [[1]]
        )

    def test_6(self):
        self.assertEqual(
            MatrixMover(self.two).down().right().stop(), [[0, 0], [0, 1]]
        )

    def test_7(self):
        self.assertEqual(
            MatrixMover(self.two).down().down().up().stop(), [[0, 0], [1, 0]]
        )

    def test_8(self):
        self.assertEqual(
            MatrixMover(self.two).left().left().right().stop(), [[0, 1], [0, 0]]
        )

    def test_9(self):
        self.assertEqual(
            MatrixMover(self.three).left().left().down().stop(), [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        )

    def test_10(self):
        self.assertEqual(
            MatrixMover(self.three).up().right().down().down().left().left().up().up().right().down().stop(),
            [
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0]
            ]
        )

    def test_11(self):
        self.assertEqual(
            MatrixMover(self.two_x_three).right().stop(),
            [
                [0, 0],
                [1, 0],
                [0, 0]
            ]
        )


if __name__ == "__main__":
    unittest.main()
