from copy import deepcopy
import numpy as np
from settings import *
from board import Board
class AI:
    def __init__(self,main, drawer, board):
    
        self.main = main
        self.drawer = drawer
        self.board = board

        self.grid = board.getGrid()

        self.astar = Astar()

class Astar:
    def __init__(self, grid):
        self.grid = grid

    def g(self, grid):
        return np.amax(grid)/10

    def h(self, grid):
        return sum(np.multiply(grid, WEIGHT))

    def f(self, grid):
        return self.g(grid) + self.h(grid)

    def run(self, depth, grid):
        if depth > DEPTH:
            return self.f(grid)
        for move in MOVES:
            new = deepcopy(grid)
            if Board.check_valid_move(move, new):
                grid, _ = Board.move_on_input(move, grid)
                