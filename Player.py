
from Strategy import MoveStrategy, BuildStrategy

class Worker:
    """Class representing a worker."""
    def __init__(self, symbol, default_position):
        self.symbol = symbol
        self._position = default_position 

    @property
    def get_symbol(self):
        return self.symbol
    
    @property
    def get_position(self):
        return self._position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

class WorkerFactory:
    @staticmethod
    def get_factory(color):
        factories = {"white": WhiteWorkerFactory, "blue": BlueWorkerFactory}
        factory_class = factories.get(color)
        if factory_class:
            return factory_class()
        else:
            raise ValueError("Invalid player type")

    def create_workers(self):
        raise NotImplementedError

class WhiteWorkerFactory(WorkerFactory):
    def create_workers(self):
        return [Worker("A", (3, 1)), Worker("B", (3, 3))]

class BlueWorkerFactory(WorkerFactory):
    def create_workers(self):
        return [Worker("Y", (1, 1)), Worker("Z", (1, 3))]

class Player:
    """Class representing a player."""
    def __init__(self, color, workers):
        self.color = color
        self.workers = workers

    def get_direction_delta(self, direction):
        direction_deltas = {"n": (-1, 0), "ne": (-1, 1), "e": (0, 1), "se": (1, 1),
                            "s": (1, 0), "sw": (1, -1), "w": (0, -1), "nw": (-1, -1)}
        return direction_deltas[direction]

    def _execute(self, board):
        selected_worker = self.select_worker()
       
        while True:
            move_direction = self.select_direction("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")
            try:
                self._execute_strategy(MoveStrategy, move_direction, board, selected_worker)
                break
            except ValueError as e:
                print(f"This cell is taken")

        build_direction = self.select_direction("Select a direction to build (n, ne, e, se, s, sw, w, nw): ")
        self._execute_strategy(BuildStrategy, build_direction, board, selected_worker)

    def _execute_strategy(self, strategy_class, direction, board, worker):
        strategy = strategy_class(self.get_direction_delta(direction))
        strategy._execute(board, worker)

    def select_worker(self):
        while True:
            worker_symbol = input("Select a worker to move: ")
            for worker in self.workers:
                if worker.get_symbol == worker_symbol:
                    return worker
            print(f"No worker found with symbol {worker_symbol}. Try again.")

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

        player_types = {"human": HumanPlayer, "heuristic": HeuristicPlayer}
        player_class = player_types.get(player_type)
        if player_class:
            return player_class(color, workers)
        else:
            raise ValueError("Invalid player type")

class HumanPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)
    
    def _execute(self, board):
        super()._execute(board)

    def select_worker(self):
        return super().select_worker()

    def select_direction(self, prompt):
        return super().select_direction(prompt)

class HeuristicPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)
    
    def _execute(self, game):
        pass
