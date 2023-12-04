
import sys
from Game import SantoriniGame
from Player import PlayerFactory

class SantoriniCLI:
    """Command-line interface."""

    def __init__(self, args):
        # Save Args
        self._white_player_type = args['white_player']
        self._blue_player_type = args['blue_player']
        self._undo_redo = args['undo_redo'] == "on"
        self._score_display = args['score_display'] == "on"

        white = PlayerFactory.get_factory('white', self._white_player_type)
        blue = PlayerFactory.get_factory('blue', self._blue_player_type)
        players = [white, blue]

        self._game = SantoriniGame(players)

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
    cli = SantoriniCLI(args)
    cli._game.run()