
import copy
from Board import Board
from cli import SantoriniCLI, parse_args  # fix?
from Player import PlayerFactory
from exceptions import Loss, Win
from Memento import Originator, Caretaker


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, white, blue, undo_redo, score_display):
        self._board = Board()
        self._args = (white, blue, undo_redo, score_display)

        self._white = PlayerFactory.get_factory("white", white, self._board)
        self._blue = PlayerFactory.get_factory("blue", blue, self._board)

        self._undo_redo = undo_redo
        self._score_display = score_display

        self._turn = 1
        self._current = self._white


        if self._undo_redo == "on":
            self._originator = Originator(self._board.state)
            self._caretaker = Caretaker(self._originator)
            
        self._update_state()

    def won(self):
        self._next()
        for worker in self._current.workers:
            print(worker.position)
        SantoriniCLI().print_end(self.restart, self._current.color)
    
    def copy_turn(self):
        return copy.copy(self._turn)

    def _update_state(self):
        turn_copy = copy.copy(self._turn)
        white_workers_pos = self._white.worker_deep_copy()
        blue_workers_pos = self._blue.worker_deep_copy()
        grid = copy.deepcopy(self._board.grid)
        self._originator.generate_game_state(turn_copy, white_workers_pos, blue_workers_pos, grid)
        self._board._update_state(turn_copy, white_workers_pos, blue_workers_pos, grid)

    def _restore_state(self):
        state = self._originator.state
        self._turn = state.turn
        self._white.workers = state.white_workers
        self._blue.workers = state.blue_workers
        self._board.grid = state.grid
        self._update_state()

    def memento_display(self):
        command = SantoriniCLI().get_memento()

        if command == "undo":
            self._caretaker.undo()
            self._restore_state()
            return True
        elif command == "redo":
            self._caretaker.redo()
            self._restore_state()
            return True
        elif command == "next":
            return False
        
    def restart(self):
        (white, blue, undo_redo, score_display) = self._args
        self.__init__(white, blue, undo_redo, score_display)
        self.run()

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
            
            try:
                self._current.update_possibilities(self._board)
            except Loss:
                self.won()
                break

            if self._undo_redo == "on":
                # print(self._originator.)
                if self.memento_display():
                    continue
                self._current.update_possibilities(self._board)

            try:
                self._board.check_win(self._blue)
                self._board.check_win(self._white)
                symbol, move, build = self._execute_command()
                self._next()
            except Win:
                self.won()
            print(f"{symbol}, {move}, {build}", end="")
            if self._score_display == "on":
                deep_workers = self._current.worker_deep_copy()
                workers_positions = [worker.position for worker in deep_workers]
                score = self._board.score(workers_positions)
                print(f", ({score[0]}, {score[1]}, {score[2]})", end="")
            print(end="\n")

    def _next(self):
        self._current = self._white if self._turn % 2 == 0 else self._blue
        self._turn += 1

    # Memento Pattern
    def _execute_command(self):
        if self._undo_redo == "on":
            self._caretaker.backup()
            # self._caretaker.show_history()

        return self._current.execute()

    @property
    def current(self):
        return self._current


if __name__ == "__main__":
    args = parse_args()
    santorini_game = SantoriniGame(**args)
    santorini_game.run()
