import pygame
import sys

from settings import *
from copy import deepcopy
from board import Board
from drawer import Drawer
from ai import AI


class Game:
    def __init__(self):
        """
        Builds the initial configuration of the main class
        """
        self.state = 'menu_state'
        self.old_state = 'menu_state'

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()  # will enable us to run at 60 frames per seconds

        self.drawer = Drawer()
        self.board = Board(self, self.drawer)
        self.ai = AI(self, self.drawer, self.board)

        self.round = 0

    def board_input(self):
        """
        Gathers the input of the user during the game. If the players enters The arrow keys or the 'z', 'q', 's, 'd'
        input the function will return the letter corresponding to the move.
        If the players presses on escape, the function will change the state to the pause state.
        :return: return the letter corresponding to the move the players wants to play. Otherwise, returns none.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    return 'u'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    return 'r'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    return 'l'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    return 'd'
                elif event.key == pygame.K_ESCAPE:
                    self.old_state = deepcopy(self.state)
                    self.state = 'pause_state'

    def menu_input(self):
        """
        Gathers the input of the user during the menu. Changes the state according to the input.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.state = 'board_state'
                elif event.key == pygame.K_e:
                    self.state = 'ai_expectimax_state'
                elif event.key == pygame.K_m:
                    self.state = 'ai_montecarlo_state'

    def pause_input(self):
        """
        Gathers the input of the user during the pause. Changes the state according to the input.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = deepcopy(self.old_state)
                elif event.key == pygame.K_m:
                    self.state = 'menu_state'
                    self.board.new_board()

    def game_over_input(self):
        """
        Gathers the input of the user during the game over. Changes the state according to the input.
        If the TRAINING variable has been set to expectimax or monte carlo, then the training_input() function will
        be called.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.board.new_board()
                    self.state = deepcopy(self.old_state)
                elif event.key == pygame.K_m:
                    self.board.new_board()
                    self.state = 'menu_state'

        if TRAINING > 0 and NBROUND > self.round:
            self.training_input()

    def training_input(self):
        """
        If the TRAINING variable in the settings.py file hase been set to 1 then the AI using Monte-carlo will be
        called. If it is set to 2 then it will be the Expectimax AI that will be called
        :return: None
        """
        if TRAINING == 1:
            self.add_to_file("montecarlo", SIMULATION)
            self.round += 1
            self.board.new_board()
            self.state = 'ai_montecarlo_state'
        elif TRAINING == 2:
            self.add_to_file("expectimax", DEPTH)
            self.round += 1
            self.board.new_board()
            self.state = 'ai_expectimax_state'

    def add_to_file(self, ai, complexity):
        """
        Adds the results the AI obtained during the game to a .txt file in the /2048/results/ folder.
        the name of the .txt file depends on the AI that has played and the depth/simulation used.
        example : if the AI is Monte-carlo and the number of simulation is 20, the filename will be "montecarlo20.txt"
        :param ai: (String) The AI used in a string
        :param complexity: (Int) The Depth/simulation of the AI as an int.
        :return: None
        """
        file1 = open("results/" + ai + str(complexity) + ".txt", "a")
        score = self.board.get_score()
        file1.write(str(score) + " " + str(complexity) + "\n")
        file1.close()

    def board_state(self):
        """
        Runs the game as a human.
        :return: None
        """
        self.screen.fill(COLORS['background'])
        self.board.run()
        pygame.display.update()

    def ai_expectimax_state(self):
        """
        Runs the game as the AI expectimax.
        :return: None
        """
        self.screen.fill(COLORS['background'])
        self.board.draw()
        self.ai.run_expectimax()
        self.board_input()
        pygame.display.update()

    def ai_montecarlo_state(self):
        """
        Runs the game as the AI Monte-carlo.
        :return: None
        """
        self.screen.fill(COLORS['background'])
        self.board.draw()
        self.ai.run_montecarlo()
        self.board_input()
        pygame.display.update()

    def pause_state(self):
        """
        Display the pause screen.
        :return: None
        """
        self.drawer.draw_pause_shortcuts()
        self.pause_input()
        pygame.display.update()

    def menu_state(self):
        """
        Display the menu screen
        :return: None
        """
        self.drawer.draw_menu_shortcuts()
        self.menu_input()
        pygame.display.update()

    def game_over_state(self):
        """
        Display the game over screen
        :return: None
        """
        self.drawer.draw_game_over_shortcuts(self.board.score, self.board.grid)
        self.game_over_input()
        pygame.display.update()

    def state_manager(self):
        """
        Organise which state is running
        :return: None
        """
        if self.state == 'menu_state':
            self.menu_state()
        elif self.state == 'board_state':
            self.board_state()
        elif self.state == 'pause_state':
            self.pause_state()
        elif self.state == 'game_over_state':
            self.game_over_state()
        elif self.state == 'ai_expectimax_state':
            self.ai_expectimax_state()
        elif self.state == 'ai_montecarlo_state':
            self.ai_montecarlo_state()

    def run(self):
        """
        Main loop of the application.
        :return: None
        """
        while True:
            self.state_manager()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
