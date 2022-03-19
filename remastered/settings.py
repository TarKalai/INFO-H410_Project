# game setup
import numpy as np
WIDTH       = 900
HEIGHT      = 540
FPS         = 60
MARGESIZE   = 5
GRIDSIZE    = 4
TILESIZE    = int((HEIGHT - (GRIDSIZE*2+2) * MARGESIZE) / GRIDSIZE)
TILEDISPLACEMENT = TILESIZE + 2*MARGESIZE
SPEED       = TILEDISPLACEMENT / 6

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
    4096: (96, 217, 146)
}

TEST_GRID = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [0, 0, 0, 0]])

loose_grid = np.array([[2, 4, 2, 4],
                      [4, 2, 4, 2],
                      [2, 4, 2, 4],
                      [4, 2, 4, 2]])
