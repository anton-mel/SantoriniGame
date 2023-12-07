class BoardRowIterator:
    def __init__(self, grid) -> None:
        self._grid = grid
        self._index = 0

    def __next__(self):
        if self._index >= 5:
            raise StopIteration()

        row = self._grid[self._index]
        self._index += 1
        return row

    def __iter__(self):
        return self

class Board:
    """Class representing the Santorini Board."""

    SIZE = 5

    def __init__(self):
        self._grid = [[Cell() for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def print_board(self):
        """Print the board."""
        for row in self:
            print("+--+--+--+--+--+")
            for cell in row:
                print(
                    f"|{cell.level}{cell.worker.symbol if cell.worker else ' '}",
                    end="",
                )
            print("|")
        print("+--+--+--+--+--+")

    def build(self, pos):
        x, y = pos

        self._grid[x][y].upgrade()

    def __iter__(self):
        return BoardRowIterator(self._grid)

class Cell:
    def __init__(self, level=0) -> None:
        self._level = level

    def upgrade(self):
        if self._level < 3:
            self._level += 1

    @property
    def level(self):
        return self._level
