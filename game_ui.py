import sys, os, random
import numpy as np
import colors as c
import re
import pathlib
# from tkinter import CENTER
# from matplotlib.widgets import Widget
import pygame
from pygame.locals import *

# Constant for the size of the screen.
WIDTH = 800
HEIGHT = 510
# Constant for the size of the text.
TXT_CORE_SIZE = 38
TXT_MENU_SIZE = 50


class Py2048:
    def __init__(self, gs, screen):
        """
        Init the game.

        :param gs:   The grid size. It is an Int.
        :param screen:      The screen, Surface object.
        """

        # Attributes for the main core of the game.
        self.screen = screen
        self.gs = gs
        self.ms = 6
        self.ts = (HEIGHT - (gs + 1) * self.ms) / gs
        self.grid = np.zeros((gs, gs), dtype=int)

    def draw(self):
        # Initialing Color
        self.screen.fill(c.GC['background'])
        myFont = pygame.font.SysFont('Arial', 40, bold=1)
        # Drawing Rectangle
        for i in range(self.gs):
            for j in range(self.gs):
                value = self.grid[i][j]

                color = c.GC[value]

                pos_x = j * (self.ts + self.ms) + self.ms
                pos_y = i * (self.ts + self.ms) + self.ms

                pygame.draw.rect(self.screen, color, pygame.Rect(pos_x, pos_y, self.ts, self.ts),
                                 border_radius=8)  # pos + dimension

                if value == 0:
                    continue

                text_surface = myFont.render(f'{value}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(pos_x + self.ts / 2, pos_y + self.ts / 2))
                self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def startGame(self):
        self.add_number(nb=2)
        while True:
            self.draw()
            command = self.waitKey()
            print(command)

            if command == 'q':
                break
            elif command == 'u':
                self.move_up()
            elif command == 'l':
                self.move_left()
            elif command == 'r':
                self.move_right()
            elif command == 'd':
                self.move_down()

            self.add_number()

    def move_up(self):
        """
        Use the properties of matrices to implement the movement of the tiles in the game.
        :return:
        """
        check = np.zeros_like(self.grid, dtype=int)
        for col in range(self.gs):  # Lines
            count = 0
            for row in range(self.gs):  # Colones
                if self.grid[row, col] != 0:
                    if row > 0 and count > 0 and not check[count - 1, col] and self.grid[count - 1, col] == self.grid[
                        row, col]:
                        self.grid[count - 1, col] *= 2
                        check[count - 1, col] += 1
                        self.grid[row, col] = 0
                    elif row != count:
                        self.grid[count, col] = self.grid[row, col]
                        self.grid[row, col] = 0
                        count += 1
                    else:
                        count += 1

    def move_right(self):
        self.grid = np.rot90(self.grid, 1)
        self.move_up()
        self.grid = np.rot90(self.grid, -1)

    def move_left(self):
        self.grid = np.rot90(self.grid, -1)
        self.move_up()
        self.grid = np.rot90(self.grid, 1)

    def move_down(self):
        self.grid = np.rot90(self.grid, 2)
        self.move_up()
        self.grid = np.rot90(self.grid, 2)

    @staticmethod
    def waitKey():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_z:
                        return 'u'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        return 'r'
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                        return 'l'
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        return 'd'
                    elif event.key == pygame.K_ESCAPE:
                        return 'q'

    def add_number(self, nb=1):
        """
        Will add number 2 or 4 to the grid at a random available position at the begining of each turn. In the
        beginning of the game we need to add 2 numbers, so we specify nb = 2.
        :param nb: number of numbers to add
        :return: /
        """
        available_pos = list(zip(*np.where(self.grid == 0)))
        print(available_pos)
        if len(available_pos)>0:
            for position in random.sample(available_pos, k=nb):
                if random.random() > 0.1:
                    self.grid[position] = 2
                else:
                    self.grid[position] = 4



    def exit(self):
        """
        Exit the application.
        """
        pygame.quit()
        sys.exit()
