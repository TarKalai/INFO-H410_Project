import pygame
from settings import *


class Drawer:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

    def draw_text(self, text, size, x, y, R, G, B, center):
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
            self.display_surface.blit(text, (WIDTH // 2 - width // 2, y))
        else:
            self.display_surface.blit(text, (x, y))

    def draw_board_shortcuts(self, score):
        """
        Draw in game shortcuts.
        :param score: (Int) the score of the game.
        """
        self.draw_text("Score : {}".format(score), TXT_CORE_SIZE, GAMESIZE + 30, 10, 255, 255, 255, False)
        self.draw_text("Shortcuts of the game", TXT_CORE_SIZE, GAMESIZE + 30, 40, 255, 255, 255, False)
        self.draw_text("Pause: Escape", TXT_CORE_SIZE, GAMESIZE + 30, 70, 255, 255, 255, False)

        self.draw_text("Move up: <z> or up", TXT_CORE_SIZE, GAMESIZE + 30, 100, 255, 255, 255, False)
        self.draw_text("Move down: <s> or down", TXT_CORE_SIZE, GAMESIZE + 30, 130, 255, 255, 255, False)
        self.draw_text("Move left: <q> or left", TXT_CORE_SIZE, GAMESIZE + 30, 160, 255, 255, 255, False)
        self.draw_text("Move right: <d> or right", TXT_CORE_SIZE, GAMESIZE + 30, 190, 255, 255, 255, False)

    def draw_menu_shortcuts(self):
        """
        Drawn the menu screen shortcuts.
        :return: None
        """
        self.display_surface.fill((0, 0, 0))
        self.draw_text("Welcome to 2048. A game designed by : ", TXT_MENU_SIZE, 100, 50, 255, 255, 255, False)

        self.draw_text("    - De Vos Sébastien", TXT_MENU_SIZE, 100, 90, 255, 255, 255, False)
        self.draw_text("    - Silberwasser David", TXT_MENU_SIZE, 100, 130, 255, 255, 255, False)
        self.draw_text("    - Tarik Kalai", TXT_MENU_SIZE, 100, 170, 255, 255, 255, False)

        self.draw_text("Press <h> if you want to play the game yourself.", TXT_MENU_SIZE, 100, 250, 255, 255, 255,
                       False)
        self.draw_text("Press <e> to let the AI expectimax play the game.", TXT_MENU_SIZE, 100, 300, 255, 255, 255,
                       False)
        self.draw_text("Press <m> to let the AI montecarlo play the game.", TXT_MENU_SIZE, 100, 350, 255, 255, 255,
                       False)

    def draw_pause_shortcuts(self):
        """
        Draw the pause screen shortcuts.
        :return: None
        """
        self.display_surface.fill((0, 0, 0))
        self.draw_text("Game Paused: ", TXT_MENU_SIZE, 100, 50, 255, 255, 255, True)
        self.draw_text("Press <Escape> to unpause the game ", TXT_MENU_SIZE, 100, 100, 255, 255, 255, True)
        self.draw_text("Press <m> to go to the menu screen", TXT_MENU_SIZE, 100, 150, 255, 255, 255, True)

    def draw_game_over_shortcuts(self, score, grid):
        """
        Draw the game over text.
        :param score:
        :param grid:
        :return:
        """
        text = "CONGRATS, YOU ARE OFFICIALLY A LOSER!"
        if np.amax(grid) >= 2048:
            text = "CONGRATS, YOU WON!"

        self.draw_text(text, TXT_FINAL_SIZE, 20, 50, 255, 255, 255, True)
        self.draw_text("SCORE : " + str(score), TXT_FINAL_SIZE + 20, 20, 120, 255, 255, 255, True)
        self.draw_text("To play again press: <Space>", TXT_FINAL_SIZE, 20, 200, 255, 255, 255, True)
        self.draw_text("To go back to menu press: <m>", TXT_FINAL_SIZE, 20, 250, 255, 255, 255, True)

    def blur_screen(self, board):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 200, 2):
            fade.set_alpha(alpha)
            board.visible_sprites.draw(self.display_surface)
            self.display_surface.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.Clock().tick(FPS)
