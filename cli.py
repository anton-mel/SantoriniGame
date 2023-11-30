
import logging
from game import SantoriniGame, Move

class SantoriniCLI:
    """Command-line interface."""

    def __init__(self):
        self._santorini_game = SantoriniGame()
        # we will maybe use it as a key to come back in the history
        self._current_turn = 1

    def run(self):
        """Infinite turn loop."""
        while True:
            print(f"Turn: {self._current_turn}, {self._santorini_game.get_current_player()} ({self._santorini_game.get_current_player_workers()})")
            self._santorini_game.print_board()

            self._process_turn()

            self._current_turn += 1

    def _process_turn(self):
        worker_to_move = input("Select a worker to move: ")
        direction_to_move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")
        direction_to_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw): ")

        move = Move(worker_to_move, direction_to_move, direction_to_build)
        self._santorini_game.execute_move(move)


if __name__ == "__main__":
    try:
        SantoriniCLI().run()
    except KeyboardInterrupt:
        print("\nGame terminated by the player.")
    except Exception as e:
        print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        logging.error(str(e.__class__.__name__) + ": " + repr(str(e)))