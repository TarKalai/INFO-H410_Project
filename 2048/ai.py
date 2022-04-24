from copy import deepcopy
import random
import numpy as np
from settings import *
from math import *

class AI:
    def __init__(self,main, drawer, board):
        self.main = main
        self.drawer = drawer
        self.board = board

        self.grid = self.board.getGrid()

        self.expectimax = Expectimax(self.board)
        self.montecarlo = Montecarlo(self.board)

    def run_expectimax(self):
        _, move = self.expectimax.run(0, self.grid, True)
        self.board.move(move)
        self.grid = self.board.getGrid()

    def run_montecarlo(self):
        move = self.montecarlo.run()
        self.board.move(move)
        self.montecarlo.updateGrid()


class Expectimax:
    def __init__(self, board):
        self.board = board

    def heuristic(self, grid):
        return sum(sum(np.multiply(grid, WEIGHT)))

    def run(self, depth, grid, is_max):
        if depth > DEPTH:
            return self.heuristic(grid), ""
        if self.board.checkGameOver(grid):
            return -1000, ""
        
        if is_max:
            alpha, fmove = -INFINITY(), ""
            for move in MOVES:
                tempgrid = deepcopy(grid)
                if self.board.check_valid_move(move, tempgrid):
                    tempgrid, _ = self.board.move_on_input(move, tempgrid)
                    tempgrid = self.board.add_number(tempgrid)
                    value, _ = self.run(depth+1, tempgrid, not is_max)
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
    def __init__(self, board):
        self.board = board
        self.node = Node(self.board.getGrid())
        self.expandTree(self.node)

    
    def updateGrid(self):
        self.node = Node(self.board.getGrid())
        self.expandTree(self.node)

    def run(self):
        simulation = 0
        while simulation < SIMULATION:
            mothernode = self.node
            while mothernode.getNumberOfChild() > 0:
                mothernode = self.selectWorkingNode(mothernode)
            if mothernode.getNbvisit() == 0:
                self.rollout(mothernode)
                self.updateScoreParent(mothernode, mothernode.getScore())
            else:
                self.expandTree(mothernode)
                child = self.selectWorkingNode(mothernode)
                if child is not None:
                    self.rollout(child)
                    self.updateScoreParent(child, child.getScore())
                else:
                    mothernode.setScore(0)
            simulation += 1
        move = self.end()
        return move

    def end(self):
        score = -INFINITY()
        move = ""
        for child in self.node.getChild():
            if child.getNbvisit()>0:
                temp = child.getScore()/child.getNbvisit()
                if temp>score:
                    score = temp
                    move = child.getMove()
        return move

    def updateScoreParent(self, node, score):
        parent = node.getParent()
        if parent is not None:
            parent.setScore(parent.getScore()+score)
            parent.setNbvisit(parent.getNbvisit()+1)
            self.updateScoreParent(parent, score)
            
    def expandTree(self, node):
        for move in MOVES:
            tempgrid = deepcopy(node.getGrid())
            if self.board.check_valid_move(move, tempgrid):
                tempgrid, _ = self.board.move_on_input(move, tempgrid)
                tempgrid = self.board.add_number(tempgrid)
                child = Node(tempgrid)
                child.setMove(move)
                child.setParent(node)
                node.addChild(child)


    def selectWorkingNode(self, node):
        ucb = -INFINITY()
        finalnode = None
        for child in node.getChild():
            ucbchild = self.formula(child)
            if ucbchild > ucb:
                ucb = ucbchild
                finalnode = child
        return finalnode

    def formula(self, node):
        if node.getNbvisit():
            return node.getScore()/node.getNbvisit() + 2*sqrt(log(self.node.getNbvisit())/node.getNbvisit())
        else:
            return INFINITY()

    def rollout(self, node):
        temp = deepcopy(node.getGrid())
        while not self.board.checkGameOver(temp):
            available = deepcopy(MOVES)
            while True:
                random_index = random.randrange(len(available))
                input_move = available[random_index]
                if not self.board.check_valid_move(input_move, temp):
                    available.remove(input_move)
                else:
                    break
            # random_index = random.randrange(len(available))
            # input_move = MOVES[random_index]
            temp, _ = self.board.move_on_input(input_move, temp)
            temp = self.board.add_number(temp)
        node.setScore(sum(sum(temp))/50)
        node.setNbvisit(1)
        
class Node:
    def __init__(self, grid):
        self.grid = grid
        self.score = 0
        self.nbvisit = 0
        self.parent = None
        self.child = []
        self.move = ""

    def setMove(self, move):
        self.move = move

    def getMove(self):
        return self.move

    def addChild(self, node):
        self.child.append(node)
    
    def getChild(self):
        return self.child
    
    def getNumberOfChild(self):
        return len(self.child)

    def getParent(self):
        return self.parent
    
    def getScore(self):
        return self.score

    def getNbvisit(self):
        return self.nbvisit

    def getGrid(self):
        return self.grid
    
    def setScore(self, score):
        self.score = score

    def setGrid(self, grid):
        self.grid = grid
        
    def setNbvisit(self, nbvisit):
        self.nbvisit = nbvisit
    
    def setParent(self, node):
        self.parent = node
