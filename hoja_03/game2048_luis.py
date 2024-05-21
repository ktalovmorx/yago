# -*- coding: utf-8 -*-
"""
Created on Mon May 15 21:38:56 2017

@author: Luis
"""

# https://gabrielecirulli.github.io/2048/

import random

class Game2048(object):

    def __init__(self, cells):
        self.__board__ = Board(cells)
        self.__max_value__ = self.__board__.get_max_value()
        self.__score__ = 0


    def score(self):
        return self.__score__    
    
    def max_cell(self):
        return self.__max_value__
        
    def is_blocked(self):
        return self.__board__.is_blocked()
        
    
    def get_size(self):
        return self.__board__.get_size()
        
        
    def get_value(self, row, col):
        return self.__board__.get_value(row, col)
                
    
    def put_value(self, row, col, value):
        self.__board__.put_value(row, col, value)
        self.__update__(0)
    
    def add_new_cell(self):
        cells = self.__board__.get_free_cells()
        if len(cells)>0:
            (row, col) = random.choice(cells)
            if random.random() < 0.75:
                self.__board__.put_value(row, col, 2)
            else:
                self.__board__.put_value(row, col, 4)
        self.__update__(0)
    
    
    def __update__(self, score): 
        self.__score__ += score 
        self.__max_value__ = self.__board__.get_max_value()

            
    def down(self):
        moved, score = self.__board__.move(True, False)
        self.__update__(score)
        return moved
        
    def up(self):
        moved, score = self.__board__.move(False, False)
        self.__update__(score)
        return moved
    
    
    def left(self):
        moved, score = self.__board__.move(False, True)
        self.__update__(score)
        return moved
    
    
    def right(self):
        moved, score = self.__board__.move(True, True)
        self.__update__(score)
        return moved
    
    
    def __str__(self):
        res = str(self.__board__)
        res += '{0:6}-{1:6}'.format(self.__max_value__, self.__score__)
        return res


class Board(object):

    EMPTY = 0
    OUT = -1
        
    def __init__(self, cells):
        """
        precondition:
        -------------
          The minimun size of the board is 2x2
        """
        if len(cells)<0:
            raise Exception('The minimun size of the board is 2')
        if len(cells) != len(cells[0]):
            raise Exception('The matrix must be square')
        self.cells = cells

        
    def __can_move_cell__(self, row, col):
        value = self.cells[row][col]
        if value == 0:
            found_mov = True
        else:
            found_mov = False
            i = 0
            pos_lst = [(-1,0),(1,0),(0,-1),(0,1)] 
            while i < len(pos_lst) and not found_mov:
                row_i = row + pos_lst[i][0]
                col_i = col + pos_lst[i][1]
                found_mov = self.get_value(row_i, col_i) == value
                i += 1
        return found_mov
            
    def is_blocked(self):
        row = 0
        found_mov = False
        while row < self.get_size() and not found_mov:
            col = 0
            while col < self.get_size() and not found_mov:
                found_mov = self.__can_move_cell__(row, col)
                col += 1
            row += 1
        return not found_mov
        
    
    def get_size(self):
        return len(self.cells)
        
        
    def get_value(self, row, col, trasposed=False):
        if row<0 or row>=self.get_size() or \
           col<0 or col>=self.get_size():
           return Board.OUT
        if not trasposed:
            return self.cells[row][col]
        else:
            return self.cells[col][row]
            
    
    def put_value(self, row, col, value, trasposed=False):
        if not trasposed:
            self.cells[row][col] = value
        else:
            self.cells[col][row] = value
    
    
    def get_free_cells(self):
        free_cells = []
        for row in range(len(self.cells)):
            for col in range(len(self.cells)):
                if self.cells[row][col] == Board.EMPTY:
                    free_cells.append((row, col))
        return free_cells
                    
    def __move_cell__(self, row_col, move_to, current, inc, trasposed):
        score = 0
        moved = False
        move_to_value = self.get_value(row_col, move_to, trasposed)
        cur_value = self.get_value(row_col, current, trasposed)
        if cur_value != 0:
            if move_to_value == 0:
                self.put_value(row_col, move_to, cur_value, trasposed)
                self.put_value(row_col, current, 0, trasposed)
                moved = True
            elif move_to_value == cur_value:
                value = 2*cur_value
                self.put_value(row_col, move_to, value, trasposed)
                self.put_value(row_col, current, 0, trasposed)
                moved = True
                score += value
                move_to += inc
            else: # move_to_value!=0 and  move_to_value != cur_value
                #print('1-{0}:{1}:{2}:{3}'.format(self,move_to, current,inc))
                move_to += inc
                moved = current != move_to
                if moved:
                    # the order of these two instruction cannot be changed
                    self.put_value(row_col, current, 0, trasposed)
                    self.put_value(row_col, move_to, cur_value, trasposed)
                #print('2-{0}:{1}:{2}'.format(self,move_to, current))
                    
        return moved, score, move_to
                    
    def __move_row_col__(self, row_col, ini, end, move_rows):
        trasposed = not move_rows
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
            tmp_moved, tmp_score, move_to = self.__move_cell__(row_col, move_to, current, inc, trasposed)
            #print('{0}:{1}:{2}'.format(self,move_to, current))
            score += tmp_score
            moved = moved or tmp_moved 
            current += inc
        return moved, score
        

    def move(self, start_end, move_rows):
        ini = 0
        end = len(self.cells) 
        if start_end:
            ini = len(self.cells) -1
            end = -1
        
        score = 0
        moved = False
        for i in range(len(self.cells)):
            tmp_mv, tmp_sc = self.__move_row_col__(i, ini, end, move_rows)
            score += tmp_sc
            moved = moved or tmp_mv
        
        return moved, score
        
        
    def get_max_value(self):    
        max_value = 0
        for row in self.cells:
            for cell in row:
                if cell>max_value:
                    max_value = cell
        return max_value
        
        
    def __str__(self):
        res = ''
        size = self.get_size()
        for row in range(size):
            for col in range(size):
                res += '{0:5}'.format(self.get_value(row, col))
            res += '\n'
	
        return res
        
    
class Controller(object):
    
    def __init__(self, dim, num_initial_cells, seed):
        random.seed(seed)
        self.game = Game2048(self.build_cells(dim))
        for i in range(num_initial_cells):
            self.game.add_new_cell()
    
    @staticmethod
    def build_cells(dim):
        cells = []
        for i in range(dim):
            cells.append([Board.EMPTY] * dim)
        return cells
        
    def play(self):
        print(self.game)
        move = 'X'
        while move != 'q' and not self.game.is_blocked():
            move = input('use the keys adwx:')
            if move == 'a':
                self.game.left()
            elif move == 'd':
                self.game.right()
            elif move == 'w':
                self.game.up()
            elif move == 'x':
                self.game.down()
            self.game.add_new_cell()
            print(self.game)
            
           
def main(seed=0):
     controller = Controller(4, 2, seed)
     controller.play()

     
TESTS = [
        (
            [[2,2,2,2],
             [4,2,0,2],
             [2,2,0,0],
             [2,0,0,2]], 'left;__str__'
        ), (
            [[2,2,2,2],
             [4,4,0,0],
             [2,2,0,0],
             [4,0,0,0]], 'up;__str__'
        ), (
            [[2,0,0,0],
             [0,2,0,0],
             [0,0,2,0],
             [0,0,0,2]], 'up;__str__'
        ), (
            [[2,0,0,0],
             [0,2,0,0],
             [0,0,2,0],
             [0,0,0,2]], 'right;__str__'
        ), (
            [[2,2,4,2],
             [2,2,0,2],
             [2,2,2,0],
             [2,0,0,2]], 'left;__str__'
        ), (
            [[2,2,4,2],
             [2,2,0,2],
             [2,2,2,0],
             [2,0,0,2]], 'right;__str__'
        ), (
            [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]], 'down;__str__'
        ), (
            [[4,2,4,2,4],
             [4,2,0,2,0],
             [2,4,2,0,4],
             [2,0,4,2,0],
             [0,0,0,0,8]], 'down;__str__'
        ), (
            [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]], 'is_blocked'
        ), (
            [[4,2,4,2],
             [2,4,2,4],
             [4,2,4,2],
             [2,4,2,4]], 'is_blocked'
        ), (
            [[0,8,16,8],
             [8,16,8,16],
             [16,8,0,8],
             [0,16,8,16]], 'add_new_cell;add_new_cell;is_blocked'
        ), (
            [[0,8,16,8],
             [8,16,8,16],
             [16,8,0,8],
             [0,16,8,16]], 'put_value 0 0 8;put_value 3 3 8;put_value 3 0 16;add_new_cell;is_blocked'
        ), (
            [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]], 'put_value 1 2 8;__str__'
        ), (
            [[4, 4, 0, 0],
             [4, 4, 0, 0], 
             [4, 0, 0, 0],
             [4, 0, 0, 0]],
            'up;__str__'            
        ) ]
        
import os


def gen_tests():
    tests_dir = '../tests/'
    if not os.path.exists(tests_dir):
        os.mkdir(tests_dir)
    for i in range(len(TESTS)):
        this_test_dir = tests_dir + 'T{0:02}/'.format(i+1)
        if not os.path.exists(this_test_dir):
            os.mkdir(this_test_dir)
        game = Game2048(TESTS[i][0])
        testin = open(this_test_dir+'test.in', 'w')
        testout = open(this_test_dir+'test.out', 'w')
        testin.write(str(game))
        testin.write('\n')
        commands = TESTS[i][1].split(';')
        testin.write(str('\n'.join(commands)))
        for cmd in commands:
            cmdargs = cmd.split(' ')
            args = map(int, cmdargs[1:])
            method = getattr(game, cmdargs[0])
            value = method(*args)
            if not value is None:
                print(value)
                testout.write(str(value) + '\n')
            

            
                 
def test_board1():
    cells = [[2,2,2,2],
             [4,2,0,2],
             [2,2,0,0],
             [2,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, True)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board2():
    cells = [[2,0,0,0],
             [0,2,0,0],
             [0,0,2,0],
             [0,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, True)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board3():
    cells = [[2,0,0,0],
             [0,2,0,0],
             [0,0,2,0],
             [0,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(True, False)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board4():
    cells = [[2,0,0,0],
             [0,2,0,0],
             [0,0,2,0],
             [0,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, False)
    print('{0}:{1}:{2}'.format(board, moved, score))


def test_board5():
    cells = [[2,2,4,2],
             [2,2,0,2],
             [2,2,2,0],
             [2,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, True)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board6():
    cells = [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, True)
    print('{0}:{1}:{2}'.format(board, moved, score))

    
def test_board7():
    cells = [[2,2,4,2],
             [2,2,0,2],
             [2,2,2,0],
             [2,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, False)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board8():
    cells = [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(False, False)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board9():
    cells = [[2,2,4,2],
             [2,2,0,2],
             [2,2,2,0],
             [2,0,0,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(True, False)
    print('{0}:{1}:{2}'.format(board, moved, score))

def test_board10():
    cells = [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]]
    board = Board(cells)
    print(board)
    moved, score = board.move(True, False)
    print('{0}:{1}:{2}:{3}'.format(board, moved, score, board.get_max_value()))

def test_board11():
    cells = [[4,2,4,2],
             [4,2,0,2],
             [2,4,2,0],
             [2,0,4,2]]
    board = Board(cells)
    print('{0}:{1}:{2}'.format(board, board.is_blocked(), board.get_max_value()))

def test_board12():
    cells = [[4,2,4,2],
             [2,4,2,4],
             [4,2,4,2],
             [2,4,2,4]]
    board = Board(cells)
    print('{0}:{1}:{2}'.format(board, board.is_blocked()), board.get_max_value())



