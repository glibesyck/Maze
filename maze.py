"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack

directions = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1]
]

class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        stack_of_cells = Stack()
        stack_of_cells.push((self._start_cell.row, self._start_cell.col))
        self._mark_path(self._start_cell.row, self._start_cell.col)
        while not stack_of_cells.is_empty():
            current_cell = stack_of_cells.peek()
            valid_neighbor = False 
            for direction in directions:
                if self._valid_move(current_cell[0]+direction[0], current_cell[1]+direction[1]):
                    stack_of_cells.push((current_cell[0]+direction[0], current_cell[1]+direction[1]))
                    valid_neighbor = True
                    self._mark_path(current_cell[0]+direction[0], current_cell[1]+direction[1])
                    if self._exit_found(current_cell[0]+direction[0], current_cell[1]+direction[1]):
                        return True
                    break #we don't need 2 valid neighbor at the same time
            if not valid_neighbor:
                self._mark_tried(current_cell[0], current_cell[1])
                stack_of_cells.pop()
        return False

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for row in range(self._maze_cells.num_rows()):
            for col in range(self._maze_cells.num_cols()):
                if self._maze_cells[row, col] == 'x' or self._maze_cells[row, col]  == 'o':
                    self._maze_cells[row, col] = '_' 

    def __str__(self):
        """Returns a text-based representation of the maze."""
        info = ''
        for row in range(self._maze_cells.num_rows()):
            for col in range(self._maze_cells.num_cols()):
                if self._maze_cells[row, col] is None:
                    info+='_ '
                else:
                    info += f'{self._maze_cells[row, col]} '
            info +='\n'
        info = info[:-1]
        return info

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols() \
               and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN

class _CellPosition(object):
    """Private storage class for holding a cell position."""
    def __init__(self, row, col):
        self.row = row
        self.col = col