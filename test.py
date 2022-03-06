import numpy as np

TEST_GRID = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [0, 0, 0, 0]])
test = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [0, 0, 0, 1]])

print((test.all() == TEST_GRID).all())