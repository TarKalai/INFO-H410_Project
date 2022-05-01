import pygame
import random

from settings import *
from copy import deepcopy
from tile import Tile


class Board:
    def __init__(self, main, drawer):

        self.main = main
        self.drawer = drawer
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()

        self.grid = np.zeros((GRIDSIZE, GRIDSIZE), dtype=int)
        self.new_board()

        self.score = 0
        self.commands = {
            'u': self.move_up,
            'd': self.move_down,
            'l': self.move_left,
            'r': self.move_right
        }

    def new_board(self):
        """
        Create a new empty board game with 2 tiles.
        return /
        """
        self.grid = np.zeros((GRIDSIZE, GRIDSIZE), dtype=int)
        self.score = 0
        self.grid = self.add_number(self.grid, nb=2)
        self.update_board()

    def update_board(self):
        """
        Update the board after a move. 
        """
        self.visible_sprites.empty()
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                x = int(col_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                y = int(row_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                Tile((x, y), [self.visible_sprites], self.grid[row_index, col_index])

    def input(self):
        """
        Retrieves the move from the board_input() function of the main.py file which is the input the players has given.
        it will then call the move function and pass the move_input as argument.
        :return: None
        """
        input_move = self.main.board_input()
        if input_move in MOVES:
            self.move(input_move)

    def move(self, input_move):
        """
        First it will check if the input leads to a valid move. If True, it will update the grid based on the move,
        update the score and add a new number at a random place on the board.
        After, it will check if the game is over or not. If the game is over, the state of the game will change
        to 'game_over_state'.
        :param input_move: (String) The move played by the player
        :return: None
        """
        if self.check_valid_move(input_move, self.grid):
            self.grid, self.score = self.commands[input_move](self.grid, self.score)
            self.grid = self.add_number(self.grid)
            self.update_board()
            if self.check_game_over(self.grid):
                self.main.old_state = deepcopy(self.main.state)
                self.main.state = 'game_over_state'
                self.drawer.blurScreen(self)

    def move_on_input(self, input_move, grid, score=0):
        """
        Calls the correct move command based on the input_move received and gives it the grid and the current score as
        arguments.
        :param input_move: (String) The moved that is asked to play.
        :param grid: (Numpy Array) A numpy array of the game.
        :param score: (Int) The score of the current game.
        :return: The grid moved based on the input, and the updated score of the game.
        """
        return self.commands[input_move](grid, score)

    def add_number(self, grid, nb=1):
        """
        Will add number 2 or 4 to the grid at a random available position at the beginning of each turn. In the
        beginning of the game we need to add 2 numbers, so we specify nb = 2.
        :param grid: (Numpy Array) A numpy array of the game.
        :param nb: (Int) Number of numbers to add.
        :return: The grid with the added numbers.
        """
        available_pos = list(zip(*np.where(grid == 0)))
        if len(available_pos) > 0:
            for position in random.sample(available_pos, k=nb):
                if random.random() > 0.1:
                    grid[position] = 2
                else:
                    grid[position] = 4
        return grid

    def run(self):
        """
        :return:
        """
        self.draw()
        self.input()

    def draw(self):
        """
        Draw the tiles and the shortcuts on the screen
        :return: None
        """
        self.visible_sprites.draw(self.display_surface)
        self.drawer.drawBoardShortcuts(self.score)

    def move_up(self, grid, score):
        """
        Will move the tiles upwards and fuse the tiles if they can.
        :param grid: (Numpy Array) A numpy array of the game.
        :param score: (Int) the score of the current game.
        :return: the grid moved upwards, and the updated score of the game.
        """
        check = np.zeros_like(grid, dtype=int)  # A matrice of 0, if the tiles merge, the position will be equal to 1.
        for col in range(GRIDSIZE):  # Lines
            count = 0
            for row in range(GRIDSIZE):  # Colones
                if grid[row, col] != 0:
                    if row > 0 and count > 0 and not check[count - 1, col] \
                            and grid[count - 1, col] == grid[row, col]:
                        grid[count - 1, col] *= 2
                        grid[row, col] = 0
                        check[count - 1, col] += 1
                        score += grid[count - 1, col]
                    elif row != count:
                        grid[count, col] = grid[row, col]
                        grid[row, col] = 0
                        count += 1
                    else:
                        count += 1
        return grid, score

    def move_right(self, grid, score):
        """
        Will rotate the board matrice to the left, thus making it like a right move is an up move. We can thus apply
        move_up and then rotate backward the matrice.
        :param grid: (Numpy Array) A numpy array of the game.
        :param score: (Int) the score of the current game.
        :return: The grid moved rightwards, and the updated score of the game.
        """
        grid = np.rot90(grid, 1)
        grid, score = self.move_up(grid, score)
        grid = np.rot90(grid, -1)
        return grid, score

    def move_left(self, grid, score):
        """
        Will rotate the board matrice to the right, thus making it like a left move is an up move. We can thus apply
        move_up and then rotate backward the matrice.
        :param grid: (Numpy Array) A numpy array of the game.
        :param score: (Int) the score of the current game.
        :return: The grid moved leftwards, and the updated score of the game.
        """
        grid = np.rot90(grid, -1)
        grid, score = self.move_up(grid, score)
        grid = np.rot90(grid, 1)
        return grid, score

    def move_down(self, grid, score):
        """
        Will rotate the board matrice twice to the left, thus making it like a down move is an up move. We can thus
        apply move_up and then rotate backward the matrice.
        :param grid: (Numpy Array) A numpy array of the game.
        :param score: (Int) the score of the current game.
        :return: The grid moved downwards, and the updated score of the game.
        """
        grid = np.rot90(grid, 2)
        grid, score = self.move_up(grid, score)
        grid = np.rot90(grid, 2)
        return grid, score

    def check_valid_move(self, move, grid):
        """
        It will check if the move the player is trying to play is valid or not.
        :param move: (String) The move that tries to be played.
        :param grid: (Numpy Array) A numpy array of the game.
        :return: (Boolean) True if the move is valid, False otherwise.
        """
        if move in MOVES:
            original = deepcopy(grid)
            original, score = self.commands[move](original, 0)
            if not (original == grid).all():
                return True
        return False

    def check_game_over(self, grid):
        """
        It will check if the game is over or not by trying all possible moves (i.e. : 'u','r','d','l').
        :param grid: (Numpy Array) A numpy array of the game.
        :return: (Boolean) True if the game is over, False otherwise.
        """
        for move in MOVES:
            original = deepcopy(grid)
            original, score = self.commands[move](original, 0)
            if not (original == grid).all():
                return False
        return True

    def get_grid(self):
        return self.grid

    def get_score(self):
        return self.score
