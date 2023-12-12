
from exceptions import MoveError, Win
from Memento import GameState


class GridIterator:
    """Grid Iterator that prints Cell Step by Step."""

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
    """Santorini Board."""

    SIZE = 5

    def __init__(self):
        self._grid = [[Cell() for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._state = None

    @property
    def state(self):
        return self._state

    def _update_state(self, turn, white_workers_pos, blue_workers_pos, grid):
        self._state = GameState(
            turn,
            white_workers_pos,
            blue_workers_pos,
            grid
        )

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

    def total_distance_score(self):
        min_distance = 99
        result = 0

        for blue_worker in self._state.blue_workers:
            x1 = blue_worker.position[0]
            y1 = blue_worker.position[1]

            for white_worker in self._state.white_workers:
                x2 = white_worker.position[0]
                y2 = white_worker.position[1]

                min_distance = min(abs(x1 - x2) + abs(y1 - y2), min_distance)
            result += min_distance

        return 8 - result

    def score(self, workers_positions):
        total_distance = self.total_distance_score()
        curr_cell_score = self.total_cell_score(workers_positions)
        curr_pos_score = self.height_score(workers_positions)

        return curr_cell_score, curr_pos_score, total_distance

    def check_score(self, symbol, new_positions):
        workers_positions = self._state.get_workers_pos_by_symbol(symbol)
        curr_worker = self._state.get_worker_by_symbol(symbol)
        previous_position = curr_worker.position
        curr_worker.position = new_positions

        try:
            return self.score(workers_positions)
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
    """Board Cell."""

    def __init__(self, level=0) -> None:
        self._level = level

    def upgrade(self):
        if self._level < 4:
            self._level += 1

    @property
    def level(self):
        return self._level
