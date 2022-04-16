import pygame
from settings import *
from board import Board
from drawer import Drawer
from ai import AI
import sys
import matplotlib.pyplot as plt

class Game:
    def __init__(self): 
        self.state = 'menu_state'
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
                        self.state = 'pause_state'
    
    def menu_input(self):
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
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'board_state'
                    elif event.key == pygame.K_m:
                        self.state = 'menu_state'
                        self.board.new_board()
                        
    def game_over_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.board.new_board()
                        self.state = 'board_state'
                    elif event.key == pygame.K_m:
                        self.board.new_board()
                        self.state = 'menu_state'
        if TRAINING == 1 and NBROUND > self.round:
            self.addToFile("montecarlo", SIMULATION)
            self.round +=1
            self.board.new_board()
            self.state = 'ai_montecarlo_state'
        elif TRAINING == 2 and NBROUND > self.round:
            self.addToFile("expectimax", DEPTH)
            self.round +=1
            self.board.new_board()
            self.state = 'ai_expectimax_state'
    
    def addToFile(self, filename, param):
        file1 = open(filename+str(param)+".txt", "a")  # append mode
        score = self.board.getScore()
        file1.write(str(score)+" "+str(param)+"\n")
        file1.close()

    def plot(self, filename, param):
        score = []
        depth = []
        data = open(filename+str(param), 'r')
        for elem in data: 
            elem = elem.split()
            score.append(elem[0])
            depth.append(elem[1])
        plt.bar(score, depth, color = 'g', label = 'File Data')
        plt.xlabel('Depth', fontsize = 12)
        plt.ylabel('Score', fontsize = 12)
        plt.title('Performance', fontsize = 20)
        plt.legend()
        plt.show()

                        
                        
    def board_state(self):
        self.screen.fill(COLORS['background'])
        self.board.run()
        pygame.display.update()

    def ai_expectimax_state(self):
        self.screen.fill(COLORS['background'])
        self.board.draw()
        self.ai.run_expectimax()
        pygame.display.update()

    def ai_montecarlo_state(self):
        self.screen.fill(COLORS['background'])
        self.board.draw()
        self.ai.run_montecarlo()
        pygame.display.update()

    def pause_state(self):
        self.drawer.drawPauseShortcuts()
        self.pause_input()
        pygame.display.update()        
    
    def menu_state(self):
        self.drawer.drawMenuShortcuts()
        self.menu_input()
        pygame.display.update()
    
    def game_over_state(self):
        self.drawer.drawGameOverShortcuts(self.board.score, self.board.grid)
        self.game_over_input()
        pygame.display.update()

    def state_manager(self):
        """
        Organise which state is running
        """
        if self.state == 'menu_state':
            self.menu_state()
        elif self.state == 'board_state':
            self.board_state()
        elif self.state == 'pause_state':
            self.pause_state()
        elif self.state == 'game_over_state':
            self.game_over_state()
        elif self.state =='ai_expectimax_state':
            self.ai_expectimax_state()
        elif self.state =='ai_montecarlo_state':
            self.ai_montecarlo_state()
    
    def run(self):
        while True:
            self.state_manager()
            self.clock.tick(FPS)
if __name__ == '__main__':
    game = Game()
    game.run()
