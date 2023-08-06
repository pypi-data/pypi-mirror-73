import unittest
from typing import Callable, List, Union


def move(mat: List[List[int]]) -> Callable[[str], Union[Callable, str]]:
    position = [[x, row.index(1)] for x, row in enumerate(mat) if row.count(1) > 0][0]
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    def mover(action: str):
        action = action.casefold()
        if action == "stop":
            return [
                [int([x, y] == position) for y in range(len(mat[0]))]
                for x in range(len(mat))
            ]

        position[0] = position[0] + directions[action][0]
        if position[0] >= len(mat):
            position[0] = 0
        elif position[0] < 0:
            position[0] = len(mat) - 1

        position[1] = position[1] + directions[action][1]
        if position[1] >= len(mat[0]):
            position[1] = 0
        elif position[1] < 0:
            position[1] = len(mat[0]) - 1

        return mover

    return mover


def move(mat: List[List[int]]) -> Callable[[str], Union[Callable, str]]:
    matrix = [row.copy() for row in mat]

    def up():
        matrix.append(matrix.pop(0))

    def down():
        matrix.insert(0, matrix.pop())

    def right():
        for row in matrix:
            row.insert(0, row.pop())

    def left():
        for row in matrix:
            row.append(row.pop(0))

    actions = {
        "up": up,
        "down": down,
        "left": left,
        "right": right
    }

    def mover(action: str):
        action = action.casefold()
        if action == "stop":
            return matrix

        actions[action]()
        return mover

    return mover


import unittest
from typing import Callable, List, Union


# def move(mat: List[List[int]]) -> Callable[[str], Union[Callable, str]]:

def move(mat):
    print(mat)
    coord = [([i], [row.index(1)]) for i, row in enumerate(mat) if 1 in row]
    print(coord)
    y = (coord[0][0])[0];
    x = (coord[0][1])[0];
    print('coord = ', x, y)
    height = len(mat);
    length = len(mat[0]);
    print('height = ', height, 'length = ', length)

    def draw_map(finx, finy):
        nonlocal height
        nonlocal length
        print('new x = ', finx, 'new y = ', finy)
        print('draw map ', mat)
        print('\n')
        mat[y][x] = 0
        mat[finy][finx] = 1
        print('new map = ', mat)
        newmap = mat
        print(newmap)
        return newmap

    cntr = ''

    def moves(mvs):
        nonlocal x
        nonlocal y
        nonlocal height
        nonlocal length
        nonlocal cntr
        print('start x, y = ', x, y)
        cntr = cntr + mvs + ' '
        print('Inner', cntr, 'Added', mvs)
        print('right = ', cntr.count('right'))
        print('left = ', cntr.count('left'))
        print('up = ', cntr.count('up'))
        print('down = ', cntr.count('down'))
        print('stop = ', cntr.count('stop'))
        changex = cntr.count('right') - cntr.count('left');
        print('change x = ', changex)
        changey = cntr.count('down') - cntr.count('up');
        print('change y = ', changey)
        totx = x + changex;
        print('total x = ', totx)
        toty = y + changey;
        print('total y = ', toty)
        print('height, length = ', height, ' ', length)

        if totx < 0:
            if abs(totx) > length - 1:
                remposx = length - 1 - (totx % length); print('new x = ', remposx)
            elif abs(totx) <= length - 1:
                remposx = length - 1 + totx; print('new x = ', remposx)

        if totx >= 0:
            if totx > length - 1:
                remposx = totx % length; print('new x = ', remposx)
            elif totx <= length - 1:
                remposx = totx; print('new x = ', remposx)

        if toty < 0:
            if abs(toty) > height - 1:
                remposy = height - 1 - (toty % height); print('new y = ', remposy)
            elif abs(toty) <= height - 1:
                remposy = height - 1 + toty; print('new y = ', remposy)

        if toty >= 0:
            if toty > height - 1:
                remposy = toty % height; print('new y = ', remposy)
            elif toty <= height - 1:
                remposy = toty; print('new y = ', remposy)

        if cntr.count('stop') == 1: return draw_map(remposx, remposy)

        print('\n')

        return moves

    # print(dirlist)

    # def movedir():
    #    for i, val in enumerate(dirlist):
    #        print(dirlist[i])
    #    return moves

    return moves


def move(mat):
    coord = [([i], [row.index(1)]) for i, row in enumerate(mat) if 1 in row]
    y = (coord[0][0])[0]; x = (coord[0][1])[0]
    height = len(mat); length = len(mat[0])
    cntr = ''

    def moves(mvs):
        nonlocal x
        nonlocal y
        nonlocal height
        nonlocal length
        nonlocal cntr
        cntr = cntr + mvs + ' '
        changex = cntr.count('right')-cntr.count('left')
        changey = cntr.count('down')-cntr.count('up')
        totx = x+changex
        toty = y+changey
        if totx < 0:
            if abs(totx) > length-1: remposx = length-1 - (totx % length)
            elif abs(totx) <= length-1: remposx = length + totx
        if totx >=0:
            if totx > length-1: remposx = totx % length
            elif totx <= length-1: remposx = totx
        if toty < 0:
            if abs(toty) > height-1: remposy = height-1 - (toty % height)
            elif abs(toty) <= height-1: remposy = height + toty
        if toty >= 0:
            if toty > height-1: remposy = toty % height
            elif toty <= height-1: remposy = toty
        if cntr.count('stop') == 1: #draw_map(remposx, remposy)
            mat[y][x]=0
            mat[remposy][remposx]=1
            return mat
        return moves
    return moves


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
            move(self.one)("up")("stop"), [[1]]
        )

    def test_2(self):
        self.assertEqual(
            move(self.one)("down")("stop"), [[1]]
        )

    def test_3(self):
        self.assertEqual(
            move(self.one)("left")("stop"), [[1]]
        )

    def test_4(self):
        self.assertEqual(
            move(self.one)("right")("stop"), [[1]]
        )

    def test_5(self):
        self.assertEqual(
            move(self.one)("right")("up")("stop"), [[1]]
        )

    def test_6(self):
        self.assertEqual(
            move(self.two)("down")("right")("stop"), [[0, 0], [0, 1]]
        )

    def test_7(self):
        self.assertEqual(
            move(self.two)("down")("down")("up")("stop"), [[0, 0], [1, 0]]
        )

    def test_8(self):
        self.assertEqual(
            move(self.two)("left")("left")("right")("stop"), [[0, 1], [0, 0]]
        )

    def test_9(self):
        self.assertEqual(
            move(self.three)("left")("left")("down")("stop"), [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        )

    def test_10(self):
        self.assertEqual(
            move(self.three)("up")("right")("down")("down")("left")("left")("up")("up")("right")("down")("stop"),
            [
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0]
            ]
        )

    def test_11(self):
        self.assertEqual(
            move(self.two_x_three)("right")("stop"),
            [
                [0, 0],
                [1, 0],
                [0, 0]
            ]
        )


if __name__ == "__main__":
    unittest.main()
