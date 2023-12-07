from Board import Board
from cli import SantoriniCLI, parse_args
from Player import PlayerFactory


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, white, blue, undo_redo, score_display):
        self._cli = SantoriniCLI()
        self._white = PlayerFactory.get_factory("white", white)
        self._blue = PlayerFactory.get_factory("blue", blue)

        self._board = Board(self._white, self._blue)
        self._current = self._white

        self._undo_redo = undo_redo
        self._score_display = score_display

        self._turn = 1
        self._current = self._white

    def run(self):
        """Infinite turn loop."""
        while True:
            self._cli.print_board()
            self._cli.print_turn(
                self._turn, str(self._current), "()" + self._current.worker_string()
            )
            self.execute_command()

    def _next(self):
        self._current = self._white if self._turn == self._blue else self._blue
        self._turn += 1

    # Memento Pattern Implement Later
    def execute_command(self):
        self._current.execute(self._board)
        self._next()

    @property
    def current(self):
        return self._current

    def __repr__(self):
        for i, row in enumerate(self._board):
            print("+--+--+--+--+--+")
            for j, cell in enumerate(row):
                worker = self._white.get_worker_at((i, j))
                worker = self._blue.get_worker_at((i, j))
                height = cell.level

                print(f"|{height}{worker.symbol if worker else ' '}|", end="")
            print("\n")
            print("+--+--+--+--+--+")


if __name__ == "__main__":
    args = parse_args()

    santorini_game = SantoriniGame(**args)
