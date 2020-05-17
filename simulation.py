
import numpy as np
import itertools

class GameOfLifeSimulation(object):

    '''
    Contains the logic of the Game of Life simulation.

    Attributes:
        initial_pattern (numpy.ndarray): 2-D array specification of the initial 
            pattern for the simulation. Optional
        grid_height (int): height of the simulation grid
        grid_width (int): width of the simulation grid
        random_state (int): sets the random seed of the `NumPy` pseudo-random 
            number generator. Optional
        initial_proportion (float): proportion of alive cells to start with. Optional
        grid (numpy.ndarray): 2-D array tracking the cell states of the grid. 
            It is updated at each step of the simulation
    '''

    def __init__(
        self, 
        grid_height = 50, 
        grid_width = 50, 
        initial_proportion = 0.1, 
        random_state = 42,
        initial_pattern = None):
    
        '''
        Initializes the GameOfLifeSimulation object by providing the initial 
        configuration to start the simulation. There are two ways to provide the 
        configuration: 
        (1) provide the dimensions of the grid, proportion of 
        alive cells to start with and the seed for randomization, so a random 
        proportion of cells on the grid will be set to alive; 
        (2) specify the initial pattern

        Note: if both ways of providing the configuration is provided, the second 
            method will be used to initialize the grid

        Args:
            grid_height (int): height of grid, for first way of providing configs. 
                Defaults to 50
            grid_width (int): width of grid, for first way of providing configs. 
                Defaults to 50
            initial_proportion (float): proportion of alive cells to start with, for 
                first way of providing configs. Defaults to 0.1 (10%)
            random_state (int): sets the random seed of the `NumPy` pseudo-random
                number generator, for first way of providing configs. This makes 
                grid initial patterns reproducible. Defaults to 42
            initial_pattern (numpy.ndarray): 2-D array specification of the initial
                pattern for the simulation, for second way of providing configs. Use 
                0 to mark dead cells, and 1 for alive cells 
        '''

        self.initial_pattern = initial_pattern

        if self.initial_pattern is not None:

            self.grid_height = self.initial_pattern.shape[0]
            self.grid_width = self.initial_pattern.shape[1]

        else:

            self.grid_height = grid_height
            self.grid_width = grid_width

        self.random_state = random_state
        self.initial_proportion = initial_proportion


    def initialize(self):
        '''
        Creates the Game of Life grid using the configuration parameters
        provided at object initialization.
        '''

        if self.initial_pattern is not None:

            self.grid = self.initial_pattern
        
        else:

            np.random.seed(self.random_state)
            
            self.grid = np.random.choice(
                [0, 1], 
                (self.grid_height, self.grid_width),
                p = [1 - self.initial_proportion, self.initial_proportion]
            )


    def get_neighbors(self, coord_r, coord_c):
        '''
        Obtains the indices of surrounding 8 neighbors to a given cell using 
        toroidal geometry for cells on the borders, so the grid wraps from top 
        to bottom and left to right

        Args:
            coord_r (int): row index of cell of interest
            coord_c (int): column index of cell of interest
        
        Returns:
            tuple (list of int, list of int)

            The first list contains the row indices of the neighboring cells;
            the second list contains the column indices of the neighboring cells
        '''

        neighbors = list(itertools.product(
            range(coord_r - 1, coord_r + 2),
            range(coord_c - 1, coord_c + 2)
        ))

        neighbors = [(neighbor[0] % self.grid_height, neighbor[1] % self.grid_width)
                     for neighbor in neighbors 
                     if neighbor != (coord_r, coord_c)]
        
        neighbors_r, neighbors_c = map(list, zip(*neighbors))

        return neighbors_r, neighbors_c


    def update(self):
        '''
        Updates the grid according to Game of Life rules based on current 
        cell state and the number of alive/dead neighboring cells. 
        '''

        grid_snapshot = self.grid.copy()

        for row_i in range(self.grid_height):

            for col_i in range(self.grid_width):
                
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

