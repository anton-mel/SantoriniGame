from Strategy import MoveStrategy, BuildStrategy

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

    def __init__(self, color, workers, board):
        self.color = color
        self.workers = workers

        # Implement Strategy List
        self.strategy = MoveStrategy(board)
        self.build_strategy = BuildStrategy(board)

    def get_direction_delta(self, direction):
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

    # This May Be In the Separate Class (Strategy Caretaker)
    def _execute_strategy(self, strategy, direction, worker):
        delta = self.get_direction_delta(direction)
        strategy._execute(worker, delta)

    def _execute(self):
        selected_worker = self.select_worker()

        move_direction = self.select_direction("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")
        self._execute_strategy(self.strategy, move_direction, selected_worker)

        build_direction = self.select_direction("Select a direction to build (n, ne, e, se, s, sw, w, nw): ")
        self._execute_strategy(self.build_strategy, build_direction, selected_worker)

    def select_worker(self):
        while True:
            worker_symbol = input("Select a worker to move: ")
            for worker in self.workers:
                if worker.symbol == worker_symbol:
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
    def worker(self):
        return self.workers

    @property
    def worker(self):
        return self.color

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
        super().__init__(color, workers, board)

    def _execute(self):
        super()._execute()

    def select_worker(self):
        return super().select_worker()

    def select_direction(self, prompt):
        return super().select_direction(prompt)


class HeuristicPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)

    def _execute(self):
        pass
