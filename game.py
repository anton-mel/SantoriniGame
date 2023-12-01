
class Worker:
    """Class representing a worker."""

    def __init__(self, symbol, default_position):
        self.symbol = symbol
        self.position = default_position

    @property
    def get_symbol(self):
        return self.symbol


class Player:
    """Class representing a player."""

    def __init__(self, color, workers):
        self.color = color
        self.workers = workers

    @property
    def get_workers(self):
        return self.workers
    
    @property
    def get_color(self):
        return self.color

class WhitePlayer(Player):
    """Class representing the White player."""

    def __init__(self):
        workers = [Worker('A', (3, 1)), Worker('B', (3, 3))]
        super().__init__('white', workers)

class BluePlayer(Player):
    """Class representing the Blue player."""

    def __init__(self):
        workers = [Worker('Y', (1, 2)), Worker('Z', (1, 4))]
        super().__init__('blue', workers)


# Here Command Pattern
class Command:
    """Class representing a player move."""

    def __init__(self):
        pass


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, players):
        self._players = players
        self._board = Board(self._players[0], players[1])
        self._current = self._players[0]
        self.turn = 1

    def print_board(self):
        print(f"Turn: {self.turn}, {self._current.get_color} ({[worker[0] for worker in self._current.get_workers]})")
        self._board.print_board()

    # Command Pattern Caller (Another Class)
    def execute_command(self, command):
        pass

    @property
    def get_current_player(self):
        return self._currentxww
    

class Board:
    """Class representing the Santorini Board."""

    def __init__(self, white, blue):
        self._grid = [[(0, []) for _ in range(5)] for _ in range(5)]

        self._add_workers_to_cell(3, 1, white.get_workers[0])
        self._add_workers_to_cell(1, 3, white.get_workers[1])
        self._add_workers_to_cell(1, 1, blue.get_workers[0])
        self._add_workers_to_cell(3, 3, blue.get_workers[1])

    def print_board(self):
        """Print the board."""
        for row in range(5):
            print("+--+--+--+--+--+")
            for col in range(5):
                height, workers = self._grid[row][col]
                print(f"|{height}{workers[0] if workers else ' '}", end="")

            print("|")
        print("+--+--+--+--+--+")

    def _add_workers_to_cell(self, row, col, workers):
        """Add workers to the cell."""
        self._grid[row][col] = (0, workers)

