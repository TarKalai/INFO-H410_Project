import pygame
from settings import *

class Drawer:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()


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
            self.display_surface.blit(text, (WIDTH // 2 - width // 2, y))
        else:
            self.display_surface.blit(text, (x, y))

    def drawBoardShortcuts(self, score, is_player=True):
        """
            Draw in game shortcuts.

            :param is_player:   A Boolean, it checks if it is a player because, shorcuts are different in
                                the player mode or in the AI mode. →
        """
        self.drawText("Score : {}".format(score), TXT_CORE_SIZE, GAMESIZE + 30, 10, 255, 255, 255, False)
        self.drawText("Shortcuts of the game", TXT_CORE_SIZE, GAMESIZE + 30, 40, 255, 255, 255, False)
        self.drawText("Restart: Escape", TXT_CORE_SIZE, GAMESIZE + 30, 70, 255, 255, 255, False)
        if is_player:
            self.drawText("Move up: <z> or ", TXT_CORE_SIZE, GAMESIZE + 30, 100, 255, 255, 255, False)
            self.drawText("Move down: <s> or", TXT_CORE_SIZE, GAMESIZE + 30, 130, 255, 255, 255, False)
            self.drawText("Move left: <q> or", TXT_CORE_SIZE, GAMESIZE + 30, 160, 255, 255, 255, False)
            self.drawText("Move right: <d> or", TXT_CORE_SIZE, GAMESIZE + 30, 190, 255, 255, 255, False)
            self.drawText("Random move: <Space>", TXT_CORE_SIZE, GAMESIZE + 30, 220, 255, 255, 255, False)
        else:
            self.drawText("AI move: <Space>", TXT_CORE_SIZE, 500, 100, 255, 255, 255, False)
            self.drawText("auto AI move: <a>", TXT_CORE_SIZE, 500, 130, 255, 255, 255, False)


    def drawMenuShortcuts(self):
        self.display_surface.fill((0, 0, 0))
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
    
    def drawPauseShortcuts(self):
        self.display_surface.fill((0, 0, 0))
        self.drawText("Game Paused: ",
                      TXT_MENU_SIZE, 100, 50, 255, 255, 255, True)
        self.drawText("Press <Escape> to unpause the game ",
                      TXT_MENU_SIZE, 100, 100, 255, 255, 255, True)
        self.drawText("Press <m> to go to the menu screen",
                      TXT_MENU_SIZE, 100, 150, 255, 255, 255, True)

    def drawGameOverShortcuts(self, score, grid):
        text = "CONGRATS, YOU ARE OFFICIALLY A LOSER!"
        if np.amax(grid) >= 2048:
            text = "CONGRATS, YOU WON!"
        self.drawText(text, TXT_FINAL_SIZE, 20, 50, 255, 255, 255, True)
        self.drawText("SCORE : " + str(score), TXT_FINAL_SIZE + 20, 20, 120, 255, 255, 255, True)
        self.drawText("To play again press: <Space>", TXT_FINAL_SIZE, 20, 200, 255, 255, 255, True)
        self.drawText("To go back to menu press: <m>", TXT_FINAL_SIZE, 20, 250, 255, 255, 255, True)
        pygame.display.update()

    def blurScreen(self, board):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 200, 4):
            fade.set_alpha(alpha)
            board.visible_sprites.draw(self.display_surface)
            self.display_surface.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(FPS)
