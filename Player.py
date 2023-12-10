from Strategy import HumanStrategy
from cli import SantoriniCLI

class Worker:
    """Class representing a worker."""

    def __init__(self, symbol, default_position):
        self._symbol = symbol
        self._position = default_position

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
    def create_workers(self):
        return [Worker("A", (3, 1)), Worker("B", (1, 3))]


class BlueWorkerFactory:
    def create_workers(self):
        return [Worker("Y", (1, 1)), Worker("Z", (3, 3))]


class Player:
    """Class representing a player."""

    def __init__(self, color, workers):
        self._color = color
        self._workers = workers

    @property
    def workers(self):
        return self._workers

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color

    def __repr__(self):
        return self.color

    def worker_string(self):
        return str(self.workers[0]) + str(self.workers[1])

    def get_worker_at(self, pos):
        if self.workers[0].position == pos:
            return self.workers[0]

        if self.workers[1].position == pos:
            return self.workers[1]

        return None


class PlayerFactory:
    @staticmethod
    def get_factory(color, player_type, board):
        worker_factory = WorkerFactory.get_factory(color)
        workers = worker_factory.create_workers()

        player_types = {"human": HumanPlayer, "heuristic": HeuristicPlayer}
        player_class = player_types.get(player_type)
        if player_class:
            return player_class(color, workers, board)
        else:
            raise ValueError("Invalid player type")


class HumanPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)

        # Implement Strategy List
        self._strategy = HumanStrategy(board)

    def _execute(self):
        self._strategy(self.workers)

class HeuristicPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)

    def _execute(self):
        pass
        # super()._execute_move(move_direction, selected_worker)
        # super()._execute_build(build_direction, selected_worker)
