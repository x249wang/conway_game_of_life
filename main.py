
from simulation import GameOfLifeSimulation
from gui import GameOfLifeBoard

simulation = GameOfLifeSimulation(50, 50, 0.2)

board = GameOfLifeBoard(simulation)
board.run()


import numpy as np

oscillator = np.array(
  [[0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0], 
    [0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0], 
    [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0]]
)
simulation = GameOfLifeSimulation(
  initial_pattern = oscillator
)

board = GameOfLifeBoard(simulation)
board.run()

