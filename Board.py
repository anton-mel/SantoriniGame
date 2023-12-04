
class Board:
    """Class representing the Santorini Board."""

    SIZE = (5, 5)

    def __init__(self, white, blue):
        self._grid = [[(0, []) for _ in range(5)] for _ in range(5)]
        self._initialize_workers(white, blue)

    def _initialize_workers(self, white, blue):
        self._add_worker_to_cell((3, 1), white.get_workers[0])
        self._add_worker_to_cell((1, 3), white.get_workers[1])
        self._add_worker_to_cell((1, 1), blue.get_workers[0])
        self._add_worker_to_cell((3, 3), blue.get_workers[1])

    def print_board(self):
        """Print the board."""
        for row in range(Board.SIZE[0]):
            print("+--+--+--+--+--+")
            for col in range(Board.SIZE[1]):
                height, workers = self._grid[row][col]
                print(f"|{height}{workers.get_symbol if workers else ' '}", end="")

            print("|")
        print("+--+--+--+--+--+")

    def _add_worker_to_cell(self, position, worker):
        """Add a worker to a specific cell."""
        row, col = position
        self._grid[row][col] = (0, worker)

    def _remove_worker_from_cell(self, position):
        """Remove a worker from a specific cell."""
        row, col = position
        self._grid[row][col] = (0, None)

    def _move_worker_to_position(self, worker, new_position):
        """Move a worker to a specific position."""
        current_position = worker.get_position

        if not isinstance(self._grid[new_position[0]][new_position[1]][1], list):
            # Create Exeption
            raise ValueError

        if current_position:
            self._remove_worker_from_cell(current_position)
            worker.position = new_position
            self._add_worker_to_cell(new_position, worker)

    def _build_tower_at_position(self, position):
        """Build a tower at a specific position."""
        row, col = position
        current_height, workers = self._grid[row][col]
      
        new_height = current_height + 1
        self._grid[row][col] = (new_height, workers)
