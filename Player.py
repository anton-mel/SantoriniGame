import copy
from exceptions import *
from Strategy import HumanStrategy, HeuristicStrategy, RandomStrategy


class Worker:
    """Class representing a worker."""

    def __init__(self, board, symbol, default_position):
        self._symbol = symbol
        self._position = default_position
        self._board = board

    @property
    def symbol(self):
        return self._symbol

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    def __repr__(self) -> str:
        return self.symbol
    
    def __deepcopy__(self, memo):
        new_worker = Worker(self._board, self._symbol, self._position)
        memo[id(self)] = new_worker
        return new_worker
    

class WorkerFactory:
    @staticmethod
    def get_factory(color):
        factories = {"white": WhiteWorkerFactory, "blue": BlueWorkerFactory}
        factory_class = factories.get(color)

        if factory_class:
            return factory_class()
        else:
            raise ValueError("Invalid player type")


class WhiteWorkerFactory:
    def create_workers(self, board):
        worker1 = Worker(board, "A", (3, 1))
        worker2 = Worker(board, "B", (1, 3))

        return [worker1, worker2]


class BlueWorkerFactory:
    def create_workers(self, board):
        worker1 = Worker(board, "Y", (1, 1))
        worker2 = Worker(board, "Z", (3, 3))

        return [worker1, worker2]


class Player:
    """Class representing a player."""

    def __init__(self, color, workers):
        self._color = color
        self._workers = workers
        self._p = {}
    
    def get_worker_at(self, pos):
        if self.workers[0].position == pos:
            return self.workers[0]

        if self.workers[1].position == pos:
            return self.workers[1]

        return None
    
    def worker_deep_copy(self):
        return [copy.deepcopy(worker) for worker in self._workers]

    def __repr__(self):
        return self.color

    def worker_string(self):
        return str(self.workers[0]) + str(self.workers[1])

    def _select_worker(self, symbol):
        selected = None
        for worker in self._workers:
            if worker.symbol == symbol:
                selected = worker
                break
        return selected

    def execute(self):
        return self._strategy.execute(self)

    def update_possibilities(self, board):
        self._p.clear()

        for worker in self.workers:
            pos = worker.position
            level = board.get_cell(pos).level
            for move in board.get_ring(pos):
                cell = board.get_cell(move)

                if cell.level > 3:
                    continue

                if cell.level > level + 1:
                    continue

                if board.occupied(move):
                    continue

                for build in board.get_ring(move):
                    cell = board.get_cell(build)

                    if board.occupied(build) and build != pos:
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

    # Getters & Setters
    @property
    def workers(self):
        return self._workers
    
    @workers.setter
    def workers(self, workers):
        self._workers = workers

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color


class HumanPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)
        self._strategy = HumanStrategy(board, self._p)


class HeuristicPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)
        self._strategy = HeuristicStrategy(board, self._p)


class RandomPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)
        self._strategy = RandomStrategy(board, self._p)


class PlayerFactory:
    @staticmethod
    def get_factory(color, player_type, board):
        worker_factory = WorkerFactory.get_factory(color)
        workers = worker_factory.create_workers(board)

        player_types = {
            "human": HumanPlayer,
            "heuristic": HeuristicPlayer,
            "random": RandomPlayer,
        }
        player_class = player_types.get(player_type)

        if player_class:
            return player_class(color, workers, board)
        else:
            raise ValueError("Invalid player type")
