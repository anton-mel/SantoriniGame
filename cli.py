# Memento Pattern (For Command History)            -     DONE
# Template Pattern!                                -     DONE
# Singleton Pattern                                -     DONE
# Factory Method (args passed: human/computer)     -     DONE

import sys
from exceptions import DirectionError, WorkerError


class SantoriniCLI:
    """Client Interaction Helper Functions."""

    def select_worker(self):
        """Prompts the user to select a worker and returns the input."""
        while True:
            try:
                worker = input("Select a worker to move\n")
                valid_workers = ("A", "B", "C", "D")
                if worker not in valid_workers:
                    raise WorkerError("Not a valid worker")
            except WorkerError as e:
                self.print_worker_error(e.mes)
            else:
                return worker

    def get_direction(self, prompt):
        """
        Prompts the user to input a direction and validates it.
        Returns the validated direction.
        """

        while True:
            try:
                direction = input(prompt)
                valid_directions = ("n", "ne", "e", "se", "s", "sw", "w", "nw")
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
        prompt = "Select a direction to move (n, ne, e, se, s, sw, w, nw)\n"
        return self.get_direction(prompt)

    def get_build(self):
        prompt = "Select a direction to build (n, ne, e, se, s, sw, w, nw)\n"
        return self.get_direction(prompt)

    def print_board(self, board):
        print(board)

    def print_score(self, h_score, c_score, d_score):
        print(f" ({h_score}, {c_score}, {d_score})", end="")

    def print_invalid_move(self, e):
        print(f"Cannot {e.move_type} {e.direction}")

    def print_worker_error(self, mes):
        print(mes)

    def print_turn(self, turn, color, workers):
        print(f"Turn: {turn}, {color} ({workers})", end="")

    def print_end(self, restart, winner):
        """Prints the end of the game, including the winner, and prompts for a restart by passing the function."""

        print(f"{winner} has won")
        if input("Play again?\n").lower() != "yes":
            exit(0)
        else:
            restart()


s_cli = SantoriniCLI()


def parse_args():
    """
    Parses command line arguments for configuring the Santorini game.

    Returns:
        dict: A dictionary containing configuration options for white player type, blue player type,
              undo/redo enablement, and score display enablement.
    """

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
