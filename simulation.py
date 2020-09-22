
import numpy as np
import itertools
from constants import ALIVE_STATE, DEAD_STATE


class GameOfLifeSimulation(object):

    '''
    Contains the logic of the Game of Life simulation.

    Attributes:
        init_pattern (numpy.ndarray): 2-D array specification of the initial 
            pattern for the simulation. Optional
        grid_height (int): height of the simulation grid
        grid_width (int): width of the simulation grid
        random_state (int): sets the random seed of the `NumPy` pseudo-random 
            number generator. Optional
        init_alive_proportion (float): proportion of alive cells to start with. Optional
        grid (numpy.ndarray): 2-D array tracking the cell states of the grid. 
            It is updated at each step of the simulation
    '''

    def __init__(
            self,
            grid_height=50,
            grid_width=50,
            init_alive_proportion=0.1,
            random_state=42,
            init_pattern=None):
        '''
        Initializes the GameOfLifeSimulation object by providing the initial 
        configuration to start the simulation. There are two ways to provide the 
        initial configuration: 
        (1) provide the dimensions of the grid, proportion of 
        alive cells to start with and a seed for randomization, so a random 
        proportion of cells on the grid will be set to alive; 
        (2) specify the initial pattern directly

        Note: if both ways of providing the configuration is provided, the second 
            method will be used to initialize the grid

        Args:
            grid_height (int): height of grid, for first way of providing configs. 
                Defaults to 50
            grid_width (int): width of grid, for first way of providing configs. 
                Defaults to 50
            init_alive_proportion (float): proportion of alive cells to start with, for 
                first way of providing configs. Defaults to 0.1 (10%)
            random_state (int): sets the random seed of the `NumPy` pseudo-random
                number generator, for first way of providing configs. This makes 
                grid initial patterns reproducible. Defaults to 42
            init_pattern (numpy.ndarray): 2-D array specification of the initial
                pattern for the simulation, for second way of providing configs. Use 
                `DEAD_STATE` to mark dead cells, and `ALIVE_STATE` for alive cells 
        '''

        self.init_pattern = init_pattern

        if self.init_pattern is not None:

            self.grid_height = self.init_pattern.shape[0]
            self.grid_width = self.init_pattern.shape[1]

        else:

            self.grid_height = grid_height
            self.grid_width = grid_width

        self.random_state = random_state
        self.init_alive_proportion = init_alive_proportion

    def initialize(self):
        '''
        Initializes the Game of Life grid based on configurations provided
        '''

        if self.init_pattern is not None:
            self.grid = self.init_pattern

        else:
            np.random.seed(self.random_state)

            self.grid = np.random.choice(
                a=[DEAD_STATE, ALIVE_STATE],
                size=(self.grid_height, self.grid_width),
                p=[1 - self.init_alive_proportion, self.init_alive_proportion]
            )

    def update(self):
        '''
        Updates the whole grid according to Game of Life rules
        '''

        grid_snapshot = self.grid.copy()

        for row_index in range(self.grid_height):
            for column_index in range(self.grid_width):
                self.update_cell(grid_snapshot, row_index, column_index)

    def update_cell(self, grid_snapshot, row_index, column_index):
        '''
        Updates a specified cell according to Game of Life rules, based on the 
        cell's current state and the neighboring cells' states

        Args:
            grid_snapshot (numpy.ndarray): current state of the grid, prior to the update
            row_index (int): row location of the cell of interest
            column_index (int): column location of the cell of interest
        '''

        cell_state = grid_snapshot[row_index, column_index]

        neighbor_row_indices, neighbor_column_indices = self.get_neighbors(
            row_index, column_index,
            self.grid_height, self.grid_width
        )
        neighbor_states = grid_snapshot[neighbor_row_indices,
                                        neighbor_column_indices]

        self.grid[row_index, column_index] = self.get_next_cell_state(
            cell_state, neighbor_states)

    @staticmethod
    def get_neighbors(row_index, column_index, height_limit, width_limit):
        '''
        Obtains the indices of surrounding 8 neighbors to a given cell using 
        toroidal geometry for cells on the borders, so the grid wraps from top 
        to bottom and left to right

        Args:
            row_index (int): row location of cell of interest
            column_index (int): column location of cell of interest
            height_limit (int): grid height; neighbors beyond grid_limit in the y-direction 
                wrap around, so the top connects to the bottom for an infinite board
            width_limit (int): grid width; neighbors beyond width_limit in the x-direction
                wrap around, so the left connects to the right for an infinite board

        Returns:
            tuple (list of int, list of int)

            The first list contains the row indices of the neighboring cells;
            the second list contains the column indices of the neighboring cells
        '''

        neighbor_block = list(itertools.product(
            range(row_index - 1, row_index + 2),
            range(column_index - 1, column_index + 2)
        ))

        neighbor_block = [
            (neighbor[0] % height_limit, neighbor[1] % width_limit)
            for neighbor in neighbor_block
            if neighbor != (row_index, column_index)
        ]

        neighbor_row_indices, neighbor_column_indices = map(
            list, zip(*neighbor_block))
        return neighbor_row_indices, neighbor_column_indices

    @staticmethod
    def get_next_cell_state(cell_state, neighbor_states):
        '''
        Determines whether a cell should be alive or dead in the next step

        Args:
            cell_state (int): current state of the cell of interest;
                can be either alive or dead
            neighbor_states (numpy.ndarray): current states of the neighboring
                cells

        Returns:
            int specifying state of the cell of interest in the next step of the update 
        '''

        num_neighbors_alive = np.sum(neighbor_states == ALIVE_STATE)

        if cell_state and (2 <= num_neighbors_alive <= 3):
            return ALIVE_STATE

        elif not cell_state and num_neighbors_alive == 3:
            return ALIVE_STATE

        return DEAD_STATE
