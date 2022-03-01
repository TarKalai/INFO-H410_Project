import sys, os, random
import numpy as np
import colors as c
import re
import pathlib
from tkinter import CENTER
#from matplotlib.widgets import Widget
import pygame
from pygame.locals import *

# Constant for the size of the screen.
WIDTH = 800
HEIGHT = 500
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
        self.ms = 5
        self.ts = (HEIGHT-(gs+1)*self.ms)/gs
        self.grid = np.zeros((gs, gs), dtype=int)

    
    def draw(self):
        # Initialing Color
        self.screen.fill(c.GC['background'])
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        # Drawing Rectangle
        for x in range(self.gs):
            for y in range(self.gs):
                n = 2**(self.grid[x][y]+1)
                color = c.GC[n]
                rect_x = x*(self.ts + self.ms)+self.ms
                rect_y = y*(self.ts + self.ms)+self.ms
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, self.ts, self.ts)) # pos + dimension
                text_surface=myfont.render(f'{n}', True, (0,0,0)) 
                text_rect = text_surface.get_rect(center=(rect_x+self.ts/2, rect_y+self.ts/2))
                self.screen.blit(text_surface, text_rect)
        pygame.display.flip()



        while True:
            for event in pygame.event.get():
                self.catchExitEvent(event)

    def add_number(self, nb=1):
        """
        Will add number 2 or 4 to the grid at a random available position at the begining of each turn. In the beggining
        of the game we need to add 2 numbers, so we specify nb = 2.
        :param nb: number of numbers to add
        :return: /
        """
        available_pos = list(zip(*np.where(self.grid == 0)))

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

    def catchExitEvent(self, event):
        """
        Check if it is a quit event.

        :param event:   Event object.
        """
        if event.type == pygame.QUIT:
            self.exit()
