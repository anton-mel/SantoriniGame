from cli import SantoriniCLI
from exceptions import WorkerError, MoveError
from DirectionUtils import DirectionUtils
import random


class Strategy:
    def __init__(self, board, possibilities):
        self._board = board
        self._p = possibilities

        self._selected_worker = None
        self._selected_move = None
        self._move_direction = None
        self._selected_build = None
        self._build_direction = None

    def _get_worker(self, player):
        pass

    def _get_move(self, player):
        pass

    def _get_build(self):
        self._selected_build = random.choice(
            list(self._p[self._selected_worker][self._selected_move])
        )

        self._build_direction = DirectionUtils.calculate_direction(
            original=self._selected_move, new=self._selected_build
        )

    def _execute_steps(self):
        self._move(self._selected_move, self._selected_worker)
        self._build(self._selected_build)

    def execute(self, player):
        self._get_worker(player)
        self._get_move(player)
        self._get_build()

        self._execute_steps()

        return self._selected_worker.symbol, self._move_direction, self._build_direction

    def _move(self, position, worker):
        worker.position = position

    def _build(self, position):
        self._board.build(position)


class HumanStrategy(Strategy):
    def _get_worker(self, player):
        while True:
            try:
                symbol = SantoriniCLI().select_worker()
                worker = player._select_worker(symbol)

                symbol_in_state = (symbol in self._board.state.white_workers or symbol in self._board.state.blue_workers)
                worker_is_none = (not worker)

                if symbol_in_state and worker_is_none:
                    raise WorkerError("That is not your worker")

                if not worker:
                    raise WorkerError("Not a valid worker")

                if worker not in self._p:
                    raise WorkerError("That worker cannot move")

            except WorkerError as e:
                SantoriniCLI().print_worker_error(e.mes)
            else:
                self._selected_worker = worker
                break

    def _get_move(self, player):
        while True:
            try:
                move_direction = SantoriniCLI().get_move()
                move = DirectionUtils.move_result(
                    self._selected_worker.position, move_direction
                )

                if move not in self._p[self._selected_worker]:
                    raise MoveError("move", move_direction)

            except MoveError as e:
                SantoriniCLI().print_invalid_move(e)
            else:
                self._selected_move = move
                self._move_direction = move_direction
                break

    def _get_build(self):
        while True:
            try:
                build_direction = SantoriniCLI().get_build()
                build = DirectionUtils.move_result(self._selected_move, build_direction)

                if build not in self._p[self._selected_worker][self._selected_move]:
                    raise MoveError("build", build_direction)

            except MoveError as e:
                SantoriniCLI().print_invalid_move(e)
            else:
                self._selected_build = build
                self._build_direction = build_direction
                break


class HeuristicStrategy(Strategy):
    def _get_move(self, player):
        best_score = -10
        best_move = None
        for worker in self._p:
            for move in self._p[worker]:
                (height, center, distance) = self._board.check_score(
                    worker.symbol,
                    move,   
                )

                move_score = 3 * height + 2 * center + distance

                if self._board.get_cell(move).level == 3:
                    move_score = 10000

                if move_score > best_score:
                    best_move = move
                    best_score = move_score
                    self._selected_worker = worker
                elif move_score == best_score:
                    if bool(random.getrandbits(1)):
                        best_move = move
                        best_score = move_score
                        self._selected_worker = worker

        self._selected_move = best_move
        self._move_direction = DirectionUtils.calculate_direction(
            original=self._selected_worker.position, new=self._selected_move
        )


class RandomStrategy(Strategy):
    def _get_worker(self, player):
        self._selected_worker = random.choice(list(self._p.keys()))

    def _get_move(self, player):
        x = self._p[self._selected_worker]

        self._selected_move = random.choice(list(x.keys()))

        self._move_direction = DirectionUtils.calculate_direction(
            original=self._selected_worker.position, new=self._selected_move
        )
