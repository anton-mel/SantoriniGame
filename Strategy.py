
from abc import ABC, abstractmethod

class DirectionStrategy(ABC):
    @abstractmethod
    def _execute(self, board, worker):
        pass

class MoveStrategy(DirectionStrategy):
    def __init__(self, move_delta):
        self.move_delta = move_delta

    def _execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] + self.move_delta[0], current_position[1] + self.move_delta[1])
        board._move_worker_to_position(worker, new_position)

class BuildStrategy(DirectionStrategy):
    def __init__(self, build_delta):
        self.build_delta = build_delta

    def _execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] + self.build_delta[0], current_position[1] + self.build_delta[1])
        board._build_tower_at_position(new_position)
