from abc import ABC, abstractmethod

class Worker:
    """Class representing a worker."""
    def __init__(self, symbol, default_position):
        self.symbol = symbol
        self.position = default_position 

    @property
    def get_symbol(self):
        return self.symbol

class WorkerFactory:
    @staticmethod
    def get_factory(color):
        if color == "white":
            return WhiteWorkerFactory()
        elif color == "blue":
            return BlueWorkerFactory()
        else:
            raise ValueError("Invalid player type")

class WhiteWorkerFactory(WorkerFactory):
    def create_workers(self):
        return [Worker("A", (3, 1)), Worker("B", (3, 2))]

class BlueWorkerFactory(WorkerFactory):
    def create_workers(self):
        return [Worker("Y", (1, 2)), Worker("Z", (1, 4))]

class Player(ABC):
    """Class representing a player."""
    def __init__(self, color, workers):
        self.color = color
        self.workers = workers

    def execute(self, game, move_direction, build_direction):
        raise NotImplementedError

    @property
    def get_workers(self):
        return self.workers
    
    @property
    def get_color(self):
        return self.color

class PlayerFactory:
    @staticmethod
    def get_factory(color, player_type):
        worker_factory = WorkerFactory.get_factory(color)
        workers = worker_factory.create_workers()

        if player_type == "human":
            return HumanPlayer(color, workers)
        elif player_type == "heuristic":
            return HeuristicPlayer(color, workers)
        else:
            raise ValueError("Invalid player type")

class HumanPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)
    
    def execute(self, game, move_direction, build_direction):
        pass

class HeuristicPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)
    
    def execute(self):
        pass
