
import math
from exceptions import MoveError, Win


class GridIterator:
    """
    !!!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    DEEEELEEEETEE!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """

    def __init__(self, board):
        self._board = board
        self._current_row = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_row >= Board.SIZE:
            raise StopIteration

        row_result = self._board[self._current_row]
        self._current_row += 1

        return row_result


class Board:
    """
    Santorini Board that holds the workers and grid of Cells of buildings.

    SIZE (int): The size of the board.
    _grid (list): The 2D grid representing the board.
    _state (Memento): The state of the board.

    Methods: FIX !!!!!!!!!!!!!!! Place to methods instead
        check_win(self, player): Checks if a player has won.
        total_cell_score(self, workers_positions): Calculates the total cell score for given worker positions.
        height_score(self, workers_positions): Calculates the height score for given worker positions.
        chebyshev_distance(self, position1, position2): Calculates the Chebyshev distance between two positions.
        total_distance_score(self, color): Calculates the total distance score for a given player color.
        score(self, workers_positions, color): Calculates the score based on various factors.
        check_score(self, symbol, color, new_positions): Checks the score for a move.
        occupied(self, position): Checks if a position is occupied by a worker.
        validate(self, type, new, direction): Validates a move or build action.
        get_ring(self, pos): Returns a ring of positions around a given position.
        __iter__(self): Returns an iterator for the board.
        build(self, position): Builds a structure at the specified position on the board.
        get_cell(self, pos): Returns the cell at the specified position on the board.
    """

    SIZE = 5

    def __init__(self):
        self._grid = [[Cell() for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._state = None

    @property
    def state(self):
        return self._state

    def _update_state(self, memento):
        self._state = memento.get_state()
        self._grid = memento.get_grid()

    def check_win(self, player):
        for worker in player.workers:
            x = worker.position
            y = self.get_cell(x).level
            if y == 3:
                raise Win
        return False

    #########################################################
    # Calculate Score for Human State or Heuristic Strategies
    #########################################################

    def total_cell_score(self, workers_positions):
        result = 0
        for position in workers_positions:
            result += self.get_cell(position).level
        return result

    def height_score(self, workers_positions):
        score = 0
        for position in workers_positions:
            score += 2 - max(abs(position[0] - 2), abs(position[1] - 2))
        return score

    def chebyshev_distance(self, position1, position2):
        return max(abs(position1[0] - position2[0]), abs(position1[1] - position2[1]))
    
    def total_distance_score(self, color):
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
                minimize = min(self.chebyshev_distance(worker1.position, worker2.position), minimize)
            result += minimize
        return 8 - result

    def score(self, workers_positions, color):
        total_distance = self.total_distance_score(color)
        curr_cell_score = self.total_cell_score(workers_positions)
        curr_pos_score = self.height_score(workers_positions)

        return (curr_cell_score, curr_pos_score, total_distance)

    def check_score(self, symbol, color, new_positions):
        workers_positions = self._state.get_workers_pos_by_symbol(symbol)
        curr_worker = self._state.get_worker_by_symbol(symbol)
        previous_position = curr_worker.position
        curr_worker.position = new_positions

        try:
            return self.score(workers_positions, symbol, color)
        finally:
            curr_worker.position = previous_position

    #########################################################``
    #########################################################

    def occupied(self, position):
        worker = self._state.get_worker_by_position(position)
        return worker.symbol if worker else None

    def validate(self, type, new, direction):
        if not (0 <= new[0] < self.SIZE and 0 <= new[1] < self.SIZE):
            raise MoveError(type, direction)
        return True

    def get_ring(self, pos):
        ans = []

        for y in range(max(0, pos[0] - 1), min(5, pos[0] + 2)):
            for x in range(max(0, pos[1] - 1), min(5, pos[1] + 2)):
                if (y, x) == pos:
                    continue

                ans.append((y, x))

        return ans

    # Board Functional
    def __iter__(self):
        return GridIterator(self._grid)

    def build(self, position):
        y, x = position
        self._grid[y][x].upgrade()

    def get_cell(self, pos):
        """Get the cell at the specified position."""
        return self._grid[pos[0]][pos[1]]

    def __get_item__(self, key):
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
