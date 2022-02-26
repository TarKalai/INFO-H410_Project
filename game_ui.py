import sys, os, random
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

class Slide2048:
    def __init__(self, grid_size, tile_size, margin_size, screen):
        """
        Init the game.

        :param grid_size: The grid size. It is a tuple (n,n) of Int.
        :param tile_size: The size of the tiles. It is an Int.
        :param margin_size: The size of the margin. It is an Int.
        :param screen:      The screen, Surface object.
        """
        # Attributes for the main core of the game.
        self.screen = screen
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.margin_size = margin_size
        self.grid = [[i for i in range(4)] for j in range(4)]

    
    def draw(self):

        
        # Initialing Color
        color = (255,0,0)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        # Drawing Rectangle
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                n = 2**(self.grid[x][y]+1)
                rect_x = x*(self.tile_size + self.margin_size)
                rect_y = y*(self.tile_size + self.margin_size)
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, self.tile_size, self.tile_size)) # pos + dimension
                text_surface=myfont.render(f'{n}', True, (0,0,0)) 
                text_rect = text_surface.get_rect(center=(rect_x+self.tile_size/2, rect_y+self.tile_size/2))
                self.screen.blit(text_surface, text_rect)
        pygame.display.flip()



        while True:
            for event in pygame.event.get():
                self.catchExitEvent(event)
    
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
