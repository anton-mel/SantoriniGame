from cli import SantoriniCLI
from exceptions import WorkerError, DirectionError, MoveError
from DirectionUtils import DirectionUtils
import random

class Strategy:
    def __init__(self, board, player):
        self._board = board
        self._player = player
        self._p = {}    

        self._selected_worker = None
        self._selected_move = None
        self._selected_build = None


    def _update_possibilities(self):
        self._p = {}

        for worker in self._player.workers:
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

                    if self._board.occupied(build):
                        continue

                    if cell.level == 3:
                        continue

                    if worker.symbol not in self._p:
                        self._p[worker.symbol] = {}
                    
                    if move not in self._p[worker.symbol]:
                        self._p[worker.symbol][move] = set()

                    self._p[worker.symbol][move].add(build)

    def _get_worker(self):
        pass

    def _get_move(self):
        pass

    def _get_build(self):
        self._selected_build = random.choice(list(self._p.values[self._selected_worker][self._selected_move]))

    def _execute_steps(self):
        self._move(self._selected_move, self._selected_worker)
        self._build(self._selected_build)

    def execute(self):
        self._update_possibilities()

        self._get_worker()
        self._get_move()
        self._get_build()

        self._execute_steps()

    def _move(self, position, worker):
        worker.position = position

    def _build(self, position):
        self._board.build(position)


class HumanStrategy(Strategy):
    def _get_worker(self):
        while True:
            try:
                symbol = SantoriniCLI().select_worker()
                worker = self._player._select_worker(symbol)

                if (symbol in self._board.observers) and (not worker):
                    raise WorkerError("That is not your worker")
                
                if not worker:
                    raise WorkerError("Not a valid worker")

                if symbol not in self._p:
                    raise WorkerError("That worker cannot move")

            except WorkerError as e:
                print(e.mes)
            else:
                self._selected_worker = worker
                break

    def _get_move(self):
        while True:
            try:
                move_direction = SantoriniCLI().get_move()
                move = self._player._select_worker(self._selected_worker).update_position(move_direction)
                
                if move not in self._p[self._selected_worker.symbol]:
                    raise MoveError("move", move_direction)
                
            except MoveError as e:
                print(f"Cannot {e.move_type} {e.direction}")
            except DirectionError as e:
                print(f"{e.mes}")
            else:
                self._selected_move = move
                break

    def _get_build(self):
        while True:
            try:
                build_direction = SantoriniCLI().get_build()
                build = self._player._select_worker(self._selected_worker).update_position(build_direction, self._selected_move)
                
                if build not in self._p[self._selected_worker.symbol][self._selected_move]:
                    raise MoveError("build", build_direction)

            except MoveError as e:
                print(f"Cannot {e.move_type} {e.direction}")
            except DirectionError as e:
                print(f"{e.mes}")
            else:
                self._selected_build = build
                break


class HeuristicStrategy():
    def _get_move(self):
        for worker in self._p:
            for move in self._p[worker.symbol]:
                # get score for move
                score = None


    def _execute_steps(self):
        for worker in self._p:
            for move in self._p[worker.symbol]:
                for build in self._p[worker.symbol][move]:
                    pass


class RandomStrategy():
    def _get_worker(self):
        self._selected_worker = random.choice(list(self._p.values()))

    def _get_move(self):
        self._selected_move = random.choice(list(self._p_values[self._selected_worker].values()))

