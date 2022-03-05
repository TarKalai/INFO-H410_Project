import numpy as np

TEST_GRID = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [0, 0, 0, 0]])

result = np.rot90(TEST_GRID, 2)
result = np.rot90(result, 2)
print(TEST_GRID)
print()
print(result)