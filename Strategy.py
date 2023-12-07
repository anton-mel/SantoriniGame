from abc import ABC, abstractmethod


class DirectionStrategy(ABC):
    def __init__(self, board):
        self._board = board

    @abstractmethod
    def _execute(self, worker):
        pass

class MoveStrategy(DirectionStrategy):
    def __init__(self, board):
        super().__init__(board)

    def _execute(self, worker, delta):
        print(delta)
        current_position = worker.position
        new_position = (
            current_position[0] + delta[0],
            current_position[1] + delta[1],
        )

        worker.position = new_position

class BuildStrategy(DirectionStrategy):
    def __init__(self, board):
        super().__init__(board)

    def _execute(self, worker, delta):
        print(delta)
        current_position = worker.position
        new_position = (
            current_position[0] + delta[0],
            current_position[1] + delta[1],
        )
        
        self._board.build(new_position)