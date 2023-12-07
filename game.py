from Board import Board
from cli import SantoriniCLI, parse_args
from Player import PlayerFactory


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, white, blue, undo_redo, score_display):
        self._cli = SantoriniCLI()
        self._board = Board()
        
        # give board to each of the players
        self._white = PlayerFactory.get_factory("white", white, self._board)
        self._blue = PlayerFactory.get_factory("blue", blue, self._board)
        
        self._undo_redo = undo_redo
        self._score_display = score_display

        self._turn = 1
        self._current = self._white

    def run(self):
        """Infinite turn loop."""
        while True:
            self.__repr__()
            self._cli.print_turn(
                self._turn, str(self._current), self._current.worker_string()
            )
            self._execute_command()

    def _next(self):
        self._current = self._white if self._turn % 2 == 0 else self._blue
        self._turn += 1

    # Memento Pattern Implement Later
    def _execute_command(self):
        self._current._execute()
        self._next()

    @property
    def current(self):
        return self._current

    # maybe we want to generate a grid here and pass it to cli
    def __repr__(self):
        for i, row in enumerate(self._board):
            print("+--+--+--+--+--+")
            for j, cell in enumerate(row):
                worker_white = self._white.get_worker_at((i, j))
                worker_blue = self._blue.get_worker_at((i, j))
                height = cell.level
                worker_symbol = (
                    worker_white.symbol if worker_white else worker_blue.symbol if worker_blue else ' '
                )
                print(f"|{height}{worker_symbol}", end="")
            print("|")
        print("+--+--+--+--+--+")

if __name__ == "__main__":
    args = parse_args()
    santorini_game = SantoriniGame(**args)
    santorini_game.run()
