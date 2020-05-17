
import numpy as np
import itertools

class GameOfLifeSimulation(object):

    def __init__(
        self, 
        grid_height = 50, 
        grid_width = 50, 
        initial_proportion = 0.1, 
        random_state = 42,
        initial_pattern = None):

        self.initial_pattern = initial_pattern

        self.padding = 100

        if self.initial_pattern is not None:

            self.grid_height = self.initial_pattern.shape[0]
            self.grid_width = self.initial_pattern.shape[1]

        else:

            self.grid_height = grid_height
            self.grid_width = grid_width

        self.padded_height = self.grid_height + self.padding
        self.padded_width = self.grid_width + self.padding

        self.random_state = random_state
        self.initial_proportion = initial_proportion


    def initialize(self):

        if self.initial_pattern is not None:

            self.grid = np.pad(
                self.initial_pattern,
                pad_width = (self.padding // 2, self.padding // 2),
                mode = 'constant',
                constant_values = 0
            )
        
        else:

            np.random.seed(self.random_state)
            
            self.grid = np.random.choice(
                [0, 1], 
                (self.padded_height, self.padded_width),
                p = [1 - self.initial_proportion, self.initial_proportion]
            )


    def get_neighbors(self, coord_r, coord_c):

        neighbors = list(itertools.product(
            range(coord_r - 1, coord_r + 2),
            range(coord_c - 1, coord_c + 2)
        ))

        neighbors = [neighbor for neighbor in neighbors \
                         if neighbor != (coord_r, coord_c) and \
                         0 <= neighbor[0] < self.padded_height and \
                         0 <= neighbor[1] < self.padded_width]
        
        neighbors_r, neighbors_c = map(list, zip(*neighbors))

        return neighbors_r, neighbors_c


    def update(self):

        grid_snapshot = self.grid.copy()

        for row_i in range(self.padded_height):

            for col_i in range(self.padded_width):
                
                cell_state = grid_snapshot[row_i, col_i]

                neighbors_r, neighbors_c = self.get_neighbors(row_i, col_i)
                neighbors = grid_snapshot[neighbors_r, neighbors_c]

                num_alive = np.sum(neighbors)

                if cell_state and (2 <= num_alive <= 3):
                    self.grid[row_i, col_i] = 1
                elif not cell_state and num_alive == 3:
                    self.grid[row_i, col_i] = 1
                else:
                    self.grid[row_i, col_i] = 0
