from exceptions import MoveError
from DirectionUtils import DirectionUtils
from Memento import GameState


class GridIterator:
    """Grid Iterator that prints Cell Step by Step."""

    def __init__(self, board):
        self._board = board
        self._current_row = 0

    def __iter__(self):
        return self

    # Step-by-step Cell Printing
    def __next__(self):
        if self._current_row < Board.SIZE:
            row_result = "+--" * Board.SIZE + "+\n"
            for j in range(Board.SIZE):
                cell = self._board.get_cell((self._current_row, j))
                height = cell.level

                worker_symbol = next(
                    (
                        symbol
                        for symbol, value in self._board.observers.items()
                        if value == (self._current_row, j)
                    ),
                    None,
                )

                row_result += f"|{height}" + (worker_symbol if worker_symbol else " ")
            row_result += "|\n"
            self._current_row += 1
            return row_result
        else:
            raise StopIteration


class Board:
    """Santorini Board."""

    SIZE = 5

    def __init__(self):
        self._grid = [[Cell() for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._observers = {}
        self._state = None

    @property
    def observers(self):
        return self._observers
    
    @property
    def state(self):
        return self._state

    def _update_state(self, turn, white_workers_pos, blue_workers_pos):
        self._state = GameState(
            turn,
            white_workers_pos,
            blue_workers_pos
        )

    def remove_observer(self, observer):
        self._observers.remove({observer.symbol: observer.position})

    def add_observer(self, symbol, position):
        self._observers[symbol] = position

    def update_worker_position(self, worker):
        if worker.symbol in self._observers:
            del self._observers[worker.symbol]
            self.add_observer(worker.symbol, worker.position)

    #########################################################
    # Calculate Score for Human State or Heuristic Strategies
    #########################################################

    def total_cell_score(self, workers_positions):
        result = 0
        for position in workers_positions:
            result += self.get_cell(position).level
        return result

    def height_score(self, current_pos):
        score = 0
        for position in current_pos:
            score += 2 - max(abs(position[0] - 2), abs(position[1] - 2))
        return score

    def total_distance_score(self, white_worker_pos, blue_worker_pos):
        min_distance = 99
        result = 0

        for i in range(len(white_worker_pos)):
            x1 = white_worker_pos[i][0]
            y1 = white_worker_pos[i][1]

            for j in range(len(blue_worker_pos)):
                x2 = blue_worker_pos[j][0]
                y2 = blue_worker_pos[j][1]

                min_distance = min(abs(x1 - x2) + abs(y1 - y2), min_distance)
            result += min_distance

        return 8 - result

    def score(self, workers_positions):
        white_worker_pos = [self._observers["A"], self._observers["B"]]
        blue_worker_pos = [self._observers["Y"], self._observers["Z"]]
        total_distance = self.total_distance_score(white_worker_pos, blue_worker_pos)

        curr_cell_score = self.total_cell_score(workers_positions)
        curr_pos_score = self.height_score(workers_positions)

        return curr_cell_score, curr_pos_score, total_distance

    def check_score(self, symbol, new_positions, workers_positions):
        removed_observer_position = self._observers.pop(symbol)

        try:
            self.add_observer(symbol, new_positions)
            h, c, d = self.score(workers_positions)
            return h, c, d
        finally:
            self._observers[symbol] = removed_observer_position

    #########################################################
    #########################################################

    def occupied(self, position):
        return next(
            (key for key, value in self._observers.items() if value == position), None
        )

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
        return GridIterator(self)

    def build(self, position):
        y, x = position
        self._grid[y][x].upgrade()

    def get_cell(self, pos):
        y, x = pos
        return self._grid[y][x]

    def __get_item__(self, key):
        return self._grid[key]

    def __repr__(self):
        output = ""
        for row in self:
            output += row
        output += "+--" * Board.SIZE + "+"
        return output


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
