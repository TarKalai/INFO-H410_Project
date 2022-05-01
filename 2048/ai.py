from copy import deepcopy
import random
from settings import *
from math import *


class AI:
    def __init__(self, main, drawer, board):
        self.main = main
        self.drawer = drawer
        self.board = board

        self.grid = self.board.get_grid()

        self.expectimax = Expectimax(self.board)
        self.montecarlo = Montecarlo(self.board)

    def run_expectimax(self):
        _, move = self.expectimax.run(0, self.grid, True)
        self.board.move(move)
        self.grid = self.board.get_grid()

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
        if self.board.check_game_over(grid):
            return -1000, ""

        if is_max:
            alpha, fmove = -INFINITY(), ""
            for move in MOVES:
                tempgrid = deepcopy(grid)
                if self.board.check_valid_move(move, tempgrid):
                    tempgrid, _ = self.board.move_on_input(move, tempgrid)
                    tempgrid = self.board.add_number(tempgrid)
                    value, _ = self.run(depth + 1, tempgrid, not is_max)
                    if value > alpha:
                        alpha, fmove = value, move
            return alpha, fmove

        else:
            i = 0
            alpha, fmove = 0, ""
            for move in MOVES:
                tempgrid = deepcopy(grid)
                if self.board.check_valid_move(move, tempgrid):
                    i += 1
                    tempgrid, _ = self.board.move_on_input(move, tempgrid)
                    tempgrid = self.board.add_number(tempgrid)
                    value, _ = self.run(depth + 1, tempgrid, not is_max)
                    alpha += value
            if i:
                return alpha / i, fmove


class Montecarlo:
    def __init__(self, board):
        self.board = board
        self.node = Node(self.board.get_grid())
        self.expandTree(self.node)

    def updateGrid(self):
        self.node = Node(self.board.get_grid())
        self.expandTree(self.node)

    def run(self):
        simulation = 0
        while simulation < SIMULATION:
            mothernode = self.node
            while mothernode.get_number_of_child() > 0:
                mothernode = self.selectWorkingNode(mothernode)
            if mothernode.get_number_visit() == 0:
                self.rollout(mothernode)
                self.updateScoreParent(mothernode, mothernode.get_score())
            else:
                self.expandTree(mothernode)
                child = self.selectWorkingNode(mothernode)
                if child is not None:
                    self.rollout(child)
                    self.updateScoreParent(child, child.get_score())
                else:
                    mothernode.set_score(0)
            simulation += 1
        move = self.end()
        return move

    def end(self):
        score = -INFINITY()
        move = ""
        for child in self.node.get_child():
            if child.get_number_visit() > 0:
                temp = child.get_score() / child.get_number_visit()
                if temp > score:
                    score = temp
                    move = child.get_move()
        return move

    def updateScoreParent(self, node, score):
        parent = node.get_parent()
        if parent is not None:
            parent.set_score(parent.get_score() + score)
            parent.set_number_visit(parent.get_number_visit() + 1)
            self.updateScoreParent(parent, score)

    def expandTree(self, node):
        for move in MOVES:
            tempgrid = deepcopy(node.get_grid())
            if self.board.check_valid_move(move, tempgrid):
                tempgrid, _ = self.board.move_on_input(move, tempgrid)
                tempgrid = self.board.add_number(tempgrid)
                child = Node(tempgrid)
                child.set_move(move)
                child.set_parent(node)
                node.add_child(child)

    def selectWorkingNode(self, node):
        ucb = -INFINITY()
        finalnode = None
        for child in node.get_child():
            ucbchild = self.formula(child)
            if ucbchild > ucb:
                ucb = ucbchild
                finalnode = child
        return finalnode

    def formula(self, node):
        if node.get_number_visit():
            return node.get_score() / node.get_number_visit() + 2 * sqrt(
                log(self.node.get_number_visit()) / node.get_number_visit())
        else:
            return INFINITY()

    def rollout(self, node):
        temp = deepcopy(node.get_grid())
        while not self.board.check_game_over(temp):
            available = deepcopy(MOVES)
            while True:
                random_index = random.randrange(len(available))
                input_move = available[random_index]
                if not self.board.check_valid_move(input_move, temp):
                    available.remove(input_move)
                else:
                    break
            temp, _ = self.board.move_on_input(input_move, temp)
            temp = self.board.add_number(temp)
        node.set_score(sum(sum(temp)) / 50)
        node.set_number_visit(1)


class Node:
    def __init__(self, grid):
        self.grid = grid
        self.score = 0
        self.nbvisit = 0
        self.parent = None
        self.child = []
        self.move = ""

    def set_move(self, move):
        self.move = move

    def get_move(self):
        return self.move

    def add_child(self, node):
        self.child.append(node)

    def get_child(self):
        return self.child

    def get_number_of_child(self):
        return len(self.child)

    def get_parent(self):
        return self.parent

    def get_score(self):
        return self.score

    def get_number_visit(self):
        return self.nbvisit

    def get_grid(self):
        return self.grid

    def set_score(self, score):
        self.score = score

    def set_grid(self, grid):
        self.grid = grid

    def set_number_visit(self, nbvisit):
        self.nbvisit = nbvisit

    def set_parent(self, node):
        self.parent = node
