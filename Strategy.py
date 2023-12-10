from cli import SantoriniCLI


class DirectionStrategy:
    def __init__(self, board):
        self._board = board

    def _get_direction_delta(self, direction):
        direction_deltas = {
            "n": (-1, 0),
            "ne": (-1, 1),
            "e": (0, 1),
            "se": (1, 1),
            "s": (1, 0),
            "sw": (1, -1),
            "w": (0, -1),
            "nw": (-1, -1),
        }
        return direction_deltas[direction]

    def _move(self, direction, worker):
        delta = self._get_direction_delta(direction)
        current_position = worker.position
        new_position = (
            current_position[0] + delta[0],
            current_position[1] + delta[1],
        )

        worker.position = new_position

    def _build(self, direction, worker):
        delta = self._get_direction_delta(direction)
        current_position = worker.position
        new_position = (
            current_position[0] + delta[0],
            current_position[1] + delta[1],
        )

        self._board.build(new_position)
    
    def __call__(self, workers):
        self._execute(workers)


class HumanStrategy(DirectionStrategy):
    def __init__(self, board):
        super().__init__(board)

    def _execute(self, workers):
        selected_worker = SantoriniCLI().select_worker(workers)

        move_direction = SantoriniCLI().get_move()
        super()._move(move_direction, selected_worker)

        build_direction = SantoriniCLI().get_build()
        super()._build(build_direction, selected_worker)


class HeuristicMove():
    pass