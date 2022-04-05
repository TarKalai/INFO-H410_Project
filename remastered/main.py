import pygame
from settings import *
from board import Board


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()  # will enable us to run at 60 frames per seconds

        self.board = Board()

    def run(self):
        while True:
            self.screen.fill(COLORS['background'])
            self.board.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
