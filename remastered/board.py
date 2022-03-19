import pygame
import numpy as np
from settings import *
from tile import Tile
import random


class Board:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        self.grid = np.zeros((GRIDSIZE, GRIDSIZE), dtype=int)
        self.tileList = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]
        self.tileMovement = np.zeros((GRIDSIZE, GRIDSIZE, 2), dtype=int)
        self.tileToRemove = np.zeros_like(self.grid, dtype=int)
        self.create_board()
        self.direction = pygame.math.Vector2()
        self.canMove = True
        self.score = 0

    def create_board(self):
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                x = int(col_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                y = int(row_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                Tile((x, y), [self.background_sprites])
                if self.grid[row_index, col_index]:
                    self.tileList[row_index][col_index] = Tile((x, y), [self.visible_sprites],
                                                               self.grid[row_index, col_index])
        self.add_number(nb=2)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.moveUp(False)
            self.set_tile_target()
        elif keys[pygame.K_DOWN]:
            self.moveDown(False)
            self.set_tile_target()
        elif keys[pygame.K_LEFT]:
            self.moveLeft(False)
            self.set_tile_target()
        elif keys[pygame.K_RIGHT]:
            self.moveRight(False)
            self.set_tile_target()
        else:
            self.tileMovement = np.zeros((GRIDSIZE, GRIDSIZE, 2), dtype=int)

    def set_tile_target(self):
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                if self.tileList[i][j]:
                    dx, dy = self.tileMovement[i, j]
                    if dy + dx:
                        self.tileList[i][j].new_target(self.tileMovement[i, j])
                        self.tileList[i][j].set_direction(self.tileMovement[i, j])



    def update_tile_list(self):
        tempList = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                if self.tileToRemove[i,j]:
                    self.visible_sprites.remove(self.tileList[i][j])
        self.tileToRemove = np.zeros_like(self.grid, dtype=int)
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                if self.tileList[i][j]:
                    dx, dy = self.tileMovement[i, j]
                    if dy + dx:
                        tempList[i + dy][j + dx] = self.tileList[i][j]
        self.tileList = tempList

    def check_deplacement(self):
        for tile in self.visible_sprites:
            if not tile.finished_movement():
                self.canMove = False
                return
        self.update_tile_list()
        self.canMove = True

    def moveUp(self, test_move):
        """
        Will move the tiles upwards and fuse the tiles if they can.
        """
        check = np.zeros_like(self.grid, dtype=int)  # a matrice of 0, if the tiles merge, the position of the merge
        for col in range(GRIDSIZE):  # Lines
            count = 0
            for row in range(GRIDSIZE):  # Colones
                if self.grid[row, col] != 0:
                    if row > 0 and count > 0 and not check[count - 1, col] \
                            and self.grid[count - 1, col] == self.grid[row, col]:
                        self.grid[count - 1, col] *= 2
                        self.tileMovement[row, col] = [0, -(row - count + 1)]
                        self.grid[row, col] = 0
                        check[count - 1, col] += 1
                        if not test_move:
                            self.score += self.grid[count - 1, col]
                    elif row != count:
                        self.tileMovement[row, col] = [0, -(row - count)]
                        self.grid[count, col] = self.grid[row, col]
                        self.grid[row, col] = 0
                        count += 1
                    else:
                        count += 1
        self.tileToRemove = check

    def moveRight(self, test_move):
        """
            Will rotate the board matrice to the left, thus making it like a right move is an up move. We can thus apply
            move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, 1)
        self.tileMovement = np.rot90(self.tileMovement, 1)
        self.moveUp(test_move)
        self.grid = np.rot90(self.grid, -1)
        self.tileMovement = np.rot90(self.tileMovement, -1)
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                self.tileMovement[i, j, 0] = -self.tileMovement[i, j, 1]
                self.tileMovement[i, j, 1] = 0
        self.tileToRemove = np.rot90(self.tileToRemove, -1)

    def moveLeft(self, test_move):
        """
            Will rotate the board matrice to the right, thus making it like a left move is an up move. We can thus apply
            move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, -1)
        self.tileMovement = np.rot90(self.tileMovement, -1)
        self.moveUp(test_move)
        self.grid = np.rot90(self.grid, 1)
        self.tileMovement = np.rot90(self.tileMovement, 1)
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                self.tileMovement[i, j, 0] = self.tileMovement[i, j, 1]
                self.tileMovement[i, j, 1] = 0
        self.tileToRemove = np.rot90(self.tileToRemove, 1)

    def moveDown(self, test_move):
        """
            Will rotate the board matrice twice to the left, thus making it like a down move is an up move. We can thus
            apply move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, 2)
        self.tileMovement = np.rot90(self.tileMovement, 2)
        self.moveUp(test_move)
        self.grid = np.rot90(self.grid, 2)
        self.tileMovement = np.rot90(self.tileMovement, 2)
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                self.tileMovement[i, j, 1] = -self.tileMovement[i, j, 1]
        self.tileToRemove = np.rot90(self.tileToRemove, 2)

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
                x = int(position[1] * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                y = int(position[0] * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                if random.random() > 0.1:
                    self.grid[position] = 2
                else:
                    self.grid[position] = 4
                self.tileList[position[0]][position[1]] = Tile((x, y), [self.visible_sprites], self.grid[position])

    def run(self):
        self.background_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)
        self.check_deplacement()
        if self.canMove:
            self.input()
        # self.tileList[0][0].update()
        self.visible_sprites.update()
