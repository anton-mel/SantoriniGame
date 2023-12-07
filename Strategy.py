from abc import ABC, abstractmethod


class DirectionStrategy(ABC):
    @abstractmethod
    def execute(self, board, worker):
        pass


class MoveNorthStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] - 1, current_position[1])

        board._move_worker_to_position(worker, new_position)


class MoveNortheastStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] - 1, current_position[1] + 1)

        board._move_worker_to_position(worker, new_position)


class MoveEastStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0], current_position[1] + 1)

        board._move_worker_to_position(worker, new_position)


class MoveSoutheastStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] + 1, current_position[1] + 1)

        board._move_worker_to_position(worker, new_position)


class MoveSouthStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] + 1, current_position[1])

        board._move_worker_to_position(worker, new_position)


class MoveSouthwestStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] + 1, current_position[1] - 1)

        board._move_worker_to_position(worker, new_position)


class MoveWestStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0], current_position[1] - 1)

        board._move_worker_to_position(worker, new_position)


class MoveNorthwestStrategy(DirectionStrategy):
    def execute(self, board, worker):
        current_position = worker.get_position
        new_position = (current_position[0] - 1, current_position[1] - 1)

        board._move_worker_to_position(worker, new_position)
