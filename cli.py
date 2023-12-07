# Memento Pattern (For Command History)            -     NOT
# Strategy Pattern! 1 part fits (Human/Heuristic)  -     DONE
# Iterator Pattern                                 -     DONE
# Factory Method (args passed: human/computer)     -     DONE

import sys

class SantoriniCLI:
    """Command-line interface."""

    def __init__(self) -> None:
        pass

    def get_move(self):
        return input("Select a worker to move: ")

    def get_direction(self):
        return input("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")

    def get_build(self):
        return input("Select a direction to build (n, ne, e, se, s, sw, w, nw): ")

    def print_selection(self):
        raise NotImplementedError()

    def print_board(self):
        raise NotImplementedError()

    def print_turn(self, turn, color, workers):
        print(f"Turn: {turn}, {color} ({workers})")

    def print_end(self, winner):
        print(f"{winner} has won")
        if input("Play Again?\n") != "yes":
            exit(0)

def parse_args():
    args = sys.argv[1:]
    white_player_type = (
        args[0] if args and args[0] in ["human", "heuristic", "random"] else "human"
    )
    blue_player_type = (
        args[1]
        if len(args) > 1 and args[1] in ["human", "heuristic", "random"]
        else "human"
    )
    undo_redo_enabled = args[2] if len(args) > 2 and args[2] in ["on", "off"] else "off"
    score_display_enabled = (
        args[3] if len(args) > 3 and args[3] in ["on", "off"] else "off"
    )

    return {
        "white": white_player_type,
        "blue": blue_player_type,
        "undo_redo": undo_redo_enabled,
        "score_display": score_display_enabled,
    }
