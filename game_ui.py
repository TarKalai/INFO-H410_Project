import sys, os, random
import numpy as np
import colors as c
from copy import deepcopy

import re
import pathlib
# from matplotlib.widgets import Widget
import pygame
from pygame.locals import *

# Constant for the size of the screen.
WIDTH = 900
HEIGHT = 510
# Constant for the size of the text.
TXT_CORE_SIZE = 38
TXT_MENU_SIZE = 40
TXT_FINAL_SIZE = 50

moves = ['u', 'l', 'r', 'd']
menu_command = ['h', 'a', 'r']
game_over_command = ['y', 'm']


class Py2048:
    def __init__(self, gs, screen):
        """
        Init the game.

        :param gs:   The grid size. It is an Int.
        :param screen:      The screen, Surface object.
        """

        # Attributes for the main core of the game.
        self.screen = screen
        self.screen.fill(c.GC['background'])
        self.myFont = pygame.font.SysFont('Arial', 40, bold=1)
        self.gs = gs
        self.ms = 6
        self.ts = (HEIGHT - (gs + 1) * self.ms) / gs
        self.grid = np.zeros((gs, gs), dtype=int)  # c.loose_grid
        self.game_size = 4 * (self.ts + self.ms) + self.ms
        self.score = 0

        self.commands = {
            'u': self.moveUp,
            'd': self.moveDown,
            'l': self.moveLeft,
            'r': self.moveRight
        }

    def menu(self):
        """
        Menu appearing at the launch of the game. Through this menu you can choose who is going to play.
        :return:
        """
        self.displayMenu()
        key = ''
        valid = False
        while not valid:
            key = self.waitMenuKey()
            if key in menu_command:
                valid = True
        if key == 'h':
            self.__init__(self.gs, self.screen)
            self.startGame()

    def gameOver(self):
        self.displayGameOver()
        key = ''
        valid = False
        while not valid:
            key = self.waitGameOverKey()
            if key in game_over_command:
                valid = True
        if key == 'y':
            self.__init__(self.gs, self.screen)
            self.startGame()
        elif key == 'm':
            self.menu()

    def displayGameOver(self):
        self.blurScreen()
        text = "CONGRATS, YOU ARE OFFICIALLY A LOSER!"
        if np.amax(self.grid) >= 2048:
            text = "CONGRATS, YOU WON!"
        self.drawText(text, TXT_FINAL_SIZE, 20, 50, 255, 255, 255, True)
        self.drawText("SCORE : " + str(self.score), TXT_FINAL_SIZE + 20, 20, 120, 255, 255, 255, True)
        self.drawText("To play again press: <y>", TXT_FINAL_SIZE, 20, 200, 255, 255, 255, True)
        self.drawText("To go back to menu press: <m>", TXT_FINAL_SIZE, 20, 250, 255, 255, 255, True)
        pygame.display.update()

    def blurScreen(self):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 200):
            fade.set_alpha(alpha)
            self.drawBoard()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

    def displayMenu(self):
        self.screen.fill((0, 0, 0))
        self.drawText("Welcome to 2048. A game designed by : ",
                      TXT_MENU_SIZE, 100, 50, 255, 255, 255, False)
        self.drawText("    - De Vos Sébastien",
                      TXT_MENU_SIZE, 100, 90, 255, 255, 255, False)
        self.drawText("    - Silberwasser David",
                      TXT_MENU_SIZE, 100, 130, 255, 255, 255, False)
        self.drawText("    - Tarik Kalai",
                      TXT_MENU_SIZE, 100, 170, 255, 255, 255, False)
        self.drawText("Press <h> if you want to play the game yourself.", TXT_MENU_SIZE, 100, 250, 255, 255, 255, False)
        self.drawText("Press <a> to let the AI play the game.", TXT_MENU_SIZE, 100, 300, 255, 255, 255, False)
        pygame.display.flip()

    def startGame(self):
        self.addNumber(nb=2)
        while True:
            self.draw()
            if self.checkGameOver():
                print('the game is lost')
                break
            tag = True
            command = ""
            while tag:
                command = self.waitGameKey()
                tag = not self.checkValidMove(command)

            if command == 'q':
                break
            self.commands[command](test_move=False)
            self.addNumber()
        self.gameOver()

    def moveUp(self, test_move):
        """
            Will move the tiles upwards and fuse the tiles if they can.
            """
        check = np.zeros_like(self.grid, dtype=int)  # a matrice of 0, if the tiles merge, the position of the merge
        for col in range(self.gs):  # Lines
            count = 0
            for row in range(self.gs):  # Colones
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

    def moveRight(self, test_move):
        """
            Will rotate the board matrice to the left, thus making it like a right move is an up move. We can thus apply
            move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, 1)
        self.moveUp(test_move)
        self.grid = np.rot90(self.grid, -1)

    def moveLeft(self, test_move):
        """
            Will rotate the board matrice to the right, thus making it like a left move is an up move. We can thus apply
            move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, -1)
        self.moveUp(test_move)
        self.grid = np.rot90(self.grid, 1)

    def moveDown(self, test_move):
        """
            Will rotate the board matrice twice to the left, thus making it like a down move is an up move. We can thus
            apply move_up and then rotate backward the matrice.
            """
        self.grid = np.rot90(self.grid, 2)
        self.moveUp(test_move)
        self.grid = np.rot90(self.grid, 2)

    @staticmethod
    def waitGameKey():
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
            pygame.time.delay(20)

    @staticmethod
    def waitGameOverKey():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_y:
                        return 'y'
                    elif event.key == pygame.K_m:
                        return 'm'
                    elif event.key == pygame.K_ESCAPE:
                        return 'q'
            pygame.time.delay(20)

    @staticmethod
    def waitMenuKey():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'q'
                    elif event.key == pygame.K_h:
                        return 'h'
                    elif event.key == pygame.K_a:
                        return 'a'
                    elif event.key == pygame.K_r:
                        return 'r'
            pygame.time.delay(20)

    def checkGameOver(self):
        """
            It will check if the game is over or not by trying all possible moves, i.e. u,r,d,l.
            :param self:
            :return: returns True if the game is over
            """
        original = deepcopy(self.grid)
        for move in moves:
            self.commands[move](test_move=True)
            if not (original == self.grid).all():
                self.grid = deepcopy(original)
                return False
            self.grid = deepcopy(original)
        return True

    def checkValidMove(self, move):
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

    def addNumber(self, nb=1):
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

    def exit(self):
        """
            Exit the application.
            """
        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.fill(c.GC['background'])  # Erases the old score with the color of the background
        self.drawShortcuts(True)
        self.drawBoard()
        pygame.display.flip()

    def drawBoard(self):
        """
            Draws then board with the corresponding tile colors.
            """
        for i in range(self.gs):
            for j in range(self.gs):
                value = self.grid[i][j]

                color = c.GC[value]

                pos_x = j * (self.ts + self.ms) + self.ms
                pos_y = i * (self.ts + self.ms) + self.ms

                pygame.draw.rect(self.screen, color, pygame.Rect(pos_x, pos_y, self.ts, self.ts),
                                 border_radius=8)  # pos + dimension

                if not value:  # prevents from displaying the value 0
                    continue

                text_surface = self.myFont.render(f'{value}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(pos_x + self.ts / 2, pos_y + self.ts / 2))
                self.screen.blit(text_surface, text_rect)

    def drawText(self, text, size, x, y, R, G, B, center):
        """
            Draw text.

            :param text:    The text to draw on the  String.
            :param size:    The size of the text, Int.
            :param x:       The x position of the text, Int.
            :param y:       The y position of the text, Int.
            :param R:       The R color, Int.
            :param G:       The G color, Int.
            :param B:       The B color, Int.
            :param center:  If the text need to be in the center, Boolean.
            """
        font = pygame.font.Font(None, size)
        text = font.render(text, True, (R, G, B))
        if center:
            width = text.get_width()
            self.screen.blit(text, (WIDTH // 2 - width // 2, y))
        else:
            self.screen.blit(text, (x, y))

    def drawShortcuts(self, is_player):
        """
            Draw in game shortcuts.

            :param is_player:   A Boolean, it checks if it is a player because, shorcuts are different in
                                the player mode or in the AI mode. →
            """
        self.drawText("Score : {}".format(self.score), TXT_CORE_SIZE, self.game_size + 30, 10, 255, 255, 255, False)
        self.drawText("Shortcuts of the game", TXT_CORE_SIZE, self.game_size + 30, 40, 255, 255, 255, False)
        self.drawText("Restart: Escape", TXT_CORE_SIZE, self.game_size + 30, 70, 255, 255, 255, False)
        if is_player:
            self.drawText("Move up: <z> or ", TXT_CORE_SIZE, self.game_size + 30, 100, 255, 255, 255, False)
            self.drawText("Move down: <s> or", TXT_CORE_SIZE, self.game_size + 30, 130, 255, 255, 255, False)
            self.drawText("Move left: <q> or", TXT_CORE_SIZE, self.game_size + 30, 160, 255, 255, 255, False)
            self.drawText("Move right: <d> or", TXT_CORE_SIZE, self.game_size + 30, 190, 255, 255, 255, False)
            self.drawText("Random move: <Space>", TXT_CORE_SIZE, self.game_size + 30, 220, 255, 255, 255, False)
        else:
            self.drawText("AI move: <Space>", TXT_CORE_SIZE, 500, 100, 255, 255, 255, False)
            self.drawText("auto AI move: <a>", TXT_CORE_SIZE, 500, 130, 255, 255, 255, False)
