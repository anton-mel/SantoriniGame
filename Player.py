import copy
from exceptions import *
from Strategy import HumanStrategy, HeuristicStrategy, RandomStrategy


class Worker:
    """
    Class representing a worker on the board.

    _symbol (str): The symbol representing the worker.
    _position (tuple): The current position of the worker on the board.
    _board (Board): The game board.
    """

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
    """
    Factory Method Pattern for creating workers based on the player's color.

    Methods:
        get_factory(color): Returns a factory instance based on the specified color.
    """

    @staticmethod
    def get_factory(color):
        factories = {"white": WhiteWorkerFactory, "blue": BlueWorkerFactory}
        factory_class = factories.get(color)

        if factory_class:
            return factory_class()
        else:
            raise ValueError("Invalid player type")


class WhiteWorkerFactory:
    """
    Factory class for creating white workers.

    Methods:
        create_workers(self, board): Creates and returns a list of white workers.
    """

    def create_workers(self, board):
        worker1 = Worker(board, "A", (3, 1))
        worker2 = Worker(board, "B", (1, 3))

        return [worker1, worker2]


class BlueWorkerFactory:
    """
    Factory class for creating blue workers.

    Methods:
        create_workers(self, board): Creates and returns a list of blue workers.
    """

    def create_workers(self, board):
        worker1 = Worker(board, "Y", (1, 1))
        worker2 = Worker(board, "Z", (3, 3))

        return [worker1, worker2]


class Player:
    """
    Class representing a player controlling the game input and workers.

    _color (str): The color of the player.
    _workers (list): List of worker instances for the player.
    _strategy (Strategy): The strategy used by the player.
    """

    def __init__(self, color, workers, strategy):
        self._color = color
        self._workers = workers
        self._strategy = strategy

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
        """Returns a string representation of the player's workers."""

        return str(self.workers[0]) + str(self.workers[1])

    def _select_worker(self, symbol):
        """Selects and returns the worker with the specified symbol."""

        selected = None
        for worker in self._workers:
            if worker.symbol == symbol:
                selected = worker
                break
        return selected

    def execute(self):
        """Executes the player's strategy and returns the result."""

        # self._strategy.update_possibilities(self._workers)
        return self._strategy.execute()

    def update_possibilities(self):
        """Updates the possibilities for the player's strategy."""

        self._strategy.update_possibilities(self._workers)

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


class PlayerFactory:
    """Factory Method Pattern for creating player instances."""

    @staticmethod
    def get_factory(color, player_type, board):
        """Returns a player instance based on the specified parameters."""

        worker_factory = WorkerFactory.get_factory(color)
        workers = worker_factory.create_workers(board)

        strategies = {
            "human": HumanStrategy,
            "heuristic": HeuristicStrategy,
            "random": RandomStrategy,
        }
        strategy = strategies[player_type]
        if not strategy:
            raise ValueError("Invalid player type")

        return Player(color, workers, strategy(board, workers))
