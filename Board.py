import math
from exceptions import MoveError, Win


class GridIterator:
    """Custom Iterator for iterating over the rows of a grid."""

    def __init__(self, board):
        self._board = board
        self._current_row = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_row >= Board.SIZE:
            raise StopIteration

        row_result = list(iter(self._board))[self._current_row]
        self._current_row += 1

        return row_result


class Board:
    """
    Santorini Board that holds the workers and grid of Cells of buildings.

    SIZE (int): The size of the board (5).
    _grid (list): The 5x5 grid representing the board.
    _state (Memento): The state of the board.
    """

    SIZE = 5

    def __init__(self):
        self._state = None
        self._grid = Grid()
        self._score = ScoreCalculator(self._state, self._grid)

    @property
    def state(self):
        return self._state

    def _update_state(self, memento):
        # Uses and Supplies (Score Class) Deep Copy of the Workers
        self._state = memento.get_state()
        self._score = ScoreCalculator(self._state, self._grid)
        self._grid = memento.get_grid()

    def check_win(self, player):
        """Checks if a player has won. Input: player"""

        for worker in player.workers:
            x = worker.position
            y = self.get_cell(x).level
            if y == 3:
                raise Win
        return False

    def occupied(self, position):
        worker = self._state.get_worker_by_position(position)
        return worker.symbol if worker else None

    def validate(self, type, new, direction):
        """Validates a move or build action. Input: action type, positions, direction (for error)"""

        if not (0 <= new[0] < self.SIZE and 0 <= new[1] < self.SIZE):
            raise MoveError(type, direction)
        return True

    def get_ring(self, pos):
        """Returns a ring of positions around a given position."""

        ans = []

        for y in range(max(0, pos[0] - 1), min(5, pos[0] + 2)):
            for x in range(max(0, pos[1] - 1), min(5, pos[1] + 2)):
                if (y, x) == pos:
                    continue

                ans.append((y, x))

        return ans

    def __iter__(self):
        return GridIterator(self._grid)

    def build(self, position):
        """Builds a structure (+1) at the specified position on the board."""
        
        cell = self._grid.get_cell(position)
        cell.upgrade()

    def score(self, workers_positions, color):
        """Calculates the score (cell score, heuristic position score, distance score)."""
        total_distance = self._score.total_distance_score(color)
        curr_cell_score = self._score.total_cell_score(workers_positions)
        curr_pos_score = self._score.height_score(workers_positions)

        return (curr_cell_score, curr_pos_score, total_distance)

    def check_score(self, symbol, color, new_positions):
        """Check score by moving worker to calculate heuristic optimal moves."""
        workers_positions = self._state.get_workers_pos_by_symbol(symbol)
        curr_worker = self._state.get_worker_by_symbol(symbol)
        previous_position = curr_worker.position
        curr_worker.position = new_positions

        try:
            return self._score.score(workers_positions, color)
        finally:
            curr_worker.position = previous_position

    def score(self, workers_positions, color):
        """Calculates the score (cell score, heuristic position score, distance score)."""
        total_distance = self._score.total_distance_score(color)
        curr_cell_score = self._score.total_cell_score(workers_positions)
        curr_pos_score = self._score.height_score(workers_positions)

        return (curr_cell_score, curr_pos_score, total_distance)

    def check_score(self, symbol, color, new_positions):
        """Check score by moving worker to calculate heuristic optimal moves."""
        workers_positions = self._state.get_workers_pos_by_symbol(symbol)
        curr_worker = self._state.get_worker_by_symbol(symbol)
        previous_position = curr_worker.position
        curr_worker.position = new_positions

        try:
            return self._score.score(workers_positions, color)
        finally:
            curr_worker.position = previous_position

    def get_cell(self, pos):
        """Get the cell at the specified position."""
        return self._grid.get_cell(pos)

    def __getitem__(self, key):
        return self._grid[key]

    def __repr__(self):
        output = ""
        for i, row in enumerate(self):
            output += "+--" * Board.SIZE + "+\n"
            row_result = ""
            for j, cell in enumerate(row):
                height = cell.level
                worker_symbol = self.occupied((i, j))
                row_result += f"|{height}" + (worker_symbol if worker_symbol else " ")
            output += row_result + "|\n"
        output += "+--" * Board.SIZE + "+"
        return output

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, grid):
        self._grid = grid


class ScoreCalculator:
    """Class for calculating scores based on board and player information."""

    def __init__(self, state, grid):
        self._state = state
        self._grid = grid

    def check_win(self, player):
        """Checks if a player has won."""
        for worker in player.workers:
            x = worker.position
            y = self._state.get_cell(x).level
            if y == 3:
                raise Win
        return False

    def total_cell_score(self, workers_positions):
        """Calculates the total cell score for given worker positions."""
        result = 0
        for position in workers_positions:
            result += self._grid.get_cell(position).level
        return result

    def height_score(self, workers_positions):
        """Calculates the height score for given player workers list."""
        score = 0
        for position in workers_positions:
            score += 2 - max(abs(position[0] - 2), abs(position[1] - 2))
        return score

    def chebyshev_distance(self, position1, position2):
        """Calculates Chebyshev distance between two positions."""
        return max(abs(position1[0] - position2[0]), abs(position1[1] - position2[1]))

    def total_distance_score(self, color):
        """Calculates the total distance score for a given player color."""
        minimize = 0
        result = 0

        if color == "white":
            workers1 = self._state.blue_workers
            workers2 = self._state.white_workers
        else:
            workers1 = self._state.white_workers
            workers2 = self._state.blue_workers

        for worker1 in workers1:
            minimize = 99
            for worker2 in workers2:
                minimize = min(
                    self.chebyshev_distance(worker1.position, worker2.position),
                    minimize,
                )
            result += minimize
        return 8 - result

    def score(self, workers_positions, color):
        """Calculates the score (cell score, heuristic position score, distance score)."""
        total_distance = self.total_distance_score(color)
        curr_cell_score = self.total_cell_score(workers_positions)
        curr_pos_score = self.height_score(workers_positions)

        return (curr_cell_score, curr_pos_score, total_distance)

    def check_score(self, symbol, color, new_positions):
        """Check score by moving worker to calculate heuristic optimal moves."""
        workers_positions = self._state.get_workers_pos_by_symbol(symbol)
        curr_worker = self._state.get_worker_by_symbol(symbol)
        previous_position = curr_worker.position
        curr_worker.position = new_positions

        try:
            return self.score(workers_positions, color)
        finally:
            curr_worker.position = previous_position


class Grid:
    def __init__(self):
        self._grid = [[Cell() for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]

    def get_cell(self, pos):
        """Get the cell at the specified position."""
        return self._grid[pos[0]][pos[1]]

    def __iter__(self):
        return iter(self._grid)


class Cell:
    """
    Board Cell holding a buildings.

    _level (int): The level of the cell.
    """

    def __init__(self, level=0) -> None:
        self._level = level

    def upgrade(self):
        """Upgrades the cell level if it is below the maximum."""

        if self._level < 4:
            self._level += 1

    @property
    def level(self):
        return self._level
