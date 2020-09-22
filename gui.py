
import tkinter as tk
from simulation import GameOfLifeSimulation
from constants import *


class GameOfLifeBoard(object):
    '''
    Contains the GUI of the Game of Life board.

    Attributes:
            simulation (GameOfLifeSimulation): logic class of the simulation
            root (tkinter.Tk): the main window, or toplevel widget of Tk
            canvas_height (int): height of Canvas widget
            canvas_width (int): width of Canvas widget
            cell_height (float): height of individual cells; depends on `canvas_height` 
                    and `grid_height` of simulation
            cell_width (float): width of individual cells; depends on `canvas_width` 
                    and `grid_width` of simulation
            canvas (tkinter.Canvas): Canvas widget for displaying the board
            color_map (dict): maps cell states to colors for graphics
            cells (dict): dictionary of item specifiers for individual cells on the board.
                    It should have an entry for every element of `grid` of simulation 
    '''

    def __init__(self, simulation):
        '''
        Initializes the GameOfLifeBoard object.

        Args:
                simulation (GameOfLifeSimulation): object containing the simulation logic,
                        including the initial pattern
        '''

        self.simulation = simulation

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)

        self.canvas_height = min(
            self.simulation.grid_height * CANVAS_HEIGHT_MULTIPLIER, MIN_CANVAS_HEIGHT)
        self.canvas_width = self.canvas_height * \
            self.simulation.grid_width / self.simulation.grid_height

        self.cell_height = self.canvas_height / self.simulation.grid_height
        self.cell_width = self.canvas_width / self.simulation.grid_width

        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            borderwidth=CANVAS_NO_BORDER_SIZE,
            highlightthickness=CANVAS_NO_HIGHLIGHT,
        )
        self.canvas.pack()

        self.color_map = {DEAD_STATE: DEAD_COLOR, ALIVE_STATE: ALIVE_COLOR}

        self.cells = {}

        self.simulation.initialize()
        self.draw_board()

    def draw_board(self):
        '''
        Sets up board on canvas
        '''

        for row_index in range(self.simulation.grid_height):
            for column_index in range(self.simulation.grid_width):
                self.draw_cell(row_index, column_index)

    def draw_cell(self, row_index, column_index):
        '''
        Adds a new cell (i.e. rectangle) onto the canvas, specified by 
        its location (row and column)

        Args:
                row_index (int): row location of the cell of interest
                column_index (int): column location of the cell of interest
        '''

        self.cells[row_index, column_index] = self.canvas.create_rectangle(
            (
                column_index * self.cell_width,
                row_index * self.cell_height,
                (column_index + 1) * self.cell_width,
                (row_index + 1) * self.cell_height
            ),
            outline=CANVAS_NO_OUTLINE,
            fill=DEAD_COLOR
        )

    def update_board(self):
        '''
        Performs one step of update to the board based on changes in cell states.
        Currently set to update every 1 second
        '''

        for row_index in range(self.simulation.grid_height):
            for column_index in range(self.simulation.grid_width):
                self.update_cell_color(row_index, column_index)

        self.simulation.update()

        self.canvas.after(UPDATE_DELAY_MS, self.update_board)

    def update_cell_color(self, row_index, column_index):
        '''
        Updates the color of a cell on the canvas according to its new state

        Args:
                row_index (int): row location of the cell of interest
                column_index (int): column location of the cell of interest
        '''

        cell_color = self.get_cell_color(
            self.simulation.grid,
            row_index,
            column_index,
            self.color_map
        )

        self.canvas.itemconfig(
            self.cells[row_index, column_index],
            fill=cell_color
        )

    @staticmethod
    def get_cell_color(grid, row_index, column_index, color_map):
        '''
        Obtains the color of a given cell on the board.

        Args:
                grid (numpy.ndarray): matrix tracking states of cells on grid
                row_index (int): row index of cell of interest
                column_index (int): column index of cell of interest
                color_map (dict): dictionary mapping cell states to their respective color values

        Returns:
                string specifying color of the cell
        '''

        cell_state = grid[row_index, column_index]
        cell_color = color_map[cell_state]

        return cell_color

    def run(self):
        '''
        Runs complete animation for the simulation, by first drawing the 
        initial pattern and then updating it step by step.
        '''

        self.update_board()
        self.root.mainloop()
