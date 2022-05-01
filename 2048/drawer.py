import pygame
from settings import *


class Drawer:
    def __init__(self):
        """
        Initialise the drawer object with the pygame display.
        """
        self.display_surface = pygame.display.get_surface()

    def draw_text(self, text, size, x, y, r, g, b, center=False):
        """
        Draw text.
        :param text:    (String) The text to draw on the screen.
        :param size:    (Int) The size of the text.
        :param x:       (Int) The x coordinate of the text.
        :param y:       (Int) The y coordinate of the text.
        :param r:       (Int) The R color.
        :param g:       (Int) The G color.
        :param b:       (Int) The B color.
        :param center:  (Boolean) If the text needs to be centered.
        """
        font = pygame.font.Font(None, size)
        text = font.render(text, True, (r, g, b))
        if center:
            width = text.get_width()
            self.display_surface.blit(text, (WIDTH // 2 - width // 2, y))
        else:
            self.display_surface.blit(text, (x, y))

    def draw_board_shortcuts(self, score):
        """
        Draw in game shortcuts.
        :param score: (Int) the score of the game.
        :return: None
        """
        self.draw_text("Score : {}".format(score), TXT_CORE_SIZE, GAMESIZE + 30, 10, 255, 255, 255)
        self.draw_text("Shortcuts of the game", TXT_CORE_SIZE, GAMESIZE + 30, 40, 255, 255, 255)
        self.draw_text("Pause: Escape", TXT_CORE_SIZE, GAMESIZE + 30, 70, 255, 255, 255)

        self.draw_text("Move up: <z> or up", TXT_CORE_SIZE, GAMESIZE + 30, 100, 255, 255, 255)
        self.draw_text("Move down: <s> or down", TXT_CORE_SIZE, GAMESIZE + 30, 130, 255, 255, 255)
        self.draw_text("Move left: <q> or left", TXT_CORE_SIZE, GAMESIZE + 30, 160, 255, 255, 255)
        self.draw_text("Move right: <d> or right", TXT_CORE_SIZE, GAMESIZE + 30, 190, 255, 255, 255)

    def draw_menu_shortcuts(self):
        """
        Drawn the menu screen shortcuts.
        :return: None
        """
        self.display_surface.fill((0, 0, 0))
        self.draw_text("Welcome to 2048. A game designed by : ", TXT_MENU_SIZE, 100, 50, 255, 255, 255)

        self.draw_text("    - De Vos Sébastien", TXT_MENU_SIZE, 100, 90, 255, 255, 255)
        self.draw_text("    - Silberwasser David", TXT_MENU_SIZE, 100, 130, 255, 255, 255)
        self.draw_text("    - Tarik Kalai", TXT_MENU_SIZE, 100, 170, 255, 255, 255)

        self.draw_text("Press <h> if you want to play the game yourself.", TXT_MENU_SIZE, 100, 250, 255, 255, 255)
        self.draw_text("Press <e> to let the AI expectimax play the game.", TXT_MENU_SIZE, 100, 300, 255, 255, 255)
        self.draw_text("Press <m> to let the AI montecarlo play the game.", TXT_MENU_SIZE, 100, 350, 255, 255, 255)

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
        :param score: (Int) the score of the game
        :param grid: (Numpy Array) A numpy array of the game.
        :return: None
        """
        text = "CONGRATS, YOU ARE OFFICIALLY A LOSER!"
        if np.amax(grid) >= 2048:
            text = "CONGRATS, YOU WON!"

        self.draw_text(text, TXT_FINAL_SIZE, 20, 50, 255, 255, 255, True)
        self.draw_text("SCORE : " + str(score), TXT_FINAL_SIZE + 20, 20, 120, 255, 255, 255, True)
        self.draw_text("To play again press: <Space>", TXT_FINAL_SIZE, 20, 200, 255, 255, 255, True)
        self.draw_text("To go back to menu press: <m>", TXT_FINAL_SIZE, 20, 250, 255, 255, 255, True)

    def blur_screen(self, board):
        """
        Blur the screen and fades it to black.
        :param board: (Object) the board object containing the grid score and all its functions.
        :return: None
        """
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 200, 2):
            fade.set_alpha(alpha)
            board.visible_sprites.draw(self.display_surface)
            self.display_surface.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.Clock().tick(FPS)
