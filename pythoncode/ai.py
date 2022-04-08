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

        self.minmax = Minmax()

class Minmax:
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, grid):
        return sum(np.multiply(grid, WEIGHT))

    def run(self, depth, grid):
        if depth > DEPTH:
            return self.heuristic(grid)
        if Board.checkGameOver(grid):
            return -1
        value, deplacement = 0, ""
        for move in MOVES:
            new = deepcopy(grid)
            if Board.check_valid_move(move, new):
                grid, _ = Board.move_on_input(move, grid)
                

class Montecarlo:
    pass
                