# Memento Pattern (For Command History)            -     NOT
# Template Pattern!                                -     NOT
# Iterator Pattern                                 -     DONE
# Factory Method (args passed: human/computer)     -     DONE

import sys
from exceptions import DirectionError


class SantoriniCLI:
    """Client Interaction Helper Functions."""

    def __init__(self) -> None:
        pass

    def select_worker(self):
        return input("Select a worker to move:\n")

    def get_direction(self, prompt):
        while True:
            try: 
                direction = input(prompt)
                valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
                if direction not in valid_directions:
                    raise DirectionError(f"Not a valid direction")
            except DirectionError as e:
                print(f"{e.mes}")
            else:
                return direction

    def get_memento(self):
        prompt = "undo, redo, or next\n"
        return input(prompt)

    def get_move(self):
        prompt = "Select a direction to move (n, ne, e, se, s, sw, w, nw):\n"
        return self.get_direction(prompt)

    def get_build(self):
        prompt = "Select a direction to build (n, ne, e, se, s, sw, w, nw):\n"
        return self.get_direction(prompt)

    def print_selection(self):
        raise NotImplementedError()

    def print_board(self):
        raise NotImplementedError()

    def print_invalid_move(e):
        print(f"Cannot {e.move_type} {e.direction}")

    def print_worker_error(e):
        print(e.mes)

    def print_turn(self, turn, color, workers):
        print(f"Turn: {turn}, {color} ({workers})", end="")

    def print_end(self, run_game, winner):
        print(f"{winner} has won")
        if input("Play Again?\n") != "yes":
            exit(0)
        else:
            run_game()



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
