class MoveError(Exception):
    """Fix later"""

    def __init__(self, move_type, direction):
        super().__init__()
        self.move_type = move_type
        self.direction = direction

class WorkerError(Exception):
    """Fix later"""

    def __init__(self, mes):
        super().__init__()
        self.mes = mes

class DirectionError(Exception):
    """Fix later"""

    def __init__(self, mes):
        super().__init__()
        self.mes = mes

class MementoError(Exception):
    """Fix later"""

    def __init__(self):
        super().__init__()