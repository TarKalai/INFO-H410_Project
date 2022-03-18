import pygame
import numpy as np
from settings import *
from tile import Tile


class Board:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        self.grid = TEST_GRID  # np.zeros((GRIDSIZE, GRIDSIZE), dtype=int)
        self.tileList = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]
        self.create_board()

    def create_board(self):
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                x = int(col_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                y = int(row_index * (TILESIZE + 2 * MARGESIZE) + 2 * MARGESIZE)
                Tile((x, y), [self.background_sprites])
                if self.grid[row_index, col_index]:
                    self.tileList[row_index][col_index] = Tile((x, y), [self.visible_sprites], self.grid[row_index, col_index])

    def run(self):
        self.background_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)
        self.tileList[0][0].update()
        self.visible_sprites.update()
