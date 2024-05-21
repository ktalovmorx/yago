# -*- coding: utf-8 -*-
"""
Created on Mon May 15 21:38:56 2017

@author: Luis
"""

# https://gabrielecirulli.github.io/2048/

import random
import sys
import json

EMPTY = 0
OUT = -1
FILE_CONFIG = '2048.ini'


def build_cells(dim: int) -> list[list[int]]:
    cells = []
    for i in range(dim):
        cells.append([EMPTY] * dim)
    return cells

def init(dim: int) -> dict:
    assert dim is None or dim > 2, f'The minimun size is 3'
    with open(FILE_CONFIG) as fconf:
        conf = json.loads(fconf.read())

    if dim is not None:
        conf['dim'] = dim
    else:
        conf['dim'] = int(conf['dim'])
    conf['max_score'] = int(conf['max_score'])

    game = {
        'board': build_cells(conf['dim']),
        'score': 0,
        'max_value': 0,
        'max_score': conf['max_score']
    }
    add_new_cell(game)
    add_new_cell(game)
    return game

def finalize(game: dict) -> None:
    c = {
        'dim': get_size(game),
        'max_score': max(game['max_score'], game['score'])
    }
    with open(FILE_CONFIG, 'w') as conf:
        conf.write(json.dumps(c))



def get_size(game: dict) -> int:
    return len(game['board'])


def set_max_value(game: dict) -> int:
    max_value = 0
    for row in game['board']:
        for cell in row:
            if cell > max_value:
                max_value = cell
    return max_value


def update(game: dict, score: int) -> None:
    game['score'] += score
    set_max_value(game)

def get_row_col(pos: tuple[int, int],
                trasposed: bool = False) -> tuple[int, int]:
    row, col = pos
    if trasposed:
        row, col = col, row
    return row, col

def get_value(game: dict,
              pos: tuple[int, int],
              trasposed: bool = False) -> int:

    row, col = get_row_col(pos, trasposed)
    if row < 0 or row >= get_size(game) or \
       col < 0 or col >= get_size(game):
        val = OUT
    else:
        val = game['board'][row][col]
    return val

def put_value(game: dict,
              pos: tuple[int, int],
              value: int,
              trasposed: bool = False):
    row, col = get_row_col(pos, trasposed)
    game['board'][row][col] = value


def get_free_cells(game: dict) -> list[tuple[int, int]]:
    free_cells = []
    for row in range(len(game['board'])):
        for col in range(len(game['board'])):
            if game['board'][row][col] == EMPTY:
                free_cells.append((row, col))
    return free_cells

def add_new_cell(game: dict) -> None:
    cells = get_free_cells(game)
    if len(cells) > 0:
        pos = random.choice(cells)
        if random.random() < 0.75:
            put_value(game, pos, 2)
        else:
            put_value(game, pos, 4)
    update(game, 0)






def can_move_cell(game: dict, pos: tuple[int, int]) -> bool:
    value = get_value(game, pos)
    if value == EMPTY:
        found_mov = True
    else:
        found_mov = False
        i = 0
        pos_lst = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while i < len(pos_lst) and not found_mov:
            pos_i = (pos[0] + pos_lst[i][0], pos[1] + pos_lst[i][1])
            found_mov = get_value(game, pos_i) == value
            i += 1
    return found_mov

def is_blocked(game: dict) -> bool:
    row = 0
    found_mov = False
    while row < get_size(game) and not found_mov:
        col = 0
        while col < get_size(game) and not found_mov:
            found_mov = can_move_cell(game, (row, col))
            col += 1
        row += 1
    return not found_mov


def move_cell(game: dict,
              current: tuple[int, int],
              move_to: int,
              inc: int,
              move_cols: bool) -> tuple[bool, int, int]:
    score = 0
    moved = False
    move_to_pos = (current[0], move_to)
    move_to_value = get_value(game, move_to_pos, move_cols)
    cur_value = get_value(game, current, move_cols)
    if cur_value != 0:
        if move_to_value == 0:
            put_value(game, move_to_pos, cur_value, move_cols)
            put_value(game, current, 0, move_cols)
            moved = True
        elif move_to_value == cur_value:
            value = 2*cur_value
            put_value(game, move_to_pos, value, move_cols)
            put_value(game, current, 0, move_cols)
            moved = True
            score += value
            move_to += inc
        else:  # move_to_value!=0 and  move_to_value != cur_value
            move_to += inc
            move_to_pos = (move_to_pos[0], move_to)
            moved = current[1] != move_to
            if moved:
                # the order of these two instruction cannot be changed
                put_value(game, current, 0, move_cols)
                put_value(game, move_to_pos, cur_value, move_cols)

    return moved, score, move_to

def move_row(game: dict, row: int, ini: int, end: int,
             move_cols: bool) -> tuple[bool, int]:
    score = 0
    moved = False
    inc = 1
    if ini > end:
        inc = -1
    current = ini + inc
    move_to = ini
    while current != end:
        """
        all the cells between move_to and current (excluding both)
        contains 0.
        move_to <= current (if ini<end)
        """
        pos = (row, current)
        tmp_moved, tmp_score, move_to = \
            move_cell(game, pos, move_to,
                      inc, move_cols)
        score += tmp_score
        moved = moved or tmp_moved
        current += inc
    return moved, score


def move(game: dict, start_end: bool, move_cols: bool) -> bool:
    ini = 0
    end = len(game['board'])
    if start_end:
        ini = len(game['board']) - 1
        end = -1

    score = 0
    moved = False
    for i in range(len(game['board'])):
        tmp_mv, tmp_sc = move_row(game, i, ini, end, move_cols)
        score += tmp_sc
        moved = moved or tmp_mv
    update(game, score)
    return moved


def down(game: dict) -> bool:
    moved = move(game, True, True)
    return moved

def up(game: dict) -> bool:
    moved = move(game, False, True)
    return moved

def left(game: dict) -> bool:
    moved = move(game, False, False)
    return moved


def right(game: dict) -> bool:
    moved = move(game, True, False)
    return moved


def game2str(game: dict) -> str:
    dim = get_size(game)
    line = '-' * (6*dim + 1) + '\n'
    res = line
    size = get_size(game)
    for row in range(size):
        scol = '|'
        for col in range(size):
            val = get_value(game, (row, col))
            if val == 0:
                val = ''
            scol += f'{val:5}|'
        res += scol + '\n' + line
    score = game['score']
    mval = game['max_value']
    res += f'{mval:6}-{score:6}'
    return res

def play(game: dict):
    print(game2str(game))
    move = 'X'
    while move != 'q' and not is_blocked(game):
        move = input('use the keys adwx (q to quit):')
        moved = False
        if move == 'a':
            moved = left(game)
        elif move == 'd':
            moved = right(game)
        elif move == 'w':
            moved = up(game)
        elif move == 'x':
            moved = down(game)
        if moved:
            add_new_cell(game)
        print(game2str(game))

def main(dim):
    game = init(dim)
    play(game)
    finalize(game)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        dim = None
    else:
        dim = int(sys.argv[1])
    if len(sys.argv) == 3:
        random.seed(int(sys.argv[3]))
    main(dim)

# TESTS = [
#         (
#             [[2,2,2,2],
#              [4,2,0,2],
#              [2,2,0,0],
#              [2,0,0,2]], 'left;__str__'
#         ), (
#             [[2,2,2,2],
#              [4,4,0,0],
#              [2,2,0,0],
#              [4,0,0,0]], 'up;__str__'
#         ), (
#             [[2,0,0,0],
#              [0,2,0,0],
#              [0,0,2,0],
#              [0,0,0,2]], 'up;__str__'
#         ), (
#             [[2,0,0,0],
#              [0,2,0,0],
#              [0,0,2,0],
#              [0,0,0,2]], 'right;__str__'
#         ), (
#             [[2,2,4,2],
#              [2,2,0,2],
#              [2,2,2,0],
#              [2,0,0,2]], 'left;__str__'
#         ), (
#             [[2,2,4,2],
#              [2,2,0,2],
#              [2,2,2,0],
#              [2,0,0,2]], 'right;__str__'
#         ), (
#             [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]], 'down;__str__'
#         ), (
#             [[4,2,4,2,4],
#              [4,2,0,2,0],
#              [2,4,2,0,4],
#              [2,0,4,2,0],
#              [0,0,0,0,8]], 'down;__str__'
#         ), (
#             [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]], 'is_blocked'
#         ), (
#             [[4,2,4,2],
#              [2,4,2,4],
#              [4,2,4,2],
#              [2,4,2,4]], 'is_blocked'
#         ), (
#             [[0,8,16,8],
#              [8,16,8,16],
#              [16,8,0,8],
#              [0,16,8,16]], 'add_new_cell;add_new_cell;is_blocked'
#         ), (
#             [[0,8,16,8],
#              [8,16,8,16],
#              [16,8,0,8],
#              [0,16,8,16]], 'put_value 0 0 8;put_value 3 3 8;put_value 3 0 16;add_new_cell;is_blocked'
#         ), (
#             [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]], 'put_value 1 2 8;__str__'
#         ), (
#             [[4, 4, 0, 0],
#              [4, 4, 0, 0],
#              [4, 0, 0, 0],
#              [4, 0, 0, 0]],
#             'up;__str__'
#         ) ]

# import os


# def gen_tests():
#     tests_dir = '../tests/'
#     if not os.path.exists(tests_dir):
#         os.mkdir(tests_dir)
#     for i in range(len(TESTS)):
#         this_test_dir = tests_dir + 'T{0:02}/'.format(i+1)
#         if not os.path.exists(this_test_dir):
#             os.mkdir(this_test_dir)
#         game = Game2048(TESTS[i][0])
#         testin = open(this_test_dir+'test.in', 'w')
#         testout = open(this_test_dir+'test.out', 'w')
#         testin.write(str(game))
#         testin.write('\n')
#         commands = TESTS[i][1].split(';')
#         testin.write(str('\n'.join(commands)))
#         for cmd in commands:
#             cmdargs = cmd.split(' ')
#             args = map(int, cmdargs[1:])
#             method = getattr(game, cmdargs[0])
#             value = method(*args)
#             if not value is None:
#                 print(value)
#                 testout.write(str(value) + '\n')




# def test_board1():
#     cells = [[2,2,2,2],
#              [4,2,0,2],
#              [2,2,0,0],
#              [2,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, True)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board2():
#     cells = [[2,0,0,0],
#              [0,2,0,0],
#              [0,0,2,0],
#              [0,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, True)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board3():
#     cells = [[2,0,0,0],
#              [0,2,0,0],
#              [0,0,2,0],
#              [0,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(True, False)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board4():
#     cells = [[2,0,0,0],
#              [0,2,0,0],
#              [0,0,2,0],
#              [0,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, False)
#     print('{0}:{1}:{2}'.format(board, moved, score))


# def test_board5():
#     cells = [[2,2,4,2],
#              [2,2,0,2],
#              [2,2,2,0],
#              [2,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, True)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board6():
#     cells = [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, True)
#     print('{0}:{1}:{2}'.format(board, moved, score))


# def test_board7():
#     cells = [[2,2,4,2],
#              [2,2,0,2],
#              [2,2,2,0],
#              [2,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, False)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board8():
#     cells = [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(False, False)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board9():
#     cells = [[2,2,4,2],
#              [2,2,0,2],
#              [2,2,2,0],
#              [2,0,0,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(True, False)
#     print('{0}:{1}:{2}'.format(board, moved, score))

# def test_board10():
#     cells = [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]]
#     board = Board(cells)
#     print(board)
#     moved, score = board.move(True, False)
#     print('{0}:{1}:{2}:{3}'.format(board, moved, score, board.get_max_value()))

# def test_board11():
#     cells = [[4,2,4,2],
#              [4,2,0,2],
#              [2,4,2,0],
#              [2,0,4,2]]
#     board = Board(cells)
#     print('{0}:{1}:{2}'.format(board, board.is_blocked(), board.get_max_value()))

# def test_board12():
#     cells = [[4,2,4,2],
#              [2,4,2,4],
#              [4,2,4,2],
#              [2,4,2,4]]
#     board = Board(cells)
#     print('{0}:{1}:{2}'.format(board, board.is_blocked()), board.get_max_value())
