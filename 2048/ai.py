from copy import deepcopy
import random
from settings import *
from math import *


class AI:
    def __init__(self, main, drawer, board):
        """
        Initialise the AI object with The main class, the drawer and the board.
        :param main: (Object) The Game Class.
        :param drawer: (Object) The Drawer Class.
        :param board: (Object) The Board Class.
        """
        self.main = main
        self.drawer = drawer
        self.board = board

        self.grid = self.board.get_grid()

        self.expectimax = Expectimax(self.board)
        self.montecarlo = Montecarlo(self.board)

    def run_expectimax(self):
        """
        Run a move of the expectimax AI.
        :return: None
        """
        _, move = self.expectimax.run(0, self.grid, True)
        self.board.move(move)
        self.grid = self.board.get_grid()

    def run_montecarlo(self):
        """
        Run a move of the expectimax AI.
        :return: None
        """
        move = self.montecarlo.run()
        self.board.move(move)
        self.montecarlo.update_grid()


class Expectimax:
    def __init__(self, board):
        """
        Initialise Expectimax object with the Board.
        :param board: (Object) The Board Class.
        """
        self.board = board

    def heuristic(self, grid):
        """
        Sum all value of the matrix resulting from the matrix multiplication between the grid of the game with the
        weights associated to each position.
        :param grid: (Numpy Array) The grid of the game.
        :return: (Int) The sum of all the values from the matrix multiplication.
        """
        return sum(sum(np.multiply(grid, WEIGHT)))

    def run(self, depth, grid, is_max):
        """
        Run the Expectimax algorithm. At the root node of the tree, is_max is True, meaning that it will take the
        maximum values between all its children and go wherever the value is maximum. All the children, since they are a
        level beneath the root node have is_max as False. They will thus update their score with the average of the
        scores of all their children. After that it cycles between is_max and not is_max.

        It is thus recommended to use an even number for the depth of the tree to have expectimax run efficiently.
        Otherwise, It will run poorly (meaning it will result in a bad score in average) because the score doesn't take
        into account the randomness by not averaging at the leaf nodes.

        :param depth: (Int) The depth at which the AI will run to.
        :param grid: (Numpy Array) A numpy array of the game.
        :param is_max: (Boolean) True if the node has to take the max value of its children, False if it has to average.
        :return: (Int, String) The value of its heuristic's evaluation, and the move to play.
        """
        if depth > DEPTH:
            return self.heuristic(grid), ""
        if self.board.check_game_over(grid):
            return -1000, ""

        if is_max:
            alpha, final_move = -INFINITY(), ""
            for move in MOVES:
                temp_grid = deepcopy(grid)
                if self.board.check_valid_move(move, temp_grid):
                    temp_grid, _ = self.board.move_on_input(move, temp_grid)
                    temp_grid = self.board.add_number(temp_grid)
                    value, _ = self.run(depth + 1, temp_grid, not is_max)
                    if value > alpha:
                        alpha, final_move = value, move
            return alpha, final_move
        else:
            i = 0
            alpha, final_move = 0, ""
            for move in MOVES:
                temp_grid = deepcopy(grid)
                if self.board.check_valid_move(move, temp_grid):
                    i += 1
                    temp_grid, _ = self.board.move_on_input(move, temp_grid)
                    temp_grid = self.board.add_number(temp_grid)
                    value, _ = self.run(depth + 1, temp_grid, not is_max)
                    alpha += value
            if i:
                return alpha / i, final_move


class Montecarlo:
    def __init__(self, board):
        """
        Initialise the Monte-Carlo object with the Board.
        Creates the first node and expands it directly to create the first children.
        :param board: (Object) The Board Class.
        """
        self.board = board
        self.node = Node(self.board.get_grid())
        self.expand_tree(self.node)

    def update_grid(self):
        """
        Updates the root node with the grid of the game, and expands it to create the first children.
        :return: None
        """
        self.node = Node(self.board.get_grid())
        self.expand_tree(self.node)

    def run(self):
        """
        First the Monte-Carlo algorithme will select the node it will want to either expand or rollout. This is done
        by computing the UCB value of each node by going to the tree. The UCB value make a trade-off between exploration
        and exploitation, see the function formula() for further details.

        Once it has selected a leaf node, we will check if we already made a rollout (meaning if we played randomly till
        the end of the game for this node) or not. If it hasn't done any rollout, meaning it hasn't been visited yet,
        then we do a rollout and backtrack the result to each parent until the root node and update the score of this
        value.

        If it has already been visited, then we expand the node, select the child node by computing the UCB value. And
        make this node do a rollout and back track its results to its parent nodes.

        In the end, when the number of simulation has been exhausted, we select the child that has the highest ratio
        between the score and the number of visits. The move this child has made is the move the AI will output.

        :return: (String) The move to play.
        """
        simulation = 0
        while simulation < SIMULATION:
            node = self.node
            while node.get_number_of_child() > 0:
                node = self.select_working_node(node)
            if node.get_number_visit() == 0:
                self.rollout(node)
                self.update_score_parent(node, node.get_score())
            else:
                self.expand_tree(node)
                child = self.select_working_node(node)
                if child is not None:
                    self.rollout(child)
                    self.update_score_parent(child, child.get_score())
                else:
                    node.set_score(0)  # meaning that it is at the end of the game, and it is pointless to compute.
            simulation += 1
        move = self.end()
        return move

    def end(self):
        """
        Gets the move of the child that has the highest ratio between the score and the number of visits.
        :return: (String) The move of the best child.
        """
        score = -INFINITY()
        move = ""
        for child in self.node.get_child():
            if child.get_number_visit() > 0:
                temp = child.get_score() / child.get_number_visit()
                if temp > score:
                    score = temp
                    move = child.get_move()
        return move

    def update_score_parent(self, node, score):
        """
        Updates the score of all the parent nodes until the root node.
        :param node: (Object) The node whose parent needs their score to be updated.
        :param score: (Int) The score to be added to each parent.
        :return: None
        """
        parent = node.get_parent()
        if parent is not None:
            parent.set_score(parent.get_score() + score)
            parent.set_number_visit(parent.get_number_visit() + 1)
            self.update_score_parent(parent, score)

    def expand_tree(self, node):
        """
        Expands the tree by taking a leaf node and creating child with all the possible move that can be done from
        the grid of the node.
        :param node: (Object) The node which will be expanded.
        :return: None
        """
        for move in MOVES:
            temp_grid = deepcopy(node.get_grid())
            if self.board.check_valid_move(move, temp_grid):
                temp_grid, _ = self.board.move_on_input(move, temp_grid)
                temp_grid = self.board.add_number(temp_grid)
                child = Node(temp_grid)
                child.set_move(move)
                child.set_parent(node)
                node.add_child(child)

    def select_working_node(self, node):
        """
        Will select the child node of the node with the best UCB value.
        :param node: (Object) The node to select its child from.
        :return: (Object) The node with the best UCB value.
        """
        ucb = -INFINITY()
        final_node = None
        for child in node.get_child():
            ucb_child = self.formula(child)
            if ucb_child > ucb:
                ucb = ucb_child
                final_node = child
        return final_node

    def formula(self, node):
        """
        Computes the UCB formula (when not specified the score and visit correspond to the node given by argument) :
        UCB = score/visit + C * sqrt( log(root_visit)/visit )
        C is a constant to make a trade-off between exploitation and exploration. We have decided to put it to 2.

        This UCB formula is used in the Monte-Carlo tree search algorithme to determine which node to explore.
        The left part of the formula corresponds to the exploitation part, and the right part of the equation
        corresponds to the exploitation part.

        If the node has not made a rollout yet, meaning it hasn't been visited yet, its UCB value is infinity.

        :param node: (Object) The node to compute the UCB value of.
        :return: (Int) The UCB value.
        """
        if node.get_number_visit():
            return node.get_score() / node.get_number_visit() + 2 * sqrt(
                log(self.node.get_number_visit()) / node.get_number_visit())
        else:
            return INFINITY()

    def rollout(self, node):
        """
        Will make the node play randomly until the end of the game and recover the final score. The actual grid of the
        node is not modified as a copy has been used to perform the random playing. Once the node has reached the end
        of the game, we set the number of visit to 1 and score of the node as the sum of all the values on the grid
        divided by 50. This is to  provide balance between the exploration and exploitation part of the UCB formula.
        (We first want it to explore, then to exploit).
        :param node: The node which will make a rollout.
        :return: None
        """
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
        self.nb_visit = 0
        self.parent = None
        self.child = []
        self.move = ""

    def get_number_of_child(self):
        """
        Compute the length of the list child and return its value.
        :return: (Int) The number of child of a Node.
        """
        return len(self.child)

    """
    All the setters and getters of the Class Node.
    """
    def set_move(self, move):
        self.move = move

    def get_move(self):
        return self.move

    def add_child(self, node):
        self.child.append(node)

    def get_child(self):
        return self.child

    def get_parent(self):
        return self.parent

    def get_score(self):
        return self.score

    def get_number_visit(self):
        return self.nb_visit

    def get_grid(self):
        return self.grid

    def set_score(self, score):
        self.score = score

    def set_grid(self, grid):
        self.grid = grid

    def set_number_visit(self, nb_visit):
        self.nb_visit = nb_visit

    def set_parent(self, node):
        self.parent = node
