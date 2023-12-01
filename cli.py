# We need at least 4 patterns (non-trivial)
# Possible Distribution:
# Memento Pattern (For Command History)
# Strategy Pattern! 1 part fits (Human/Heuristic)
# Command Pattern (For )
# Fctory Method (args passed: human/computer)

import sys
from game import SantoriniGame, Command, Player

class SantoriniCLI:
    """Command-line interface."""

    def __init__(self, args):
        self._white_player = args['white_player']
        self._blue_player = args['blue_player']
        self._undo_redo = args['undo_redo'] == "on"
        self._score_display = args['score_display'] == "on"

        # Create players and workers
        white_workers = [("A", (3, 1)), ("B", (3, 2))]
        blue_workers = [("Y", (1, 2)), ("Z", (1, 4))]
        white = Player(self._white_player, white_workers)
        blue = Player(self._blue_player, blue_workers)
        players = [white, blue]

        # Create the Game
        self._game = SantoriniGame(players)        

    def run(self):
        """Infinite turn loop."""
        while True: # change later
            self._game.print_board()
            self._process_turn()

    def _process_turn(self):
        worker_to_move = input("Select a worker to move: ")
        direction_to_move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")
        direction_to_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw): ")

        command = Command()
        # Think about Command Pattern


def parse_args():
    args = sys.argv[1:]
    white_player_type = args[0] if args and args[0] in ["human", "heuristic", "random"] else "human"
    blue_player_type = args[1] if len(args) > 1 and args[1] in ["human", "heuristic", "random"] else "human"
    undo_redo_enabled = args[2] if len(args) > 2 and args[2] in ["on", "off"] else "off"
    score_display_enabled = args[3] if len(args) > 3 and args[3] in ["on", "off"] else "off"

    return {
        "white_player": white_player_type,
        "blue_player": blue_player_type,
        "undo_redo": undo_redo_enabled,
        "score_display": score_display_enabled
    }

if __name__ == "__main__": 
    args = parse_args()

    # Create players and workers
    white_workers = [("A", (3, 1)), ("B", (3, 2))]
    blue_workers = [("Y", (1, 2)), ("Z", (1, 4))]

    white_player = Player("white", white_workers)
    blue_player = Player("blue", blue_workers)

    players = [white_player, blue_player]

    # Initialize the game & board with players
    santorini_game = SantoriniGame(players)

    # Run & display the game
    cli = SantoriniCLI(args)
    cli.run()
