
from abc import ABC, abstractmethod
import random

class Strategy(ABC):
    @abstractmethod
    def execute(self, game):
        pass

class WorkerSelectionStrategy(Strategy):
    def execute(self, game):
        raise NotImplementedError

class RandomWorkerSelectionStrategy(WorkerSelectionStrategy):
    def execute(self, game):
        workers = game.get_all_workers()
        return random.choice(workers)

class DirectionSelectionStrategy(Strategy):
    def execute(self):
        raise NotImplementedError

class RandomDirectionSelectionStrategy(DirectionSelectionStrategy):
    def execute(self):
        directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        return random.choice(directions)

class MoveStrategy(Strategy):
    def execute(self, game, worker, direction):
        game.move_worker(worker, direction)

class BuildStrategy(Strategy):
    def execute(self, game, worker, direction):
        game.build_building(worker, direction)

class SantoriniStrategy:
    def __init__(self, worker_strategy, move_strategy, build_strategy):
        self.worker_strategy = worker_strategy
        self.move_strategy = move_strategy
        self.build_strategy = build_strategy

    def execute_strategy(self, game):
        worker = self.worker_strategy.execute(game)
        direction_move = self.move_strategy.execute()
        direction_build = self.build_strategy.execute()

        try:
            self.move_strategy.execute(game, worker, direction_move)
            self.build_strategy.execute(game, worker, direction_build)
        except Exception as e:
            print(f"Exception: {e}")

# Example Usage
random_worker_strategy = RandomWorkerSelectionStrategy()
random_move_strategy = RandomDirectionSelectionStrategy()
random_build_strategy = RandomDirectionSelectionStrategy()

move_strategy = MoveStrategy()
build_strategy = BuildStrategy()

strategy = SantoriniStrategy(random_worker_strategy, random_move_strategy, random_build_strategy)

class SantoriniCLI:
    # ... (your existing code)

    def _process_turn(self):
        strategy.execute_strategy(self._game)
