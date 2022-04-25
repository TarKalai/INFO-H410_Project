# game setup
import numpy as np

"""settings relevent to the size of the window and number of tiles you want to play. by default we advise not to change these"""
WIDTH       = 900
HEIGHT      = 540
FPS         = 60
MARGESIZE   = 5
GRIDSIZE    = 4
TILESIZE    = int((HEIGHT - (GRIDSIZE*2+2) * MARGESIZE) / GRIDSIZE)
GAMESIZE    = HEIGHT
TXT_CORE_SIZE = 38
TXT_MENU_SIZE = 40
TXT_FINAL_SIZE = 50

"""
If you want to store the results of the game the AI plays change the Training value.
The number NBROUND represents the number of time the ai will play the game, so by placing 100 the ai will play 100 times the game and 
store the 100 results in a file of name <AIused><DEPTH or SIMULATION>.txt in the results directory. ex : results/expectimax4.txt 
"""
TRAINING = 2 # 0 is no data gathering, 1 for montecarlo, 2 for expectimax
NBROUND = 1

"""For Expectimax change the depth and for MonteCarlo change the number of simulations"""
DEPTH = 4
SIMULATION = 30


def INFINITY():
    return 9999

MOVES = ['u', 'l', 'r', 'd']


COLORS = {
    'background': (189, 172, 161),
    0: (204, 192, 179),
    2: (238, 228, 219),
    4: (240, 226, 202),
    8: (242, 177, 121),
    16: (236, 141, 85),
    32: (250, 123, 92),
    64: (234, 90, 56),
    128: (237, 207, 114),
    256: (242, 208, 75),
    512: (237, 200, 80),
    1024: (227, 186, 19),
    2048: (236, 196, 2),
    4096: (96, 217, 146),
    8192: (100, 100, 100),
    16384: (150, 150, 150),
    32768: (200, 200, 200),
    65536: (250, 250, 250)
}

TEST_GRID = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [0, 0, 0, 0]])

loose_grid = np.array([[2, 4, 2, 4],
                      [4, 2, 4, 2],
                      [2, 4, 2, 32],
                      [4, 2, 128, 32]])

WEIGHT = np.array( [[0.135759, 0.121925, 0.102812, 0.099937],
                    [0.0997992, 0.0888405, 0.076711, 0.0724143],
                    [0.060654, 0.0562579, 0.037116, 0.0161889],
                    [0.0125498, 0.00992495, 0.00575871, 0.00335193]])
