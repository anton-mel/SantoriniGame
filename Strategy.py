from cli import s_cli
from exceptions import WorkerError, MoveError, Loss
from DirectionUtils import DirectionUtils
import random


class Strategy:
    """
    Base class representing a strategy for playing the Santorini board game.

    Attributes:
        _p (dict): Dictionary storing possible moves and builds for each worker.
        _selected_worker (Worker): The currently selected worker for the strategy.
        _selected_move (tuple): The selected move coordinates.
        _move_direction (str): The direction of the selected move.
        _selected_build (tuple): The selected build coordinates.
        _build_direction (str): The direction of the selected build.
    """

    def __init__(self, board, workers, player_type):
        self._board = board
        self._p = {}
        self._color = player_type
        self._w_symbols = (worker.symbol for worker in workers)

        self._selected_worker = None
        self._selected_move = None
        self._move_direction = None
        self._selected_build = None
        self._build_direction = None

    def _get_worker(self):
        pass

    def _get_move(self):
        pass

    def _get_build(self):
        self._selected_build = random.choice(
            list(self._p[self._selected_worker][self._selected_move])
        )

        self._build_direction = DirectionUtils.calculate_direction(
            original=self._selected_move, new=self._selected_build
        )

    def update_possibilities(self, workers):
        """Updates possible moves and builds for each worker on the board."""

        self._p.clear()

        for worker in workers:
            pos = worker.position
            level = self._board.get_cell(pos).level
            for move in self._board.get_ring(pos):
                cell = self._board.get_cell(move)

                if cell.level > 3:
                    continue

                if cell.level > level + 1:
                    continue

                if self._board.occupied(move):
                    continue

                for build in self._board.get_ring(move):
                    cell = self._board.get_cell(build)

                    if self._board.occupied(build) and build != pos:
                        continue

                    if cell.level > 3:
                        continue

                    if worker not in self._p:
                        self._p[worker] = {}

                    if move not in self._p[worker]:
                        self._p[worker][move] = set()

                    self._p[worker][move].add(build)

        if len(self._p) == 0:
            raise Loss

    def _execute_steps(self):
        self._move(self._selected_move, self._selected_worker)
        self._build(self._selected_build)

    def execute(self):
        """
        Executes the entire strategy, including worker selection, move selection, and building.
        Returns a tuple containing worker symbol, move direction, and build direction.
        """
        self._get_worker()
        self._get_move()
        self._get_build()

        self._execute_steps()

        return self._selected_worker.symbol, self._move_direction, self._build_direction

    def _move(self, position, worker):
        worker.position = position

    def _build(self, position):
        self._board.build(position)


class HumanStrategy(Strategy):
    """
    Subclass of Strategy representing a human-controlled strategy.

    Methods:
        execute(self):
            Executes the entire human strategy, including worker selection, move selection, and building.
            Returns a tuple containing worker symbol, move direction, and build direction.
    """

    def _get_worker(self):
        while True:
            try:
                symbol = s_cli.select_worker()

                if symbol not in self._w_symbols:
                    raise WorkerError("That is not your worker")

                for w in self._p.keys():
                    if w.symbol == symbol:
                        worker = w

                if worker not in self._p:
                    raise WorkerError("That worker cannot move")

            except WorkerError as e:
                s_cli.print_worker_error(e.mes)
            else:
                self._selected_worker = worker
                break

    def _get_move(self):
        while True:
            try:
                move_direction = s_cli.get_move()
                move = DirectionUtils.move_result(
                    self._selected_worker.position, move_direction
                )

                if move not in self._p[self._selected_worker]:
                    raise MoveError("move", move_direction)

            except MoveError as e:
                s_cli.print_invalid_move(e)
            else:
                self._selected_move = move
                self._move_direction = move_direction
                break

    def _get_build(self):
        while True:
            try:
                build_direction = s_cli.get_build()
                build = DirectionUtils.move_result(self._selected_move, build_direction)

                if build not in self._p[self._selected_worker][self._selected_move]:
                    raise MoveError("build", build_direction)

            except MoveError as e:
                s_cli.print_invalid_move(e)
            else:
                self._selected_build = build
                self._build_direction = build_direction
                break


class HeuristicStrategy(Strategy):
    """
    Subclass of Strategy representing a heuristic-based strategy.

    Methods:
        execute(self):
            Executes the entire heuristic strategy, including worker selection, move selection, and building.
            Returns a tuple containing worker symbol, move direction, and build direction.
    """

    def _get_move(self):
        best_score = -10
        best_move = None
        for worker in self._p:
            for move in self._p[worker]:
                (height, center, distance) = self._board.check_score(
                    worker.symbol,
                    self._color,
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
    """
    Subclass of Strategy representing a random strategy.

    Methods:
        execute(self):
            Executes the entire random strategy, including worker selection, move selection, and building.
            Returns a tuple containing worker symbol, move direction, and build direction.
    """

    def _get_worker(self):
        self._selected_worker = random.choice(list(self._p.keys()))

    def _get_move(self):
        x = self._p[self._selected_worker]

        self._selected_move = random.choice(list(x.keys()))

        self._move_direction = DirectionUtils.calculate_direction(
            original=self._selected_worker.position, new=self._selected_move
        )
