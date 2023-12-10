from exceptions import MoveError

class BoardCellIterator:
    def __init__(self, board) -> None:
        self._board = board
        self._row = 0
        self._col = 0

    def __next__(self):
        if self._row == self._board.SIZE:
            raise StopIteration()

        cell = self._board.get_cell((self._row, self._col))
        self._col += 1
        if self._col == self._board.SIZE:
            self._col = 0
            self._row += 1
        return cell

    def __iter__(self):
        return self

class Board:
    """Class representing the Santorini Board."""

    SIZE = 5

    def __init__(self):
        self._grid = [[Cell() for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def build(self, pos):
        x, y = pos

        self._grid[x][y].upgrade()

    def valid_move(self, new_position, direction):
        if not (0 <= new_position[0] < self.SIZE and 0 <= new_position[1] < self.SIZE):
            raise MoveError("move", direction)

        new_cell = self.get_cell(new_position)
        if new_cell.worker is not None:
            raise MoveError("move", direction)
    
    def get_cell(self, pos):
        x, y = pos
        return self._grid[x][y]

    def __iter__(self):
        return BoardCellIterator(self)

class Cell:
    def __init__(self, level=0) -> None:
        self._level = level

    def upgrade(self):
        if self._level < 3:
            self._level += 1

    @property
    def level(self):
        return self._level
