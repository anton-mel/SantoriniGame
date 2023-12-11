from Board import Board
from cli import SantoriniCLI, parse_args  # fix?
from Player import PlayerFactory
from exceptions import GameOverError
from Memento import Originator, Caretaker


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, white, blue, undo_redo, score_display):
        self._board = Board()

        self._white = PlayerFactory.get_factory("white", white, self._board)
        self._blue = PlayerFactory.get_factory("blue", blue, self._board)

        self._undo_redo = undo_redo
        self._score_display = score_display

        self._turn = 1
        self._current = self._white

        self._update_state()

        if self._undo_redo == "on":
            self._originator = Originator(self._board.state)
            self._caretaker = Caretaker(self._originator)

    def won(self):
        for key, value in self._board.observers.items():
            if self._board.get_cell(value).level == 3:
                self._next()
                SantoriniCLI().print_end(self.run, self._current.color)
                return True
        return False

    def _update_state(self):
        white_workers_pos = self._white.worker_pos()
        blue_workers_pos = self._blue.worker_pos()
        self._board._update_state(self._turn, white_workers_pos, blue_workers_pos)

    def memento_display(self):
        while True:
            command = SantoriniCLI().get_memento()

            if command == "undo":
                self._caretaker.undo()
            elif command == "redo":
                self._caretaker.redo()
            else:
                break

    def run(self):
        """Infinite turn loop."""
        while True:
            self._update_state()

            SantoriniCLI().print_board(self._board)
            SantoriniCLI().print_turn(
                self._turn,
                str(self._current),
                self._current.worker_string(),
            )

            if self._score_display == "on":
                positions = [worker.position for worker in self.current.workers]
                h, c, d = self._board.score(positions)
                SantoriniCLI().print_score(h, c, d)
            print(end="\n")

            self._current._update_possibilities(self._board)

            if self._undo_redo == "on":
                self.memento_display()

            if self.won():
                break

            try:
                symbol, move, build = self._execute_command()
                self._next()
            except GameOverError:
                self.won()
                break
            else:
                print(f"{symbol}, {move}, {build}", end="")
                if self._score_display == "on":
                    current_pos = self._current.worker_pos()
                    h, c, d = self._board.score(current_pos)
                    print(f", ({h}, {c}, {d})", end="")
                print(end="\n")

    def _next(self):
        self._current = self._white if self._turn % 2 == 0 else self._blue
        self._turn += 1

    # Memento Pattern
    def _execute_command(self):
        if self._undo_redo == "on":
            self._caretaker.backup()
            self._caretaker.show_history()

        return self._current.execute()

    @property
    def current(self):
        return self._current


if __name__ == "__main__":
    args = parse_args()
    santorini_game = SantoriniGame(**args)
    santorini_game.run()
