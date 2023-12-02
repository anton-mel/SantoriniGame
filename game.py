
from Strategy import Strategy
from Board import Board

class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, players):
        self._players = players
        self._board = Board(self._players[0], players[1])
        self._current = self._players[0]
        self._turn = 1
    
    def _next(self):
        self._current = self._players[self._turn % 2]
        self._turn += 1

    def print_board(self):
        print(f"Turn: {self._turn}, {self._current.get_color} ({''.join([worker.get_symbol for worker in self._current.get_workers])})")
        self._board.print_board()

    # Memento Pattern Implement Later
    def execute_command(self, w, d, b):
        strategy = Strategy(w, d, b)
        strategy.execute(self._board)
        self._next()

    @property
    def get_current_player(self):
        return self._current
    


