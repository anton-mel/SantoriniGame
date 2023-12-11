from Board import Board
from cli import SantoriniCLI, parse_args  # fix?
from Player import PlayerFactory
from exceptions import MoveError, MementoError, GameOverError
from Memento import Originator, Caretaker


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, white, blue, undo_redo, score_display):
        self._board = Board()

        self._white = PlayerFactory.get_factory("white", white, self._board)
        self._blue = PlayerFactory.get_factory("blue", blue, self._board)

        self._undo_redo = undo_redo
        self._score_display = score_display

        if self._undo_redo == "on":
            self._originator = Originator("Initial State")
            self._caretaker = Caretaker(self._originator)

        self._turn = 1
        self._current = self._white

    def won(self):
        for key, value in self._board.observers.items():
            if self._board.get_cell(value).level == 3:
                self._next()
                SantoriniCLI().print_end(self._current.color)
                return True
        return False

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
            print(self._board)
            SantoriniCLI().print_turn(
                self._turn, str(self._current), self._current.worker_string()
            )

            if self._score_display == "on":
                h, c, d = self._board.score()
                print(f", ({h}, {c}, {d})", end="")
            print(end="\n")

            self._current._update_possibilities(self._board)

            if self._undo_redo == "on":
                self.memento_display()

            if self.won():
                break

            try:
                self._execute_command()
                self._next()
            except GameOverError:
                self.won()
                break

    def _next(self):
        self._current = self._white if self._turn % 2 == 0 else self._blue
        self._turn += 1

    # Memento Pattern
    def _execute_command(self):
        white_workers_pos = [worker.position for worker in self._white.workers]
        blue_workers_pos = [worker.position for worker in self._blue.workers]

        if self._undo_redo == "on":
            self._caretaker.backup()

            self._originator.generate_game_state(
                self._turn, white_workers_pos, blue_workers_pos
            )
            self._caretaker.show_history()

        symbol, move_direction, build_direction = self._current.execute()
        print(f"{symbol}, {move_direction}, {build_direction}", end="")
        if self._score_display == "on":
            h, c, d = self._board.score()
            print(f", ({h}, {c}, {d})", end="")
        print(end="\n")

    @property
    def current(self):
        return self._current


if __name__ == "__main__":
    args = parse_args()
    santorini_game = SantoriniGame(**args)
    santorini_game.run()
