
import copy
from Board import Board
from cli import s_cli, parse_args  #?
from Player import PlayerFactory
from exceptions import Loss, Win
from Memento import Originator, Caretaker, GameState


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

        self._originator = Originator(self._board.state)
        self._caretaker = Caretaker(self._originator)

        # Save default positions
        self._originator.restore(self._generate_state())
        self._caretaker.backup()

    def print_turn(self):
        s_cli.print_board(self._board)
        s_cli.print_turn(
            self._turn,
            str(self._current),
            self._current.worker_string(),
        )
            
    def won(self):
        self._next()
        s_cli.print_end(self.restart, self._current.color)
    
    def copy_turn(self):
        return copy.copy(self._turn)

    def _generate_state(self):
        # Generate DeepCopy of the GameState
        turn_copy = copy.copy(self._turn)
        white_workers = self._white.worker_deep_copy()
        blue_workers = self._blue.worker_deep_copy()
        grid = copy.deepcopy(self._board.grid)

        game_state = GameState(turn_copy, white_workers, blue_workers, grid)
        memento = self._originator.generate(game_state)

        return memento

    def _restore_state(self):
        state = self._originator.save()
        self._turn = state.get_turn()
        self._current = self._blue if (self._turn) % 2 == 0 else self._white
        self._white.workers = state.get_white_workers()
        self._blue.workers = state.get_blue_workers()
        self._board.grid = state.get_grid()

    def memento_display(self):
        command = s_cli.get_memento()

        if command == "undo":
            # Undo the current state and move to the next
            self._caretaker.undo()
            self._restore_state()
            return True
        elif command == "redo":
            # Similarly
            self._caretaker.redo()
            self._restore_state() 
            return True
        elif command == "next":
            # Update the Caretaker Mementos
            self._originator.restore(self._generate_state())
            self._caretaker.backup()
            return False
        else:
            raise ValueError
        
    def restart(self):
        (white, blue, undo_redo, score_display) = self._args
        self.__init__(white, blue, undo_redo, score_display)
        self.run()

    def run(self):
        """Infinite turn loop."""
        while True:
            # Initially pass to the board (printing) last updated state
            self._board._update_state(self._generate_state()) 

            self.print_turn()

            # Scores Before the Move is Executed
            if self._score_display == "on":
                print(",", end="")
                positions = [worker.position for worker in self.current.workers]
                score = self._board.score(positions, self._current.color)
                s_cli.print_score(score[0], score[1], score[2])
            print(end="\n")

            try:
                # Update possibilities & check if lost
                self._current.update_possibilities()
            except Loss:
                self._next()
                self.won()
                break

            # Display Memento
            undo_redo_done = None
            if self._undo_redo == "on":
                # Contoll Undo/Redo Command Function
                undo_redo_done = self.memento_display()
                if undo_redo_done:
                    continue

                # Since we first want to check if lost, then memento updates
                # So there should be generated new possibilities on the new state
                self._current.update_possibilities(self._current.color)

            try:
                # Ask for the direction strategies
                self._board.check_win(self._blue)
                self._board.check_win(self._white)

                # Execute Command
                symbol, move, build = self._execute_command()
            except Win:
                self.won()
            
            print(f"{symbol},{move},{build}", end="")

            # Scores After the Move is Executed
            if self._score_display == "on":
                self._board._update_state(self._generate_state()) 
                positions = [worker.position for worker in self.current.workers]
                score = self._board.score(positions, self._current.color) 
                s_cli.print_score(score[0], score[1], score[2])

            print(end="\n")
            self._next()

    def _next(self):
        self._turn += 1
        self._current = self._blue if self._turn % 2 == 0 else self._white

    # Memento Pattern
    def _execute_command(self):
        return self._current.execute()

    @property
    def current(self):
        return self._current


if __name__ == "__main__":
    args = parse_args()
    santorini_game = SantoriniGame(**args)
    santorini_game.run()
