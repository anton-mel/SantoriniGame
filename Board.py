

class Board:
    """Class representing the Santorini Board."""

    SIZE = (5, 5)

    def __init__(self, white, blue):
        self._grid = [[(0, []) for _ in range(5)] for _ in range(5)]

        self._add_workers_to_cell(3, 1, white.get_workers[0])
        self._add_workers_to_cell(1, 3, white.get_workers[1])
        self._add_workers_to_cell(1, 1, blue.get_workers[0])
        self._add_workers_to_cell(3, 3, blue.get_workers[1])

    def print_board(self):
        """Print the board."""
        for row in range(Board.SIZE[0]):
            print("+--+--+--+--+--+")
            for col in range(Board.SIZE[1]):
                height, workers = self._grid[row][col]
                print(f"|{height}{workers.get_symbol if workers else ' '}", end="")

            print("|")
        print("+--+--+--+--+--+")

    def _add_workers_to_cell(self, row, col, workers):
        """Add workers to the cell."""
        self._grid[row][col] = (0, workers)
