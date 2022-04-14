from copy import deepcopy
import numpy as np
from settings import *

class AI:
    def __init__(self,main, drawer, board):
    
        self.main = main
        self.drawer = drawer
        self.board = board

        self.grid = self.board.getGrid()

        self.expectimax = Expectimax(self.board)

    def run_expectimax(self):
        _, move = self.expectimax.run(0, self.grid, True)
        self.board.move(move)
        self.grid = self.board.getGrid()

class Expectimax:
    def __init__(self, board):
        self.board = board
        pass

    def heuristic(self, grid):
        return sum(sum(np.multiply(grid, WEIGHT)))

    def run(self, depth, grid, is_max):
        if depth > DEPTH:
            return self.heuristic(grid), ""
        if self.board.checkGameOver(grid):
            return -1000, ""
        
        
        if is_max:
            alpha, fmove = -9999, ""
            for move in MOVES:
                tempgrid = deepcopy(grid)
                if self.board.check_valid_move(move, tempgrid):
                    tempgrid, _ = self.board.move_on_input(move, tempgrid)
                    tempgrid = self.board.add_number(tempgrid)
                    value,_ = self.run(depth+1, tempgrid, not is_max)
                    if value > alpha:
                        alpha, fmove = value, move
            return alpha, fmove

        else:
            i = 0
            alpha, fmove = 0, ""
            for move in MOVES:
                tempgrid = deepcopy(grid)
                if self.board.check_valid_move(move, tempgrid):
                    i+=1
                    tempgrid, _ = self.board.move_on_input(move, tempgrid)
                    tempgrid = self.board.add_number(tempgrid)
                    value, _ = self.run(depth+1, tempgrid, not is_max)
                    alpha += value
            if i:
                return alpha/i, fmove
                

class Montecarlo:
    pass
                