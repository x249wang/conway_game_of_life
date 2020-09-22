
# Runs Game of Life simulation animation

from simulation import GameOfLifeSimulation
from gui import GameOfLifeBoard

simulation = GameOfLifeSimulation(50, 50, 0.1)
# 50x50 grid, 10% of cells randomly set to alive initially

board = GameOfLifeBoard(simulation)
board.run()


# import numpy as np

# oscillator = np.array(
#     [[0, 0, 0, 0, 0, 0],
#      [0, 1, 1, 0, 0, 0],
#      [0, 1, 1, 0, 0, 0],
#      [0, 0, 0, 1, 1, 0],
#      [0, 0, 0, 1, 1, 0],
#      [0, 0, 0, 0, 0, 0]]
# )

# simulation = GameOfLifeSimulation(
#     init_pattern=oscillator
# )

# board = GameOfLifeBoard(simulation)
# board.run()
