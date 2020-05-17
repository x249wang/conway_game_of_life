
from simulation import GameOfLifeSimulation
from gui import GameOfLifeBoard

simulation = GameOfLifeSimulation(50, 50, 0.2)

board = GameOfLifeBoard(simulation)
board.run()


import numpy as np

oscillating_pattern = np.array(
  [[0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0], 
    [0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0], 
    [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0]]
)
simulation = GameOfLifeSimulation(
  initial_pattern = oscillating_pattern
)

board = GameOfLifeBoard(simulation)
board.run()

