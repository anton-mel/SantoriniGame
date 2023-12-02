from abc import ABC, abstractmethod
from Strategy import *

class Worker:
    """Class representing a worker."""
    def __init__(self, symbol, default_position):
        self.symbol = symbol
        self.position = default_position 

    @property
    def get_symbol(self):
        return self.symbol
    
    @property
    def get_position(self):
        return self.position

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

    def select_worker(self):
        raise NotImplementedError

    def select_direction(self, prompt):
        raise NotImplementedError
    
    def get_move_strategy(self, direction):
        if direction == "n":
            return MoveNorthStrategy()
        elif direction == "ne":
            return MoveNortheastStrategy()
        elif direction == "e":
            return MoveEastStrategy()
        elif direction == "se":
            return MoveSoutheastStrategy()
        elif direction == "s":
            return MoveSouthStrategy()
        elif direction == "sw":
            return MoveSouthwestStrategy()
        elif direction == "w":
            return MoveWestStrategy()
        elif direction == "nw":
            return MoveNorthwestStrategy()
        else:
            raise ValueError(f"Invalid direction: {direction}")

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
    
    def execute(self, board):
        selected_worker = self.select_worker()
        move_direction = self.select_direction("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")
        build_direction = self.select_direction("Select a direction to build (n, ne, e, se, s, sw, w, nw): ")

        # Strategies Move
        self.move_strategy = self.get_move_strategy(move_direction)
        self.move_strategy.execute(board, selected_worker)


    def select_worker(self):
        while True:
            worker_symbol = input("Select a worker to move: ")
            # Check here if random
            for worker in self.workers:
                if worker.get_symbol == worker_symbol:
                    return worker
            print(f"No worker found with symbol {worker_symbol}. Try again.")

    # Build and Move
    def select_direction(self, prompt):
        while True:
            try:
                direction = input(prompt)
                valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
                if direction not in valid_directions:
                    raise ValueError(f"Invalid direction: {direction}")
                return direction
            except ValueError as e:
                print(f"Error: {e}. Try again.")

class HeuristicPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)
    
    # Implement AI
    def execute(self, game):
        pass