import pygame
import numpy as np
from settings import *
from copy import deepcopy
from tile import Tile
import random

moves = ['u', 'l', 'r', 'd']


class Board:
    def __init__(self):
        # get the display surface

        self.display_surface = pygame.display.get_surface()
        # sprite group setup

        self.visible_sprites = pygame.sprite.Group()

        self.grid = np.zeros((GRIDSIZE, GRIDSIZE), dtype=int)
        self.create_board()

        self.canMove = True
        self.score = 0
        self.commands = {
            'u': self.move_up,
            'd': self.move_down,
            'l': self.move_left,
            'r': self.move_right
        }


    def create_board(self):
        self.add_number(nb=2)
        self.update_board()
        

    def update_board(self):
        self.visible_sprites.empty()
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                x = int(col_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                y = int(row_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                Tile((x, y),  [self.visible_sprites], self.grid[row_index, col_index])
    

    def input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_z:
                        self.move('u')
                        return 
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move('r')
                        return 
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                        self.move('l')
                        return
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.move('d')
                        return
                    elif event.key == pygame.K_ESCAPE:
                        return 'q' # TODO ecrirela fonction qui appel le menu
    
    def move(self, input):
        print("Je suis dans le move")
        self.commands[input]()
        self.add_number()
        self.update_board()

    def add_number(self, nb=1):
        """
        Will add number 2 or 4 to the grid at a random available position at the begining of each turn. In the
        beginning of the game we need to add 2 numbers, so we specify nb = 2.
        :param nb: number of numbers to add
        :return: /
        """
        available_pos = list(zip(*np.where(self.grid == 0)))
        if len(available_pos) > 0:
            for position in random.sample(available_pos, k=nb):
                if random.random() > 0.1:
                    self.grid[position] = 2
                else:
                    self.grid[position] = 4


    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.input()


    def move_up(self, test_move=False):
        """
            Will move the tiles upwards and fuse the tiles if they can.
        """
        check = np.zeros_like(self.grid, dtype=int)  # a matrice of 0, if the tiles merge, the position of the merge
        for col in range(GRIDSIZE):  # Lines
            count = 0
            for row in range(GRIDSIZE): # Colones
                if self.grid[row, col] != 0:
                    if row > 0 and count > 0 and not check[count - 1, col] \
                            and self.grid[count - 1, col] == self.grid[row, col]:
                        self.grid[count - 1, col] *= 2
                        self.grid[row, col] = 0
                        check[count - 1, col] += 1
                        if not test_move:
                            self.score += self.grid[count - 1, col]
                    elif row != count:
                        self.grid[count, col] = self.grid[row, col]
                        self.grid[row, col] = 0
                        count += 1
                    else:
                        count += 1

    def move_right(self, test_move=False):
        """
            Will rotate the board matrice to the left, thus making it like a right move is an up move. We can thus apply
            move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, 1)
        self.move_up(test_move)
        self.grid = np.rot90(self.grid, -1)

    def move_left(self, test_move=False):
        """
            Will rotate the board matrice to the right, thus making it like a left move is an up move. We can thus apply
            move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, -1)
        self.move_up(test_move)
        self.grid = np.rot90(self.grid, 1)

    def move_down(self, test_move=False):
        """
            Will rotate the board matrice twice to the left, thus making it like a down move is an up move. We can thus
            apply move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, 2)
        self.move_up(test_move)
        self.grid = np.rot90(self.grid, 2)

    def check_valid_move(self, move):
        """
            It will check if the move the player is trying to play is valid or not
            :param self:
            :param move: the move that tries to be played
            :return: returns True if the move is valid
        """
        if move in moves:
            original = deepcopy(self.grid)
            self.commands[move](test_move=True)
            if not (original == self.grid).all():
                self.grid = deepcopy(original)
                return True
            self.grid = deepcopy(original)
            return False
        return True
