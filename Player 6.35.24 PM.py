from cli import SantoriniCLI
from exceptions import *
from DirectionUtils import DirectionUtils
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

        # Observer Pattern (Subject Method)
        self._board.update_worker_position(self)
        print(self._board.observers)

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
    def create_workers(self, board):
        worker1 = Worker(board, "A", (3, 1))
        worker2 = Worker(board, "B", (1, 3))

        board.add_observer(worker1)
        board.add_observer(worker2)

        return [worker1, worker2]


class BlueWorkerFactory:
    def create_workers(self, board):
        worker1 = Worker(board, "Y", (1, 1))
        worker2 = Worker(board, "Z", (3, 3))

        board.add_observer(worker1)
        board.add_observer(worker2)

        return [worker1, worker2]


class Player:
    """Class representing a player."""

    def __init__(self, color, workers):
        self._color = color
        self._workers = workers

    def get_worker_at(self, pos):
        if self.workers[0].position == pos:
            return self.workers[0]

        if self.workers[1].position == pos:
            return self.workers[1]

        return None

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
    
    def _update_position(self, current, direction):
        delta = DirectionUtils.get_direction_delta(direction)
        new_position = (
            current[0] + delta[0],
            current[1] + delta[1])
        return new_position

    def _move(self, direction, worker, board):
        current = worker.position
        new_position = self._update_position(current, direction)
        board.validate("move", new_position, direction)
        
        # Cannot Move to the Occupied Cell
        if board.occupied(new_position):
            raise MoveError("move", direction)
        # Cannot Skip Cells on Raise
        if board.get_cell(current).level + 1 < board.get_cell(new_position).level:
            raise MoveError("move", direction)
        # Cannot Move to the Cell High of 4
        if board.get_cell(new_position).level > 3:
            raise MoveError("move", direction)

        worker.position = new_position

    def _build(self, direction, worker, board):
        current = worker.position
        new_position = self._update_position(current, direction)
        board.validate("build", new_position, direction)

        # Cannot Build Too High
        if board.get_cell(new_position).level > 3:
            raise MoveError("build", direction)

        board.build(new_position)

    def execute(self):
        self._strategy.execute()

    # Getters & Setters
    @property
    def workers(self):
        return self._workers

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color


class HumanPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)
        self._strategy = HumanStrategy(board, self)

    # def _execute(self):
        # while True:
        #     try:
        #         symbol = SantoriniCLI().select_worker()
        #         worker = super()._select_worker(symbol)

        #         if (symbol in board.observers) and (not worker):
        #             raise WorkerError("That is not your worker")
                
        #         if not worker:
        #             raise WorkerError("Not a valid worker")

        #         break
        #     except WorkerError as e:
        #         print(e.mes)

        # while True:
        #     try:
        #         move_direction = SantoriniCLI().get_move()
        #         super()._move(move_direction, worker, board)
        #         break
        #     except MoveError as e:
        #         print(f"Cannot {e.move_type} {e.direction}")
        #     except DirectionError as e:
        #         print(f"{e.mes}")

        # while True:
        #     try:
        #         build_direction = SantoriniCLI().get_build()
        #         super()._build(build_direction, worker, board)
        #         break
        #     except MoveError as e:
        #         print(f"Cannot {e.move_type} {e.direction}")
        #     except DirectionError as e:
        #         print(f"{e.mes}")

        # return symbol, move_direction, build_direction

class HeuristicPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)
        self._strategy = HeuristicStrategy(board, self)

class RandomPlayer(Player):
    def __init__(self, color, workers, board):
        super().__init__(color, workers)
        self._strategy = RandomStrategy(board, self)


class PlayerFactory:
    @staticmethod
    def get_factory(color, player_type, board):
        worker_factory = WorkerFactory.get_factory(color)
        workers = worker_factory.create_workers(board)

        player_types = {"human": HumanPlayer, "heuristic": HeuristicPlayer, "random": RandomPlayer}
        player_class = player_types.get(player_type)

        if player_class:
            return player_class(color, workers, board)
        else:
            raise ValueError("Invalid player type")

