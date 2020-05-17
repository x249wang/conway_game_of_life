
import tkinter as tk
from simulation import GameOfLifeSimulation

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
		self.root.title("Conway's Game of Life")

		self.canvas_height = min(
			self.simulation.grid_height * 20,
			750
		)
		self.canvas_width = self.canvas_height * self.simulation.grid_width / self.simulation.grid_height

		self.cell_height = self.canvas_height / self.simulation.grid_height    
		self.cell_width = self.canvas_width / self.simulation.grid_width

		self.canvas = tk.Canvas(
			self.root, 
			width = self.canvas_width, 
			height = self.canvas_height,
			borderwidth = 0, 
			highlightthickness = 0
		)
		self.canvas.pack()

		self.color_map = {0: 'white', 1: 'black'}

		self.cells = {}


	def get_cell_state_color(self, row_idx, col_idx):
		'''
		Obtain color of the cell based on its state.

		Args:
			row_idx (int): row index of cell
			col_idx (int): column index of cell
		
		Returns:
			string specifying color of the cell ("white" for dead; "black" for white)
		'''

		cell_state = self.simulation.grid[row_idx, col_idx]

		cell_color = self.color_map[cell_state]

		return cell_color


	def draw_board(self):
		'''
		Draws the initial pattern of the board
		'''

		self.simulation.initialize()

		for row_i in range(self.simulation.grid_height):
			
			for col_i in range(self.simulation.grid_width):

				cell_color = self.get_cell_state_color(row_i, col_i)

				self.cells[row_i, col_i] = self.canvas.create_rectangle(
					(
						col_i * self.cell_width, 
						row_i * self.cell_height,
						(col_i + 1) * self.cell_width,
						(row_i + 1)* self.cell_height
					),
					outline = '',
					fill = cell_color
				)
			

	def update_board(self):
		'''
		Updates the board at each step in time based on changes in cell states.

		Note: currently set to update every 1 second
		'''

		self.simulation.update()

		for row_i in range(self.simulation.grid_height):

			for col_i in range(self.simulation.grid_width):

				cell_color = self.get_cell_state_color(row_i, col_i)

				self.canvas.itemconfig(
					self.cells[row_i, col_i], 
					fill = cell_color
				)

		self.canvas.after(1000, self.update_board)


	def run(self):
		'''
		Runs complete animation for the simulation, by first drawing the 
		initial pattern and then updating it step by step.
		'''

		self.draw_board()
		self.update_board()
		self.root.mainloop()

