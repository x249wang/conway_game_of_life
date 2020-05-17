
import tkinter as tk
from simulation import GameOfLifeSimulation

class GameOfLifeBoard(object):

  def __init__(self, simulation):

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

    self.root.geometry(
      f"{int(self.canvas_height)}x{int(self.canvas_width)}"
    )

    self.canvas = tk.Canvas(
      self.root, 
      width = self.canvas_width, 
      height = self.canvas_height,
      borderwidth = 0, 
      highlightthickness = 0
    )
    self.canvas.pack()

    self.padding_per_side = self.simulation.padding // 2

    self.color_map = {0: 'white', 1: 'black'}

    self.cells = {}


  def get_cell_state_color(self, row_idx, col_idx):

    cell_state = self.simulation.grid[
      row_idx + self.padding_per_side, 
      col_idx + self.padding_per_side
    ]

    cell_color = self.color_map[cell_state]

    return cell_color


  def draw_board(self):

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

    self.simulation.update()

    for row_i in range(self.simulation.grid_height):

      for col_i in range(self.simulation.grid_width):

        cell_color = self.get_cell_state_color(row_i, col_i)

        self.canvas.itemconfig(
          self.cells[row_i, col_i], 
          fill = cell_color
        )

    self.canvas.after(200, self.update_board)


  def run(self):

    self.draw_board()
    self.update_board()
    self.root.mainloop()

